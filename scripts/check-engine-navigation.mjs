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
assert.equal(nav.nodes.get('engine').children.length,5);
assert.equal(nav.parts('cylinder-1').length,15);
assert.equal(nav.parts('main-support-1').length,5);
assert.equal(nav.fromUrl('/viewer/part.html?id=c1-piston-1'),'c1-piston-1');
assert.equal(nav.fromUrl('/viewer/engine.html?part=missing'),null);
assert.deepEqual(nav.ancestors('c1-piston-1').map(n=>n.id),['engine','rotating','cylinder-1','piston-group-1','c1-piston-1']);
const results=nav.search('cylinder 4 lifter');
assert.ok(results.some(n=>n.id==='c4-intake-lifter-body'));
assert.ok(results.every(n=>nav.ancestors(n.id).some(a=>a.id==='valvetrain-cylinder-4')));
console.log(`Navigation verified: ${all.length} parts reachable once, ${nav.nodes.size} deep links, search and legacy links.`);
