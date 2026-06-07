import inspect
import os
import sys
import importlib
from manimlib.config import get_module
from manimlib.extract_scene import is_child_scene

def get_sorted_scene_classes(module_name):
    module = get_module(module_name)
    if hasattr(module, 'SCENES_IN_ORDER'):
        return module.SCENES_IN_ORDER
    importlib.import_module(module.__name__)
    line_to_scene = {}
    name_scene_list = inspect.getmembers(module, lambda obj: is_child_scene(obj, module))
    for name, scene_class in name_scene_list:
        if inspect.getmodule(scene_class).__name__ != module.__name__:
            continue
        lines, line_no = inspect.getsourcelines(scene_class)
        line_to_scene[line_no] = scene_class
    return [line_to_scene[index] for index in sorted(line_to_scene.keys())]

def stage_scenes(module_name):
    scene_classes = get_sorted_scene_classes(module_name)
    if len(scene_classes) == 0:
        print('There are no rendered animations from this module')
        return
    animation_dir = os.path.join(os.path.expanduser('~'), 'Dropbox/3Blue1Brown/videos/2021/holomorphic_dynamics/videos')
    files = os.listdir(animation_dir)
    sorted_files = []
    for scene_class in scene_classes:
        scene_name = scene_class.__name__
        clips = [f for f in files if f.startswith(scene_name + '.')]
        for clip in clips:
            sorted_files.append(os.path.join(animation_dir, clip))
    count = 0
    while True:
        staged_scenes_dir = os.path.join(animation_dir, os.pardir, 'staged_scenes_{}'.format(count))
        if not os.path.exists(staged_scenes_dir):
            os.makedirs(staged_scenes_dir)
            break
        count += 1
    for count, f in reversed(list(enumerate(sorted_files))):
        symlink_name = os.path.join(staged_scenes_dir, 'Scene_{:03}_{}'.format(count, f.split(os.sep)[-1]))
        os.symlink(f, symlink_name)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('No module given.')
    module_name = sys.argv[1]
    stage_scenes(module_name)