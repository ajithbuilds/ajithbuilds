# Hero pipeline artwork

The active header is `assets/hero-devops-mlops-glass-4k.gif`. Both workflows remain visible in every frame, with DevOps above MLOps and matching stages progressing together. It is one 48-frame, 3840 × 4800 animation, preserving readable full-width scenes.

DevOps: source → build → verification → packaging → deployment → monitoring.

MLOps: data preparation → training/evaluation → MLflow tracking → inference packaging → Kubernetes serving → monitoring and retraining feedback.

Run `python3 scripts/generate_hero_hq.py`, then `python3 scripts/build_preview.py`. The main animation generator also invokes the HQ renderer. Native SVG logos and geometry retain sharp edges; clean scene cuts prevent overlapping captions. `assets/hero-enhanced.svg` and `assets/hero-poster.png` provide full-resolution static artwork.

These are illustrative workflows rather than evidence that every stage is integrated into a single deployed system. Earlier versions are backed up outside the repository. Detailed project architectures remain under `assets/work`.

The workflows share glass geometry and typography. DevOps uses cool blue/cyan accents; MLOps uses a soft violet backdrop, lilac glass, mint scan lines, and a moving orbit marker to suggest model lineage. Product logos retain their own colours.

For clickable contact links between the workflows, `scripts/split_hero.py` exports `hero-devops-workflow-4k.gif` and `hero-mlops-4k.gif` from the same master, preserving their frame count and duration. The README places GitHub, LinkedIn and Gmail above the banner. The HQ generator invokes this export automatically.

Contact links and navigation live at the very top above both workflow panels; the navigation wordmark and social-link arrows are removed. `scripts/generate_role_banner.py` renders the separate role strip at 3840 × 640: Kubernetes cluster activity, a Prometheus health pulse, and MLflow/model-network signals. Complete role titles stay visible throughout each scene.

The identity header is exported as `hero-identity-4k.png`, allowing four linked liquid-glass credential cards below the role line, ordered Red Hat, Kubernetes, AWS, Azure. The animated role strip is positioned between the DevOps and MLOps panels.

The identity header is rendered directly from vector text, without the AJITHBUILDS wordmark. The top contact/navigation bar uses a muted blue-grey/violet glass surface with a subtle inset highlight.
