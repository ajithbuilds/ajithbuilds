# Maintaining the profile locally

The public profile source is [README.md](../README.md). Edit it first; regenerate the HTML and static edition afterward. Do not hand-edit generated previews.

## Setup

Python 3.12+ and Node.js are required. Tested here with Python 3.14, Pillow 12.2.0, Mistune 3.2.0, Beautiful Soup 4.14.3, Node.js 25.9.0, and resvg 2.6.2. The artwork scripts use macOS Arial/Verdana fonts.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm ci --prefix tools --ignore-scripts --no-audit --no-fund
```

## Refresh and verify

```sh
python3 scripts/build_preview.py
python3 scripts/verify_profile.py
```

Open `preview.html` manually for the animated local view or `preview-static.html` for the static view. Both are generated and ignored by Git. They load local assets and suppress the external view counter. The animated preview respects the system's reduced-motion setting. The pause/resume control was removed at the user's request; a static edition remains available. If VS Code shows an older Markdown view, reload its window and reopen the correct README.

The builder records content hashes for the README, posters, and referenced images. Verification fails if the preview or its images changed since the last build. Poster freshness is content-based, not dependent on filesystem timestamps.

## Rebuild architecture artwork

```sh
python3 scripts/rebuild_architectures.py
```

Or rebuild one diagram:

```sh
python3 scripts/rebuild_architectures.py ai-agent
```

Supported names: `platform`, `reliability`, `ai-agent`, `finops`. Each pipeline authors SVG stages, rasterizes with the pinned local renderer, creates the GIF, and refreshes previews. Finished GIFs and rendered PNGs are atomically replaced so readers cannot see a partially written image. Run rebuilds sequentially rather than launching concurrent generators against the same assets.

Header animation: `python3 scripts/generate_animations.py`.
Technology GIFs: `python3 scripts/generate_tech_badges.py`.
After either, run the preview builder and verifier. The original SVG badges and their local raster inputs remain available.

## Publishing constraints

Nothing in this task was pushed, renamed remotely, or deployed. The repository currently resolves to `ajithbuilds/ajithkumarbsh060`. A GitHub profile README requires a public repository named `ajithbuilds`, matching the account. When publishing later, retain the entire `assets` directory referenced by the README and its static edition.

Keep this view-counter URL exactly as-is, including the legacy identifier:

```text
https://komarev.com/ghpvc/?username=ajithkumarren&color=1565C0&style=flat-square&label=Profile+Views
```

The count is stored by the external provider. Renaming the GitHub account does not require changing the counter identifier. Do not make test requests to it.

Career metrics and certification claims are user-supplied. Western Union and AWS Solutions Architect – Associate are explicit user corrections to the original resume. No credential ID, expiry date, or employer verification was supplied. Program links describe the certification; they are not personal verification records.

## Recovery

A complete pre-audit source/assets snapshot is stored outside this repository at `../profile-backup/pre-e2e-review.tgz`. Superseded graphics were moved, not permanently deleted, to `../profile-backup/e2e-legacy-assets/` with a manifest. The original Git history bundle and original README are also retained in `../profile-backup/`.

The outcome strip is animated with `python3 scripts/animate_impact.py`, which regenerates its vector base and renders a 72-frame GIF using the local SVG renderer. Run `python3 scripts/build_preview.py` afterward. The pulse and query paths are illustrative, not time-series measurements.

For the native-vector 4K-wide hero, run `python3 scripts/generate_hero_hq.py`, then rebuild the preview. The main animation generator also uses this renderer. The combined GIF is 3840 × 4800 and shows DevOps and MLOps together in every frame; the SVG and full-resolution poster are retained alongside it. Clean scene cuts avoid caption ghosting.

Generate the 30-tool Tech Stack showcase with `python3 scripts/generate_stack_showcase.py`, then rebuild the preview. Seven 4K-wide scenes pair the existing local product marks with category-specific operational illustrations. This is a tools showcase, not a claim that every product is integrated into one deployment. Existing detailed stack tags remain available below.

Rebuild the complete colour-icon design with `python3 scripts/rebuild_brand_assets.py`. Shared product artwork is resolved through `scripts/brand_icons.py`; semantic symbols remain purpose-drawn. The process rebuilds detailed glass tags, all four architectures, both hero workflows, role and stack showcases, previews, and acceptance checks. All dependencies and logo files are local.

The Built for production illustration is a local vector-based operations console. Rebuild it with `python3 scripts/generate_production_console.py`; its product marks use the shared colour-icon resolver. Both full rebuild entry points include this graphic.
