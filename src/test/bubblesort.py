import math
from pythonperf.base import Performance, ArgLenFactor
#from pylab import plot, show
import random
import unittest

@Performance(factor=ArgLenFactor(0), scale="O(1000) < 100 * O(100)")
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
        self.assertTrue(bubble_sort.test_scale(gen_args_for_sort), "The bubble sort perf test failed")

#if __name__ == '__main__':
#    unittest.main()

#times = xrange(1000,6000,100)
#values = plot_times(bubble_sort, gen_args_for_sort, times)
#plot(times, [time for (num, time) in values])                                                                                  -
#show()
