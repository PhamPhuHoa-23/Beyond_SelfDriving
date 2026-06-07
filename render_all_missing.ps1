# render_all_missing.ps1 — render mọi scene chưa có MP4
# Chạy từ thư mục Lab01_3B1B

$scenes = @(
    @{file="beyond/scenes/intro/i03_roadmap.py";         cls="I03Roadmap"},
    @{file="beyond/scenes/part01/p01_s05_fm_empower.py"; cls="P01S05FmEmpower"},
    @{file="beyond/scenes/part01/p01_s07_vla_arch.py";   cls="P01S07VlaArch"},
    @{file="beyond/scenes/part01/p01_s09_takeaways.py";  cls="P01S09Takeaways"},
    @{file="beyond/scenes/part02/p02_s03_evolution.py";  cls="P02S03Evolution"},
    @{file="beyond/scenes/part02/p02_s06_three_questions.py"; cls="P02S06ThreeQuestions"},
    @{file="beyond/scenes/part02/p02_s08_dataset.py";    cls="P02S08Dataset"},
    @{file="beyond/scenes/part02/p02_s09_turbotrain.py"; cls="P02S09TurboTrain"},
    @{file="beyond/scenes/part02/p02_s10_riskmap.py";    cls="P02S10RiskMap"},
    @{file="beyond/scenes/part02/p02_s11_summary.py";    cls="P02S11Summary"},
    @{file="beyond/scenes/part02/p02_s12_bridge.py";     cls="P02S12Bridge"},
    @{file="beyond/scenes/part03/p03_s03_smart_intersection.py"; cls="P03S03SmartIntersection"},
    @{file="beyond/scenes/part03/p03_s04_calibration.py"; cls="P03S04Calibration"},
    @{file="beyond/scenes/part03/p03_s06_cooperfuse.py"; cls="P03S06CooperFuse"},
    @{file="beyond/scenes/part03/p03_s07_digital_twin.py"; cls="P03S07DigitalTwin"},
    @{file="beyond/scenes/part03/p03_s08_localization.py"; cls="P03S08Localization"},
    @{file="beyond/scenes/part03/p03_s10_v2x_realo.py";  cls="P03S10V2XReaLO"},
    @{file="beyond/scenes/part03/p03_s11_opencda.py";    cls="P03S11OpenCDA"},
    @{file="beyond/scenes/part03/p03_s12_simboost.py";   cls="P03S12SimBoost"},
    @{file="beyond/scenes/part03/p03_s14_bridge.py";     cls="P03S14Bridge"},
    @{file="beyond/scenes/part04/p04_s02_annotation_cost.py"; cls="P04S02AnnotationCost"},
    @{file="beyond/scenes/part04/p04_s04_turbotrain_gradient.py"; cls="P04S04TurboTrainGrad"},
    @{file="beyond/scenes/part04/p04_s06_efficiency_summary.py"; cls="P04S06EfficiencySummary"},
    @{file="beyond/scenes/part04/p04_s07_latency_chain.py"; cls="P04S07LatencyChain"},
    @{file="beyond/scenes/part04/p04_s09_bridge.py";     cls="P04S09Bridge"},
    @{file="beyond/scenes/part05/p05_s02_physical_ai_vision.py"; cls="P05S02PhysicalAI"},
    @{file="beyond/scenes/part05/p05_s04_urbansim.py";   cls="P05S04UrbanSim"},
    @{file="beyond/scenes/part05/p05_s06_vid2sim.py";    cls="P05S06Vid2Sim"},
    @{file="beyond/scenes/part05/p05_s08_final_summary.py"; cls="P05S08FinalSummary"}
)

$total = $scenes.Count
$i = 0
foreach ($s in $scenes) {
    $i++
    Write-Host "[$i/$total] Rendering $($s.cls)..." -ForegroundColor Cyan
    manim -ql --disable_caching $s.file $s.cls 2>&1 | Select-Object -Last 2
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK" -ForegroundColor Green
    } else {
        Write-Host "  FAILED (exit $LASTEXITCODE)" -ForegroundColor Red
    }
}
Write-Host "`nDone. $total scenes processed." -ForegroundColor Yellow
