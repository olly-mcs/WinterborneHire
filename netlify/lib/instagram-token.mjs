// Shared helpers for the Instagram feed functions.
//
// The first access token comes from the INSTAGRAM_ACCESS_TOKEN environment variable
// (set in Netlify, never in the code). Tokens last 60 days, so instagram-refresh
// swaps it for a fresh one every week and keeps that in Netlify Blobs.
import { getStore } from "@netlify/blobs";

const STORE = "instagram";
const KEY = "token";

// Identifies which environment token a stored token was refreshed from, without storing it twice.
const fingerprint = (token) => (token ? token.slice(-12) : "");

export async function readToken() {
  const envToken = process.env.INSTAGRAM_ACCESS_TOKEN || "";
  try {
    const saved = await getStore(STORE).get(KEY, { type: "json" });
    // A new token pasted into Netlify always wins over an older refreshed one.
    if (saved?.token && saved.seededFrom === fingerprint(envToken)) return saved.token;
  } catch (error) {
    console.error("Could not read the saved Instagram token:", error);
  }
  return envToken;
}

export async function saveToken(token) {
  const envToken = process.env.INSTAGRAM_ACCESS_TOKEN || "";
  await getStore(STORE).setJSON(KEY, {
    token,
    seededFrom: fingerprint(envToken),
    refreshedAt: new Date().toISOString(),
  });
}
