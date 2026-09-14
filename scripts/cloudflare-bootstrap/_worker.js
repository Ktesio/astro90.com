// Only used while the domain and Access are being provisioned. No site assets
// are included in this deployment. The normal Zola build has no Worker.
export default {
  fetch() {
    return new Response("This site is private.\n", {
      status: 403,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  },
};
