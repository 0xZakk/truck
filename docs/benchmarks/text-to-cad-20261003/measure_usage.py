"""Extract numeric usage only for this experiment's two workers and coordinator.

Requires the local Codex session log directory as an explicit argument; reports
contain numeric metadata only, never other conversation text or credentials.
"""
import argparse, datetime, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'reference/engine/text-to-cad-20261003'
AGENTS={'/root/cad_pilot_baseline':'baseline','/root/cad_pilot_plugin':'plugin'}
PARENT='01a0ca30-ff04-7ba2-93b9-5b8f9144b71c'

def scan(p):
    first=None;last=None;finish=None;settings=[]
    for line in p.open():
        try:d=json.loads(line)
        except ValueError:continue
        v=d.get('payload',{})
        if d.get('type')=='turn_context':
            item={k:v[k] for k in ('model','effort') if k in v}
            if item and item not in settings:settings.append(item)
        if v.get('type')=='token_count' and v.get('info'):
            last={'timestamp':d['timestamp'],'usage':v['info']['total_token_usage']}
            if first is None:first=last
        if v.get('type')=='task_complete':finish=d['timestamp']
    return {'first_counter':first,'last_counter':last,'last_final_message_utc':finish,'settings':settings}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('sessions',type=Path);a=ap.parse_args()
    report={'capture_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'workers':{},'notes':['Cumulative fresh-session worker usage includes their full assignment and rework.','Input includes cached input; reasoning is a subset of output. Do not add either subset again.','Coordinator is shared overhead, not assigned twice to individual arms. Final report-writing after this snapshot is excluded.']}
    for p in (a.sessions/'2026/10/03').glob('*.jsonl'):
        try:
            with p.open() as f:meta=json.loads(next(f))['payload']
        except (ValueError,KeyError,StopIteration):continue
        agent=meta.get('agent_path')
        if agent in AGENTS and meta.get('parent_thread_id')==PARENT:
            report['workers'][AGENTS[agent]]={'session_id':meta['id'],'start_utc':meta['timestamp'],**scan(p)}
    p=next((a.sessions/'2026/09/22').glob('*'+PARENT+'.jsonl'))
    end=scan(p)['last_counter'];start=json.loads((OUT/'root-token-start.json').read_text())
    initial=start['payload']['info']['total_token_usage']
    report['coordinator']={'start_counter_utc':start['timestamp'],'end_counter_utc':end['timestamp'],'usage_delta':{k:v-initial.get(k,0) for k,v in end['usage'].items()},'scope':'paired brief, dispatch, shared tracking, independent QC, viewer and result preparation after restart; excludes earlier installation/research'}
    (OUT/'usage.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
