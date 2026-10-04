// Runs weekly: swaps the Instagram access token for a fresh 60-day one and saves it,
// so the feed keeps working without anyone renewing the token by hand.
import { readToken, saveToken } from "../lib/instagram-token.mjs";

export default async () => {
  const token = await readToken();
  if (!token) {
    console.log("No Instagram token set yet; nothing to refresh.");
    return;
  }

  const url = `https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${encodeURIComponent(token)}`;
  const res = await fetch(url);
  const data = await res.json();
  if (!res.ok || !data.access_token) {
    console.error("Instagram token refresh failed:", JSON.stringify(data.error || res.status));
    return;
  }

  await saveToken(data.access_token);
  console.log(`Instagram token refreshed; valid for about ${Math.round((data.expires_in || 0) / 86400)} days.`);
};

export const config = { schedule: "@weekly" };
