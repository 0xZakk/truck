import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { buildNavigation } from './engine-navigation.js';
import { sliderCrank } from './engine-motion.js';

const $ = id => document.getElementById(id);
for(const control of document.querySelectorAll('button,input,select'))control.disabled=true;
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
orbit.minDistance=2; orbit.maxDistance=12000;camera.far=30000;camera.near=.05;
scene.add(new THREE.HemisphereLight(0xffffff,0x45596b,2));
const key = new THREE.DirectionalLight(0xffffff,2.5);key.position.set(250,400,250);scene.add(key);
const fill = new THREE.DirectionalLight(0xc6ecff,1.5);fill.position.set(-250,150,-150);scene.add(fill);
const grid = new THREE.GridHelper(1600,32,0xa7b7bf,0xc6d0d5);grid.position.y=-43;scene.add(grid);
new ResizeObserver(()=>{const w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}).observe(stage);
function resetCamera(){camera.position.set(450,315,560);orbit.target.set(0,155,0);orbit.update();}
resetCamera();
const groups=new Map(),objects=new Map();
let data,nav,current='engine',playing=false,ghost=false,section=false,angle=0,explosion=0;
const clip=new THREE.Plane(new THREE.Vector3(-1,0,0),0);
const toView=a=>new THREE.Vector3(a[0],a[2],-a[1]);
const covers=['block','cylinder-head','valve-cover','timing-cover','oil-pan'];
function linkTo(a,id){a.href=nav.url(id);a.onclick=e=>{if(e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();navigate(id);};}
function card(id,search=false){
  const n=nav.nodes.get(id),a=document.createElement('a');a.className='nav-card';a.dataset.node=id;linkTo(a,id);
  if(id===current)a.setAttribute('aria-current','page');
  const title=document.createElement('strong');title.textContent=n.name;
  const detail=document.createElement('small');detail.textContent=search?nav.ancestors(id).slice(0,-1).map(n=>n.name).join(' › '):n.type==='part'?'Inspect part':`${nav.parts(id).length} parts · Open assembly`;
  const text=document.createElement('div');text.append(title,detail);const arrow=document.createElement('span');arrow.className='arrow';arrow.textContent='›';arrow.setAttribute('aria-hidden','true');a.append(text,arrow);return a;
}
function clearSearch(){ $('part-search').value='';$('search-results').hidden=true;$('browse').hidden=false;$('clear-search').hidden=true; }
function search(){
  const query=$('part-search').value.trim();if(!query){clearSearch();return;}
  $('browse').hidden=true;$('search-results').hidden=false;$('clear-search').hidden=false;
  const results=nav.search(query);$('search-count').textContent=results.length?`${results.length} results${results.length>40?' · showing first 40':''}`:'No matches. Try a part name such as “piston”.';
  $('results').replaceChildren(...results.slice(0,40).map(n=>card(n.id,true)));
}
function styles(){
  $('section').setAttribute('aria-pressed',String(section));$('ghost').setAttribute('aria-pressed',String(ghost));
  for(const [id,object] of objects)object.traverse(o=>{if(o.isMesh){const transparent=ghost&&covers.includes(id);o.material.clippingPlanes=section?[clip]:[];o.material.transparent=transparent;o.material.opacity=transparent?.12:1;o.material.depthWrite=!transparent;o.material.needsUpdate=true;}});
}
function partDetails(n){
  const d=data.definitions.find(d=>d.id===n.definition);$('description').textContent=n.function;
  linkTo($('part-page'),n.parent);$('part-page').textContent=`See assembled in ${nav.nodes.get(n.parent).name} →`;
  $('part-evidence').replaceChildren();
  const paragraphs=[`Geometry: ${d.geometry_status}. ${data.occurrences.filter(o=>o.definition===d.id).length} instances in this reconstruction.`,...(d.unresolved||[])];
  if(d.model_bounds_mm)paragraphs.push(`Modeled envelope: ${d.model_bounds_mm.map(n=>n.toFixed(2)).join(' × ')} mm (CAD X × Y × Z). Model measurements, not verified manufacturing dimensions.`);
  for(const text of paragraphs){const p=document.createElement('p');p.textContent=text;$('part-evidence').append(p);}
  $('part-sources').replaceChildren();for(const id of d.sources||[]){const s=data.sources[id];if(!s)continue;const a=document.createElement('a');a.className='source';a.href=s.url;a.target='_blank';a.rel='noopener';a.textContent=s.title;$('part-sources').append(a);}
  $('step-download').href=d.step;
  const siblings=nav.nodes.get(n.parent).children.filter(id=>nav.nodes.get(id).type==='part'),index=siblings.indexOf(n.id);
  for(const [element,id,prefix] of [['previous-part',siblings[index-1],'← Previous'],['next-part',siblings[index+1],'Next →']]){const a=$(element);a.hidden=!id;if(id){linkTo(a,id);a.textContent=prefix;a.title=nav.nodes.get(id).name;}}
}
function navigate(id,historyMode='push'){
  if(!nav?.nodes.has(id))return;
  const changed=current!==id;current=id;const n=nav.nodes.get(id),isPart=n.type==='part',visible=new Set(nav.parts(id));
  togglePlay(false);angle=0;explosion=0;section=false;ghost=false;$('explode').value='0';clearSearch();
  for(const [key,object] of objects)object.visible=visible.has(key);
  grid.visible=!isPart;styles();pose();resetCamera();frameAssembly();
  const path=nav.ancestors(id);$('breadcrumbs').replaceChildren();
  for(const node of path){if(node!==path[0]){const separator=document.createElement('span');separator.className='crumb-separator';separator.textContent='›';separator.setAttribute('aria-hidden','true');$('breadcrumbs').append(separator);}const el=document.createElement(node.id===id?'span':'a');el.textContent=node.name;if(node.id===id)el.setAttribute('aria-current','page');else linkTo(el,node.id);$('breadcrumbs').append(el);}
  $('up').hidden=!n.parent;if(n.parent){linkTo($('up'),n.parent);$('up').textContent=`← Up to ${nav.nodes.get(n.parent).name}`;}
  linkTo($('home'),'engine');$('home').hidden=id==='engine';
  $('nav-title').textContent=id==='engine'?'Explore the engine':n.name;
  $('view-title').textContent=n.name;$('view-kind').textContent=isPart?'Individual part':id==='engine'?'Whole engine':'Assembly';
  $('level-label').textContent=id==='engine'?'Start here':isPart?'Inspect a part':'Explore an assembly';
  $('nav-description').textContent=isPart?'':`${visible.size} parts${id==='engine'?' in this reconstruction':''}. Choose ${id==='engine'?'an assembly to see what’s inside.':'a component below to take a closer look.'}`;
  $('selection').hidden=!isPart;if(isPart)partDetails(n);
  $('contents-title').textContent=isPart?`Parts in ${nav.nodes.get(n.parent).name}`:id==='engine'?'Choose an assembly':'Inside this assembly';
  $('parts').replaceChildren(...(isPart?nav.nodes.get(n.parent).children:n.children).map(key=>card(key)));
  document.querySelector('aside').scrollTop=0;
  $('assembly-controls').hidden=isPart;
  $('motion-controls').hidden=![...visible].some(key=>{let p=data.occurrences.find(o=>o.id===key).parent;while(p){const a=data.assemblies.find(a=>a.id===p);if(a.motion)return true;p=a.parent;}return false;});
  $('ghost').hidden=!covers.some(id=>visible.has(id))||isPart;
  $('status').textContent=isPart?'Inspecting one part · Use the path above to return':`Showing ${visible.size} parts · Click a part to inspect it`;
  document.title=`${n.name} · Ford 4.9L engine`;
  if(historyMode==='replace')history.replaceState(null,'',nav.url(id));else if(historyMode==='push'&&changed)history.pushState(null,'',nav.url(id));
  if(historyMode==='push'){$('nav-title').tabIndex=-1;$('nav-title').focus({preventScroll:true});}
}
function frameAssembly(){
  scene.updateMatrixWorld(true);
  const box=new THREE.Box3();
  for(const object of objects.values())if(object.visible)box.expandByObject(object);
  if(box.isEmpty())return;
  const sphere=box.getBoundingSphere(new THREE.Sphere());
  clip.constant=sphere.center.x;
  grid.position.y=box.min.y-12;
  grid.scale.setScalar(Math.max(.02,sphere.radius/400));
  const direction=camera.position.clone().sub(orbit.target).normalize();
  const halfFov=Math.min(camera.fov*Math.PI/360,Math.atan(Math.tan(camera.fov*Math.PI/360)*camera.aspect));
  const distance=Math.max(5,sphere.radius/Math.sin(halfFov)*1.35);
  orbit.target.copy(sphere.center);orbit.target.y-=sphere.radius*0.08;
  camera.position.copy(orbit.target).addScaledVector(direction,distance);orbit.update();
}
function pose(){
  if(!data)return;
  const m=data.mechanism;
  for(const a of data.assemblies){
    const g=groups.get(a.id);g.position.copy(toView(a.position_cad_mm||[0,0,0]));g.rotation.set(0,0,0);
    if(!a.motion)continue;
    const state=sliderCrank(angle+(a.motion.phase_deg||0),m.stroke_mm/2,m.rod_length_mm);
    if(a.motion.type==='crank')g.rotation.x=angle*Math.PI/180;
    if(a.motion.type==='cam')g.rotation.x=-angle*Math.PI/360;
    if(a.motion.type==='rod'){g.position.y+=state.journalY;g.position.z+=state.journalZ;g.rotation.x=state.rodAngle;}
    if(a.motion.type==='piston')g.position.y+=state.pistonY;
  }
  for(const o of data.occurrences){
    objects.get(o.id).position.copy(toView(o.position_cad_mm)).addScaledVector(toView(o.explode_cad_mm),explosion);
  }
  $('angle').value=String(angle);$('angle-value').textContent=`${Math.round(angle)}°`;
  $('explode-value').textContent=`${Math.round(explosion*100)}%`;
}
function togglePlay(value){playing=value;$('play').setAttribute('aria-pressed',String(playing));$('play').textContent=playing?'Pause crank motion':'Play crank motion';}
$('play').onclick=()=>togglePlay(!playing);
$('angle').oninput=e=>{togglePlay(false);angle=Number(e.target.value);pose();};
$('explode').oninput=e=>{explosion=Number(e.target.value);pose();frameAssembly();};
$('section').onclick=()=>{section=!section;styles();};$('ghost').onclick=()=>{ghost=!ghost;styles();};
$('reset').onclick=()=>navigate(current,'none');
$('part-search').oninput=search;$('part-search').onkeydown=e=>{if(e.key==='Escape')clearSearch();};
$('clear-search').onclick=()=>{clearSearch();$('part-search').focus();};
window.addEventListener('popstate',()=>{if(nav)navigate(nav.fromUrl(location.href)||'engine','none');});
const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();let down;
renderer.domElement.addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);
renderer.domElement.addEventListener('pointerup',e=>{
  if(!nav||!down||e.button!==0||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;
  const r=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);
  raycaster.setFromCamera(pointer,camera);const hits=raycaster.intersectObjects([...objects.values()].filter(o=>o.visible),true);
  const hit=hits.find(h=>!section||clip.distanceToPoint(h.point)>=0);if(hit){let o=hit.object;while(o&&!o.userData.occurrence)o=o.parent;if(o&&o.userData.occurrence!==current)navigate(o.userData.occurrence);}
});
try{
  const response=await fetch('/inventory/engine/full-assembly.json');if(!response.ok)throw new Error(`Manifest: ${response.status}`);data=await response.json();nav=buildNavigation(data);
  for(const a of data.assemblies){const g=new THREE.Group();groups.set(a.id,g);}
  for(const a of data.assemblies)(a.parent?groups.get(a.parent):scene).add(groups.get(a.id));
  const loader=new GLTFLoader();
  const models=new Map(await Promise.all(data.definitions.map(async d=>[d.id,(await loader.loadAsync(d.glb)).scene])));
  for(const o of data.occurrences){
    const object=models.get(o.definition).clone(true);object.scale.setScalar(data.coordinate_system.display_scale);
    object.userData.occurrence=o.id;
    const r=o.rotation_cad_deg||[0,0,0];
    // Convert CAD rotation matrix by the fixed CAD-to-view basis.
    const basis=new THREE.Matrix4().makeRotationX(-Math.PI/2);
    const cad=new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(...r.map(v=>v*Math.PI/180),'ZYX'));
    object.quaternion.setFromRotationMatrix(basis.clone().multiply(cad).multiply(basis.clone().invert()));
    object.traverse(n=>{if(n.isMesh){n.material=n.material.clone();n.material.side=THREE.DoubleSide;}});
    groups.get(o.parent).add(object);objects.set(o.id,object);
  }

  $('coverage').textContent=`${data.definitions.length} component designs assembled as ${data.occurrences.length} parts. This is an incomplete engine reconstruction.`;
  for(const text of data.omissions){const li=document.createElement('li');li.textContent=text;$('omissions').append(li);}
  const requested=nav.fromUrl(location.href);navigate(requested||'engine','replace');
  if(!requested){$('error').hidden=false;$('error').textContent='That component was not found. Choose an assembly to continue.';}
  for(const control of document.querySelectorAll('button,input,select'))control.disabled=false;
  document.body.dataset.ready='true';
}catch(e){$('error').hidden=false;$('error').textContent=`Could not load the assembly: ${e.message}`;$('status').textContent='Assembly unavailable';console.error(e);}
let last=performance.now();
function animate(now){const dt=Math.min((now-last)/1000,.1);last=now;if(playing&&data){angle=(angle+dt*30)%360;pose();}orbit.update();renderer.render(scene,camera);requestAnimationFrame(animate);}
requestAnimationFrame(animate);
