# drivex/render/render_part03.ps1
# ─────────────────────────────────────────────────────────────────
# Render Part 03 scenes.
# Run from drivex/ directory.
# ─────────────────────────────────────────────────────────────────

Set-Location $PSScriptRoot\..

$scenes = @(
    @{ file="scenes\part03\p03_s01_title.py";              class="P03S01Title" },
    @{ file="scenes\part03\p03_s02_four_pillars.py";       class="P03S02FourPillars" },
    @{ file="scenes\part03\p03_s03_smart_intersection.py"; class="P03S03SmartIntersection" },
    @{ file="scenes\part03\p03_s04_calibration_time.py";   class="P03S04CalibrationTime" },
    @{ file="scenes\part03\p03_s05_calibration_space.py";  class="P03S05CalibrationSpace" },
    @{ file="scenes\part03\p03_s06_data_collection.py";    class="P03S06DataCollection" },
    @{ file="scenes\part03\p03_s07_localization_why.py";   class="P03S07LocalizationWhy" },
    @{ file="scenes\part03\p03_s08_kalman_filter.py";      class="P03S08KalmanFilter" },
    @{ file="scenes\part03\p03_s09_cooper_fuse.py";        class="P03S09CooperFuse" },
    @{ file="scenes\part03\p03_s10_v2x_realo.py";          class="P03S10V2XReaLO" },
    @{ file="scenes\part03\p03_s11_opencda_ros.py";        class="P03S11OpenCDAROS" },
    @{ file="scenes\part03\p03_s12_simboost.py";           class="P03S12SimBoost" },
    @{ file="scenes\part03\p03_s13_infrax.py";             class="P03S13InfraX" },
    @{ file="scenes\part03\p03_s14_bridge.py";             class="P03S14Bridge" }
)

foreach ($s in $scenes) {
    Write-Host "Rendering $($s.class) ..." -ForegroundColor Cyan
    manim -ql $s.file $s.class
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR rendering $($s.class)" -ForegroundColor Red
        exit 1
    }
    Write-Host "Done: $($s.class)" -ForegroundColor Green
}

Write-Host "`nAll Part 03 scenes rendered." -ForegroundColor Yellow
