#!/bin/bash
# Render all Part 2 scenes
export PATH="/Library/TeX/texbin:$PATH"
QUALITY=${1:--ql}

echo "=== Rendering Part 2: Cooperative Multi-Agent ==="

SCENES=(
  "drivex_video/scenes/part2/01_intro.py Part2Intro"
  "drivex_video/scenes/part2/02_background.py BackgroundStats"
  "drivex_video/scenes/part2/03_shift.py ShiftToE2E"
  "drivex_video/scenes/part2/04_occlusion_gaps.py OcclusionProblem"
  "drivex_video/scenes/part2/04_occlusion_gaps.py ResearchGaps"
  "drivex_video/scenes/part2/05_vla_tt.py V2XPnP_Framework"
  "drivex_video/scenes/part2/05_vla_tt.py TurboTrain"
  "drivex_video/scenes/part2/06_riskmap.py RiskMap_Planning"
  "drivex_video/scenes/part2/06_riskmap.py Part2Conclusion"
)

FAILED=(); SUCCESS=0
for entry in "${SCENES[@]}"; do
  FILE=$(echo $entry | awk '{print $1}')
  CLASS=$(echo $entry | awk '{print $2}')
  echo "► Rendering $CLASS..."
  if manim $QUALITY "$FILE" "$CLASS"; then
    echo "  ✅ $CLASS done"; SUCCESS=$((SUCCESS + 1))
  else
    echo "  ❌ $CLASS FAILED"; FAILED+=("$CLASS")
  fi
done

echo "=== Done: $SUCCESS/${#SCENES[@]} scenes rendered ==="
[ ${#FAILED[@]} -gt 0 ] && echo "Failed: ${FAILED[*]}"
