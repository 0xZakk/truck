import {engineLearningModules} from '../viewer/engine-learning-modules.js';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {buildNavigation} from '../viewer/engine-navigation.js';
const manifest=JSON.parse(await readFile(new URL('../inventory/engine/full-assembly.json',import.meta.url)));
const original=JSON.stringify(manifest), nav=buildNavigation(manifest);
assert.equal(JSON.stringify(manifest),original,'Navigation must not alter CAD transforms');
const all=nav.parts('engine');
assert.equal(new Set(all).size,manifest.occurrences.length);
assert.equal(all.length,manifest.occurrences.length,'Each part belongs to exactly one browsing branch');
for(const n of nav.nodes.values()){
  const path=nav.ancestors(n.id);
  assert.equal(path[0].id,'engine',`${n.id} must be reachable`);
  assert.equal(new Set(path.map(n=>n.id)).size,path.length);
  assert.equal(nav.fromUrl(nav.url(n.id)),n.id,'Deep links must round-trip');
}
assert.ok(nav.nodes.get('engine').children.includes('lubrication'));
assert.equal(nav.parts('oil-pump-assembly').length,14);
assert.equal(nav.parts('oil-drive-assembly').length,2);
for(const [identifier,ratio] of [['oil-pump-intermediate-rotation',-.5],['oil-pump-inner-rotation',-.5],['oil-pump-outer-rotation',-.4]]){
  assert.deepEqual(manifest.assemblies.find(assembly=>assembly.id===identifier)?.motion,{type:'rotary',axis:'z',ratio});
}
assert.equal(manifest.occurrences.find(part=>part.id==='oil-pump-drive-retainer').parent,'oil-pump-intermediate-rotation');
assert.equal(nav.parts('oil-pickup-assembly').length,3);
assert.equal(nav.parts('induction').length,206);
assert.equal(nav.parts('intake-head-locator').length,1);
assert.ok(nav.ancestors('intake-head-locating-dowel').some(node=>node.id==='induction'));
assert.equal(nav.parts('fuel-test-valve').length,8);
assert.equal(nav.parts('front-manifold-eye').length,3);
for(const identifier of ['front-manifold-lifting-eye','front-manifold-stud13','front-manifold-bolt14']){
  assert.ok(nav.ancestors(identifier).some(node=>node.id==='exhaust'));
  assert.equal(nav.fromUrl(nav.url(identifier)),identifier);
}
assert.equal(nav.parts('intake-studs').length,7);
assert.equal(nav.parts('throttle-assembly').length,29);
assert.equal(nav.parts('cylinder-1').length,15);
assert.equal(nav.parts('main-support-1').length,5);
assert.equal(nav.fromUrl('/viewer/part.html?id=c1-piston-1'),'c1-piston-1');
assert.equal(nav.fromUrl('/viewer/engine.html?part=missing'),null);
assert.deepEqual(nav.ancestors('c1-piston-1').map(n=>n.id),['engine','rotating','cylinder-1','piston-group-1','c1-piston-1']);
const results=nav.search('cylinder 4 lifter');
assert.ok(results.some(n=>n.id==='c4-intake-lifter-body'));
assert.ok(results.every(n=>nav.ancestors(n.id).some(a=>a.id==='valvetrain-cylinder-4')));
assert.equal(nav.search('timing cover')[0].id,'timing-cover','Exact part names outrank broad ancestor matches');
const learning=Object.assign({},...await Promise.all(engineLearningModules.map(async name=>JSON.parse(await readFile(new URL(`../inventory/engine/${name}-learning.json`,import.meta.url))))));
for(const [id,entry] of Object.entries(learning)){
  assert.ok(nav.nodes.has(id));
  for(const step of [...(entry.steps||[]),...(entry.troubleshooting||[])])if(step.part)assert.ok(nav.nodes.has(step.part),step.part);
  for(const step of [...(entry.steps||[]),...(entry.troubleshooting||[])])if(step.source)assert.ok(manifest.sources[step.source],step.source);
  for(const source of entry.sources)assert.ok(manifest.sources[source],source);
}
const pumpEvidence=JSON.parse(await readFile(new URL('../inventory/engine/oil-pump-evidence.json',import.meta.url)));
const comparison=pumpEvidence.comparison_dimensions;
const plunger=manifest.definitions.find(d=>d.id==='oil-pump-relief-plunger').model_bounds_mm;
const spring=manifest.definitions.find(d=>d.id==='oil-pump-relief-spring').model_bounds_mm;
assert.ok(Math.abs(plunger[0]-comparison.plunger_length_mm)<.01);
assert.ok(Math.abs(plunger[1]-comparison.plunger_diameter_mm)<.01);
assert.ok(Math.abs(spring[0]-comparison.spring_free_length_mm)<.1,'Spring free envelope must match comparison dimension');
assert.ok(Math.abs(spring[1]-comparison.spring_outer_diameter_mm)<.1);

