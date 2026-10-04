// GET /api/instagram: the latest Instagram posts as JSON for the site's feed grid.
// Netlify's CDN caches the response for an hour, so Instagram is asked at most once an hour.
import { readToken } from "../lib/instagram-token.mjs";

const FIELDS = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp";
const LIMIT = 12;

const json = (body, status, cache) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=300",
      "Netlify-CDN-Cache-Control": cache,
    },
  });

export default async () => {
  const token = await readToken();
  if (!token) {
    return json({ posts: [], error: "not-configured" }, 503, "no-store");
  }

  const url = `https://graph.instagram.com/me/media?fields=${FIELDS}&limit=${LIMIT}&access_token=${encodeURIComponent(token)}`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    if (!res.ok || data.error) {
      console.error("Instagram API error:", JSON.stringify(data.error || res.status));
      return json({ posts: [], error: "instagram-error" }, 502, "no-store");
    }

    const posts = (data.data || [])
      .map((item) => ({
        id: item.id,
        // Videos show their cover image; photos and carousels show the (first) image.
        image: item.media_type === "VIDEO" ? item.thumbnail_url : item.media_url,
        isVideo: item.media_type === "VIDEO",
        isCarousel: item.media_type === "CAROUSEL_ALBUM",
        caption: (item.caption || "").slice(0, 300),
        permalink: item.permalink,
        timestamp: item.timestamp,
      }))
      .filter((post) => post.image && post.permalink);

    return json({ posts }, 200, "public, durable, s-maxage=3600, stale-while-revalidate=86400");
  } catch (error) {
    console.error("Could not reach Instagram:", error);
    return json({ posts: [], error: "unreachable" }, 502, "no-store");
  }
};

export const config = { path: "/api/instagram" };
