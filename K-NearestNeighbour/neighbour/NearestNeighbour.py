'''
Created on Oct 15, 2016

@author: SantoshKompally
'''

try:
    import Queue as Q  
    import numpy as np
    import copy
    import math
    import datetime
except ImportError:
    print("problem with importing the queue or numpy or copy.")


class Item():
    def __init__(self, attributes, target):
        self.attributes = attributes
        self.target = target
        self.distance = 0
        
    def __cmp__(self, other):
        if self.distance != other.distance:
            return self.distance - other.distance
        else:
# since the weights are same then we might have a plus or minus, both plus or both minus.
            
            if self.target == '-' :
                return -1
            elif self.target == '+' :
                return 1
            
    def getDistance(self):
        return self.distance
    
    def getAttributes(self):
        return self.attributes
    
    def targ(self):
        return self.target
    def calcDistance(self, otherAttribues):
        self.distance = 0
        for i in range(len(self.attributes)):
            self.distance = self.distance + (self.attributes[i] - otherAttribues[i]) * (self.attributes[i] - otherAttribues[i])
        
        return self.distance

def errorForeachShuffle_new(shuffledData, kFold, closestNeighbor, numberOfExamples):
    
    finalSummationsOfAllFolds = []
    sumOfErrors = []
    if  ((len(shuffledData)%kFold)/float(kFold))  > 0.5 :
        number_of_elements= int(len(shuffledData)/kFold) + 1
    else:         
        number_of_elements= int(len(shuffledData)/kFold)
    count = 0;
    for i in range(kFold):
        trainingSet = []
        testSet = []
        error = []
        if(i < kFold -1 ):
            for j in range(len(shuffledData)):
            
                if j >= count and j < (count + number_of_elements):
                    testSet.append(shuffledData[j])
                else:
                    trainingSet.append(shuffledData[j])  
        
        else:
            for j in range(len(shuffledData)):
                
                if j >= (kFold-1)*number_of_elements:
                    testSet.append(shuffledData[j])
                else :  
                    trainingSet.append(shuffledData[j])  
                    
        count = count + number_of_elements ;
        trainingSet_local = copy.deepcopy(trainingSet)
        test_set_local = copy.deepcopy(testSet)
#         print "test set" 
#         for temp in test_set_local:
#             print temp.attributes
        
        matrixOfErrors = calculateError(trainingSet_local, test_set_local, closestNeighbor)
        for k in range(closestNeighbor):
            error.append(sum(matrixOfErrors[:, k]))
        sumOfErrors.append(error)    
     
#    print np.array(sumOfErrors) 
    
    sumOfErrors = np.array(sumOfErrors)
    
    for i in range(closestNeighbor):
        finalSummationsOfAllFolds.append(sum(sumOfErrors[:, i]) / float(numberOfExamples))
    
#     print np.array(finalSummationsOfAllFolds)
    return finalSummationsOfAllFolds
    


def readInputFile(fileName):
    output = []
    outputdict = {}
    key = 0
    with open(fileName, "r") as f:
        numberOfInputs, numberOfAttributes = f.readline().split()
        
        for i in range(int(numberOfInputs)):
            inputs = f.readline().split()
            for j in range(int(numberOfAttributes)):
                if inputs[j] != '.':
                    output.append(Item([j, i], inputs[j]))
                    outputdict[key] = Item([j, i], inputs[j])
                    key = key + 1
    return output, outputdict
    


def  calculateMatrix(fileName, numberOfMatrices):
    
    with open(fileName, "r") as f:
        
        givenInputs, dictInputs = readInputFile(fileName)
        numberOfInputs, numberOfAttributes = f.readline().split()
        arr = [[[0 for t1 in xrange(int(numberOfAttributes))] for t2 in xrange(int(numberOfInputs))] for t3 in xrange(int(numberOfMatrices))]
        for i in range(int(numberOfInputs)):
            inputs = f.readline().split()
            for j in range(int(numberOfAttributes)):
                
               
                pq = Q.PriorityQueue();
# the major problem here is the input set is being red again and again.
# deep copy is used here. Please take a note of this.             
                givenInputs1 = copy.deepcopy(givenInputs)
                if inputs[j] == '.':
                    for inp in givenInputs1:
                        inp.calcDistance([j, i])
                    for inp in givenInputs1:
                        pq.put(inp);
                        
# the count variable maintains the final output for each set whether positive or negative.                    
                count = 0
                for k in range(numberOfMatrices):
# the logic for finding the closest neighbors is taken care here.
# there should not be a problem with the data being updated simultaneously because we are using input from data set.
# to calculate the distance. 
                    if inputs[j] == '.':
                        t = pq.get()
                       
                        if(t.target == '+'):
                            count = count + 1
                        else:
                            count = count - 1
                                    
                        if count > 0:
                           
                            arr[k][i][j] = '+'
                        else:
                            arr[k][i][j] = '-'
                    else:
                        arr[k][i][j] = inputs[j];
                        
    return arr
    

# training set will contain the training examples.
# test set will give us the test examples.
# kcloset will be used to determine the closest value in testing set.