assert.equal(nav.parts('fuel-system').length,125);
assert.equal(nav.parts('regulator-vacuum-line').length,2);
assert.equal(nav.parts('pcv-valve-assembly').length,6);
assert.equal(nav.parts('oil-filter-assembly').length,13);
assert.equal(nav.parts('oil-filter-adapter-assembly').length,1);
assert.equal(nav.parts('oil-pressure-switch-assembly').length,9);
assert.equal(nav.parts('oil-pan-assembly').length,54);
assert.equal(nav.parts('pushrod-cover-assembly').length,14);
assert.equal(nav.parts('cam-retention-assembly').length,7);
assert.equal(nav.parts('block-plugs').length,1);
assert.equal(nav.parts('egr').length,40);
assert.equal(nav.parts('egr-valve-assembly').length,12);
assert.equal(nav.parts('egr-position-sensor').length,16);
assert.equal(nav.search('EVP wiper contact')[0].id,'evp-wiper');
assert.equal(nav.search('rear camshaft bore plug')[0].id,'rear-cam-plug');
assert.deepEqual(nav.ancestors('cam-timing-key').map(n=>n.id),['engine','closures','cam-retention-assembly','cam-timing-key']);
for(const line of ['supply','return'])assert.equal(nav.parts(`fuel-${line}-coupling`).length,8);
for(let i=1;i<=6;i++)assert.equal(nav.parts(`fuel-injector-${i}`).length,13);
assert.equal(nav.parts('idle-air').length,8);
assert.equal(nav.parts('throttle-sensor').length,7);
assert.equal(nav.parts('exhaust').length,7);

