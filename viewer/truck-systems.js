const host=document.getElementById('systems');
const search=document.getElementById('system-search');
const detail=document.getElementById('system-detail');
let data;
function render(){
  const query=search.value.trim().toLowerCase();
  host.replaceChildren();
  for(const system of data.systems){
    if(query && !`${system.name} ${system.scope}`.toLowerCase().includes(query))continue;
    const a=document.createElement('a');a.className='system-card';a.href=`#${system.id}`;
    const title=document.createElement('h2');title.textContent=system.name;
    const status=document.createElement('span');status.className='status';status.textContent=system.status;
    const p=document.createElement('p');p.textContent=system.scope;
    const count=document.createElement('span');count.className='action';count.textContent=system.viewer?'Explore parts and references →':`${system.sources.length} indexed reference pages →`;
    a.append(title,status,p,count);host.append(a);
  }
  if(!host.children.length)host.textContent='No matching systems. Try “brakes”, “clutch”, or “wiring”.';
}
function show(){
  detail.replaceChildren();
  const system=data.systems.find(s=>s.id===location.hash.slice(1));
  detail.hidden=!system;if(!system)return;
  const title=document.createElement('h2');title.textContent=system.name;
  const p=document.createElement('p');p.textContent=system.scope;
  detail.append(title,p);
  if(system.viewer){const a=document.createElement('a');a.className='action';a.href=system.viewer;a.textContent='Open 3D component explorer →';detail.append(a);}
  const note=document.createElement('p');note.textContent=system.viewer?'The component model is provisional. References below cover the wider system.':'3D modeling is pending. These factory reference pages provide the starting point; applicability to the installed truck still needs review.';detail.append(note);
  const label=document.createElement('label');label.textContent='Find a reference in this system';
  const filter=document.createElement('input');filter.type='search';filter.placeholder='Component, procedure, or specification';label.append(filter);detail.append(label);
  const list=document.createElement('div');list.className='references';detail.append(list);
  const resultCount=document.createElement('p');resultCount.setAttribute('aria-live','polite');label.after(resultCount);
  function references(){
    const q=filter.value.toLowerCase();const matches=system.sources.filter(s=>s.title.toLowerCase().includes(q));list.replaceChildren();resultCount.textContent=`${matches.length} reference pages`;
    for(const source of matches.slice(0,100)){
      const a=document.createElement('a');a.href='/'+source.path.split('/').map(encodeURIComponent).join('/');a.target='_blank';a.rel='noopener';a.textContent=source.title;list.append(a);
    }
    if(matches.length>100){const more=document.createElement('p');more.textContent='Showing the first 100 pages. Narrow your search to find a particular component.';list.append(more);}
  }
  filter.addEventListener('input',references);references();
}
try{
  const response=await fetch('/inventory/truck/systems.json');if(!response.ok)throw Error(response.status);
  data=await response.json();render();show();search.disabled=false;
  search.addEventListener('input',render);window.addEventListener('hashchange',()=>{show();if(!detail.hidden)detail.scrollIntoView({block:'start'});});
}catch(error){host.textContent='The system library could not load. Reload the page to try again.';console.error(error);}
