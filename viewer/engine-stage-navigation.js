// Opt-in candidate navigation. Canonical links and CAD hierarchy are unchanged.
import {buildNavigation} from './engine-navigation.js';
export function buildStageNavigation(manifest){
 if(manifest.motion_revision!=='clockwise-inclined-v1'||!manifest.integration_stage)throw new Error('Coordinated candidate manifest required');
 const nav=buildNavigation(manifest),aliases=manifest.integration_stage.navigation_aliases||{};
 for(const [from,to] of Object.entries(aliases)){
  if(nav.nodes.has(from)||!nav.nodes.has(to)||from===to)throw new Error(`Invalid candidate alias: ${from}`);
 }
 const resolve=id=>aliases[id]||id;
 return {...nav,
  url(id){const url=new URL(nav.url(resolve(id)),'http://localhost');url.searchParams.set('stage','timing');return url.pathname+url.search;},
  fromUrl(value){const url=new URL(value,'http://localhost');const id=url.searchParams.get('part')||url.searchParams.get('id')||url.searchParams.get('assembly')||'engine';const target=resolve(id);return nav.nodes.has(target)?target:null;},
  resolve,
 };
}
