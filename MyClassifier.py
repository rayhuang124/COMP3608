import sys
import csv
import math
import statistics
from DTNode import DTNode 

################################### NAIVE BAYES ###################################

def naive_bayes(training_set, testing_set):
    yes_set = []
    no_set = []

    for i in range(0, len(training_set)):
        class_yn = training_set[i][len(training_set[i])-1]
        if class_yn == "yes":
            yes_set.append(training_set[i])
        else:
            no_set.append(training_set[i])

    no_of_attributes = len(testing_set[0])
    y_means = []
    y_stdev = []
    for i in range(0, no_of_attributes):
        attribute_list = []
        for y in range(0, len(yes_set)): 
            attribute_list.append(float(yes_set[y][i]))
        mean = sum(attribute_list)/len(attribute_list)
        std = statistics.stdev(attribute_list)
        y_means.append(mean)
        y_stdev.append(std)

    n_means = []
    n_stdev = []
    for i in range(0, no_of_attributes):
        attribute_list = []
        for y in range(0, len(no_set)): 
            attribute_list.append(float(no_set[y][i]))
        mean = sum(attribute_list)/len(attribute_list)
        std = statistics.stdev(attribute_list)
        n_means.append(mean)
        n_stdev.append(std)

    training_length = len(training_set)
    len_yes = len(yes_set)
    len_no = len(no_set)

    answers = []
    for i in range(0, len(testing_set)):
        p_yes = p_yes = len_yes/training_length
        p_no = len_no/training_length
        for y in range(0, len(testing_set[0])):
            y_prob_function = (1/(y_stdev[y] * math.sqrt(2 * math.pi))) * math.exp((-math.pow(float(testing_set[i][y]) - y_means[y], 2))/(2 * math.pow(y_stdev[y], 2)))
            n_prob_function = (1/(n_stdev[y] * math.sqrt(2 * math.pi))) * math.exp((-math.pow(float(testing_set[i][y]) - n_means[y], 2))/(2 * math.pow(n_stdev[y], 2)))
            p_yes = p_yes * y_prob_function
            p_no = p_no * n_prob_function
    
        if p_no > p_yes:
            answers.append("no")
        else:
            answers.append("yes")

    return answers
################################## DECISION TREE ##################################
def entropy(subset):
    classes = count_yn(subset) 
    total = len(subset)
    if classes[0] == 0:
        first = 0
    else:
        first = - classes[0]/total * math.log(classes[0]/total, 2)
    
    if classes[1] == 0:
        second = 0
    else:
        second = - classes[1]/total * math.log(classes[1]/total, 2)
    return first + second

def count_yn(subset):
    classes = [0, 0] # yes, no
    for i in range(0, len(subset)):
        if subset[i][-1] == "yes":
            classes[0] += 1
        elif subset[i][-1] == "no":
            classes[1] += 1
    return classes

def separate_by_attribute(subset, number):
    att_names = []
    separated_attributes = []
    for i in range(0, len(subset)):
        if subset[i][number] not in att_names:
            att_names.append(subset[i][number])
            separated_attributes.append([subset[i][number], [subset[i]]])
        else:
            for y in range(0, len(separated_attributes)):
                if separated_attributes[y][0] == subset[i][number]:
                    separated_attributes[y][1].append(subset[i])
    return separated_attributes

