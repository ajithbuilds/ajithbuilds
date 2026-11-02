"""Rebuild the shared colour-icon treatment throughout the local profile."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
COMMANDS=[
 [sys.executable,'scripts/generate_certification_cards.py'],
 [sys.executable,'scripts/apply_colour_tech_tags.py'],
 ['node','scripts/render_tech_tags.cjs'],
 [sys.executable,'scripts/generate_tech_badges.py'],
 [sys.executable,'scripts/rebuild_architectures.py'],
 [sys.executable,'scripts/generate_hero_hq.py'],
 [sys.executable,'scripts/generate_role_banner.py'],
 [sys.executable,'scripts/generate_stack_showcase.py'],
 [sys.executable,'scripts/generate_production_console.py'],
 [sys.executable,'scripts/build_preview.py'],
 [sys.executable,'scripts/verify_profile.py'],
]
if __name__=='__main__':
 for command in COMMANDS:subprocess.run(command,cwd=ROOT,check=True)
