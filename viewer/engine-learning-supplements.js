// Append cross-system explanations without replacing the mechanical lessons.
export const engineLearningSupplements = [
  {lessons:'engine-control-electrical-learning.json',sources:'engine-control-electrical-learning-sources.json'},
];

export function supplementEngineLearning(base, sources, navigationIds, supplements) {
  const learning={...base}, registry={...sources}, ids=new Set(navigationIds);
  for(const supplement of supplements) {
    for(const [id,source] of Object.entries(supplement.sources)) {
      if(registry[id] && JSON.stringify(registry[id])!==JSON.stringify(source))throw new Error(`Conflicting learning source: ${id}`);
      registry[id]=source;
    }
    for(const [id,extra] of Object.entries(supplement.lessons)) {
      if(!ids.has(id))throw new Error(`Supplement target is absent: ${id}`);
      for(const item of [...(extra.steps||[]),...(extra.troubleshooting||[])]) {
        if(item.part&&!ids.has(item.part))throw new Error(`Supplement link is absent: ${item.part}`);
        if(item.source&&!registry[item.source])throw new Error(`Supplement source is absent: ${item.source}`);
      }
      for(const source of extra.sources||[])if(!registry[source])throw new Error(`Supplement source is absent: ${source}`);
      const old=learning[id];
      learning[id]=old?{
        ...old,
        summary:[old.summary,extra.summary].filter(Boolean).join(' '),
        limits:[old.limits,extra.limits].filter(Boolean).join(' '),
        steps:[...(old.steps||[]),...(extra.steps||[])],
        troubleshooting:[...(old.troubleshooting||[]),...(extra.troubleshooting||[])],
        sources:[...new Set([...(old.sources||[]),...(extra.sources||[])])],
      }:extra;
    }
  }
  return {learning,sources:registry};
}

export function engineSourceUrl(source) {
  if(!source.path)return source.url;
  const path='/'+source.path.replace(/^\//,'').split('/').map(encodeURIComponent).join('/');
  return Number.isInteger(source.pdf_page_1_based)&&source.pdf_page_1_based>0
    ?`${path}#page=${source.pdf_page_1_based}`:path;
}