# Forming and Training the Tree
def decision_tree(training_set, attributes, default):
    # Empty Training Set
    if training_set == []:
        return DTNode(True, default, {})
    
    # Finding Majority Class for Examples
    classes = count_yn(training_set)

    majority = "yes"
    if classes[1] > classes[0]:
        majority = "no"

    # Same Classes
    if classes[0] == 0:
        return DTNode(True, "no", {})
    elif classes[1] == 0:
        return DTNode(True, "yes", {})

    # Empty Attribute List
    if attributes == []:
        return DTNode(True, majority, {})

    # Same Attributes
    same_attributes = []
    for i in range(0, len(training_set[0])-1):
        same_attributes.append(training_set[0][i])
    
    same = True
    for i in range(0, len(training_set)):
        if training_set[i][0:len(training_set[i])-1] != same_attributes:
            same = False
            break

    if same:
        return DTNode(True, majority, {})
        
    ### Splitting on Attribute and Creation of Tree
    entropy_ts = entropy(training_set)

    # Best Attribute
    best_attribute = attributes[0]
    best_attribute_sep_list = []

    best_gain = -1
    training_length = len(training_set)
    for i in range(0, len(attributes)):
        separated_attributes = separate_by_attribute(training_set, attributes[i])
        info_gain = 0
        for y in range(0, len(separated_attributes)):
            info_gain += len(separated_attributes[y][1])/training_length * entropy(separated_attributes[y][1])
        if entropy_ts - info_gain > best_gain:
            best_gain = entropy_ts - info_gain
            best_attribute = attributes[i] 
            best_attribute_sep_list = separated_attributes
    
    tree = DTNode(False, best_attribute, {})

    new_att = []
    for i in range(0, len(attributes)):
        if attributes[i] != best_attribute:
            new_att.append(attributes[i])

    for i in range(0, len(best_attribute_sep_list)):
        node = decision_tree(best_attribute_sep_list[i][1], new_att, majority)
        tree.children[best_attribute_sep_list[i][0]] = node
    
    return tree

################################## MAIN PROGRAM ###################################

def printer(node, depth):
    for attribute in node.children:
        if node.children[attribute].leaf == True:
            print(((depth) * "|  ") + str(node.attribute+1) + " = " + str(attribute) + ": " + str(node.children[attribute].attribute))
        else:
            print(depth*"|  " + str(node.attribute+1) + " = " + attribute)
            printer(node.children[attribute], depth + 1)

# Processes CSV Data
def read_training_data(path): 
    with open(path, mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        data = list(csv_reader)
    return data

training_set = read_training_data(sys.argv[1])
testing_set = read_training_data(sys.argv[2])
algorithm = sys.argv[3]

# Applying Algorithm
if algorithm == "NB":
    answers = naive_bayes(training_set, testing_set)
    for answer in answers:
        print(answer)
        
elif algorithm == "DT":
    attribute_list = []
    for i in range(0, len(testing_set[0])):
        attribute_list.append(i)

    tree = decision_tree(training_set, attribute_list, "yes") 

    for i in range(0, len(testing_set)):
        current_node = tree
        while current_node.leaf == False:
            current_node = current_node.children[testing_set[i][current_node.attribute]]
        print(current_node.attribute)

# Graphical Decision Tree
elif algorithm == "DTG":
    attribute_list = []
    for i in range(0, len(testing_set[0])-1):
        attribute_list.append(i)

    tree = decision_tree(training_set, attribute_list, "yes") 
    printer(tree, 0)

####################### 10-FOLD STRATIFIED CROSS VALIDATION #######################
# Comment out the main program section above when finding accuracy.
'''
def read_training_data(path): 
    with open(path, mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        data = list(csv_reader)
    return data

unformatted_folds = read_training_data(sys.argv[2])
algorithm = sys.argv[1]

folds = []
fold = []
for i in range(0, len(unformatted_folds)):
    if unformatted_folds[i] == []:
        folds.append(fold)
        fold = []
    else:
        fold.append(unformatted_folds[i])
folds.append(fold)

sum_accuracies = 0
for i in range(0, len(folds)):
    testing_set = folds[i]
    required_answers = []

    formatted_test = []
    for z in range(0, len(testing_set)):
        required_answers.append(testing_set[z][-1])
        formatted_test.append(testing_set[z][:-1])

    training_set = []
    for y in range(0, len(folds)):
        if y != i:
            for g in range(0, len(folds[y])):
                training_set.append(folds[y][g])
    
    if algorithm == "NB":
        results = naive_bayes(training_set, formatted_test)

    if algorithm == "DT":
        attribute_list = []
        for i in range(0, len(formatted_test[0])):
            attribute_list.append(i)

        tree = decision_tree(training_set, attribute_list, "yes") 
        results = []
        for i in range(0, len(formatted_test)):
            current_node = tree
            while current_node.leaf == False:
                current_node = current_node.children[testing_set[i][current_node.attribute]]
            results.append(current_node.attribute)

    correct = 0
    for f in range(0, len(results)):
        if results[f] == required_answers[f]:
            correct += 1
    
    sum_accuracies += correct/len(required_answers)

print(sum_accuracies/10)
'''