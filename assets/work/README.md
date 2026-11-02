# Work architecture graphics

The README embeds the animated version and links to a full-size vector diagram for each work section. Static PNGs retain every label without stage highlights. All four use the same local liquid-glass material and typography.

| Section | Vector source | Animation | Generator | Animator |
| --- | --- | --- | --- | --- |
| Platform engineering | [SVG](platform-glass-architecture.svg) | [GIF](platform-glass-architecture.gif) | generate_platform_architecture.py | animate_platform_architecture.py |
| Token refresh | [SVG](reliability-glass-architecture.svg) | [GIF](reliability-glass-architecture.gif) | generate_reliability_architecture.py | animate_reliability_architecture.py |
| SCP AI Agent | [SVG](ai-agent-glass-architecture.svg) | [GIF](ai-agent-glass-architecture.gif) | generate_ai_agent_architecture.py | animate_ai_agent_architecture.py |
| FinOps | [SVG](finops-glass-architecture.svg) | [GIF](finops-glass-architecture.gif) | generate_finops_architecture.py | animate_finops_architecture.py |

Run `python3 scripts/rebuild_architectures.py` from the repository root after installing the pinned tools. See [maintenance](../../docs/MAINTENANCE.md).

Platform details and metrics come from the supplied resume and user narrative. Token-refresh topology, SCP AI Agent options, and FinOps lifecycle come from user-supplied architecture references. These illustrate the stated designs; they are not runtime traces or independently verified production measurements. Client and certification corrections follow the user's explicit instructions.

The AI retrieval diagram follows Azure's order: parallel vector/keyword retrieval, reciprocal rank fusion, then semantic reranking. It distinguishes persisted Cosmos DB history from in-memory graph checkpoint state. The FinOps diagram places customer review/merge before infrastructure apply and shows potential recommendations separately from observed outcomes. Private endpoint and environment examples were not copied into the public diagrams.

Technology headings use locally embedded product artwork from `assets/architecture-icons/`; that directory records provenance. Concept headings use purpose-drawn symbols for authentication, storage, review, and refresh. The SVGs remain self-contained.
