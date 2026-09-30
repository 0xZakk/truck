// Shared by the viewer and navigation checker so no lesson file escapes link validation.
export const engineLearningModules = ['lubrication','intake','damper','cooling','ignition','ac-compressor-motion','ac-compressor-bearing','ac-compressor-manifold','ac-compressor-shaft-support','ac-compressor-manifold-passages','fuel-test-valve-motion-viewer','starter','starter-solenoid','starter-engagement','starter-wiring','starter-wiring-fit','starter-motor-feed','manifold-lifting-eye','intake-locating-dowel','exhaust-front-profile','exhaust-rear-entries','rear-manifold-mounts','carrier-1994','common-carrier','oil-pan-joint','valvetrain-motion','water-pump-joint','component-interface','throttle-linkage','dipstick','dipstick-assembly','intake-cap','iac-attachment','throttle-plate-fasteners','iac-closure','iac-electrical','distributor-center-contact','throttle-cable','intake-runner-exterior','evr-mechanism','throttle-stop','exhaust-rear-collector'];

// A reused material definition can supply a lesson for each placed occurrence.
// Explicit occurrence/assembly lessons take precedence over definition defaults.
export function resolveEngineLearning(manifest, navigationIds, ...modules) {
  const entries=Object.assign({},...modules), result={};
  const direct=new Set([...navigationIds,...[...manifest.assemblies,...manifest.occurrences].map(row=>row.id)]);
  for(const [id,lesson] of Object.entries(entries)) {
    if(direct.has(id))continue;
    const placed=manifest.occurrences.filter(row=>row.definition===id);
    if(!placed.length)throw new Error(`Learning target is absent: ${id}`);
    for(const row of placed)result[row.id]=lesson;
  }
  for(const [id,lesson] of Object.entries(entries))if(direct.has(id))result[id]=lesson;
  return result;
}
