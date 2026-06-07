# Background QA loop: render + extract frames for studio scenes (Part 01 default).
# Logs: studio/_qa_loop/manifest.jsonl
# Frames: studio/_qa_loop/frames/<ClassName>/

param(
    [string]$Part = "01",
    [string]$From = "",
    [string]$Only = ""
)

$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"
Set-Location "C:\Users\admin\Downloads\ML\Lab01_3B1B"

$args = @("scripts/scene_qa_loop.py", "--part", $Part)
if ($From) { $args += @("--from", $From) }
if ($Only) { $args += @("--only", $Only) }

& python @args 2>&1 | Tee-Object -FilePath "studio\_qa_loop\last_run.log"
