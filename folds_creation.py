import sys
import csv 

def read_training_data(path): 
    with open(path, mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        data = list(csv_reader)
    return data

data = read_training_data(sys.argv[1])
yes_set = []
no_set = []
for i in range(0, len(data)):
    class_yn = data[i][len(data[i])-1]
    if class_yn == "yes":
        yes_set.append(data[i])
    else:
        no_set.append(data[i])

formatted_folds = [[], [], [], [], [], [], [], [], [], []]
for i in range(0, len(yes_set)):
    formatted_folds[i%10].append(yes_set[i])

for i in range(0, len(no_set)):
    formatted_folds[i%10].append(no_set[i])

folds = []
for i in range(0, 10):
    for y in range(0, len(formatted_folds[i])):
        folds.append(formatted_folds[i][y])
    if i != 9:
        folds.append([])

with open("pf dcfs.csv", mode = "w") as csv_file:
    writer = csv.writer(csv_file, delimiter = ",")
    for line in folds:
        writer.writerow(line)
