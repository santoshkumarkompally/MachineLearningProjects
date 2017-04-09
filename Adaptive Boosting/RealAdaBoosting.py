'''
Created on Dec 4, 2016

@author: SantoshKompally
'''


import operator
import math
import numpy as np
import Utility as ut

   
   
# when passed a position and output array it will consider both the side as mentioned in the parameter.
# greater than or equal to the above number is considered as negative and vice versa.         

def error_real_ada(output_array, prob_array, position, size, operator):
    
# considering everything to the left as input as -1.
    correct_positive = 0
    correct_negative = 0
    wrong_positive = 0
    wrong_negative = 0
    our_classification = []
    for i in range(size):   
         
        if operator(i, position):
            if output_array[i] == -1 :
                correct_negative = correct_negative + prob_array[i]
            else:
                wrong_negative = wrong_negative + prob_array[i]
            our_classification.append(-1)        
        else :
            if output_array[i] == 1 :
                correct_positive = correct_positive + prob_array[i] 
            else:
                wrong_positive = wrong_positive + prob_array[i]
            our_classification.append(1)         
       
    return math.sqrt(correct_positive * wrong_positive) + math.sqrt(wrong_negative * correct_negative) 



def minimum_error_real_ada(output_array, prob_array, size): 
    
    minimum_err = size;
    position = -1
    operator_local = operator.gt
    for i in range(size):
        
        greater_error = error_real_ada(output_array, prob_array, i, size, operator.ge)
        less_error = error_real_ada(output_array, prob_array, i, size, operator.lt)
        
            
        if greater_error < minimum_err :
            
            position = i
            minimum_err = greater_error
            operator_local = operator.ge
            
        if less_error < minimum_err :
           
            position = i
            minimum_err = less_error 
            operator_local = operator.lt               
     
    return  position, minimum_err, operator_local    

  
                

def calculate_new_probability_real_ada(old_probablility, output_array, position, size, operator_local, epsilon1):
    
    new_probability_array = []
    new_probability = 0
    correct_positive = 0
    correct_negative = 0
    wrong_positive = 0
    wrong_negative = 0
    our_classification = []
    
    
    for i in range(size):   
        
        if operator_local(i, position):
            if output_array[i] == -1 :
                correct_negative = correct_negative + old_probablility[i]
            else:
                wrong_negative = wrong_negative + old_probablility[i]
            our_classification.append(-1)        
        else :
            if output_array[i] == 1 :
                correct_positive = correct_positive + old_probablility[i] 
            else:
                wrong_positive = wrong_positive + old_probablility[i]
            our_classification.append(1)         
   
    c_plus = 0.5 * math.log ((correct_positive + epsilon1) / (wrong_positive + epsilon1))
    c_minus = 0.5 * math.log ((wrong_negative + epsilon1) / (correct_negative + epsilon1))
    
    for i in range(size):   
        new_probability = old_probablility[i] * math.exp(-1 * output_array[i] * (c_plus if our_classification[i] == 1 else c_minus))
        new_probability_array.append(new_probability)  

    return np.sum(new_probability_array), np.array(new_probability_array) / np.sum(new_probability_array) , c_plus, c_minus, our_classification           
    
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
classification_sum = np.zeros(int(size))
zt = 1 
et = 0

for i in range(number_of_iterations):
    print "ITERATION: ", i + 1
    position, minimum_err, operator_local = minimum_error_real_ada(output_array, probability_array, size)
    operator_symbol = "<" if operator_local == operator.ge else ">="
    print "selected weak classifier is: x %s %s" % (operator_symbol, input_array[position])
    print "The G error value of Ht: %s" % (minimum_err)
#    normalization_factor, probability_array = calculate_new_probability(probability_array, output_array, position, alpha, size, operator_local)
    normalization_factor, probability_array, c_plus, c_minus, our_classification = calculate_new_probability_real_ada(probability_array, output_array, position, size, operator_local, float(epsilon))
    for i, item in enumerate(ft):
        ft[i] = item + (c_plus if our_classification[i] == 1 else c_minus)
     
    zt = zt * normalization_factor  
    
    for i in range(size):
        if (output_array[i] == 1 and ft[i] < 0) or (output_array[i] == -1 and ft[i] > 0):
            et += 1
    
#    print "normalization factor: ", normalization_factor
    print "The weights Ct+,Ct-:", c_plus, ",", c_minus
    print "The probabilities normalization factor Zt: " , normalization_factor
#    print "probability after normalization are:", probability_array
    probability_formatted = [float(format(x, '.3f')) for x in probability_array]
    print "The probabilities after normalization: ", probability_formatted
    print "The values ft(xi) for each one of the examples: ", [x for x in ft]  
    print "The error of the boosted classifier Et:", et / float(size)
    print "The bound on Et: ", zt , "\n \n"
    et = 0
    
   



