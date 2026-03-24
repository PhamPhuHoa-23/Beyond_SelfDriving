# FAQ & Troubleshooting

Common questions and solutions for Manim Community.

## General Usage

### Why does Manim say "there are no scenes inside that module"?
- Ensure your class inherits from `Scene` (e.g., `class MyScene(Scene):`).
- Check if you are pointing to the correct file in the CLI.

### Why is the output just a black frame?
- You must define a `construct()` method.
- You must use `self.play()` or `self.add()` to put objects on screen.

### Transparent Background
- Use the `-t` or `--transparent` flag in the CLI.
- Note: This only works with certain file formats like MOV or standard PNG sequences.

### LaTeX Errors
- Ensure MiKTeX or TeX Live is installed and in your PATH.
- If characters are missing, try clearing the `media/Tex` cache folder.

## Learning Resources
- [Manim Discord](https://discord.gg/mMRrgeS)
- [Manim Reddit](https://www.reddit.com/r/manim/)
- [Theorem of Beethoven (YouTube)](https://www.youtube.com/c/TheoremofBeethoven)
