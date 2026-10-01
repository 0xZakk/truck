import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {buildStageNavigation} from '../viewer/engine-stage-navigation.js';
import {engineLearningModules,resolveEngineLearning} from '../viewer/engine-learning-modules.js';
const path=process.argv[2]||'inventory/engine/corrected-engine-stage-v3.json',manifest=JSON.parse(fs.readFileSync(path)),original=JSON.stringify(manifest),nav=buildStageNavigation(manifest);
assert.deepEqual(nav.parts('front-seal-assembly').sort(),['front-seal-case','front-seal-elastomer','front-seal-garter-spring'].sort());
assert.equal(nav.parts('engine').length,manifest.occurrences.length);assert.equal(new Set(nav.parts('engine')).size,manifest.occurrences.length);
for(const node of nav.nodes.values()){
 assert.equal(nav.fromUrl(nav.url(node.id)),node.id);assert.equal(new URL(nav.url(node.id),'http://localhost').searchParams.get('stage'),'timing');
 const ancestors=nav.ancestors(node.id);assert.equal(ancestors[0].id,'engine');assert.equal(new Set(ancestors.map(x=>x.id)).size,ancestors.length);
}
for(const query of ['part=front-seal','id=front-seal','assembly=front-seal'])assert.equal(nav.fromUrl('/viewer/engine.html?'+query),'front-seal-assembly');
assert.equal(nav.fromUrl(nav.url('front-seal')),'front-seal-assembly');
const modules=engineLearningModules.map(n=>JSON.parse(fs.readFileSync(`inventory/engine/${n}-learning.json`)));
const lessons=resolveEngineLearning(manifest,nav.nodes.keys(),...modules,manifest.integration_stage.learning_additions);
let links=0;
for(const [id,lesson]of Object.entries(lessons)){
 assert(nav.nodes.has(id));
 for(const source of lesson.sources||[])assert(manifest.sources[source],`Missing source ${source}`);
 for(const step of [...lesson.steps||[],...lesson.troubleshooting||[]]){
  if(step.part){assert(nav.nodes.has(nav.resolve(step.part)),`Missing link ${step.part}`);links++;}
  if(step.source)assert(manifest.sources[step.source],`Missing source ${step.source}`);
 }
}
const bad=structuredClone(manifest);bad.integration_stage.navigation_aliases['front-seal']='absent';assert.throws(()=>buildStageNavigation(bad));
assert.equal(JSON.stringify(manifest),original);
const files=[path,'viewer/engine-stage-navigation.js','viewer/engine-navigation.js','viewer/engine-learning-modules.js','scripts/check-engine-candidate-navigation.mjs',...engineLearningModules.map(n=>`inventory/engine/${n}-learning.json`)];
const report={status:'PASS candidate navigation and learning references',parts:manifest.occurrences.length,nodes:nav.nodes.size,lessons:Object.keys(lessons).length,links,legacySealAlias:'front-seal-assembly',canonicalModified:false,bindings:Object.fromEntries(files.map(p=>[p,createHash('sha256').update(fs.readFileSync(p)).digest('hex')])),limits:['Not wired into atlas; no browser or visual acceptance','Known staged assembly collisions remain']};
fs.writeFileSync(process.argv[3]||'inventory/engine/engine-stage-v3-navigation-validation.json',JSON.stringify(report,null,2)+'\n');console.log({status:report.status,parts:report.parts,nodes:report.nodes,lessons:report.lessons,links});
