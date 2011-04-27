import time
import re
import sys


def plot_times(func, generate_args, plot_sequence):
  return [
    (n, measure_run_time(func, generate_args(n+1)))
    for n in plot_sequence
  ]


def measure_run_time(f, args):
    start = time.clock()
    f(*args)
    duration = time.clock() - start
    return duration

class Factor:
    pass


class ArgLenFactor(Factor):
    def __init__(self, idx=0):
        self.idx = idx
    def __call__(self, *args, **kwargs):
        return len(args[self.idx])


class Scale:
    def test_scale(self, f, input_generator):
        """
        Returns True if the methods meets the scale requirements.
        """
        pass

    @classmethod
    def create(cls, scale):
        """
        Factory method. Returns None if the given string does not match this scale type.
        """
        return None


class ComparisonScale(Scale):
    regexp = '\s*O\((\d+)\)\s*<\s*(\d+)\s*\*\s*O\((\d+)\)\s*'

    def __init__(self, scale_str, upper_scale, lower_scale, multiply_scale):
        self.upper_scale = upper_scale
        self.multiply_scale = multiply_scale
        self.lower_scale = lower_scale
        self.scale_str = scale_str

    @classmethod
    def create(cls, scale):
        m = re.match(cls.regexp, scale)
        if m is not None:
            return ComparisonScale(
                scale_str = scale,
                upper_scale = int(m.group(1)),
                multiply_scale = int(m.group(2)),
                lower_scale = int(m.group(3))
            )
        else:
            return None

    def test_scale(self, f, input_generator):
        if self.lower_scale is None or self.upper_scale is None or self.multiply_scale is None:
            return False

        res_lower = measure_run_time(f, input_generator(self.lower_scale))
        res_upper = measure_run_time(f, input_generator(self.upper_scale))
        max_upper = self.multiply_scale * res_lower
        ret = res_upper < max_upper

        if not ret:
            sys.stderr.write("Scale test '%s' for '%s' failed, max for upper bound: %f, measured: %f\n"
                             % (self.scale_str, f.__name__, max_upper, res_upper))
        else:
            print "Scale test '%s' for '%s' passed" % (self.scale_str, f.__name__)

        return ret


class ScaleFactory:
    scales = [ComparisonScale]

    @classmethod
    def get_scale(cls, scale):
        """
        Returns the scale object for the given scale string.
        """
        for s in cls.scales:
            instance = s.create(scale)
            if instance is not None:
                return instance
        return None


class PerformanceFunctor:
    def __init__(self, f, factor=None, scale=None):
        self.f = f
        self.scale = ScaleFactory.get_scale(scale)

    def test_sequence(self, input_generator):
        input_sizes = xrange(self.lower,self.upper,self.step)
        times = [
            self.measure_run_time(input_generator(n+1))
            for n in input_sizes
        ]
        return False

    def test_scale(self, input_generator):
        if self.scale is None:
            return False
        result = self.scale.test_scale(self.f, input_generator)
        if hasattr(self.f, 'test_scale'):
            result = result and self.f.test_scale(input_generator)
        return result

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

