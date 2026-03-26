# drivex/render/render_part04.ps1
# ─────────────────────────────────────────────────────────────────
# Render Part 04 scenes.
# Run from drivex/ directory.
# ─────────────────────────────────────────────────────────────────

Set-Location $PSScriptRoot\..

$scenes = @(
    @{ file="scenes\part04\p04_s01_title.py";                class="P04S01Title"             },
    @{ file="scenes\part04\p04_s02_why_efficiency.py";       class="P04S02WhyEfficiency"      },
    @{ file="scenes\part04\p04_s03_annotation_cost.py";      class="P04S03AnnotationCost"     },
    @{ file="scenes\part04\p04_s04_coopre.py";               class="P04S04CooPre"             },
    @{ file="scenes\part04\p04_s05_multi_task_conflict.py";  class="P04S05MultiTaskConflict"  },
    @{ file="scenes\part04\p04_s06_turbotrain.py";           class="P04S06TurboTrain"         },
    @{ file="scenes\part04\p04_s07_latency_chain.py";        class="P04S07LatencyChain"       },
    @{ file="scenes\part04\p04_s08_quantv2x.py";             class="P04S08QuantV2X"           },
    @{ file="scenes\part04\p04_s09_efficiency_summary.py";   class="P04S09EfficiencySummary"  },
    @{ file="scenes\part04\p04_s10_bridge.py";               class="P04S10Bridge"             }
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

Write-Host "`nAll Part 04 scenes rendered." -ForegroundColor Yellow
