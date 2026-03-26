# drivex/render/render_part01.ps1
# ─────────────────────────────────────────────────────────────────
# Render all Part 01 scenes at low quality (-ql = 480p15).
# Run from the drivex/ directory:
#   cd c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex
#   .\render\render_part01.ps1
# ─────────────────────────────────────────────────────────────────

Set-Location $PSScriptRoot\..

$scenes = @(
    @{ file="scenes\part01\p01_s01_opening.py";    class="P01S01Opening" },
    @{ file="scenes\part01\p01_s02_genai_boom.py"; class="P01S02GenAIBoom" },
    @{ file="scenes\part01\p01_s03_av_arch.py";    class="P01S03AVArch" },
    @{ file="scenes\part01\p01_s04_longtail.py";   class="P01S04LongTail" },
    @{ file="scenes\part01\p01_s05_fm_empower.py"; class="P01S05FMEmpower" },
    @{ file="scenes\part01\p01_s06_vla_roadmap.py";class="P01S06VLARoadmap" },
    @{ file="scenes\part01\p01_s07_vla_arch.py";   class="P01S07VLAArch" },
    @{ file="scenes\part01\p01_s08_autovla.py";    class="P01S08AutoVLA" },
    @{ file="scenes\part01\p01_s09_takeaways.py";  class="P01S09Takeaways" }
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

Write-Host "`nAll Part 01 scenes rendered." -ForegroundColor Yellow
