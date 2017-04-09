'''
Created on Sep 3, 2016

@author: SantoshKompally
'''

# import math library for log
import math
import numpy as np

# function to read the input from the given input file.
def readinput_file(input_file):
    output = []
    with open(input_file) as f:
        first_line = f.readline().rstrip("\n")
        input = first_line.split(" ")
        number_of_inputs = int(input[0])
        number_of_features = int(input[1])
        remaining_lines = f.readlines()
    val = 1    
    for line in remaining_lines:
        input_line = line.rstrip('\n').split()
        input_line.insert(0, val)
        val = val + 1
        output.append(input_line)
        if len(input_line) - 1 != number_of_features:
            print("problem in the number of input features." + str(len(input_line)))
            exit()  
            
    return number_of_inputs, number_of_features, output
        
# function to calculate the entropy for the given input array.
def calculateEntropy(a):
    result = 0
    # if loop is written the case in which temp is 0. In that case 1/temp will return exception.
    for temp in a:
        if temp == 0:
            result = result + 0
        else:    
            result = result + temp * math.log((1 / temp), 2)
        
    return result        
   
# function to calculate the maximum value from the given array.
def calculateMaximumvalue(input_list):
    return max(input_list)

# function to calculate maximum gain from given list of nodes.

# partition is a input  array that contains the partition set.
# input_array contains the whole input set.
# number_of_features is the number of features
# input size is the number of examples.
def gain_per_partition(partition, input_array, number_of_features, input_size):
    features = []
    sub_input_set = []
    for i in partition:
        for j in input_array:
            if j[0] == i:
                sub_input_set.append(j)
                
    arr = np.array(sub_input_set)
    
    # get list of features           
    for i in range (1, number_of_features):
        features.append(arr[:, i])
    
    # targets is the last column.    
    target_array = arr[:, number_of_features]     
#     for i in  range(0,len(target_array)):
#         print (target_array[i]) 
    
    list_of_gains = []           
    # for each feature calculate the conditional entropy.
    for feature in features:
        list_of_gains.append(entropy_of_given_set(target_array) - calcualte_conditional_Entropy(feature , target_array))
        
#    print("max gain is:")    
#    print (max(list_of_gains) * len(partition)/float(input_size))

    return max(list_of_gains) * len(partition) / float(input_size)

def calcualte_conditional_Entropy(feature_array, target_array):
    
    unique_features = np.unique(feature_array)
    unique_targets = np.unique(target_array)
#     make a 2 dimensional array where the title for rows is uniqie_features and column title is unique_targets.
    list_of_key_value_pairs = []
    
    for i in range(0, len(feature_array)):
        # always reinitialize to blank value.
        key_value_pair = []
        key_value_pair.append(feature_array[i])
        key_value_pair.append(target_array[i])
        list_of_key_value_pairs.append(key_value_pair)
        
    # we are storing the data in dict of dicts.
    d = {}
    for feature in unique_features:
        d[feature] = {}
        
    for feature in unique_features:    
        for target in unique_targets:
            d[feature][target] = 0    
            
    
    
    # iterate through list of key value pairs.
    
    for temp in list_of_key_value_pairs:
        d[temp[0]][temp[1]] = d[temp[0]][temp[1]] + 1
    
# find the number of times each value is appearing.

    features_dict = {}
    
    # initialize the features dictionary to 0.
    for row in unique_features:
        features_dict[row] = 0
    
    for row in unique_features:
        for col in unique_targets:
            features_dict[row] = features_dict[row] + d[row][col] 

#     print(features_dict)        

    for feature in unique_features:    
        for target in unique_targets:
            # putting float here to have the precision intact.
            d[feature][target] = d[feature][target] / float(features_dict[feature])
        
#     print(d)
    
    # now we have to call the conditional probability function.
    entropy = int(0)
    for key, value in d.iteritems():
        input_arr = []
        
        for val in value:
            # print d[key][val]
            input_arr.append(d[key][val])
                
        entropy = entropy + (features_dict[key] / float(len(feature_array)) * calculateEntropy(input_arr))    
    
    return entropy
    
def selectPartition(list_of_partitions, number_of_inputs, number_of_features, input_array):
    d = {} 
    for partition in list_of_partitions:
        d[partition] = gain_per_partition(list_of_partitions[partition], input_array, number_of_features, number_of_inputs)
        
#    print d
    
    # iterate and split the partition which has the maximum value.
    value = 0
    partition = "none"
    for key in d.iterkeys():
        if d[key] >= value :
            value = d[key]
            partition = key
    
