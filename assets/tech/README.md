# Detailed technology tags

The thirty tags share the same original-colour product marks as the architecture and workflow graphics. `scripts/apply_colour_tech_tags.py` embeds the artwork from `assets/stack-icons` into dark tag surfaces; `scripts/render_tech_tags.cjs` rasterizes at 3x and `scripts/generate_tech_badges.py` adds the glass sheen and gentle motion.

Earlier label geometry and source URLs are retained in `sources.json`. Current logo artwork and hashes are recorded in `../stack-icons/sources.json`. Use `python3 scripts/rebuild_brand_assets.py` to rebuild the complete page consistently.
