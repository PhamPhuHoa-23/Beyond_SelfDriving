# Advanced Configuration & CLI

Manim can be configured via CLI flags, environment variables, or a `manim.cfg` file.

## CLI Flags (Render Command)

### Quality
- `-ql`, `--low_quality`: 480p, 15fps.
- `-qm`, `--medium_quality`: 720p, 30fps.
- `-qh`, `--high_quality`: 1080p, 60fps.
- `-qk`, `--fourk_quality`: 2160p, 60fps.

### Output Control
- `-p`, `--preview`: Automatically opens the video after rendering.
- `-f`, `--show_in_file_browser`: Opens the folder containing the video.
- `-s`, `--save_last_frame`: Saves only the final frame as an image.
- `-o OUT`, `--output_file OUT`: Sets a custom filename.

### Miscellaneous
- `-t`, `--transparent`: Renders with transparency.
- `-n START,END`, `--from_animation_number START,END`: Renders only a specific range of animations.

## Configuration Files (`manim.cfg`)
You can create a `manim.cfg` file in your project root to set defaults.
```ini
[CLI]
quality = m
preview = True
background_color = #ece6ff
```

## Environment Variables
- `MANIM_PLUGINS`: Path to plugins.
- `MANIM_CONFIG_FILE`: Path to a global config file.
