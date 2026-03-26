# drivex/render/render_part02.ps1
# ─────────────────────────────────────────────────────────────────
# Render Part 02 scenes  (title card + stubs now; full impl TBD).
# Run from drivex/ directory.
# ─────────────────────────────────────────────────────────────────

Set-Location $PSScriptRoot\..

$scenes = @(
    @{ file="scenes\part02\p02_s01_title.py";       class="P02S01Title" },
    @{ file="scenes\part02\p02_s02_background.py";  class="P02S02Background" },
    @{ file="scenes\part02\p02_s03_evolution.py";   class="P02S03Evolution" },
    @{ file="scenes\part02\p02_s04_occlusion.py";   class="P02S04Occlusion" },
    @{ file="scenes\part02\p02_s05_related_works.py"; class="P02S05RelatedWorks" },
    @{ file="scenes\part02\p02_s06_three_questions.py"; class="P02S06ThreeQuestions" },
    @{ file="scenes\part02\p02_s07_v2xpnp.py";      class="P02S07V2XPnP" },
    @{ file="scenes\part02\p02_s08_dataset.py";      class="P02S08Dataset" },
    @{ file="scenes\part02\p02_s09_turbotrain.py";   class="P02S09TurboTrain" },
    @{ file="scenes\part02\p02_s10_riskmap.py";      class="P02S10RiskMap" },
    @{ file="scenes\part02\p02_s11_summary.py";      class="P02S11Summary" },
    @{ file="scenes\part02\p02_s12_bridge.py";       class="P02S12Bridge" }
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

Write-Host "`nAll Part 02 scenes rendered." -ForegroundColor Yellow
