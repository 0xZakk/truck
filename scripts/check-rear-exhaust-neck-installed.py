#!/usr/bin/env python3
"""Read-only staged/installed collector replay; no canonical writes."""
from pathlib import Path
import argparse,importlib.util,json
p=Path(__file__).with_name('install-rear-exhaust-neck.py');spec=importlib.util.spec_from_file_location('rear_install',p);installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--installed',action='store_true');a=a.parse_args();result=installer.validate(a.installed);installer.dump(installer.STAGE/('installed-recheck.json' if a.installed else 'recheck.json'),result);print(result['status'])
