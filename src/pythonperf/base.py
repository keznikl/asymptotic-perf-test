import time
import re
import sys


def plot_times(func, generate_args, plot_sequence):
  return [
    (n, measure_run_time(func, generate_args(n+1)))
    for n in plot_sequence
  ]


class Factor:
    pass

class ArgLenFactor(Factor):
    def __init__(self, idx=0):
        self.idx = idx
    def __call__(self, *args, **kwargs):
        return len(args[self.idx])

class PerformanceFunctor:
    def __init__(self, f, factor=None, scale=None):
        self.f = f
        self.lower = 1000
        self.upper = 5000
        self.step = 1000
        self.factor = factor
        self.scale = scale
        self.upper_scale = None
        self.multiply_scale = None
        self.lower_scale = None
        if scale is not None:
            m = re.match('\s*O\((\d+)\)\s*<\s*(\d+)\s*\*\s*O\((\d+)\)\s*', scale)
            if m is not None:
                self.upper_scale = int(m.group(1))
                self.multiply_scale = int(m.group(2))
                self.lower_scale = int(m.group(3))
                #sys.stderr.write("Performance scale: upper scale %d, lower scale %d, multiplier %d\n" % (
                #                 self.upper_scale, self.lower_scale, self.multiply_scale))
            else:
                raise Exception("The given scale strinf does not match any supported format")

    def measure_run_time(self, args):
        #print "Calling function %s\n" % self.f
        start = time.clock()
        self.f(*args)
        duration = time.clock() - start
        #print "Call finished in %f seconds\n" % duration
        return duration

    def test_sequence(self, input_generator):
        input_sizes = xrange(self.lower,self.upper,self.step)
        times = [
            self.measure_run_time(input_generator(n+1))
            for n in input_sizes
        ]
        return False

    def test_scale(self, input_generator):
        if self.lower_scale is None or self.upper_scale is None or self.multiply_scale is None:
            return False
        res_lower = self.measure_run_time(input_generator(self.lower_scale))
        res_upper = self.measure_run_time(input_generator(self.upper_scale))
        max_upper = self.multiply_scale * res_lower
        ret = res_upper < max_upper
        if not ret:
            sys.stderr.write("Scale test '%s' for '%s' failed, max for upper bound: %f, measured: %f\n"
                             % (self.scale, self.f.__name__, max_upper, res_upper))
        else:
            print "Scale test '%s' for '%s' passed" % (self.scale, self.f.__name__)
        return ret
    def __call__(self, *args, **kwargs):
        self.f(args, kwargs)

class Performance:
    def __init__(self,scale=None, factor=None):
        self.factor = factor
        self.scale = scale
    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        return PerformanceFunctor(f, scale=self.scale, factor=self.factor)

