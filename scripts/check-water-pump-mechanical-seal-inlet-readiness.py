"""Current inlet/neighbor readiness uses the same fault-sensitive seal gates."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.call([sys.executable,str(ROOT/'scripts/check-water-pump-mechanical-seal-candidate.py'),'--report',str(ROOT/'inventory/engine/water-pump-mechanical-seal-inlet-readiness-validation.json'),*sys.argv[1:]]))