def error1(trainingSet, testingSet, kclosest):
# is the training set list of Items other wise we give a error and terminate the code. How to do this?
    error = 0
    for testingExample in testingSet:
    
        pq = Q.PriorityQueue()
        for item in trainingSet:
            item.calcDistance(testingExample.getAttributes())
            pq.put(item)
        k = kclosest
        counter = 0
        while k > 0 and pq.not_empty :
            s = pq.get()  
            if s.target == '-':
                counter = counter - 1
            else:
                counter = counter - 1
                
        if counter > 0 and testingExample.target == '+':
            error = error + 1  
        if counter <= 0 and testingExample.target == '+':
            error = error + 1         
                    
    return error



# shuffle data in the required format.
def shuffled(data, order, numberOfExamples):
    data_local = copy.deepcopy(data)
    local_order = copy.deepcopy(order)
    list1 = []
    for i in range(int(numberOfExamples)):
        list1.append(data_local[int(local_order[i])])
    return list1   

# we have the output from reading the second file. 
# we read the first file and call the error functions needed.       
def findVariance(fileName, output_dict, numberOfNeighbors):
     
    sum1 = []
    small_e = []
    variance = []
    with open(fileName, 'r') as f:
         
        kfold, numberOfExamples, numberOfShuffles = f.readline().split()
        for i in range(int(numberOfShuffles)):
            order = f.readline().split()
            shuffledData = (shuffled(output_dict, order, numberOfExamples))
            sum1.append(errorForeachShuffle_new(shuffledData, int(kfold), numberOfNeighbors, numberOfExamples))
    sum1 = np.array(sum1)        
#    print(sum1) 
    # calculate the sum of all errors.
    for i in range(numberOfNeighbors):
        small_e.append(np.sum(sum1[:, i]) / float(numberOfShuffles));
      
#     print("value of small e:")    
#     print small_e
    
# calculating (Ej - e)^2
    for i in range(int(numberOfShuffles)):
        for j in range(numberOfNeighbors):
            sum1[i][j] = ((sum1[i][j] - small_e[j]) * (sum1[i][j] - small_e[j]))   
        
#     print sum1        
    for i in range(int(numberOfNeighbors)):
        variance.append(math.sqrt(np.sum(sum1[:, i]) / float((int(numberOfShuffles) - 1))))
        
#     print "variance is:"
#     print variance    
    return small_e, variance 
        



def errorForeachShuffle(shuffledData, kFold, closestNeighbor, numberOfExamples):
    
    finalSummationsOfAllFolds = []
    sumOfErrors = []
    numberToBeAdded = 0
    if len(shuffledData) % kFold != 0:
        numberToBeAdded = kFold - (len(shuffledData) % kFold)
    sizeOfEachSegment = (len(shuffledData) + numberToBeAdded) / kFold  
    count = 0;
    for i in range(kFold):
        trainingSet = []
        testSet = []
        error = []
        for j in range(len(shuffledData)):
            if j >= count and j < (count + sizeOfEachSegment):
                testSet.append(shuffledData[j])
            else:
                trainingSet.append(shuffledData[j])
        
    
        count = count + sizeOfEachSegment ;  
        trainingSet_local = copy.deepcopy(trainingSet)
        test_set_local = copy.deepcopy(testSet) 
        
#         for temp in testSet:
#             print temp.attributes
        
        matrixOfErrors = calculateError(trainingSet_local, test_set_local, closestNeighbor)
        for k in range(closestNeighbor):
            error.append(sum(matrixOfErrors[:, k]))
        sumOfErrors.append(error)    
     
#    print np.array(sumOfErrors) 
    
    sumOfErrors = np.array(sumOfErrors)
    
    for i in range(closestNeighbor):
        finalSummationsOfAllFolds.append(sum(sumOfErrors[:, i]) / float(numberOfExamples))
    
#     print np.array(finalSummationsOfAllFolds)
    return finalSummationsOfAllFolds
    



    



# training set and test set are arrays of Item objects. 
# for Item class please refer to the top. 
def calculateError(trainingSet, testSet, numberOfClosestNeighbors):
    error = []
    for example in testSet:
        count = 0
        list_local = []
        pq = Q.PriorityQueue()
        for eachTrainingExample in trainingSet:
            eachTrainingExample.calcDistance(example.attributes)
            list_local.append(eachTrainingExample);
            pq.put(eachTrainingExample)
        sorted(list_local);
       
        localError = []
        for k in range(numberOfClosestNeighbors):
            
            if  not pq.empty():
                a = pq.get()
                if a.targ() == "-" :
                    count = count - 1
                else:
                    count = count + 1    
            
            if (count > 0 and example.targ() == "+")  or (count <= 0 and example.targ() == "-") :
                localError.append(0)
            else:
                localError.append(1)    
                 
        error.append(localError)  
#    print np.array(error)    
    return np.array(error) 






# number of neighbors is set to 5.
numberOfNearestNeighbors = 5
matrix = calculateMatrix("test3-2.txt", numberOfNearestNeighbors);
output, outputdict = readInputFile("test3-2.txt");
small_e, variance = findVariance("test3-1.txt", outputdict, numberOfNearestNeighbors)
print(datetime.datetime.now())
for k in range(numberOfNearestNeighbors):
    print "nearest neighbor: %s" % (k + 1)
    print np.array(matrix[k])
    print "value of e: %s" % (small_e[k]) 
    print "value of Sigma: %s" % (variance[k]) 
    print("\n")
print(datetime.datetime.now())   
    
    



