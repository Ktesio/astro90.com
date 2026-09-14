/* Visibility routes around convex shorelines, with room for the whole boat. */
(() => {
  const distance = (a, b) => Math.hypot(b.x - a.x, b.y - a.y);
  const mix = (a, b, t) => ({ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t });
  const cross = (a, b, p) => (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);
  const inside = (p, polygon) => polygon.every((a, i) => cross(a, polygon[(i + 1) % polygon.length], p) > .01);

  function outline(points, clearance) {
    // Intersect sixteen supporting half-planes. The result encloses the entire
    // source silhouette, including detached rocks, rather than cutting corners.
    const planes = Array.from({ length: 16 }, (_, i) => {
      const angle = i * Math.PI / 8;
      const x = Math.cos(angle), y = Math.sin(angle);
      return { x, y, d: Math.max(...points.map(p => x * p.x + y * p.y)) + clearance };
    });
    return planes.map((a, i) => {
      const b = planes[(i + 1) % planes.length];
      const det = a.x * b.y - a.y * b.x;
      return { x: (a.d * b.y - a.y * b.d) / det, y: (a.x * b.d - a.d * b.x) / det };
    });
  }

  function clearSegment(a, b, obstacles) {
    for (const polygon of obstacles) {
      let enter = 0, leave = 1, misses = false;
      for (let i = 0; i < polygon.length; i++) {
        const p = polygon[i], q = polygon[(i + 1) % polygon.length];
        const length = distance(p, q);
        const start = cross(p, q, a) / length;
        const slope = ((q.x - p.x) * (b.y - a.y) - (q.y - p.y) * (b.x - a.x)) / length;
        if (Math.abs(slope) < .00001) {
          if (start <= .01) { misses = true; break; }
        } else {
          const t = (.01 - start) / slope;
          if (slope > 0) enter = Math.max(enter, t);
          else leave = Math.min(leave, t);
          if (enter >= leave) { misses = true; break; }
        }
      }
      if (!misses && enter < leave - .00001) return false;
    }
    return true;
  }

  function build(regions, width, height, radius) {
    const obstacles = [], boundaries = [], docks = new Map();
    const margin = radius + 3;
    const inBounds = p => p.x >= margin && p.x <= width - margin && p.y >= margin && p.y <= height - margin;
    for (const region of regions) {
      // Twelve pixels cover the hover lift and a little clear water. Routing
      // vertices sit farther out so turns have space to round off smoothly.
      obstacles.push(outline(region.shore, radius + 12));
      const boundary = outline(region.shore, radius + 32);
      boundaries.push(boundary);
      // Dense phone layouts may put a label or neighbouring rock beside the
      // closest berth. Offer farther offshore berths in the same open water.
      docks.set(region.id, [32, 56, 80].flatMap(extra => {
        const ring = outline(region.shore, radius + extra);
        return ring.flatMap((p, i) => [p, mix(p, ring[(i + 1) % ring.length], .5)]);
      }));
      if (region.label) {
        obstacles.push(outline(region.label, radius + 3));
        boundaries.push(outline(region.label, radius + 23));
      }
    }
    const water = p => inBounds(p) && !obstacles.some(polygon => inside(p, polygon));
    const vertices = boundaries.flat().filter(water);
    const safePoint = preferred => water(preferred) ? preferred : vertices.reduce((best, p) => !best || distance(p, preferred) < distance(best, preferred) ? p : best, null);
    return { obstacles, vertices, docks, water, safePoint };
  }

  function rounded(path, obstacles) {
    if (path.length < 3) return path;
    const points = [path[0]];
    for (let i = 1; i < path.length - 1; i++) {
      const a = path[i - 1], p = path[i], b = path[i + 1];
      const trim = Math.min(20, distance(a, p) / 4, distance(p, b) / 4);
      const entry = mix(p, a, trim / distance(a, p));
      const exit = mix(p, b, trim / distance(p, b));
      const curve = Array.from({ length: 17 }, (_, n) => {
        const t = n / 16;
        return mix(mix(entry, p, t), mix(p, exit, t), t);
      });
      const candidate = [points.at(-1), ...curve, b];
      if (candidate.slice(1).every((q, n) => clearSegment(candidate[n], q, obstacles))) points.push(...curve);
      else points.push(p);
    }
    points.push(path.at(-1));
    return points;
  }

  function plan(model, start, destination, preferred) {
    if (!model.water(start)) return null;
    const goals = (model.docks.get(destination) || []).filter(model.water);
    if (!goals.length) return null;
    const nodes = [start, ...model.vertices, ...goals];
    const firstGoal = nodes.length - goals.length;
    const lengths = nodes.map(() => Infinity), previous = nodes.map(() => -1), visited = new Set();
    lengths[0] = 0;
    for (let step = 0; step < nodes.length; step++) {
      let current = -1;
      for (let i = 0; i < nodes.length; i++) if (!visited.has(i) && (current < 0 || lengths[i] < lengths[current])) current = i;
      if (current < 0 || !Number.isFinite(lengths[current])) break;
      visited.add(current);
      for (let i = 0; i < nodes.length; i++) {
        if (visited.has(i)) continue;
        const next = lengths[current] + distance(nodes[current], nodes[i]);
        if (next < lengths[i] && clearSegment(nodes[current], nodes[i], model.obstacles)) {
          lengths[i] = next;
          previous[i] = current;
        }
      }
    }
    let end = -1, cost = Infinity;
    for (let i = firstGoal; i < nodes.length; i++) {
      const score = lengths[i] + distance(nodes[i], preferred) * 2;
      if (score < cost) { cost = score; end = i; }
    }
    if (end < 0) return null;
    const path = [];
    for (let i = end; i >= 0; i = previous[i]) path.unshift(nodes[i]);
    const curve = rounded(path, model.obstacles);
    // Verify every rendered segment too. Rapid retargeting can start mid-turn.
    return curve.slice(1).every((p, i) => clearSegment(curve[i], p, model.obstacles)) ? curve : path;
  }

  globalThis.Astro90SeaRoutes = { build, plan, clearSegment, distance };
})();
