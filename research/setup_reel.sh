#!/usr/bin/env bash
# Safe setup for the Reel skills (replaces ResearchStudio's install.sh for this repo).
# What it does NOT do, on purpose: no sudo, no system packages, no writes to ~/.claude / ~/.codex agent settings
# (upstream install.sh seeds "skipDangerousModePermissionPrompt" and "sandbox_mode: danger-full-access"), no skill symlinks.
# Run from the repo root:  bash research/setup_reel.sh
set -euo pipefail

RS_DIR="${RS_DIR:-../ResearchStudio}"
RS_COMMIT="${RS_COMMIT:-063f100}"   # pinned: the ResearchStudio version the HarnessRSI Daily posters were made with

if [ ! -d "$RS_DIR/.git" ]; then
  git clone --quiet https://github.com/microsoft/ResearchStudio.git "$RS_DIR"
fi
git -C "$RS_DIR" fetch --quiet origin
git -C "$RS_DIR" checkout --quiet "$RS_COMMIT" || echo "WARN: could not pin $RS_COMMIT; using $(git -C "$RS_DIR" rev-parse --short HEAD)"

python3 -m pip install --user --quiet pymupdf pillow numpy "python-docx>=1.1.2" qrcode playwright imageio-ffmpeg \
  "edge-tts>=7.2.8" "fonttools>=4.59"
python3 -m playwright install chromium   # browser only; without --with-deps (that one calls sudo)

missing=0
for tool in pdftotext pandoc; do
  command -v "$tool" >/dev/null || { echo "MISSING: $tool (required: pdftotext for paper2assets, pandoc for blog .md)"; missing=1; }
done
for tool in libreoffice ffmpeg; do
  command -v "$tool" >/dev/null || echo "optional: $tool not found (only video/PPTX extras need it)"
done

SK="$RS_DIR/ResearchStudio-Reel/skills"
echo "Reel skills (read each SKILL.md and run its scripts directly):"
for s in paper2assets paper2poster paper2blog; do echo "  $SK/$s/SKILL.md"; done
exit $missing
