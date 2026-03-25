#!/bin/bash
# Render all Part 1 scenes (low quality for preview)
# Run with: bash render_part1.sh
# Or high quality: bash render_part1.sh -qh

export PATH="/Library/TeX/texbin:$PATH"
QUALITY=${1:--ql}  # default: low quality (-ql), pass -qh for high

echo "=== Rendering Part 1: Foundation Models for Autonomous Driving ==="
echo "Quality: $QUALITY"
echo ""

SCENES=(
  "drivex_video/scenes/part1/01_intro.py IntroQuestion"
  "drivex_video/scenes/part1/01_intro.py IntroOutline"
  "drivex_video/scenes/part1/01_intro.py TitleScene"
  "drivex_video/scenes/part1/02_boom.py GenerativeAIBoom"
  "drivex_video/scenes/part1/02_boom.py FoundationModelParadigm"
  "drivex_video/scenes/part1/03_arch.py AVArchitectures"
  "drivex_video/scenes/part1/04_challenges.py CornerCases"
  "drivex_video/scenes/part1/05_vla_roadmap.py FoundationEmpowerment"
  "drivex_video/scenes/part1/05_vla_roadmap.py VLARoadmap"
  "drivex_video/scenes/part1/05_vla_roadmap.py VLADatasets"
  "drivex_video/scenes/part1/06_vla_architectures.py VLAArchitectures"
  "drivex_video/scenes/part1/06_vla_architectures.py ArchitectureComparison"
  "drivex_video/scenes/part1/07_autovla.py AutoVLA_Concept"
  "drivex_video/scenes/part1/07_autovla.py AutoVLA_Results"
  "drivex_video/scenes/part1/08_conclusion.py KeyTakeaways"
  "drivex_video/scenes/part1/08_conclusion.py FutureDirections"
  "drivex_video/scenes/part1/08_conclusion.py BridgeToPart2"
)

FAILED=()
SUCCESS=0

for entry in "${SCENES[@]}"; do
  FILE=$(echo $entry | awk '{print $1}')
  CLASS=$(echo $entry | awk '{print $2}')
  
  echo "► Rendering $CLASS from $FILE..."
  if manim $QUALITY "$FILE" "$CLASS"; then
    echo "  ✅ $CLASS done"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "  ❌ $CLASS FAILED"
    FAILED+=("$CLASS")
  fi
  echo ""
done

echo "=== Done: $SUCCESS/${#SCENES[@]} scenes rendered ==="
if [ ${#FAILED[@]} -gt 0 ]; then
  echo "Failed scenes:"
  for f in "${FAILED[@]}"; do
    echo "  - $f"
  done
fi
