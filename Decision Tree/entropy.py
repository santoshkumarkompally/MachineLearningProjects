'''
Created on Sep 11, 2016

@author: SantoshKompally
'''
import math
def calculateEntropy(a):
    result = 0
    # if loop is written the case in which temp is 0. In that case 1/temp will return exception.
    for temp in a:
        if temp == 0:
            result = result + 0
        else:    
            result = result + temp * math.log((1 / temp), 2)
        
    return result    


a=[0.666,0.333]
print(calculateEntropy(a))