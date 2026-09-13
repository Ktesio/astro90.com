import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import monogram from "../brand/monogram.json";

// Geometry and the SVG share one authored silhouette. There is no idle clock:
// the site's input scheduler calls render only while pointer/scroll state moves.
export function createBrandScene(host) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: "low-power",
    });
  } catch {
    return null;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.7));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 80);
  camera.position.z = 9.6;
  const environment = new RoomEnvironment();
  const pmrem = new THREE.PMREMGenerator(renderer);
  const environmentMap = pmrem.fromScene(environment, 0.035);
  scene.environment = environmentMap.texture;
  environment.dispose();
  pmrem.dispose();

  const shape = new THREE.Shape();
  monogram.contours[0].forEach(([x, y], index) => {
    const point = [
      (x / monogram.width - 0.5) * 4.6,
      (0.5 - y / monogram.height) * 4.05,
    ];
    index ? shape.lineTo(...point) : shape.moveTo(...point);
  });
  shape.closePath();
  const geometry = new THREE.ExtrudeGeometry(shape, {
    depth: 0.38,
    bevelEnabled: true,
    bevelSegments: 5,
    steps: 1,
    bevelSize: 0.065,
    bevelThickness: 0.075,
    curveSegments: 32,
  });
  geometry.center();
  const gold = new THREE.MeshPhysicalMaterial({
    color: 0xf4c84c,
    metalness: 0.92,
    roughness: 0.26,
    clearcoat: 0.5,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.65,
  });
  const navy = new THREE.MeshPhysicalMaterial({
    color: 0x111d30,
    metalness: 0.7,
    roughness: 0.3,
    envMapIntensity: 1.3,
  });
  const group = new THREE.Group();
  group.add(new THREE.Mesh(geometry, gold));
  const backing = new THREE.Mesh(geometry, navy);
  backing.position.z = -0.38;
  backing.scale.set(0.988, 0.988, 1.22);
  group.add(backing);
  scene.add(group);
  const key = new THREE.DirectionalLight(0xffe6ab, 4);
  key.position.set(-3, 5, 6);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xb4c8ef, 3);
  rim.position.set(4, -1, 4);
  scene.add(rim);

  let active = true;
  renderer.domElement.setAttribute("aria-hidden", "true");
  host.append(renderer.domElement);
  const resize = () => {
    const { width, height } = host.getBoundingClientRect();
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    window.dispatchEvent(new Event("astro90:render"));
  };
  const observer = new ResizeObserver(resize);
  observer.observe(host);
  resize();
  const render = ({ x = 0, y = 0, progress = 0, reduced = false } = {}) => {
    if (!active) return;
    const p = reduced ? 0 : progress;
    group.rotation.set(
      0.1 + y * 0.18 - p * 0.18,
      -0.34 + x * 0.4 + p * 0.56,
      -0.075 + x * 0.045 + p * 0.12,
    );
    group.position.set(x * 0.08 - p * 0.35, -y * 0.06 + p * 0.18, 0);
    camera.position.z = 9.6 - p * 4.9;
    gold.roughness = 0.26 + p * 0.1;
    key.position.set(-3 + x * 3, 5 - y * 2, 6);
    renderer.render(scene, camera);
  };
  render();
  host.classList.add("is-rendered");
  renderer.domElement.addEventListener("webglcontextlost", () => {
    active = false;
    host.classList.remove("is-rendered");
  });
  return {
    render,
    dispose() {
      observer.disconnect();
      geometry.dispose();
      gold.dispose();
      navy.dispose();
      environmentMap.dispose();
      renderer.dispose();
      renderer.domElement.remove();
      host.classList.remove("is-rendered");
    },
  };
}
