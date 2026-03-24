# 3D Mobjects Reference

Manim supports 3D animations using the `ThreeDScene` and specialized 3D mobjects.

## Core Scene

### `ThreeDScene`
- **Methods**:
    - `set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)`: Sets the initial 3D view.
    - `begin_ambient_camera_rotation(rate=0.1)`: Slowly rotates the camera.
    - `move_camera(phi, theta, distance, frame_center, added_anims)`: Animates camera movement.

## 3D Shapes

### Basic Objects
- `Sphere(radius=1, resolution=(32, 32))`
- `Cube(side_length=2)`
- `Prism(dimensions=[3, 2, 1])`
- `Cone(base_radius=1, height=2)`
- `Cylinder(radius=1, height=2)`
- `Torus(major_radius=3, minor_radius=1)`
- `Line3D(start, end)`

### Surfaces
- `Surface(func, u_range=[0, 1], v_range=[0, 1])`: Parametric surface.
- `ParametricSurface`: Alias for Surface.

## 3D Specific Methods
- `rotate_about_origin(angle, axis)`
- `set_shade_in_3d(True)`: Enables proper depth sorting for some renderers.
