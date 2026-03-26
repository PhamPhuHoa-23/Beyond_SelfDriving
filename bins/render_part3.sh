#!/bin/bash
# Render all Part 3 scenes (using the finalized files)
export PATH="/Library/TeX/texbin:$PATH"
QUALITY=${1:--ql}

echo "=== Rendering Part 3: Bridging Simulation and Reality ==="

SCENES=(
  "drivex_video/scenes/part3/01_intro.py Part3Intro"
  "drivex_video/scenes/part3/01_intro.py UCLAIntersection"
  "drivex_video/scenes/part3/02_intersection_data.py IntersectionSetup"
  "drivex_video/scenes/part3/02_intersection_data.py DataCollection"
  "drivex_video/scenes/part3/03_calibration_localization.py SensorCalibration"
  "drivex_video/scenes/part3/03_calibration_localization.py MapLocalization"
  "drivex_video/scenes/part3/04_fusion_real.py LateFusion"
  "drivex_video/scenes/part3/04_fusion_real.py IntermediateFusion"
  "drivex_video/scenes/part3/05_digital_twin.py DigitalTwin"
  "drivex_video/scenes/part3/05_digital_twin.py Part3Conclusion"
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
