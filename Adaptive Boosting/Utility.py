'''
Created on Dec 4, 2016

@author: SantoshKompally
'''
from decimal import Decimal
import math
# reads the input and then gives the specified output.
def read_input(file_name):

    with open(file_name) as f:
    
        number_of_iterations, number_of_examples, epsilon = [Decimal(item) for item in f.readline().split()]
        input_array = [float(item) for item in f.readline().split()]
        output_array = [float(item) for item in f.readline().split()]
        probablity_array = [float(item) for item in f.readline().split()]
        
        return number_of_iterations, number_of_examples, epsilon, input_array, output_array, probablity_array

def calculate_alpha(epsilon):
    
    return 0.5 * math.log((1 - epsilon) / epsilon)
    
def read_file_name():
    
    file_name = raw_input("Please enter the input file Name with complete path.")
    
    return file_name    