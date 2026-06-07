# Merge videos
$videoDir = "C:\Users\admin\Downloads\ML\Lab01_3B1B\drivex\media\videos"
$outputDir = "C:\Users\admin\Downloads\ML\Lab01_3B1B\drivex\media\videos\FINAL"
$resolution = "1080p15"

New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

$sceneOrder = "i01_title_card","i02_hook","i03_roadmap","p01_s01_opening","p01_s02_genai_boom","p01_s03_av_arch"

$concatFile = "$outputDir\concat_list.txt"
$concatContent = ""

foreach ($scene in $sceneOrder) {
    $videoPath = "$videoDir\$scene\$resolution"
    $mp4Files = @(Get-ChildItem $videoPath -Filter "*.mp4" -ErrorAction SilentlyContinue)
    if ($mp4Files.Count -gt 0) {
        $firstFile = $mp4Files[0].FullName
        $concatContent += "file '$firstFile'`n"
        Write-Host "OK: $scene"
    }
}

Set-Content -Path $concatFile -Value $concatContent
Write-Host "Merging with ffmpeg..."

$outputVideo = "$outputDir\WhiteTheme_Final.mp4"
& ffmpeg -f concat -safe 0 -i $concatFile -c copy -y $outputVideo 2>&1 | tail -5

if (Test-Path $outputVideo) {
    $size = (Get-Item $outputVideo).Length / 1MB
    Write-Host "DONE: $([Math]::Round($size, 2)) MB" -ForegroundColor Green
}
