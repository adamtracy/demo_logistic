#!/usr/bin/env python

"""
Logistic Equation Calculator

See: https://en.wikipedia.org/wiki/Logistic_map

Xn+1 = R*Xn(1-Xn)
where Xn is a number between zero and one that represents the ratio of existing population
to the maximum possible population. The values of interest for the parameter
R are those in the interval 0,4

"""

import numpy
import itertools
import json


class LogisticEquation:

    # each datapoint is plotted with a circle where r=1px.  The default window port size is 900x400
    def __init__(self,
                 num_iterations=10,
                 num_buckets=450,
                 r_min=2.5,
                 r_max=4.0,
                 x_min=0.0,
                 x_max=1.0):
        self.num_iterations = num_iterations
        # num_buckets is the number of positions for graphing across the values
        # of Rho.  Since there's 2pixels per circle in the plot, and the svg width
        # is hardcoded to 900, that's 450.
        self.num_buckets = num_buckets
        self.r_min = r_min
        self.r_max = r_max
        self.x_min = x_min
        self.x_max = x_max
        self.plot = list()

    @staticmethod
    def logistic(r, x):
        return r * (x * (1-x))

    def calc(self):
        # seed the calculation with a basic starting point.
        x = self.logistic(self.r_min, 0.5)
        # Divide Rho into the number of buckets and calculate a series of X values at
        # each position.  I try to capture up to num_iterations' worth of data points for
        # each Rho value to have a reasonably consistent data density.  I only run through the
        # iteration loop up to 5 times, though, so I guess when you zoom in really far,
        # you might end up with nothing.
        for r in numpy.arange(self.r_min, self.r_max, (self.r_max - self.r_min) / self.num_buckets):
            points = list()
            for _ in itertools.repeat(None, 5):
                for n in itertools.repeat(None, self.num_iterations):
                    x = self.logistic(r, x)
                    # check to see if x is in range of x_min/max
                    if self.x_min <= x <= self.x_max:
                        points.append([r, x])
                if len(points) >= self.num_iterations:
                    break
            self.plot.extend(points)


if __name__ == '__main__':
    lc = LogisticEquation(r_min=3.5,
                          r_max=3.6,
                          x_min=0.7,
                          x_max=0.9)
    lc.calc()
    print(json.dumps(lc.plot))

