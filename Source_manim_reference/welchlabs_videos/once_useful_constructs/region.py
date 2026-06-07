from copy import deepcopy
import itertools as it
from manimlib.constants import *
from manimlib.mobject.mobject import Mobject
from manimlib.utils.iterables import adjacent_pairs

class Region(Mobject):
    CONFIG = {'display_mode': 'region'}

    def __init__(self, condition=lambda x, y: True, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.condition = condition

    def _combine(self, region, op):
        self.condition = lambda x, y: op(self.condition(x, y), region.condition(x, y))

    def union(self, region):
        self._combine(region, lambda bg1, bg2: bg1 | bg2)
        return self

    def intersect(self, region):
        self._combine(region, lambda bg1, bg2: bg1 & bg2)
        return self

    def complement(self):
        self.bool_grid = ~self.bool_grid
        return self

class HalfPlane(Region):

    def __init__(self, point_pair, upper_left=True, *args, **kwargs):
        if not upper_left:
            point_pair = list(point_pair)
            point_pair.reverse()
        (x0, y0), (x1, y1) = (point_pair[0][:2], point_pair[1][:2])

        def condition(x, y):
            return (x1 - x0) * (y - y0) > (y1 - y0) * (x - x0)
        Region.__init__(self, condition, *args, **kwargs)

def region_from_line_boundary(*lines, **kwargs):
    reg = Region(**kwargs)
    for line in lines:
        reg.intersect(HalfPlane(line, **kwargs))
    return reg

def region_from_polygon_vertices(*vertices, **kwargs):
    return region_from_line_boundary(*adjacent_pairs(vertices), **kwargs)

def plane_partition(*lines, **kwargs):
    result = []
    half_planes = [HalfPlane(line, **kwargs) for line in lines]
    complements = [deepcopy(hp).complement() for hp in half_planes]
    num_lines = len(lines)
    for bool_list in it.product(*[[True, False]] * num_lines):
        reg = Region(**kwargs)
        for i in range(num_lines):
            if bool_list[i]:
                reg.intersect(half_planes[i])
            else:
                reg.intersect(complements[i])
        if reg.bool_grid.any():
            result.append(reg)
    return result

def plane_partition_from_points(*points, **kwargs):
    lines = [[p1, p2] for p1, p2 in it.combinations(points, 2)]
    return plane_partition(*lines, **kwargs)