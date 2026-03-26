# drivex/render/render_intro.ps1
# ─────────────────────────────────────────────────────────────────
# Render all INTRO scenes at low quality (-ql = 480p15).
# Run from the drivex/ directory:
#   cd c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex
#   .\render\render_intro.ps1
# ─────────────────────────────────────────────────────────────────

Set-Location $PSScriptRoot\..

$scenes = @(
    @{ file="scenes\intro\i01_title_card.py"; class="I01TitleCard" },
    @{ file="scenes\intro\i02_hook.py";        class="I02Hook" },
    @{ file="scenes\intro\i03_roadmap.py";     class="I03Roadmap" }
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

Write-Host "`nAll INTRO scenes rendered." -ForegroundColor Yellow
