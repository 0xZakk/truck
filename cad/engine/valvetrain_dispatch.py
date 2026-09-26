"""Select one geometry/motion authority for each installed valve-train revision."""


def apply_valve_transforms(manifest, poses, degrees=0):
    models = {o['valvetrain'].get('model') for o in manifest['occurrences']
              if o.get('valvetrain')}
    if 'source-sized-v2' in models:
        if models != {'source-sized-v2'}:
            raise ValueError('Mixed valve-train revisions cannot share one assembly')
        from valve_source_integration import apply_valve_transforms as apply
    else:
        from valve_layout_integration import apply_valve_transforms as apply
    return apply(manifest, poses, degrees)


def occurrence_shape(occurrence, shape, degrees=0):
    if occurrence.get('valvetrain', {}).get('model') == 'source-sized-v2':
        from valve_source_integration import occurrence_shape as deform
    else:
        from valve_layout_integration import occurrence_shape as deform
    return deform(occurrence, shape, degrees)