assert.equal(nav.parts('damper-assembly').length,6);
assert.equal(nav.parts('accessory-drive').length,187);
assert.ok(nav.nodes.has('alternator-thermactor-common-carrier'));
for(const old of ['alternator-support-bracket','thermactor-support-bracket'])assert.ok(!nav.nodes.has(old));
assert.equal(nav.parts('accessory-support-brackets').length,20);
assert.equal(nav.parts('ac-compressor').length,67);
for(const component of ['ac-compressor-rear-manifold','ac-compressor-manifold-suction-seal','ac-compressor-manifold-discharge-seal','ac-compressor-manifold-bolt']){
  assert.ok(nav.ancestors(component).some(node=>node.id==='ac-compressor'));
}
assert.equal(nav.parts('starter-assembly').length,132);
const starterParts=manifest.occurrences.filter(entry=>entry.id.startsWith('starter-'));
assert.ok(new Set(starterParts.map(entry=>JSON.stringify(entry.explode_cad_mm))).size>=105);
const starterDefinitions=manifest.definitions.filter(entry=>entry.id.startsWith('starter-'));
assert.equal(new Set(starterDefinitions.map(entry=>entry.function)).size,60);
assert.ok(!nav.nodes.has('starter-solenoid-coil-envelope'));
for(const component of ['starter-solenoid-s-terminal','starter-solenoid-contact-bridge','starter-solenoid-pull-winding','starter-solenoid-hold-winding']){
  assert.ok(nav.ancestors(component).some(node=>node.id==='starter-solenoid-assembly'));
}
for(const role of ['pull-s','pull-m','hold-s','hold-frame']){
  for(const prefix of ['starter-solenoid-lead-','starter-solenoid-lead-insulation-']){
    assert.ok(nav.ancestors(prefix+role).some(node=>node.id==='starter-solenoid-assembly'));
  }
}
for(const component of ['starter-drive-pinion','starter-drive-clutch','starter-armature-shaft','starter-solenoid-plunger']){
  assert.ok(nav.ancestors(component).some(node=>node.id==='starter-assembly'));
}
assert.ok(manifest.assemblies.filter(entry=>entry.id.startsWith('starter-')).every(entry=>!entry.motion));
const compressorGroups=manifest.assemblies.filter(entry=>entry.motion?.type==='fs10');
for(const component of ['starter-motor-positive-feed','starter-motor-feed-jacket','starter-motor-feed-grommet','starter-motor-ground-bridge','starter-brush-pigtail-positive-1','starter-brush-pigtail-positive-4','starter-brush-pigtail-ground-2','starter-brush-pigtail-ground-3']){
  assert.ok(nav.ancestors(component).some(node=>node.id==='starter-motor-assembly'));
}
assert.equal(compressorGroups.length,17);
for(const [role,count] of [['pulley',1],['shaft',1],['piston',5],['shoe',10]]){
  assert.equal(compressorGroups.filter(entry=>entry.motion.role===role).length,count);
}
for(const group of compressorGroups)assert.ok(nav.ancestors(group.id).some(node=>node.id==='ac-compressor'));
for(const page of ['engine','part']){
  const markup=await readFile(new URL(`../viewer/${page}.html`,import.meta.url),'utf8');
  for(const identifier of ['compressor-controls','compressor-angle','compressor-value','compressor-play','compressor-engaged']){
    assert.equal(markup.split(`id="${identifier}"`).length-1,1,`${page}: ${identifier}`);
  }
}
assert.equal(nav.parts('thermactor-pump-assembly').length,19);
assert.equal(nav.parts('power-steering-pump-assembly').length,46);
assert.equal(nav.parts('alternator-assembly').length,26);
assert.equal(nav.parts('fan-clutch-assembly').length,35);
assert.equal(nav.parts('cooling-connections').length,7);
assert.equal(nav.parts('engine-coolant-temperature-assembly').length,5);
assert.equal(nav.parts('ignition-leads').length,42);
assert.equal(nav.parts('ignition-coil-mount').length,7);
for(let cylinder=1;cylinder<=6;cylinder++)assert.equal(nav.parts(`ignition-lead-${cylinder}-assembly`).length,6);
assert.equal(nav.parts('tensioner-support-assembly').length,6);
assert.equal(nav.parts('water-pump-pulley-assembly').length,5);
assert.deepEqual(nav.ancestors('tensioner-pulley-wheel').map(node=>node.id),['engine','accessory-drive','tensioner-pulley-assembly','tensioner-pulley-wheel']);
assert.ok(nav.ancestors('water-pump-pulley-bolt-1').some(node=>node.id==='water-pump-assembly'));
assert.deepEqual(nav.ancestors('damper-elastomer').map(n=>n.id),['engine','rotating','damper-assembly','damper-elastomer']);
console.log(`Navigation verified: ${all.length} parts reachable once, ${nav.nodes.size} deep links, search and legacy links.`);

assert.equal(nav.parts('egr-exhaust-line').length,4);

assert.equal(nav.parts('egr-vacuum-regulator').length,4);

assert.equal(nav.parts('egr-vacuum-lines').length,1);

assert.equal(nav.parts('rear-manifold-mounts').length,2);
for(const id of ['rear-manifold-bolt15','rear-manifold-bolt16']) { assert.ok(nav.ancestors(id).some(n=>n.id==='exhaust')); assert.equal(nav.fromUrl(nav.url(id)),id); }

assert.equal(nav.parts('carrier-1994-engine-attachments').length,8);


assert.equal(nav.parts('oil-pan-fastener-assembly').length,50);
assert(!manifest.occurrences.some(p=>p.id.startsWith('pan-side-gasket-')));

for(let i=1;i<=6;i++){const ids=nav.parts(`valvetrain-cylinder-${i}`);for(const kind of ['intake','exhaust'])for(const suffix of ['valve','rocker','pushrod','lifter-body'])assert(ids.includes(`c${i}-${kind}-${suffix}`));}

assert.equal(nav.parts('water-pump-mechanical-seal-assembly').length,6);
assert.ok(!nav.nodes.has('water-pump-seal'));
assert.ok(nav.nodes.has('accelerator-cable-bracket'));
