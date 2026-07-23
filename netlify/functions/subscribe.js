import { getStore } from "@netlify/blobs";

export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  let subscription;
  try {
    subscription = await req.json();
  } catch {
    return new Response("Invalid JSON", { status: 400 });
  }

  if (!subscription || !subscription.endpoint || !subscription.keys) {
    return new Response("Invalid subscription", { status: 400 });
  }

  const store = getStore("push-subscriptions");
  const key = Buffer.from(subscription.endpoint).toString("base64url");
  await store.setJSON(key, subscription);

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
};
