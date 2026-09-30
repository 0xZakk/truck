import { buildThrottleSpringMesh } from './throttle-return-spring-mesh.js';
import { createThrottleCableMotion, cableAngle } from './throttle-cable-motion.js';
import { createEvrDiscreteMotion } from './evr-discrete-motion.js';
import { engineLearningModules, resolveEngineLearning } from './engine-learning-modules.js?revision=rear-neck-20260930';
import { explodeOffset } from './engine-explode-stages-candidate.js';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { occurrenceValvePose, springMeshData } from './engine-valve-layout.js';
import {sourceOccurrencePose} from './engine-valve-source.js';
import {sourceSpringMeshDataFast,prewarmSourceSpringCache} from './engine-valve-source-spring-cache.js';
import { buildNavigation } from './engine-navigation.js?revision=linkage-20260926';
import { sliderCrank, rotaryViewRotation, compressorState } from './engine-motion.js';

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
void prewarmSourceSpringCache(96,12);
let data,nav,learning={},current='engine',playing=false,ghost=false,section=false,angle=0,throttleAngle=0,explosion=0;
let compressorAngle=0,compressorEngaged=true,compressorPlaying=false;
let throttleSpringPaths=null;
let evrMotion=null,evrFrame=null,evrPending=false,evrRequestSerial=0;
let cableMotionPromise=null,cableFrame=null,cableRequested=null,cableRequestSerial=0,cableMotionFailed=false,modelRevision='';
const clip=new THREE.Plane(new THREE.Vector3(-1,0,0),0);
const toView=a=>new THREE.Vector3(a[0],a[2],-a[1]);
function cadQuaternion(rotation=[0,0,0]){
  const basis=new THREE.Matrix4().makeRotationX(-Math.PI/2);
  const matrix=new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(...rotation.map(value=>value*Math.PI/180),'ZYX'));
  return new THREE.Quaternion().setFromRotationMatrix(basis.clone().multiply(matrix).multiply(basis.clone().invert()));
}
const covers=['engine-oil-dipstick-tube','throttle-linkage-shield-estimated','pilot-bearing-case','pilot-bearing-seal','evr-body','evr-cap','egr-tube-heat-sleeve','egr-tube-valve-nut','egr-body','egr-lower-shell','egr-upper-shell','evp-body','evp-lid','pushrod-cover','oil-pressure-body','oil-pressure-insulator','oil-pressure-rim','oil-filter-case','pcv-body','pcv-outlet-head',...['supply','return'].flatMap(line=>['male','female','cage'].map(part=>`fuel-${line}-coupling-${part}`)),'fuel-test-body','fuel-test-core','fuel-test-cap',...Array.from({length:6},(_,i)=>`spark-plug-${i+1}-shell`),...Array.from({length:6},(_,i)=>`spark-plug-${i+1}-insulator`),'ignition-coil-case','distributor-cap','distributor-housing','coolant-outlet-housing','water-pump-housing','block','cylinder-head','valve-cover','timing-cover','oil-pan','oil-pump-housing','oil-pump-cover','efi-upper-intake','efi-lower-intake','throttle-housing','iac-valve-body','iac-solenoid-can','tps-housing','tps-cover','regulator-upper-housing','regulator-lower-housing','exhaust-front','exhaust-rear',...Array.from({length:6},(_,i)=>`injector-${i+1}-metal-body`),...Array.from({length:6},(_,i)=>`injector-${i+1}-connector-shell`)];
covers.push('alternator-drive-housing','alternator-rear-housing','fan-clutch-front-cover','fan-clutch-housing');
covers.push('engine-coolant-temperature-body','engine-coolant-temperature-insulator');
covers.push('ps-pump-reservoir','ps-pump-housing','ps-pump-valve-cover');
covers.push('ac-compressor-front-cylinder','ac-compressor-rear-cylinder','ac-compressor-front-head','ac-compressor-rear-head');
covers.push('thermactor-housing','thermactor-front-plate','thermactor-rear-plate');
covers.push('starter-frame','starter-brush-end-plate','starter-drive-end-housing','starter-solenoid-shell','starter-solenoid-end-cap');
covers.push('evr-magnetic-shell-illustrative','evr-bobbin-illustrative');
const story=document.createElement('section');story.id='assembly-story';$('parts').after(story);
function lessonSource(id){
  const source=data.sources[id];if(!source)return null;
  const a=document.createElement('a');a.className='source';
  // Encode each on-disk segment: manual directory names contain literal %20.
  a.href=source.path?'/'+source.path.replace(/^\//,'').split('/').map(encodeURIComponent).join('/'):source.url;
  a.target='_blank';a.rel='noopener';a.textContent=source.title;
  return a;
}
function explain(id){
  story.replaceChildren();const entry=learning[id];if(!entry)return;
  const intro=document.createElement('p');intro.textContent=entry.summary;
  const limits=document.createElement('p');limits.className='study-limits';limits.textContent=entry.limits;story.append(intro,limits);
  for(const [title,items] of [['How it works',entry.steps],['Issues to investigate',entry.troubleshooting]]){
    const details=document.createElement('details'),summary=document.createElement('summary');summary.textContent=title;details.append(summary);
    for(const item of items||[]){const h=document.createElement('h3');h.textContent=item.title;const p=document.createElement('p');p.textContent=item.text;details.append(h,p);if(item.part){const a=document.createElement('a');linkTo(a,item.part);a.textContent=`Explore ${nav.nodes.get(item.part).name} →`;details.append(a);}if(item.source){const a=lessonSource(item.source);if(a)details.append(a);}}
    story.append(details);
  }
  const refs=document.createElement('details'),summary=document.createElement('summary');summary.textContent='References';refs.append(summary);
  for(const id of entry.sources||[]){const a=lessonSource(id);if(a)refs.append(a);}story.append(refs);
}
function linkTo(a,id){a.href=nav.url(id);a.onclick=e=>{if(e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();navigate(id);};}
function card(id,search=false){
  const n=nav.nodes.get(id),a=document.createElement('a');a.className='nav-card';a.dataset.node=id;linkTo(a,id);
  if(id===current)a.setAttribute('aria-current','page');
  const title=document.createElement('strong');title.textContent=n.name;
  const detail=document.createElement('small');detail.textContent=search?nav.ancestors(id).slice(0,-1).map(n=>n.name).join(' › '):n.type==='part'?'Inspect part':`${nav.parts(id).length} ${nav.parts(id).length===1?'part':'parts'} · Open assembly`;
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
  $('part-sources').replaceChildren();for(const id of d.sources||[]){const a=lessonSource(id);if(a)$('part-sources').append(a);}
  $('step-download').href=d.step;
  const siblings=nav.nodes.get(n.parent).children.filter(id=>nav.nodes.get(id).type==='part'),index=siblings.indexOf(n.id);
  for(const [element,id,prefix] of [['previous-part',siblings[index-1],'← Previous'],['next-part',siblings[index+1],'Next →']]){const a=$(element);a.hidden=!id;if(id){linkTo(a,id);a.textContent=prefix;a.title=nav.nodes.get(id).name;}}
}
function navigate(id,historyMode='push'){
  if(!nav?.nodes.has(id))return;
  const changed=current!==id;current=id;const n=nav.nodes.get(id),isPart=n.type==='part',visible=new Set(nav.parts(id));
  togglePlay(false);toggleCompressorPlay(false);angle=0;throttleAngle=0;compressorAngle=0;compressorEngaged=true;explosion=0;section=false;ghost=false;$('explode').value='0';clearSearch();
  if(evrMotion)void requestEvrPose(0);
  for(const [key,object] of objects)object.visible=visible.has(key);
  grid.visible=!isPart;styles();pose();resetCamera();
  const path=nav.ancestors(id);$('breadcrumbs').replaceChildren();
  for(const node of path){if(node!==path[0]){const separator=document.createElement('span');separator.className='crumb-separator';separator.textContent='›';separator.setAttribute('aria-hidden','true');$('breadcrumbs').append(separator);}const el=document.createElement(node.id===id?'span':'a');el.textContent=node.name;if(node.id===id)el.setAttribute('aria-current','page');else linkTo(el,node.id);$('breadcrumbs').append(el);}
  $('up').hidden=!n.parent;if(n.parent){linkTo($('up'),n.parent);$('up').textContent=`← Up to ${nav.nodes.get(n.parent).name}`;}
  linkTo($('home'),'engine');$('home').hidden=id==='engine';
  $('nav-title').textContent=id==='engine'?'Explore the engine':n.name;
  $('view-title').textContent=n.name;$('view-kind').textContent=isPart?'Individual part':id==='engine'?'Whole engine':'Assembly';
  const visibleDefinitions=new Set(data.occurrences.filter(o=>visible.has(o.id)).map(o=>o.definition));
  if(data.definitions.some(d=>visibleDefinitions.has(d.id)&&d.geometry_status==='provisional'))$('view-kind').textContent+=' · provisional study';
  $('level-label').textContent=id==='engine'?'Start here':isPart?'Inspect a part':'Explore an assembly';
  $('nav-description').textContent=isPart?'':`${visible.size} parts${id==='engine'?' in this reconstruction':''}. Choose ${id==='engine'?'an assembly to see what’s inside.':'a component below to take a closer look.'}`;
  $('selection').hidden=!isPart;if(isPart)partDetails(n);
  explain(id);
  $('contents-title').textContent=isPart?`Parts in ${nav.nodes.get(n.parent).name}`:id==='engine'?'Choose an assembly':'Inside this assembly';
  $('parts').replaceChildren(...(isPart?nav.nodes.get(n.parent).children:n.children).map(key=>card(key)));
  document.querySelector('aside').scrollTop=0;
  $('assembly-controls').hidden=isPart;
  $('motion-controls').hidden=![...visible].some(key=>{let p=data.occurrences.find(o=>o.id===key).parent;while(p){const a=data.assemblies.find(a=>a.id===p);if(a.motion&&!['throttle','fs10'].includes(a.motion.type))return true;p=a.parent;}return false;});
  $('compressor-controls').hidden=![...visible].some(key=>{let parent=data.occurrences.find(occurrence=>occurrence.id===key).parent;while(parent){const assembly=data.assemblies.find(item=>item.id===parent);if(assembly.motion?.type==='fs10')return true;parent=assembly.parent;}return false;});
  $('throttle-controls').hidden=isPart||!(visible.has('throttle-shaft')||visible.has('tps-rotor'));
  $('evr-controls').hidden=isPart||!evrMotion||!['egr','egr-vacuum-regulator'].includes(id);
  $('ghost').hidden=!covers.some(id=>visible.has(id))||isPart;
  $('status').textContent=isPart?'Inspecting one part · Use the path above to return':`Showing ${visible.size} parts · Click a part to inspect it`;
  // Measure after the controls have reached this scope's actual height.
  frameAssembly();
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
  // A transverse cut falls in the gap between the two exhaust castings.
  // Section these along their length so both hollow collectors stay visible.
  const longitudinal=nav.ancestors(current).some(n=>n.id==='exhaust');
  clip.normal.set(longitudinal?0:-1,0,longitudinal?-1:0);
  clip.constant=longitudinal?sphere.center.z:sphere.center.x;
  grid.position.set(sphere.center.x,box.min.y-12,sphere.center.z);
  grid.scale.setScalar(Math.max(.02,sphere.radius/400));
  const direction=camera.position.clone().sub(orbit.target).normalize();
  // Frame inside the unobscured canvas, not behind the title and sliders.
  const stageRect=stage.getBoundingClientRect();
  const statusRect=$('status').getBoundingClientRect();
  const controls=$('explode').closest('.controls');
  const controlsRect=controls.getBoundingClientRect();
  const topInset=Math.max(0,statusRect.bottom-stageRect.top)+16;
  const bottomInset=controls.hidden?24:Math.max(0,stageRect.bottom-controlsRect.top)+16;
  const usableHeight=Math.max(stageRect.height*.25,stageRect.height-topInset-bottomInset);
  const fullHalfFov=camera.fov*Math.PI/360;
  const visibleCenterY=(topInset+stageRect.height-bottomInset)/2;
  const screenUp=new THREE.Vector3(0,1,0).applyQuaternion(camera.quaternion);
  const screenRight=new THREE.Vector3(1,0,0).applyQuaternion(camera.quaternion);
  const tanFov=Math.tan(fullHalfFov);
  const centerNdc=1-2*visibleCenterY/stageRect.height;
  const halfHeightNdc=usableHeight/stageRect.height;
  const topNdc=centerNdc+halfHeightNdc,bottomNdc=centerNdc-halfHeightNdc;
  const halfWidthNdc=Math.max(.5,1-48/stageRect.width);
  // Fit the projected box, including perspective depth. A bounding sphere
  // wastes most of the viewport on long, shallow assemblies like the intake.
  let distance=5;
  for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z]){
    const corner=new THREE.Vector3(x,y,z).sub(sphere.center);
    const right=corner.dot(screenRight),up=corner.dot(screenUp),depth=corner.dot(direction);
    distance=Math.max(distance,
      depth+Math.abs(right)/(camera.aspect*tanFov*halfWidthNdc),
      (up/tanFov+topNdc*depth)/halfHeightNdc,
      (-up/tanFov-bottomNdc*depth)/halfHeightNdc);
  }
  distance*=1.08;
  const targetOffset=-centerNdc*distance*tanFov;
  orbit.target.copy(sphere.center).addScaledVector(screenUp,targetOffset);
  camera.position.copy(orbit.target).addScaledVector(direction,distance);orbit.update();
}
function setValveSpringHeight(object,height,sourceSized=false){
  const segments=sourceSized&&current==='engine'?96:192;
  if(Math.abs((object.userData.springHeight??-1)-height)<1e-9 && object.userData.springSegments===segments)return;
  const meshData=sourceSized?sourceSpringMeshDataFast(height,segments,segments===96?12:16):springMeshData(height);
  object.traverse(node=>{if(!node.isMesh)return;
    if(!node.userData.dynamicValveSpring || node.geometry.attributes.position.array.length!==meshData.positions.length || Boolean(node.geometry.index)!==Boolean(meshData.indices)){
      if(node.userData.dynamicValveSpring)node.geometry.dispose();
      const geometry=new THREE.BufferGeometry();
      geometry.setAttribute('position',new THREE.BufferAttribute(meshData.positions,3));
      geometry.setAttribute('normal',new THREE.BufferAttribute(meshData.normals,3));
      geometry.setIndex(meshData.indices ? new THREE.BufferAttribute(meshData.indices,1) : null);
      node.geometry=geometry;node.userData.dynamicValveSpring=true;
    }else{
      node.geometry.attributes.position.array.set(meshData.positions);
      node.geometry.attributes.normal.array.set(meshData.normals);
      node.geometry.attributes.position.needsUpdate=true;node.geometry.attributes.normal.needsUpdate=true;
    }
    node.geometry.computeBoundingBox();node.geometry.computeBoundingSphere();
  });object.userData.springHeight=height;object.userData.springSegments=segments;
}
function setThrottleSpringPose(object, degrees){
  if(!throttleSpringPaths)return;
  const index=Math.max(0,Math.min(90,Math.round(degrees)));
  if(object.userData.throttleSpringAngle===index)return;
  const mesh=buildThrottleSpringMesh(throttleSpringPaths.frames[index],throttleSpringPaths.wire_radius_mm);
  object.traverse(node=>{if(!node.isMesh)return;
    if(!node.userData.dynamicThrottleSpring){
      const geometry=new THREE.BufferGeometry();
      geometry.setAttribute('position',new THREE.BufferAttribute(mesh.positions,3));
      geometry.setAttribute('normal',new THREE.BufferAttribute(mesh.normals,3));
      geometry.setIndex(new THREE.BufferAttribute(mesh.indices,1));
      node.geometry=geometry;node.userData.dynamicThrottleSpring=true;
    }else{
      node.geometry.attributes.position.array.set(mesh.positions);
      node.geometry.attributes.normal.array.set(mesh.normals);
      node.geometry.attributes.position.needsUpdate=true;
      node.geometry.attributes.normal.needsUpdate=true;
    }
    node.geometry.computeBoundingBox();node.geometry.computeBoundingSphere();
  });
  object.userData.throttleSpringAngle=index;
}
function requestCablePose(degrees){
  if(!data.occurrences.some(o=>o.throttle_cable)||cableMotionFailed)return;
  const index=cableAngle(degrees);
  if(index===0){
    if(cableRequested!==null||cableFrame){cableRequestSerial++;cableRequested=null;cableFrame=null;}
    return;
  }
  if(cableFrame?.angle_deg===index){
    if(cableRequested!==null){cableRequestSerial++;cableRequested=null;}
    return;
  }
  if(cableRequested===index)return;
  const serial=++cableRequestSerial;cableRequested=index;
  if(!cableMotionPromise)cableMotionPromise=(async()=>{
    const response=await fetch(`/viewer/throttle-cable-motion.json?revision=${modelRevision}`);
    if(!response.ok)throw new Error(`Cable motion: ${response.status}`);
    return createThrottleCableMotion(await response.json());
  })();
  cableMotionPromise.then(motion=>motion.frame(index)).then(frame=>{
    if(serial!==cableRequestSerial)return;
    cableFrame=frame;cableRequested=null;pose();
  }).catch(error=>{
    if(serial!==cableRequestSerial)return;
    cableMotionFailed=true;cableRequested=null;cableFrame=null;throttleAngle=0;
    $('error').hidden=false;$('error').textContent='Cable motion could not load. Reload to try again.';
    console.error(error);pose();
  });
}
function setCablePose(object,kind,displayAngle){
  const frame=cableFrame?.angle_deg===displayAngle?cableFrame:null;
  const rigid=frame?.rigid[kind];
  if(rigid){
    object.position.add(toView(rigid.translation_cad_mm));
    object.quaternion.premultiply(new THREE.Quaternion(...rigid.quaternion_viewer_xyzw));
  }
  if(!['core','compression-spring'].includes(kind))return;
  object.traverse(node=>{
    if(!node.isMesh)return;
    if(!node.userData.cableNeutralGeometry)node.userData.cableNeutralGeometry=node.geometry;
    const mesh=frame?.meshes[kind],index=frame?.angle_deg??0;
    if(node.userData.cableGeometryAngle===index)return;
    if(node.geometry!==node.userData.cableNeutralGeometry)node.geometry.dispose();
    if(!mesh)node.geometry=node.userData.cableNeutralGeometry;
    else{
      const geometry=new THREE.BufferGeometry();
      geometry.setAttribute('position',new THREE.BufferAttribute(mesh.positions,3));
      geometry.setAttribute('normal',new THREE.BufferAttribute(mesh.normals,3));
      geometry.setIndex(new THREE.BufferAttribute(mesh.indices,1));
      geometry.computeBoundingBox();geometry.computeBoundingSphere();node.geometry=geometry;
    }
    node.userData.cableGeometryAngle=index;
  });
}
async function requestEvrPose(index){
  if(!evrMotion)return;
  const serial=++evrRequestSerial;evrPending=true;pose();
  try{
    const applied=await evrMotion.setIndex(index);
    if(applied&&serial===evrRequestSerial&&$('error').textContent.startsWith('EGR vent motion could not load.'))$('error').hidden=true;
  }catch(error){
    if(serial!==evrRequestSerial)return;
    $('error').hidden=false;$('error').textContent='EGR vent motion could not load. The last complete pose is still displayed. Reload to retry.';
    console.error(error);
  }finally{if(serial===evrRequestSerial){evrPending=false;pose();}}
}
async function initializeEvrMotion(loader){
  if(!objects.has('evr-disc-spring-illustrative'))return;
  const response=await fetch(`/models/engine/evr-motion/poses.json?revision=${modelRevision}`);
  if(!response.ok)throw new Error(`EVR poses: ${response.status}`);
  evrMotion=createEvrDiscreteMotion(await response.json(),{
    async loadSpring(url,expectedHash){
      const response=await fetch(`${url}?revision=${expectedHash}`);
      if(!response.ok)throw new Error(`EVR spring: ${response.status}`);
      const bytes=await response.arrayBuffer();
      const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),v=>v.toString(16).padStart(2,'0')).join('');
      if(hash!==expectedHash)throw new Error('EVR spring does not match its validated pose');
      const gltf=await loader.parseAsync(bytes,'');gltf.scene.updateMatrixWorld(true);
      const meshes=[];gltf.scene.traverse(node=>{if(node.isMesh)meshes.push(node);});
      if(meshes.length!==1)throw new Error('Expected one EVR spring mesh');
      return meshes[0].geometry.clone().applyMatrix4(meshes[0].matrixWorld);
    },
    applyPose(frame){
      const nodes=[];objects.get('evr-disc-spring-illustrative').traverse(node=>{if(node.isMesh)nodes.push(node);});
      if(nodes.length!==1)throw new Error('Expected one installed EVR spring mesh');
      nodes[0].geometry=frame.spring;evrFrame=frame;pose();
    }
  });
  // Load the seated pair before revealing the engine, so disc and spring agree.
  await evrMotion.setIndex(0);
}
function pose(){
  if(!data)return;
  requestCablePose(throttleAngle);
  const displayThrottleAngle=cableRequested!==null?(cableFrame?.angle_deg??0):throttleAngle;
  const m=data.mechanism;
  for(const a of data.assemblies){
    const g=groups.get(a.id);g.position.copy(toView(a.position_cad_mm||[0,0,0]));g.quaternion.copy(cadQuaternion(a.rotation_cad_deg));
    if(!a.motion)continue;
    if(a.motion.type==='throttle'){g.rotateZ(-displayThrottleAngle*Math.PI/180);continue;}
    if(a.motion.type==='fs10'){
      const state=compressorState(compressorAngle,a.motion,compressorEngaged);
      g.position.add(toView([state.translationX,0,0]).applyQuaternion(g.quaternion));
      g.rotateX(state.rotationX);continue;
    }
    if(a.motion.type==='rotary'){
      const [rotationX,rotationY,rotationZ]=rotaryViewRotation(angle,a.motion);
      g.rotateX(rotationX);g.rotateY(rotationY);g.rotateZ(rotationZ);continue;
    }
    const state=sliderCrank(angle+(a.motion.phase_deg||0),m.stroke_mm/2,m.rod_length_mm);
    if(a.motion.type==='crank')g.rotateX(angle*Math.PI/180);
    if(a.motion.type==='distributor')g.rotateY(-angle*Math.PI/360);
    if(a.motion.type==='cam')g.rotateX(-angle*Math.PI/360);
    if(a.motion.type==='rod'){g.position.add(new THREE.Vector3(0,state.journalY,state.journalZ).applyQuaternion(g.quaternion));g.rotateX(state.rodAngle);}
    if(a.motion.type==='piston')g.position.add(new THREE.Vector3(0,state.pistonY,0).applyQuaternion(g.quaternion));
  }
  for(const o of data.occurrences){
    const object=objects.get(o.id);
    object.quaternion.copy(cadQuaternion(o.rotation_cad_deg));
    object.position.copy(toView(o.position_cad_mm)).add(toView(explodeOffset(o,explosion)));
    if(o.id==='evr-disc-illustrative'&&evrFrame)object.position.add(toView(evrFrame.discOffsetCadMm).applyQuaternion(object.quaternion));
    if(o.throttle_spring)setThrottleSpringPose(object,displayThrottleAngle);
    if(o.throttle_cable)setCablePose(object,o.throttle_cable.kind,displayThrottleAngle);
    if(o.valvetrain){
      const sourceSized=o.valvetrain.model==='source-sized-v2';
      const motion=sourceSized?sourceOccurrencePose(angle,o.valvetrain):occurrenceValvePose(angle,o.valvetrain);
      // Source-sized linkage offsets use engine axes; legacy offsets use part axes.
      object.position.add(sourceSized?toView(motion.translationEngineCad):toView(motion.translationCad).applyQuaternion(object.quaternion));
      object.rotateX(sourceSized?motion.rotationXDeltaRad:motion.rotationXRad);
      if(motion.springHeightMm!==undefined)setValveSpringHeight(object,motion.springHeightMm,sourceSized);
    }
  }
  $('throttle-angle').value=String(throttleAngle);$('throttle-value').textContent=`${throttleAngle}°${cableRequested!==null?' · loading cable…':''}`;
  $('evr-opening').value=String(evrFrame?.index??0);$('evr-value').textContent=`${(evrFrame?.travelMm??0).toFixed(1)} mm${evrPending?' · loading…':''}`;
  $('angle').value=String(angle);$('angle-value').textContent=`${Math.round(angle)}°`;
  $('compressor-angle').value=String(compressorAngle);$('compressor-value').textContent=`${Math.round(compressorAngle)}°`;
  $('compressor-engaged').checked=compressorEngaged;
  $('explode-value').textContent=`${Math.round(explosion*100)}%`;
}
function togglePlay(value){playing=value;$('play').setAttribute('aria-pressed',String(playing));$('play').textContent=playing?'Pause engine motion':'Play engine motion';}
function toggleCompressorPlay(value){compressorPlaying=value;$('compressor-play').setAttribute('aria-pressed',String(value));$('compressor-play').textContent=value?'Pause compressor motion':'Play compressor motion';}
$('play').onclick=()=>togglePlay(!playing);
$('compressor-play').onclick=()=>toggleCompressorPlay(!compressorPlaying);
$('compressor-angle').oninput=event=>{toggleCompressorPlay(false);compressorAngle=Number(event.target.value);pose();};
$('compressor-engaged').onchange=event=>{compressorEngaged=event.target.checked;pose();};
$('evr-opening').oninput=e=>{void requestEvrPose(Number(e.target.value));};
$('throttle-angle').oninput=e=>{throttleAngle=cableMotionFailed?0:Math.round(Number(e.target.value));pose();};
$('angle').oninput=e=>{togglePlay(false);angle=Number(e.target.value);pose();};
$('explode').oninput=e=>{explosion=Number(e.target.value);pose();frameAssembly();};
$('section').onclick=()=>{section=!section;styles();};$('ghost').onclick=()=>{ghost=!ghost;styles();};
$('reset').onclick=()=>navigate(current,'none');
$('part-search').oninput=search;$('part-search').onkeydown=e=>{if(e.key==='Escape')clearSearch();};
$('clear-search').onclick=()=>{clearSearch();$('part-search').focus();};
document.querySelectorAll('.motion-limits').forEach(detail=>detail.addEventListener('toggle',()=>{if(nav)frameAssembly();}));
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
  const response=await fetch('/inventory/engine/full-assembly.json',{cache:'no-store'});if(!response.ok)throw new Error(`Manifest: ${response.status}`);const manifestText=await response.text();data=JSON.parse(manifestText);nav=buildNavigation(data);
  const revision=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(manifestText))),byte=>byte.toString(16).padStart(2,'0')).join('');
  modelRevision=revision;
  if(data.occurrences.some(o=>o.throttle_spring)){
    const response=await fetch('/viewer/throttle-return-spring-paths.json',{cache:'no-store'});
    if(!response.ok)throw new Error(`Throttle spring paths: ${response.status}`);
    throttleSpringPaths=await response.json();
    if(throttleSpringPaths.schema!=='illustrative-throttle-spring-paths-v1'||throttleSpringPaths.frames.length!==91)throw new Error('Invalid throttle spring motion data');
  }
  const lessons=await Promise.all(engineLearningModules.map(async name=>{const response=await fetch(`/inventory/engine/${name}-learning.json`,{cache:'no-store'});if(!response.ok)throw new Error(`Learning notes: ${response.status}`);return response.json();}));learning=resolveEngineLearning(data,nav.nodes.keys(),...lessons);
  for(const a of data.assemblies){const g=new THREE.Group();groups.set(a.id,g);}
  for(const a of data.assemblies)(a.parent?groups.get(a.parent):scene).add(groups.get(a.id));
  const loader=new GLTFLoader();
  const models=new Map(await Promise.all(data.definitions.map(async d=>[d.id,(await loader.loadAsync(`${d.glb}?revision=${revision}`)).scene])));
  for(const o of data.occurrences){
    const object=models.get(o.definition).clone(true);object.scale.setScalar(data.coordinate_system.display_scale);
    object.userData.occurrence=o.id;
    object.quaternion.copy(cadQuaternion(o.rotation_cad_deg));
    object.traverse(n=>{if(n.isMesh){n.material=n.material.clone();n.material.side=THREE.DoubleSide;}});
    groups.get(o.parent).add(object);objects.set(o.id,object);
  }

  await initializeEvrMotion(loader);
  $('coverage').textContent=`${data.definitions.length} component designs assembled as ${data.occurrences.length} parts. This is an incomplete engine reconstruction.`;
  for(const text of data.omissions){const li=document.createElement('li');li.textContent=text;$('omissions').append(li);}
  const requested=nav.fromUrl(location.href);navigate(requested||'engine','replace');
  if(!requested){$('error').hidden=false;$('error').textContent='That component was not found. Choose an assembly to continue.';}
  for(const control of document.querySelectorAll('button,input,select'))control.disabled=false;
  document.body.dataset.ready='true';
}catch(e){$('error').hidden=false;$('error').textContent=`Could not load the assembly: ${e.message}`;$('status').textContent='Assembly unavailable';console.error(e);}
let last=performance.now();
function animate(now){const dt=Math.min((now-last)/1000,.1);last=now;if(data&&(playing||compressorPlaying)){if(playing)angle=(angle+dt*30)%720;if(compressorPlaying)compressorAngle=(compressorAngle+dt*30)%360;pose();}orbit.update();renderer.render(scene,camera);requestAnimationFrame(animate);}
requestAnimationFrame(animate);
