import numpy as np
import itertools as it
from copy import deepcopy
import sys
from manim_imports_ext import *
from script_wrapper import command_line_create_scene
from .inventing_math import divergent_sum, draw_you

class SimpleText(Scene):
    args_list = [('Build the foundation of what we know',), ('What would that feel like?',), ('Arbitrary decisions hinder generality',), ('Section 1: Discovering and Defining Infinite Sums',), ('Section 2: Seeking Generality',), ('Section 3: Redefining Distance',), ("``Approach''?",), ('Rigor would dictate you ignore these',), ('dist($A$, $B$) = dist($A+x$, $B+x$) \\quad for all $x$',), ('How does a useful distance function differ from a random function?',), ('Pause now, if you like, and see if you can invent your own distance function from this.',), ('$p$-adic metrics \\\\ ($p$ is any prime number)',), ('This is not meant to match the history of discoveries',)]

    @staticmethod
    def args_to_string(text):
        return initials([c for c in text if c in string.letters + ' '])

    def construct(self, text):
        self.add(OldTexText(text))

class SimpleTex(Scene):
    args_list = [('\\frac{9}{10}+\\frac{9}{100}+\\frac{9}{1000}+\\cdots = 1', 'SumOf9s'), ('0 < p < 1', 'PBetween0And1')]

    @staticmethod
    def args_to_string(expression, words):
        return words

    def construct(self, expression, words):
        self.add(OldTex(expression))

class OneMinusOnePoem(Scene):

    def construct(self):
        verse1 = OldTexText("\n            \\begin{flushleft}\n            When one takes one from one  \\\\\n            plus one from one plus one \\\\\n            and on and on but ends  \\\\\n            anon then starts again, \\\\\n            then some sums sum to one, \\\\\n            to zero other ones. \\\\\n            One wonders who'd have won \\\\\n            had stopping not been done; \\\\\n            had he summed every bit \\\\\n            until the infinite. \\\\\n            \\end{flushleft}\n        ").scale(0.5).to_corner(UP + LEFT)
        verse2 = OldTexText("\n            \\begin{flushleft}\n            Lest you should think that such \\\\\n            less well-known sums are much \\\\\n            ado about nonsense \\\\\n            I do give these two cents: \\\\\n            The universe has got \\\\\n            an answer which is not \\\\\n            what most would first surmise, \\\\\n            it is a compromise, \\\\\n            and though it seems a laugh \\\\\n            the universe gives ``half''. \\\\\n            \\end{flushleft}\n        ").scale(0.5).to_corner(DOWN + LEFT)
        equation = OldTex('1-1+1-1+\\cdots = \\frac{1}{2}')
        self.add(verse1, verse2, equation)

class DivergentSum(Scene):

    def construct(self):
        self.add(divergent_sum().scale(0.75))

class PowersOfTwoSmall(Scene):

    def construct(self):
        you, bubble = draw_you(with_bubble=True)
        bubble.write('Is there any way in which apparently             large powers of two can be considered small?')
        self.add(you, bubble, bubble.content)

class FinalSlide(Scene):

    def construct(self):
        self.add(OldTexText("\n            \\begin{flushleft}\n            Needless to say, what I said here only scratches the \n            surface of the tip of the iceberg of the p-adic metric.  \n            What is this new form of number I referred to?\n            Why were distances in the 2-adic metric all powers of \n            $\\frac{1}{2}$ and not some other base?\n            Why does it only work for prime numbers? \\\\\n            \\quad \\\\\n            I highly encourage anyone who has not seen p-adic numbers\n            to look them up and learn more, but even more edifying than\n            looking them up will be to explore this idea for yourself directly.\n            What properties make a distance function useful, and why?\n            What do I mean by ``useful''?  Useful for what purpose?\n            Can you find infinite sums or sequences which feel like\n            they should converge in the 2-adic metric, but don't converge \n            to a rational number? Go on!  Search!  Invent!\n            \\end{flushleft}\n        ", size='\\small'))