#   print("set that will be divided is: " + partition)
    return partition
   
def entropy_of_given_set(target_array):
    unique_values = np.unique(target_array)
    d = {}
    
    for key in unique_values:
        d[key] = 0
      
    # find the number times each target variable is appearing.    
    for each_value in target_array:
        d[each_value] = d[each_value] + 1 
       
    probabilty_array = []    
    for key in d:
        d[key] = d[key] / float(len(target_array)) 
        probabilty_array.append(d[key])
       
    return (calculateEntropy(probabilty_array))
                   
def split_partition_feature_select(partition_to_split, input_arr): 
    
    
    sub_input_set = []
    features = []
    for i in partition_to_split:
        
        for j in input_arr:
            
            if j[0] == i:
                sub_input_set.append(j)
             
    arr = np.array(sub_input_set)
    
#     print(arr)
    # get list of features           
    for i in range (1, number_of_features):
        features.append(arr[:, i])
    
    # targets is the last column.   
    
#     print(features) 
    target_array = arr[:, number_of_features]      
    list_of_gains = {}
    key=1         
    # for each feature calculate the conditional entropy.
    for feature in features:
        list_of_gains[key] = entropy_of_given_set(target_array) - calcualte_conditional_Entropy(feature ,target_array)
        key = key + 1
      
    val=0
    split_feature="none"
    
    print list_of_gains
    for key in list_of_gains:
        if list_of_gains[key] >= val:
            val= list_of_gains[key]
            split_feature=key
      
#     print("the nodes will be split on: " + str(val))

    unique_values = np.unique((arr[:,split_feature]))

    d=dict()
    
    for temp in unique_values:
        d[temp]=[]
    
    
    for input in unique_values:
        for row in arr:
            if row[split_feature] == input:
                # row[0] should go into input named array or 'R' or 'G' or 'B' 
                d[input].append(row[0])
                
    print(d)    
    return split_feature,d
    
    
def read_input():
    
    input = raw_input("Please enter the input in the following format: InputFile Partition File, outputFile \n")
    input_arr = input.split()
    if len(input_arr) != 3:
        print("please provide 3 arguments")
        exit()
    return input_arr[0],input_arr[1],input_arr[2]    
    
def convert_partition_file_into_dict(partition_file):
#   opening a dictionary.
    d={}    
    with open(partition_file) as f:
        lines = f.readlines()
        for line in lines:
            items = line.rstrip('\n').split()
# first value is key rest all are pairs.
            value=[]
            for i in range(1,len(items)):
                value.append(int(items[i]))           
            d[items[0]] = value   
    return d

# partition value is a dict.
#partition_key is the key from data_dict which will be partitioned.
def format_data_to_write_to_output_file(data_dict,partition_key,partition_values):
    
    data_dict1 ={}
    counter=1
    for key in data_dict:
        if key == partition_key:
            for key1 in partition_values:
                # add new values to the existing dict.
                data_dict1[str(key) + str(counter) ] = partition_values[key1]
                counter = counter+1
        # delete the existing entry since it is replaced with other entries.         
    del data_dict[partition_key]
    
    # add the newly created entries into the old dict and return it.
    
    for key in data_dict1:
        data_dict[key] = data_dict1[key]
    
    print data_dict 
    return data_dict
  
def write_to_file(nodes_dict,output):
    
    with open(output,'w') as f:
        for key in nodes_dict:
            new_values = nodes_dict[key]
            new_key = key
            val = " "
            for i in range(0,len(new_values)):
                val = val + " " + str(new_values[i])
            val = new_key +" " +  val    
            f.write(val + "\n")
         
        
# read input from the terminal and convert it in the below dict format and also give the input file 
# in place of test.txt below.
input_file,partition_file,output_file = read_input()

number_of_inputs, number_of_features, input_array = readinput_file(input_file)
partition_data = convert_partition_file_into_dict(partition_file)
print(partition_data)
partiton_to_split = selectPartition(partition_data, number_of_inputs, number_of_features, input_array)
basis_of_split,split_array=split_partition_feature_select(partition_data[partiton_to_split],input_array)


print("partition that will be split is: " + str(partiton_to_split))

print("The partition will be split on the feature: "+ str(basis_of_split))

new_nodes_strucuture = format_data_to_write_to_output_file(partition_data,partiton_to_split,split_array)

write_to_file(new_nodes_strucuture, output_file)




