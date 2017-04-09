'''
Created on Nov 27, 2016

@author: SantoshKompally
'''
import operator
import math
import numpy as np
import Utility as ut

   
# when passed a position and output array it will consider both the side as mentioned in the parameter.
# greater than or equal to the above number is considered as negative and vice versa.         
def error(output_array, prob_array, position, size, operator):
    
# considering everything to the left as input as -1.
    error = 0
    for i in range(size):
        
        if operator(i, position):
            if output_array[i] != -1 :
                error = error + prob_array[i]
        else :
            if output_array[i] != 1 :
                error = error + prob_array[i] 
    
       
    return error



def minimum_error(output_array, prob_array, size): 
    
    minimum_err = size;
    position = -1
    operator_local = operator.gt
    for i in range(size):
        
        greater_error = error(output_array, prob_array, i, size, operator.ge)
        less_error = error(output_array, prob_array, i, size, operator.lt)
        
            
        if greater_error < minimum_err :
            
            position = i
            minimum_err = greater_error
            operator_local = operator.ge
            
        if less_error < minimum_err :
           
            position = i
            minimum_err = less_error 
            operator_local = operator.lt               
       
    return  position, minimum_err, operator_local  

  
                
def calculate_alpha(epsilon):
    
    return 0.5 * math.log((1 - epsilon) / epsilon)
    
def calculate_new_probability(old_probablility, output_array, position, epsilon, size, operator_local):
    
    new_probability_array = []
    new_probability = 0
    our_classification = []
    for i in range(size):
        
        if operator_local(i, position):
            if output_array[i] != -1 :
                new_probability = old_probablility[i] * math.exp(epsilon)
            else:
                new_probability = old_probablility[i] * math.exp(-1 * epsilon)  
            our_classification.append(-1)      
        else :
            if output_array[i] != 1 :
                new_probability = old_probablility[i] * math.exp(epsilon) 
            else:
                new_probability = old_probablility[i] * math.exp(-1 * epsilon)
            our_classification.append(1)    
        new_probability_array.append(new_probability)
    
#    print new_probability_array
    return np.sum(new_probability_array), np.array(new_probability_array) / np.sum(new_probability_array) , our_classification


'''
1. The selected weak classifier: ht.
2. The error of ht: t.
3. The weight of ht: at.
4. The probabilities normalization factor: Zt.
5. The probabilities after normalization: pi
6. The boosted classifier: ft.
7. The error of the boosted classifier: Et.
8. The bound on Et.
'''

file_name = ut.read_file_name()
number_of_iterations, size , epsilon, input_array, output_array, probability_array = ut.read_input(file_name)
ft = np.zeros(int(size))
a = ""
zt = 1 
et = 0

for i in range(number_of_iterations):
    temp = i
    print "ITERATION ", i + 1
    position, minimum_err, operator_local = minimum_error(output_array, probability_array, size)
    operator_symbol = "<" if operator_local == operator.ge else ">="
    print "The selected weak classifier: x %s %s" % (operator_symbol, input_array[position])
    print "The error of Ht: %s" % (minimum_err)
    alpha = calculate_alpha(minimum_err)
    print "The weight of Ht: ", alpha 
    normalization_factor, probability_array, our_classification = calculate_new_probability(probability_array, output_array, position, alpha, size, operator_local)
    
    for i, item in enumerate(ft):
        ft[i] = item + (alpha * our_classification[i])
               
#    print "probability after normalization are:", probability_array
    zt = zt * normalization_factor
        
    for i in range(size):
        if (output_array[i] == 1 and ft[i] < 0) or (output_array[i] == -1 and ft[i] > 0):
            et += 1
    
    print "The probabilities normalization factor Zt: ", normalization_factor
    
    probability_formatted = [float(format(x, '.5f')) for x in probability_array]
    print "The probabilities after normalization: ", probability_formatted
    
    if temp == 0:
        a = a + " %s * I(x %s %s) " % (alpha, operator_symbol, input_array[position])
    else:
        a = a + "+  %s * I(x %s %s) " % (alpha, operator_symbol, input_array[position])
        
        
    print "The boosted classifier: ", a
    print "The error on selected classifier is: ", et / float(size)  
    print "Error bound is: " , zt , "\n \n "
      
    et = 0
   



