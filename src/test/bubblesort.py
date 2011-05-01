from pythonperf.base import Performance, ArgLenFactor, measure_run_time
import random
import unittest
from pythonperf.tester import ScaleTester, RegressionTester, GraphTester, GraphTester

@Performance(factor=ArgLenFactor(0), scale="O(1000) < 1000 * O(100)")
def bubble_sort(l):
    for i in xrange(len(l)-1):
        for j in xrange(len(l)-1-i):
            if l[i+1] < l[i]:
                l[i],l[i+1] = l[i+1],l[i]



def gen_args_for_sort(list_length):
    result = range(list_length) # list of 0..N-1
    random.shuffle(result) # randomize order
    # should return a tuple of arguments
    return (result,)


class BubbleTest(unittest.TestCase):
    def testBubbleScale(self):
        self.assertTrue(ScaleTester.test_scale(bubble_sort, gen_args_for_sort), "The bubble sort perf test failed")
    def testBubbleRegression(self):
        self.assertTrue(RegressionTester.test_scale(bubble_sort, gen_args_for_sort), "The bubble sort regressions test failed")
    def testBubbleGraph(self):
        self.assertTrue(GraphTester.test_scale(bubble_sort, gen_args_for_sort), "The bubble sort regressions test failed")

if __name__ == '__main__':
    unittest.main()
