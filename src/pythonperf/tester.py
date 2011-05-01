from pythonperf.base import PerformanceFunctor, measure_run_time
import matplotlib
matplotlib.use('GTKAgg')
from pylab import get_current_fig_manager, subplot, plot, legend, connect, show

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

class IterationTester(Tester):
    sample_cnt = 100
    times = None
    input_sizes = None

    @classmethod
    def test_functor(cls, functor, input_generator):
        if functor is None or not hasattr(functor, 'scale') or functor.scale is None:
            return False
        scale = functor.scale
        step_size = max(1, int((scale.upper_scale - scale.lower_scale) / cls.sample_cnt))
        cls.input_sizes = xrange(scale.lower_scale,scale.upper_scale,step_size)
        cls.times = [
            measure_run_time(functor, input_generator(n))
            for n in cls.input_sizes
        ]

class RegressionTester(IterationTester):
    @classmethod
    def test_scale(cls, functor, input_generator):
        cls.test_functor(functor, input_generator)
        return True

class GraphTester(IterationTester):
    @classmethod
    def create_tool_btn(cls, label, tooltip, fnc, toolbar, position):
        import gtk
        button = gtk.Button(label)
        button.show()
        button.connect('clicked', fnc)

        toolitem = gtk.ToolItem()
        toolitem.show()
        toolitem.set_tooltip(
            toolbar.tooltips,
            tooltip)
        toolitem.add(button)

        toolbar.insert(toolitem, position)

    @classmethod
    def test_scale(cls, functor, input_generator):
        cls.test_functor(functor, input_generator)
        plot(cls.input_sizes, cls.times)

        manager = get_current_fig_manager()
        # you can also access the window or vbox attributes this way
        toolbar = manager.toolbar

        def confirm_clicked(button):
            print 'Confirmed'
        def discard_clicked(button):
            print 'Discarded'

        next = 8; #where to insert this in the mpl toolbar
        cls.create_tool_btn("Confirm", "Click to confirm the performance data", confirm_clicked, toolbar, next)
        next +=1
        cls.create_tool_btn("Discard", "Click to discard the performance data", discard_clicked, toolbar, next)

        show()
        return True