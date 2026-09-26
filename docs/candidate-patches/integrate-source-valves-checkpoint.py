from pathlib import Path
import shutil,json
r=Path('/private/tmp/truck-desktop-integration-20260925');main=Path('/Users/zacharyfleischmann/projects/truck/truck-build')
for name in ['valve_source_layout.py','valve_source_integration.py','valve_source_evidence.py','valve_dimensions_candidate.py','valve_spring_seating_candidate.py','valvetrain_dispatch.py','valve_source_definition_adapter.py']:
 shutil.copy2(main/'cad/engine'/name,r/'cad/engine'/name)
# Preserve the accepted predecessor and changed inputs before mutation.
d=main/'cad/engine/candidates/valve-source-installed-desktop/baseline';d.mkdir(parents=True,exist_ok=True)
m=json.loads((r/'inventory/engine/full-assembly.json').read_text());shutil.copy2(r/'inventory/engine/full-assembly.json',d/'manifest.json')
for row in m['definitions']:
 if row['id'] in ['cylinder-head','lifter-body','intake-valve','exhaust-valve']:
  shutil.copy2(r/row['step'].lstrip('/'),d/(row['id']+'.step'))
p=r/'cad/engine/assembly_math.py';s=p.read_text().replace('VALVETRAIN_TRANSFORMS_VERSION=1','VALVETRAIN_TRANSFORMS_VERSION=2').replace('from valve_layout_integration import apply_valve_transforms','from valvetrain_dispatch import apply_valve_transforms');p.write_text(s)
p=r/'scripts/check-engine-atlas.py';s=p.read_text().replace('from valve_layout_integration import occurrence_shape','from valvetrain_dispatch import occurrence_shape');p.write_text(s)
p=r/'cad/engine/full_engine.py';s=p.read_text();s=s.replace('from assembly_math import transforms','from assembly_math import transforms\nfrom valvetrain_dispatch import occurrence_shape\nimport valve_source_integration as source_valves\nimport valve_source_evidence as source_evidence\nimport valve_source_definition_adapter as source_definitions')
s=s.replace("gaps=(), claims=()):", "gaps=(), claims=(), prepared=False):",1)
start=s.index('    if id in common_carrier.REMOVE_IDS: return',s.index('def define('));end=s.index('    if not shape.is_valid',start)
s=s[:start]+'    if not prepared:\n'+''.join('    '+line if line.strip() else line for line in s[start:end].splitlines(True))+'        shape=source_definitions.replacement(id,shape,VALVE_STATIONS)\n'+s[end:]
s=s.replace("    if refresh:\n", "    if '--refresh-source-valves' in sys.argv:\n        refresh='source-valves'\n    if refresh:\n",1)
s=s.replace("removed={'common-carrier'", "removed={'source-valves':set(),'common-carrier'",1)
s=s.replace("        if refresh=='valvetrain': used.difference_update(VALVE_IDS)","        if refresh=='source-valves': used.difference_update(source_definitions.IDS | {'valve-spring'})\n        if refresh=='valvetrain': used.difference_update(VALVE_IDS)")
anchor="        if refresh=='valvetrain':\n            for identifier in VALVE_IDS:"
new="""        if refresh=='source-valves':
            if previous.get('valvetrain_model')=='source-sized-v2':
                raise ValueError('Source-sized refresh requires the accepted first-stage baseline')
            old_defs={d['id']:d for d in previous['definitions']}
            inputs={key:b.import_step(ROOT/old_defs[key]['step'].lstrip('/')) for key in ['cylinder-head','lifter-body','intake-valve','exhaust-valve']}
            for identifier,shape in source_valves.replacements(inputs,previous).items():
                old=old_defs.get(identifier,old_defs['valve-spring'])
                name=identifier.split('-')[0].title()+' valve spring' if identifier.endswith('-spring') else old['name']
                define(identifier,shape,name,old['function'],old['system'],old['color'],old['sources'],old['unresolved'],old['dimension_claims'],prepared=True)
"""
assert anchor in s;s=s.replace(anchor,new+anchor)
s=s.replace("    annotated=valve_layout.annotate_manifest({'occurrences':occurrences,'assemblies':assemblies})", "    annotated=source_valves.annotate_manifest({'occurrences':occurrences,'assemblies':assemblies})")
s=s.replace("    for d in defs:\n        if d['id'] not in shapes:","    manifest=source_evidence.annotate_evidence(manifest)\n    manifest['valvetrain_model']='source-sized-v2'\n    defs[:]=manifest['definitions']\n    for d in defs:\n        if d['id'] not in shapes:")
s=s.replace("s=valve_layout.occurrence_shape(o,shapes[o['definition']],0)","s=occurrence_shape(o,shapes[o['definition']],0)")
# Every fresh/full build also needs the two distinct spring definitions.
anchor="    annotated=source_valves.annotate_manifest"
idx=s.index(anchor);s=s[:idx]+"    for kind in ('intake','exhaust'):\n        if not any(d['id']==kind+'-spring' for d in defs):\n            define(kind+'-spring',source_definitions.v.spring(kind),kind.title()+' valve spring','Returns the valve toward its seat.','valvetrain',sources=['fsm-2e5473b2bf99'],prepared=True)\n    defs[:]=[d for d in defs if d['id']!='valve-spring']\n"+s[idx:]
p.write_text(s)
