'''
Created on Dec 4, 2016

@author: SantoshKompally
'''

from decimal import Decimal
import operator
import math
import numpy as np

# reads the input and then gives the specified output.
def read_input():

    with open("input2") as f:
    
        number_of_iterations, number_of_examples, epsilon = [Decimal(item) for item in f.readline().split()]
        input_array = [float(item) for item in f.readline().split()]
        output_array = [float(item) for item in f.readline().split()]
        probablity_array = [float(item) for item in f.readline().split()]
        
        return number_of_iterations, number_of_examples, epsilon, input_array, output_array, probablity_array
    
   
   
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

def error_real_ada(output_array, prob_array, position, size, operator):
    
# considering everything to the left as input as -1.
    error = 0
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
       
    return math.sqrt(correct_positive * wrong_positive + wrong_negative * correct_negative) 



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

  
                
def calculate_alpha(epsilon):
    
    return 0.5 * math.log((1 - epsilon) / epsilon)
    
def calculate_new_probability(old_probablility, output_array, position, epsilon, size, operator_local):
    
    new_probability_array = []
    new_probability = 0
    for i in range(size):
        
        if operator_local(i, position):
            if output_array[i] != -1 :
                new_probability = old_probablility[i] * math.exp(epsilon)
            else:
                new_probability = old_probablility[i] * math.exp(-1 * epsilon)    
        else :
            if output_array[i] != 1 :
                new_probability = old_probablility[i] * math.exp(epsilon) 
            else:
                new_probability = old_probablility[i] * math.exp(-1 * epsilon)
                
        new_probability_array.append(new_probability)
    
#    print new_probability_array
    return np.sum(new_probability_array), np.array(new_probability_array) / np.sum(new_probability_array)




def calculate_new_probability_real_ada(old_probablility, output_array, position, error, size, operator_local, epsilon1):
    
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
    
    print "c_plus is: %s" % (c_plus)
    print "c_minus is: %s" % (c_minus)
    for i in range(size):   
        new_probability = old_probablility[i] * math.exp(-1 * output_array[i] * (c_plus if our_classification[i] == 1 else c_minus))
        new_probability_array.append(new_probability)   
    
    return np.sum(new_probability_array), np.array(new_probability_array) / np.sum(new_probability_array) , c_plus, c_minus           
    
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

number_of_iterations, size , epsilon, input_array, output_array, probability_array = read_input()

for i in range(number_of_iterations):
    print "round number: ", i + 1
    position, minimum_err, operator_local = minimum_error_real_ada(output_array, probability_array, size)
    operator_symbol = "<" if operator_local == operator.ge else ">="
    print "selected weak classifier is: x %s %s" % (operator_symbol, input_array[position])
    print "error: %s" % (minimum_err)
    alpha = calculate_alpha(minimum_err)
    print "alpha is: ", alpha 
#    normalization_factor, probability_array = calculate_new_probability(probability_array, output_array, position, alpha, size, operator_local)
    normalization_factor, probability_array, c_plus, c_minus = calculate_new_probability_real_ada(probability_array, output_array, position, alpha, size, operator_local, float(epsilon))
    print "normalization factor: ", normalization_factor
    print "c_plus is: ", c_plus;
    print "c_minus is: ", c_minus
#    print "probability after normalization are:", probability_array
    probability_formatted = [format(x, '.3f') for x in probability_array]
    print "probability after normalization are:", probability_formatted, "\n \n"
    
   



