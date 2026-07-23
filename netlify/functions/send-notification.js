import { getStore } from "@netlify/blobs";
import webpush from "web-push";

export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  const auth = req.headers.get("authorization") || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  if (!token || token !== process.env.ADMIN_SECRET) {
    return new Response("Unauthorized", { status: 401 });
  }

  let payload;
  try {
    payload = await req.json();
  } catch {
    return new Response("Invalid JSON", { status: 400 });
  }

  const { title, body, url } = payload || {};
  if (!title || !body) {
    return new Response("title and body are required", { status: 400 });
  }

  webpush.setVapidDetails(
    process.env.VAPID_SUBJECT,
    process.env.VAPID_PUBLIC_KEY,
    process.env.VAPID_PRIVATE_KEY
  );

  const store = getStore("push-subscriptions");
  const { blobs } = await store.list();
  const message = JSON.stringify({ title, body, url: url || "/" });

  let sent = 0;
  let pruned = 0;
  const errors = [];

  await Promise.all(
    blobs.map(async ({ key }) => {
      const subscription = await store.get(key, { type: "json" });
      if (!subscription) return;
      try {
        await webpush.sendNotification(subscription, message);
        sent += 1;
      } catch (err) {
        if (err.statusCode === 404 || err.statusCode === 410) {
          await store.delete(key);
          pruned += 1;
        } else {
          errors.push(err.message);
        }
      }
    })
  );

  return new Response(JSON.stringify({ sent, pruned, total: blobs.length, errors }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
};
