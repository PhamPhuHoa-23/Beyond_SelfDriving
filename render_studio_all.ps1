#!/usr/bin/env pwsh
# Render all studio/ scenes in scene order.
# Output: videos/<ClassName>.mp4

param(
    [ValidateSet("low", "medium", "high", "uhd")]
    [string]$Quality = "low"
)

$env:PATH = "C:\Users\admin\miniconda3\Scripts;C:\Users\admin\miniconda3\Library\bin;" + $env:PATH
$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"
$MANIM = "C:\Users\admin\miniconda3\Scripts\manimgl.exe"
$LOG   = "C:\Users\admin\Downloads\ML\Lab01_3B1B\render_studio_all.log"
$QUALITY_ARGS = @{
    low = @("-l")
    medium = @("-m")
    high = @("-r", "1920x1080", "--fps", "30")
    uhd = @("-r", "3840x2160", "--fps", "30")
}[$Quality]

Set-Location "C:\Users\admin\Downloads\ML\Lab01_3B1B"
"" | Out-File $LOG -Encoding utf8

$scenes = @(
    # Intro
    @{ file="studio/scenes/intro/i01_title_card.py";              cls="I01TitleCard" },
    @{ file="studio/scenes/intro/i02_the_hook.py";                cls="I02TheHook" },
    @{ file="studio/scenes/intro/i03_roadmap.py";                 cls="I03Roadmap" },
    @{ file="studio/scenes/intro/i04_bridge_to_p1.py";            cls="I04BridgeToP1" },
    # Part 01
    @{ file="studio/scenes/part01/p01_s01_title.py";              cls="P01S01Title" },
    @{ file="studio/scenes/part01/p01_s02a_genai_timeline.py";    cls="P01S02AGenAITimeline" },
    @{ file="studio/scenes/part01/p01_s02b_fm_definition.py";     cls="P01S02BFMDefinition" },
    @{ file="studio/scenes/part01/p01_s03a_modular.py";           cls="P01S03AModular" },
    @{ file="studio/scenes/part01/p01_s03b_e2e.py";               cls="P01S03BE2E" },
    @{ file="studio/scenes/part01/p01_s03c_hybrid.py";            cls="P01S03CHybrid" },
    @{ file="studio/scenes/part01/p01_s04a_longtail_problem.py";  cls="P01S04ALongtailProblem" },
    @{ file="studio/scenes/part01/p01_s04b_longtail_insight.py";  cls="P01S04BLongtailInsight" },
    @{ file="studio/scenes/part01/p01_s05_fm_empower.py";         cls="P01S05FMEmpower" },
    @{ file="studio/scenes/part01/p01_s06_vla_roadmap.py";        cls="P01S06VLARoadmap" },
    @{ file="studio/scenes/part01/p01_s07a_bevdriver.py";         cls="P01S07ABEVDriver" },
    @{ file="studio/scenes/part01/p01_s07b_emma.py";              cls="P01S07BEMMA" },
    @{ file="studio/scenes/part01/p01_s07c_drivevlm.py";          cls="P01S07CDriveVLM" },
    @{ file="studio/scenes/part01/p01_s08a_autovla_switch.py";    cls="P01S08AAutoVLASwitch" },
    @{ file="studio/scenes/part01/p01_s08b_autovla_results.py";   cls="P01S08BAutoVLAResults" },
    @{ file="studio/scenes/part01/p01_s09_takeaways.py";          cls="P01S09Takeaways" },
    @{ file="studio/scenes/part01/p01_s10_bridge_to_p2.py";       cls="P01S10BridgeToP2" },
    # Part 02
    @{ file="studio/scenes/part02/p02_s01_title.py";              cls="P02S01Title" },
    @{ file="studio/scenes/part02/p02_s02a_119m.py";              cls="P02S02A119M" },
    @{ file="studio/scenes/part02/p02_s02b_waymo_reduce.py";      cls="P02S02BWaymoReduce" },
    @{ file="studio/scenes/part02/p02_s03_e2e_evolution.py";      cls="P02S03E2EEvolution" },
    @{ file="studio/scenes/part02/p02_s04a_occlusion_problem.py"; cls="P02S04AOcclusionProblem" },
    @{ file="studio/scenes/part02/p02_s05_radar_waves.py";        cls="P02S05RadarWaves" },
    @{ file="studio/scenes/part02/p02_s06_related_works.py";      cls="P02S06RelatedWorks" },
    @{ file="studio/scenes/part02/p02_s06b_dataset_evolution.py"; cls="P02S06BDatasetEvolution" },
    @{ file="studio/scenes/part02/p02_s07_research_gaps.py";      cls="P02S07ResearchGaps" },
    @{ file="studio/scenes/part02/p02_s08_three_questions.py";    cls="P02S08ThreeQuestions" },
    @{ file="studio/scenes/part02/p02_s09_v2xpnp_arch.py";       cls="P02S09V2XPnPArch" },
    @{ file="studio/scenes/part02/p02_s10_v2xpnp_dataset.py";    cls="P02S10V2XPnPDataset" },
    @{ file="studio/scenes/part02/p02_s11a_turbotrain_problem.py"; cls="P02S11ATurboTrainProblem" },
    @{ file="studio/scenes/part02/p02_s11a2_root_causes.py";      cls="P02S11A2RootCauses" },
    @{ file="studio/scenes/part02/p02_s11b_turbotrain_solution.py"; cls="P02S11BTurboTrainSolution" },
    @{ file="studio/scenes/part02/p02_s11c_planning_pivot.py";    cls="P02S11CPlanningPivot" },
    @{ file="studio/scenes/part02/p02_s12_riskmap.py";            cls="P02S12RiskMap" },
    @{ file="studio/scenes/part02/p02_s13_summary.py";            cls="P02S13Summary" },
    @{ file="studio/scenes/part02/p02_s14_bridge_to_p3.py";       cls="P02S14BridgeToP3" },
    # Part 03
    @{ file="studio/scenes/part03/p03_s01_title.py";              cls="P03S01Title" },
    @{ file="studio/scenes/part03/p03_s02_sim_real_gap.py";       cls="P03S02SimRealGap" },
    @{ file="studio/scenes/part03/p03_s03_smart_intersection.py"; cls="P03S03SmartIntersection" },
    @{ file="studio/scenes/part03/p03_s04a_time_calibration.py";  cls="P03S04ATimeCalibration" },
    @{ file="studio/scenes/part03/p03_s04b_space_calibration.py"; cls="P03S04BSpaceCalibration" },
    @{ file="studio/scenes/part03/p03_s05_data_collection.py";    cls="P03S05DataCollection" },
    @{ file="studio/scenes/part03/p03_s06_localization_role.py";  cls="P03S06LocalizationRole" },
    @{ file="studio/scenes/part03/p03_s07_kalman_filter.py";      cls="P03S07KalmanFilter" },
    @{ file="studio/scenes/part03/p03_s08_cooperfuse.py";         cls="P03S08CooperFuse" },
    @{ file="studio/scenes/part03/p03_s09_v2x_realo.py";         cls="P03S09V2XReaLO" },
    @{ file="studio/scenes/part03/p03_s10_opencda_ros.py";        cls="P03S10OpenCDAROS" },
    @{ file="studio/scenes/part03/p03_s11_simboost.py";           cls="P03S11SimBoost" },
    @{ file="studio/scenes/part03/p03_s12_digital_twin.py";       cls="P03S12DigitalTwin" },
    @{ file="studio/scenes/part03/p03_s13_infrax.py";             cls="P03S13InfraX" },
    @{ file="studio/scenes/part03/p03_s14_summary.py";            cls="P03S14Summary" },
    @{ file="studio/scenes/part03/p03_s15_bridge_to_p4.py";       cls="P03S15BridgeToP4" },
    # Part 04
    @{ file="studio/scenes/part04/p04_s01_title.py";              cls="P04S01Title" },
    @{ file="studio/scenes/part04/p04_s02_v2x_overview.py";       cls="P04S02V2XOverview" },
    @{ file="studio/scenes/part04/p04_s03_annotation_cost.py";    cls="P04S03AnnotationCost" },
    @{ file="studio/scenes/part04/p04_s04_coopre_masked.py";      cls="P04S04CooPReMasked" },
    @{ file="studio/scenes/part04/p04_s05_turbotrain_landscape.py"; cls="P04S05TurboTrainLandscape" },
    @{ file="studio/scenes/part04/p04_s06_latency_chain.py";      cls="P04S06LatencyChain" },
    @{ file="studio/scenes/part04/p04_s07a_arithmetic_cost.py";   cls="P04S07AArithmeticCost" },
    @{ file="studio/scenes/part04/p04_s07b_memory_bound.py";      cls="P04S07BMemoryBound" },
    @{ file="studio/scenes/part04/p04_s08_quantv2x.py";           cls="P04S08QuantV2X" },
    @{ file="studio/scenes/part04/p04_s09_efficiency_summary.py"; cls="P04S09EfficiencySummary" },
    @{ file="studio/scenes/part04/p04_s10_bridge_to_p5.py";       cls="P04S10BridgeToP5" },
    # Part 05
    @{ file="studio/scenes/part05/p05_s01_title.py";              cls="P05S01Title" },
    @{ file="studio/scenes/part05/p05_s02a_llm_vs_robot.py";      cls="P05S02ALLMVsRobot" },
    @{ file="studio/scenes/part05/p05_s02b_two_barriers.py";      cls="P05S02BTwoBarriers" },
    @{ file="studio/scenes/part05/p05_s03_micromobility.py";      cls="P05S03Micromobility" },
    @{ file="studio/scenes/part05/p05_s04a_compositional_quote.py"; cls="P05S04ACompositionalQuote" },
    @{ file="studio/scenes/part05/p05_s04b_metaurban.py";         cls="P05S04BMetaUrban" },
    @{ file="studio/scenes/part05/p05_s04c_metaurban_scaling.py"; cls="P05S04CMetaUrbanScaling" },
    @{ file="studio/scenes/part05/p05_s05a_urbansim_bottleneck.py"; cls="P05S05AUrbanSimBottleneck" },
    @{ file="studio/scenes/part05/p05_s05b_urbansim_results.py";  cls="P05S05BUrbanSimResults" },
    @{ file="studio/scenes/part05/p05_s06a_citywalker.py";        cls="P05S06ACityWalker" },
    @{ file="studio/scenes/part05/p05_s06b_pedgen.py";            cls="P05S06BPedGen" },
    @{ file="studio/scenes/part05/p05_s07_zombie_to_alive.py";    cls="P05S07ZombieToAlive" },
    @{ file="studio/scenes/part05/p05_s08_vid2sim.py";            cls="P05S08Vid2Sim" },
    @{ file="studio/scenes/part05/p05_s09_living_city.py";        cls="P05S09LivingCity" },
    @{ file="studio/scenes/part05/p05_s10_chain_of_solutions.py"; cls="P05S10ChainOfSolutions" },
    @{ file="studio/scenes/part05/p05_s11_final_frame.py";        cls="P05S11FinalFrame" }
)

$total = $scenes.Count
$ok    = 0
$fail  = 0

foreach ($s in $scenes) {
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "[$ts] Rendering $($s.cls) ..." -ForegroundColor Cyan
    $out = & $MANIM -w @QUALITY_ARGS $s.file $s.cls 2>&1
    if ($LASTEXITCODE -eq 0) {
        $ok++
        Write-Host "  OK" -ForegroundColor Green
        "[$ts] OK  $($s.cls)" | Out-File $LOG -Append -Encoding utf8
    } else {
        $fail++
        Write-Host "  FAIL" -ForegroundColor Red
        "[$ts] FAIL $($s.cls)" | Out-File $LOG -Append -Encoding utf8
        ($out | Select-String "Error|Traceback|rror" | Select-Object -First 5) | Out-File $LOG -Append -Encoding utf8
    }
}

Write-Host ""
Write-Host "Done: $ok OK / $fail FAIL out of $total scenes." -ForegroundColor Yellow
"DONE: $ok OK / $fail FAIL / $total total" | Out-File $LOG -Append -Encoding utf8
