// A browsing hierarchy, independent of the CAD transform hierarchy.
export function buildNavigation(manifest) {
  const nodes=new Map();
  for(const a of manifest.assemblies)nodes.set(a.id,{...a,type:'assembly',children:[]});
  for(const p of manifest.occurrences)nodes.set(p.id,{...p,type:'part',children:[]});
  const group=(id,name,parent)=>nodes.set(id,{id,name,parent,type:'assembly',children:[]});
  nodes.get('engine').name='Engine';
  const titles={'throttle-moving':'Shaft, plates & lever',rotating:'Pistons & crankshaft',structure:'Block & main bearings',head:'Cylinder head & covers',valvetrain:'Camshaft & valve train',closures:'Timing drive & covers'};
  for(const [id,name] of Object.entries(titles))nodes.get(id).name=name;
  for(let i=1;i<=6;i++){
    group(`cylinder-${i}`,`Cylinder ${i}`,'rotating');
    for(const [prefix,name] of [['piston','Piston assembly'],['rod','Connecting rod assembly']]){
      const a=nodes.get(`${prefix}-group-${i}`);a.parent=`cylinder-${i}`;a.name=name;
    }
    group(`valvetrain-cylinder-${i}`,`Cylinder ${i} · complete valve train`,'valvetrain');
    group(`head-cylinder-${i}`,`Cylinder ${i} · valves`,`valvetrain-cylinder-${i}`);
    for(const type of ['intake','exhaust']){
      nodes.get(`c${i}-${type}-valve-assembly`).parent=`head-cylinder-${i}`;
      nodes.get(`c${i}-${type}-actuation`).parent=`valvetrain-cylinder-${i}`;
    }
  }
  for(let i=1;i<=7;i++){
    const id=`main-support-${i}`;group(id,`Main bearing support ${i}`,'structure');
    for(const p of manifest.occurrences)if(p.id===`main-cap-${i}`||p.id===`main-bearing-upper-${i}`||p.id===`main-bearing-lower-${i}`||p.id.startsWith(`main-cap-bolt-${i}-`))nodes.get(p.id).parent=id;
  }
  group('head-fasteners','Head bolts','head');
  for(const p of manifest.occurrences)if(p.id.startsWith('head-bolt-'))nodes.get(p.id).parent='head-fasteners';
  group('timing-drive','Timing gears','closures');
  for(const id of ['crank-timing-gear','cam-timing-gear'])nodes.get(id).parent='timing-drive';
  // Browsing keeps the retention stack together; CAD parents still distinguish
  // rotating spacer/key from the stationary plate and its fasteners.
  if(nodes.has('cam-retention-assembly'))for(const id of ['cam-gear-spacer','cam-timing-key'])nodes.get(id).parent='cam-retention-assembly';
  for(const node of nodes.values())if(node.parent==='crank-motion')node.parent='rotating';
  nodes.delete('crank-motion');
  nodes.get('cam-motion').name='Camshaft & bearings';
  for(const p of manifest.occurrences)if(p.definition==='cam-bearing')nodes.get(p.id).parent='cam-motion';
  for(const node of nodes.values())if(node.parent)nodes.get(node.parent).children.push(node.id);
  function ancestors(id){const path=[];for(let n=nodes.get(id);n;n=nodes.get(n.parent))path.unshift(n);return path;}
  function parts(id){const n=nodes.get(id);return n.type==='part'?[id]:n.children.flatMap(parts);}
  function search(query){
    const normalized=query.toLowerCase().trim().replace(/\s+/g,' '),words=normalized.split(' ');
    const rank=n=>{const name=n.name.toLowerCase();return name===normalized?0:name.includes(normalized)?1:words.every(w=>name.includes(w))?2:3;};
    return [...nodes.values()].filter(n=>n.id!=='engine'&&words.every(w=>ancestors(n.id).map(a=>a.name).join(' ').toLowerCase().includes(w)))
      .sort((a,b)=>rank(a)-rank(b));
  }
  function url(id){const n=nodes.get(id);return '/viewer/engine.html'+(id==='engine'?'':`?${n.type==='part'?'part':'assembly'}=${encodeURIComponent(id)}`);}
  function fromUrl(url){const p=new URL(url,'http://localhost').searchParams;const id=p.get('part')||p.get('id')||p.get('assembly')||'engine';return nodes.has(id)?id:null;}
  return {nodes,ancestors,parts,search,url,fromUrl};
}
