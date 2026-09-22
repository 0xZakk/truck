import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { sliderCrank } from './engine-motion.js';

const $ = id => document.getElementById(id);
const stage = $('stage');
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.localClippingEnabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
stage.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#dfe6e9');
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(),0.04).texture;
const camera = new THREE.PerspectiveCamera(35,1,0.1,5000);
const orbit = new OrbitControls(camera,renderer.domElement);
orbit.enableDamping = true;
orbit.minDistance=35; orbit.maxDistance=1600;
scene.add(new THREE.HemisphereLight(0xffffff,0x45596b,2));
const key = new THREE.DirectionalLight(0xffffff,2.5);key.position.set(250,400,250);scene.add(key);
const fill = new THREE.DirectionalLight(0xc6ecff,1.5);fill.position.set(-250,150,-150);scene.add(fill);
const grid = new THREE.GridHelper(500,20,0xa7b7bf,0xc6d0d5);grid.position.y=-43;scene.add(grid);
new ResizeObserver(()=>{const w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}).observe(stage);
function resetCamera(){camera.position.set(450,315,560);orbit.target.set(0,155,0);orbit.update();}
resetCamera();
const groups = new Map(), objects=new Map(), buttons=new Map(), hidden=new Set();
let data,evidence,selected,isolated=false,playing=false,ghost=false,section=false,angle=0,explosion=0;
const clip = new THREE.Plane(new THREE.Vector3(-1,0,0),0);
const toView = a => new THREE.Vector3(a[0],a[2],-a[1]);

