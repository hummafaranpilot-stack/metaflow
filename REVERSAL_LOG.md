# Reversal Log

Tracks edits flagged as **reversal** — temporary changes that must be reverted after compliance approval. Do not delete entries; once reverted, mark them `reverted on YYYY-MM-DD` for audit trail.

**Convention:** All reversal edits comment-out the original markup in place using `<!-- REVERSAL R-XXX START: ... -->` / `<!-- REVERSAL R-XXX END: ... -->` wrappers. To revert, locate the marker pair in the file and delete the `<!--` and `-->` lines (keeping the original markup between them).

---

## R-001 — Comment out "As Featured In" press bar in bg/desktop.html

- **Date:** 2026-05-06
- **File:** `bg/desktop.html`
- **Location:** Just above `<!-- Stock banner #1: below press bar -->` (between hero CTA block and the first stock banner).
- **Status:** pending compliance review
- **Marker:** `REVERSAL R-001 START` ... `REVERSAL R-001 END`
- **Change:** Commented out the auto-scrolling press bar showing media logos (US Weekly, Forbes Health, USA Today, The Oprah Magazine, Good Housekeeping, NBC, The Doctors).
- **Note:** Originally I deleted this block; replaced with in-place comment on user request so it can be restored without re-typing markup. The original `<!-- As Featured In — auto-scrolling press bar -->` label comment was dropped (HTML doesn't allow nested comments) — REVERSAL marker now serves as the label.

### Revert instructions
In `bg/desktop.html`, find `REVERSAL R-001 START` and `REVERSAL R-001 END`. Delete those two marker lines plus the `<!--` line right after START and the `-->` line right before END. The press-bar `<div>` between them becomes live markup again.

---

## R-002 — Comment out all video player sections in bg/desktop.html

- **Date:** 2026-05-06
- **File:** `bg/desktop.html`
- **Status:** pending compliance review
- **Marker:** `REVERSAL R-002 START: <id>` ... `REVERSAL R-002 END: <id>` (one pair per video block)
- **Change:** Commented out 8 video player blocks (each with its title, badge, poster, play overlay, and caption). Players use Cloudflare Stream HLS via `data-cf-id`. CSS (`.kw-video-section`, `.mv-player`, etc.) and the JS player loader are untouched, so no other restoration is needed.

### Blocks commented out

| ID | Title | data-cf-id |
|---|---|---|
| `mf-hook` | What Most Doctors Won't Tell You About Blood Sugar | `1f30321143d938a88c2fa62fe2847f38` |
| `mf-stats` | The Real Reason Your Blood Sugar Won't Stabilize | `95640a03db216389aafcd362dcd4178f` |
| `mf-alan` | Real Story From A Real Customer | `47fc2efd9255f8ceb342d464c0b5f652` |
| `testimonial videos row` | Real Persons, Real Reviews (Jessica + William + Donna) | `9747362533b5f7c3da1291c62557d5b4`, `b9f67fcf576433575652f2294be5fc9c`, `eeeb918011f4c6a4d17f7e445497f96a` |
| `mf-hotel` | How Blood Sugar Actually Works (The Hotel Analogy) | `860065ac734afa2667e0185eca3eae5d` |
| `mf-aspiration` | Imagine Your Life Without Daily Blood Sugar Worries | `4aae4aa56da5b26fe86b93f701c3fd52` |
| `mf-warning` | What Happens If You Keep Ignoring The Root Cause | `28c276dbc0fe3ab8593ed2b9f17e94cb` |
| `mf-patty` | From Hopeless To Free In 7 Weeks | `f9f240b382db0b28ccb91897f1c5f19c` |

### Revert instructions
In `bg/desktop.html`, search for `REVERSAL R-002 START`. For each match, delete the four wrapper lines: `<!-- REVERSAL R-002 START ... -->`, the `<!--` directly after it, the `-->` directly before END, and `<!-- REVERSAL R-002 END ... -->`. The `<section>` markup between becomes live again. Repeat for all 8 marker pairs.

To revert all R-002 in one go: search-and-replace by removing every line matching the regex `^<!-- REVERSAL R-002 (START|END):.*-->$` and the bare `<!--` / `-->` lines that wrap each block.
