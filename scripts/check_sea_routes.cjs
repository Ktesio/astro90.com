/* Keep the boat's entire hull clear of shores, including on interrupted trips. */
const assert = require('node:assert/strict');
const shores = require('../data/navigation-shores.json');
require('../static/js/sea-routes.js');
const {build, plan, distance} = globalThis.Astro90SeaRoutes;
const rectangle = (x,y,w,h) => [{x,y},{x:x+w,y},{x:x+w,y:y+h},{x,y:y+h}];

function inside(p, polygon) {
  let result = false;
  for (let i=0,j=polygon.length-1;i<polygon.length;j=i++) {
    const a=polygon[i],b=polygon[j];
    if ((a.y>p.y)!==(b.y>p.y) && p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x) result=!result;
  }
  return result;
}
function edgeDistance(p,a,b) {
  const dx=b.x-a.x,dy=b.y-a.y;
  const t=Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/(dx*dx+dy*dy)));
  return Math.hypot(p.x-a.x-t*dx,p.y-a.y-t*dy);
}
function verify(path, regions, radius) {
  for (let i=1;i<path.length;i++) {
    const a=path[i-1],b=path[i],steps=Math.max(1,Math.ceil(distance(a,b)/2));
    for(let j=0;j<=steps;j++) {
      const p={x:a.x+(b.x-a.x)*j/steps,y:a.y+(b.y-a.y)*j/steps};
      for(const region of regions) {
        assert(!inside(p,region.shore), 'Boat entered an island');
        for(let k=0;k<region.shore.length;k++) assert(edgeDistance(p,region.shore[k],region.shore[(k+1)%region.shore.length])>=radius, 'Boat hull crossed a shoreline');
      }
    }
  }
}
let journeys=0;
for(const scale of [1,.65]) {
  const positions={lighthouse:[120,60],inkube:[710,80],about:[100,450],contact:[700,470]};
  const regions=Object.entries(positions).map(([id,[x,y]])=>({id,shore:shores[id].map(([u,v])=>({x:(x+u*340)*scale,y:(y+v*226)*scale}))}));
  const radius=24*scale, model=build(regions,1200*scale,800*scale,radius);
  let start=model.safePoint({x:600*scale,y:400*scale});
  const destinations=['lighthouse','contact','inkube','about','lighthouse','inkube','contact','about','inkube','lighthouse'];
  for(const [i,id] of destinations.entries()) {
    const [x,y]=positions[id];
    const path=plan(model,start,id,{x:(x+170)*scale,y:(y+180)*scale});
    assert(path && path.length>=2, `No water route to ${id}`);
    assert.deepEqual(path[0],start,'Retargeting jumped to a different starting point');
    verify(path,regions,radius);
    // Change course from the middle of a rendered turn, not just a finished berth.
    start=i%2 ? path.at(-1) : path[Math.floor(path.length/2)];
    journeys++;
  }
}
const blocked=build([
  {id:'wall',shore:rectangle(270,-100,80,800)},
  {id:'target',shore:rectangle(470,200,70,70)},
],600,480,16);
assert.equal(plan(blocked,{x:100,y:240},'target',{x:460,y:240}),null,'A disconnected channel must not teleport the boat through land');
console.log(`PASS: ${journeys} sea routes, full-hull clearance, interrupted voyages and disconnected water.`);