function select(id){
  selected=id;
  const occurrence=data.occurrences.find(p=>p.id===id);
  $('name').textContent=occurrence.name;
  $('description').textContent=occurrence.function;
  for(const [oid,object] of objects){object.traverse(o=>{if(o.isMesh)o.material.emissive.set(oid===id?0x144d55:0x000000);});}
  for(const [oid,b] of buttons)b.setAttribute('aria-pressed',String(oid===id));
  updateVisibility();
  if(isolated)frameAssembly();
}
function updateVisibility(){
  for(const [id,object] of objects)object.visible=!hidden.has(id)&&(!isolated||id===selected);
  $('isolate').setAttribute('aria-pressed',String(isolated));
  $('hide').setAttribute('aria-pressed',String(hidden.has(selected)));
  $('hide').textContent=hidden.has(selected)?'Show part':'Hide part';
  grid.visible=!isolated;
}
function frameAssembly(){
  scene.updateMatrixWorld(true);
  const box=new THREE.Box3();
  for(const object of objects.values())if(object.visible)box.expandByObject(object);
  if(box.isEmpty())return;
  const sphere=box.getBoundingSphere(new THREE.Sphere());
  grid.position.y=box.min.y-12;
  const direction=camera.position.clone().sub(orbit.target).normalize();
  const halfFov=Math.min(camera.fov*Math.PI/360,Math.atan(Math.tan(camera.fov*Math.PI/360)*camera.aspect));
  const distance=Math.max(90,sphere.radius/Math.sin(halfFov)*1.4);
  orbit.target.copy(sphere.center);orbit.target.y-=sphere.radius*0.08;
  camera.position.copy(orbit.target).addScaledVector(direction,distance);orbit.update();
}
function pose(){
  if(!data)return;
  const m=data.mechanism, state=sliderCrank(angle,m.stroke_mm/2,m.rod_length_mm);
  groups.get('crank-group').rotation.x=state.angle;
  groups.get('rod-group').position.set(0,state.journalY,state.journalZ);
  groups.get('rod-group').rotation.x=state.rodAngle;
  groups.get('piston-group').position.set(0,state.pistonY,0);
  for(const o of data.occurrences){
    objects.get(o.id).position.copy(toView(o.position_cad_mm)).addScaledVector(toView(o.explode_cad_mm),explosion);
  }
  $('angle').value=String(angle);$('angle-value').textContent=`${Math.round(angle)}°`;
  $('explode-value').textContent=`${Math.round(explosion*100)}%`;
}
function togglePlay(value){playing=value;$('play').setAttribute('aria-pressed',String(playing));$('play').textContent=playing?'Pause mechanism':'Play mechanism';}
$('play').onclick=()=>togglePlay(!playing);
$('angle').oninput=e=>{togglePlay(false);angle=Number(e.target.value);pose();};
$('explode').oninput=e=>{explosion=Number(e.target.value);pose();frameAssembly();};
$('isolate').onclick=()=>{isolated=!isolated;hidden.delete(selected);updateVisibility();frameAssembly();};
$('hide').onclick=()=>{hidden.has(selected)?hidden.delete(selected):hidden.add(selected);updateVisibility();};
$('show-all').onclick=()=>{isolated=false;hidden.clear();updateVisibility();frameAssembly();};
$('section').onclick=()=>{section=!section;$('section').setAttribute('aria-pressed',String(section));for(const object of objects.values())object.traverse(o=>{if(o.isMesh){o.material.clippingPlanes=section?[clip]:[];o.material.needsUpdate=true;}});};
$('ghost').onclick=()=>{ghost=!ghost;$('ghost').setAttribute('aria-pressed',String(ghost));objects.get('piston-1')?.traverse(o=>{if(o.isMesh){o.material.transparent=ghost;o.material.opacity=ghost?0.18:1;o.material.depthWrite=!ghost;o.material.needsUpdate=true;}});};
$('reset').onclick=()=>{togglePlay(false);angle=0;explosion=0;$('explode').value='0';isolated=false;hidden.clear();if(section)$('section').click();if(ghost)$('ghost').click();pose();select('piston-1');resetCamera();frameAssembly();};
const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();let down;
renderer.domElement.addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);
renderer.domElement.addEventListener('pointerup',e=>{
  if(!data||!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;
  const r=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);
  raycaster.setFromCamera(pointer,camera);
  const hits=raycaster.intersectObjects([...objects.values()].filter(o=>o.visible),true);
  const hit=hits.find(h=>!section||clip.distanceToPoint(h.point)>=0);
  if(hit){let o=hit.object;while(o&&!o.userData.occurrence)o=o.parent;if(o)select(o.userData.occurrence);}
});
async function json(url){const r=await fetch(url);if(!r.ok)throw new Error(`${url}: ${r.status}`);return r.json();}
try{
  [data,evidence]=await Promise.all([json('/inventory/engine/first-assembly.json'),json('/inventory/engine/dimensions.json')]);
  for(const id of ['piston-group','rod-group','crank-group']){const g=new THREE.Group();groups.set(id,g);scene.add(g);}
  const loader=new GLTFLoader();
  const models=new Map(await Promise.all(data.definitions.map(async d=>[d.id,(await loader.loadAsync(d.glb)).scene])));
  for(const o of data.occurrences){
    const object=models.get(o.definition).clone(true);object.scale.setScalar(data.coordinate_system.display_scale);
    object.userData.occurrence=o.id;
    object.traverse(n=>{if(n.isMesh){n.material=n.material.clone();n.material.side=THREE.DoubleSide;}});
    groups.get(o.parent).add(object);objects.set(o.id,object);
  }
  for(const [id,label] of [['piston-group','Piston assembly'],['rod-group','Connecting rod assembly'],['crank-group','Mechanism context']]){
    const details=document.createElement('details');details.open=true;
    const summary=document.createElement('summary');summary.textContent=label;details.append(summary);
    for(const o of data.occurrences.filter(o=>o.parent===id)){
      const button=document.createElement('button');button.className='part';button.textContent=o.name;button.onclick=()=>select(o.id);button.setAttribute('aria-pressed','false');button.dataset.part=o.id;details.append(button);buttons.set(o.id,button);
    }$('parts').append(details);
  }
  $('part-count').textContent=`${data.occurrences.length-1} physical parts + schematic crank`;
  for(const id of ['bore','stroke','compression_height','pin_diameter','dish_depth','compression_ring_width','oil_ring_pack_width','rod_length','pin_offset']){
    const c=evidence.claims.find(c=>c.id===id);const el=document.createElement('div');el.className='dim';
    const label=document.createElement('span');label.textContent=c.id.replaceAll('_',' ');
    const value=document.createElement('span');value.textContent=`${Number(c.value.toFixed(3))} ${c.unit}`;
    const note=document.createElement('em');note.textContent=`${c.status}: ${c.note}`;
    el.append(label,value,note);$('dimensions').append(el);
  }
  for(const s of Object.values(evidence.sources)){
    const a=document.createElement('a');a.className='source';a.href=s.url;a.target='_blank';a.rel='noopener';a.textContent=s.title+(s.printed_page?` · printed p. ${s.printed_page}`:'');$('sources').append(a);
  }
  for(const text of data.omissions){const li=document.createElement('li');li.textContent=text;$('omissions').append(li);}
  pose();select('piston-1');frameAssembly();
  $('status').textContent='Orbit: drag · Zoom: scroll · Select: click a part\nCAD solids, with individual component identity';
  document.body.dataset.ready='true';
}catch(e){$('error').style.display='block';$('error').textContent=`Could not load the assembly: ${e.message}`;$('status').textContent='Assembly unavailable';console.error(e);}
let last=performance.now();
function animate(now){const dt=Math.min((now-last)/1000,0.1);last=now;if(playing&&data){angle=(angle+dt*30)%360;pose();}orbit.update();renderer.render(scene,camera);requestAnimationFrame(animate);}
requestAnimationFrame(animate);
