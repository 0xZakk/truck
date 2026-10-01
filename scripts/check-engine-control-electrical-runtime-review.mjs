// Independent review of the installed supplement composition; no shared writes.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {engineLearningModules,resolveEngineLearning} from '../viewer/engine-learning-modules.js';
import {engineLearningSupplements,supplementEngineLearning,engineSourceUrl} from '../viewer/engine-learning-supplements.js';
import {buildNavigation} from '../viewer/engine-navigation.js';
const read=p=>JSON.parse(fs.readFileSync(p));
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const frozenPath='inventory/engine/engine-control-electrical-learning-candidate.json';
const livePath='inventory/engine/engine-control-electrical-learning.json';
const sourcePath='inventory/engine/engine-control-electrical-learning-sources.json';
const mapPath='reference/engine/engine-control-electrical-map.json';
const frozen=read(frozenPath),live=read(livePath),sources=read(sourcePath),map=read(mapPath);
const normalize=x=>typeof x==='string'?x.replace(/PCM\s+pin\s*/g,'PCM').replace(/\s+/g,''):Array.isArray(x)?x.map(normalize):x&&typeof x==='object'?Object.fromEntries(Object.entries(x).map(([k,v])=>[k,normalize(v)])):x;
function semantics(candidate){
 assert.deepEqual(Object.keys(candidate).sort(),Object.keys(frozen).sort());
 for(const[id,lesson]of Object.entries(candidate)){
  assert.deepEqual(lesson.electrical_contract,frozen[id].electrical_contract,`Contract changed ${id}`);
  assert.deepEqual(normalize(lesson),normalize(frozen[id]),`Non-editorial content change ${id}`);
 }
 for(let n=1;n<=6;n++){
  const row=candidate[`fuel-injector-${n}`].electrical_contract.contacts.find(x=>x.role==='group driver');
  assert.equal(row.circuit,n%2?'555':'556');assert.equal(row.pcm_c185_cavity,n%2?58:59);
 }
 for(const id of ['throttle-sensor','egr-position-sensor','engine-coolant-temperature-assembly']){
  const r=candidate[id].electrical_contract.contacts.find(x=>x.role==='sensor signal return');assert.equal(r.circuit,'359');assert.equal(r.pcm_c185_cavity,46);
 }
}
semantics(live);
const controls=[];
function reject(name,fn){assert.throws(fn);controls.push(name);}
let bad=structuredClone(live);bad['fuel-injector-1'].electrical_contract.contacts[1].pcm_c185_cavity=59;reject('wrong injector group',()=>semantics(bad));
bad=structuredClone(live);bad['throttle-sensor'].electrical_contract.contacts[1].circuit='57';reject('wrong sensor ground',()=>semantics(bad));
bad=structuredClone(live);bad['engine-coolant-temperature-assembly'].steps[2].text=bad['engine-coolant-temperature-assembly'].steps[2].text.replace('PCM pin 49','PCM pin 46');reject('wrong oxygen ground in rendered prose',()=>semantics(bad));
const modulePaths=engineLearningModules.map(n=>`inventory/engine/${n}-learning.json`),modules=modulePaths.map(read);
const manifests=['inventory/engine/full-assembly.json','inventory/engine/corrected-engine-stage-v3.json'];
const results=[];
for(const path of manifests){
 const manifest=read(path),nav=buildNavigation(manifest),snapshot=JSON.stringify(manifest);
 const base=resolveEngineLearning(manifest,nav.nodes.keys(),...modules,...(manifest.integration_stage?[manifest.integration_stage.learning_additions]:[]));
 const baseBefore=JSON.stringify(base),sourcesBefore=JSON.stringify(manifest.sources),supplementBefore=JSON.stringify({live,sources});
 const result=supplementEngineLearning(base,manifest.sources,nav.nodes.keys(),[{lessons:live,sources}]);
 let existing=0,newCount=0,links=0;
 for(const[id,extra]of Object.entries(live)){
  const merged=result.learning[id],old=base[id];
  if(old){existing++;assert.equal(merged.summary,old.summary+' '+extra.summary);assert.equal(merged.limits,old.limits+' '+extra.limits);assert.deepEqual(merged.steps,[...(old.steps||[]),...(extra.steps||[])]);assert.deepEqual(merged.troubleshooting,[...(old.troubleshooting||[]),...(extra.troubleshooting||[])]);assert.deepEqual(merged.sources,[...new Set([...(old.sources||[]),...(extra.sources||[])])]);}
  else {newCount++;assert.deepEqual(merged,extra);}
  for(const item of [...merged.steps||[],...merged.troubleshooting||[]]){if(item.part){assert(nav.nodes.has(item.part));links++;}if(item.source)assert(result.sources[item.source]);}
  for(const source of merged.sources||[])assert(result.sources[source]);
 }
 for(const[id,lesson]of Object.entries(base))if(!live[id])assert.deepEqual(result.learning[id],lesson);
 assert.equal(existing,5);assert.equal(newCount,6);assert.equal(JSON.stringify(manifest),snapshot);assert.equal(JSON.stringify(base),baseBefore);assert.equal(JSON.stringify(manifest.sources),sourcesBefore);assert.equal(JSON.stringify({live,sources}),supplementBefore);
 const broken=structuredClone(live);broken['throttle-sensor'].steps[0].part='nonexistent-map';reject('runtime absent link '+path,()=>supplementEngineLearning(base,manifest.sources,nav.nodes.keys(),[{lessons:broken,sources}]));
 results.push({manifest:path,preserved_mechanical_lessons:existing,new_injector_assembly_lessons:newCount,part_links:links,input_mutation:false});
}
const sourceChecks=[];
for(const[id,source]of Object.entries(sources)){
 assert.equal(hash(source.path),source.sha256);const p=source.pdf_page_1_based;assert(map.source.pages.some(row=>row.pdf_page_1_based===p&&row.printed===source.printed_page));
 const url=new URL(engineSourceUrl(source),'http://example.invalid');assert.equal(url.hash,`#page=${p}`);assert.equal(decodeURIComponent(url.pathname).slice(1),source.path);assert(fs.existsSync(decodeURIComponent(url.pathname).slice(1)));
 sourceChecks.push({id,pdf_page:p,printed_page:source.printed_page,local_path_exists:true});
}
assert.deepEqual(engineLearningSupplements,[{lessons:'engine-control-electrical-learning.json',sources:'engine-control-electrical-learning-sources.json'}]);
const atlas=fs.readFileSync('viewer/atlas.js','utf8');assert(atlas.includes('supplementEngineLearning(learning,data.sources,nav.nodes.keys(),supplements)'));assert(atlas.includes('const source=learningSources[id]'));assert(atlas.includes('a.href=engineSourceUrl(source)'));
const files=[frozenPath,livePath,sourcePath,mapPath,'viewer/engine-learning-supplements.js','viewer/engine-learning-modules.js','viewer/atlas.js',...manifests,...modulePaths,'scripts/check-engine-control-electrical-runtime-review.mjs'];
const report={status:'PASS scoped CLI integration review',results,sourceChecks,negative_controls_rejected:controls,content_review:{material_regressions:[],contradictory_claims:[],minor_redundancy:['EVP repeats its reference/signal/return tuple in appended content.','ECT repeats the temperature/thermistor overview in combined summaries.'],minor_spacing:['Injector limits retain continuationK and reference:23-2; cosmetic only.'],electrical_contract_runtime:'Five merged entries retain old object fields; new electrical_contract metadata is not copied into those five runtime entries. Displayed text preserves semantics; raw integrated supplement contracts checked separately. No displayed regression.'},browser:'NOT RUN; no bypass',limits:['Static loader wiring inspected; no browser execution or fetch verification','Private manual links checked against authorized local file, not public availability','No installed electrical testing or calibration validation'],bindings:Object.fromEntries(files.map(p=>[p,hash(p)]))};
fs.writeFileSync('inventory/engine/engine-control-electrical-runtime-review.json',JSON.stringify(report,null,2)+'\n');console.log(report.status,results,controls.length,'negative controls');
