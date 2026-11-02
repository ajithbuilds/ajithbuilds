"""Rebuild selected architecture SVGs, PNGs, GIFs and local previews."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
SCRIPTS={'reliability':('generate_reliability_architecture.py','animate_reliability_architecture.py'),'ai-agent':('generate_ai_agent_architecture.py','animate_ai_agent_architecture.py'),'finops':('generate_finops_architecture.py','animate_finops_architecture.py'),'platform':('generate_platform_architecture.py','animate_platform_architecture.py')}
def run(args):subprocess.run(args,cwd=ROOT,check=True)
def main():
    selected=sys.argv[1:] or list(SCRIPTS)
    for name in selected:
        if name not in SCRIPTS:raise SystemExit(f'Unknown architecture: {name}')
        generate,animate=SCRIPTS[name]
        run([sys.executable,str(ROOT/'scripts'/generate)])
        run(['node','scripts/render_architectures.cjs',name])
        run([sys.executable,str(ROOT/'scripts'/animate)])
    run([sys.executable,'scripts/build_preview.py'])
if __name__=='__main__':main()
