from pythonperf.base import PerformanceFunctor

class Tester:
    pass

class ScaleTester(Tester):
    @classmethod
    def test_scale(cls, functor, input_generator):
        if functor is None or not hasattr(functor, 'scale') or functor.scale is None:
            return False
        scale = functor.scale
        result = scale.test_scale(functor, input_generator)
        if isinstance(functor.get_function(), PerformanceFunctor):
            result = result and cls.test_scale(functor.get_function(), input_generator)
        return result