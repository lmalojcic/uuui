import math
import sys

def algorithm(D, D_parent, X, y, depth):
    if (D == []): # vraca najvjerojatniji ishod ako je skup podataka prazan
        t = {}
        for value in D_parent:
            t[value[y]] = t.get(value[y], 0) + 1
        t_sorted = {key: value for key, value in sorted(t.items())}
        return max(t_sorted, key=t_sorted.get)
    t = {}
    for value in D:
        t[value[y]] = t.get(value[y], 0) + 1
    t_sorted = {key: value for key, value in sorted(t.items())}
    if (X == [] or len(t) == 1 or depth == 0):
        return max(t_sorted, key=t_sorted.get)
    #nac najdiskriminativniju znacajku
    start_entropy = 0
    for (key, value) in t.items():
        start_entropy += -value/len(D) * math.log2(value/len(D))
    ig = {}
    feature_values = {}
    for feature in X:
        dict_values = {}
        for value in D: #dijeljenje skupa podataka po vrijednostima znacajke
            if (value[feature] not in dict_values):
                dict_values[value[feature]] = []
            dict_values[value[feature]] =  dict_values[value[feature]] + [(value)]
        feature_values[feature] = dict_values
        entropy_values = {}
        for (key, value) in dict_values.items(): #racunanje informacijske dobiti
            entropy_values[key] = 0
            temp = {}
            for val in value:
                temp[val[y]] = temp.get(val[y], 0) + 1
            for (key2, value2) in temp.items():
                entropy_values[key] += -value2/len(value) * math.log2(value2/len(value))
        feature_entropy = 0
        for (key, value) in entropy_values.items():
            feature_entropy += value * len(dict_values[key])/len(D)
        ig[feature] = start_entropy - feature_entropy
    subtrees = []
    ig_sorted = {key: value for key, value in sorted(ig.items())}
    feature = max(ig_sorted, key=ig_sorted.get)
    
    for (key, value) in feature_values[feature].items():
        subtrees.append([key, algorithm(value, D, [x for x in X if x != feature], y, depth-1)])
    return [feature, subtrees]

def recursive_print(list, level, print_string):
    if (type(list) is str):
        print(list)
        return
    if (type(list[1]) is str):
        print(print_string + str(list[0]) + " " +  str(list[1]))
        return
    if (type(list[1][0]) is str):
        print_string = print_string + list[0] + " "
        level += 1
        recursive_print(list[1], level, print_string)
    else:
        print_string = print_string + str(level) + ":" + list[0] + "="
        for i in list[1]:
            recursive_print(i, level, print_string)

def prediction(tree, row, default):
    if (type(tree) is str):
        return(tree)
    while 1:
        feature = tree[0]
        found = False
        for i in tree[1]:
            if (row[feature] == i[0]):
                tree = i[1]
                found = True
                break   
        if (found == False):
            return(default)
        if (type(tree) is str):
            return(tree)


class ID3:
    def __init__(self):
        self.tree = []
        self.default = None
    
    def fit(self, train_file, depth):
        f = open(train_file, "r")
        data = f.readlines()
        f.close()
        data = [line.strip().split(",") for line in data]
        data_final = []
        for row in data[1:]:
            dict = {}
            for i in range(len(row)):
                dict[data[0][i]] = row[i]
            data_final.append(dict)
        X = data[0][:-1]
        goal = data[0][-1]
        self.tree = algorithm(data_final, data_final, X, goal, depth)
        print("[BRANCHES]:")
        recursive_print(self.tree, 1, "")
        default_dict = {}
        for row in data_final:
            default_dict[row[goal]] = default_dict.get(row[goal], 0) + 1
        sorted_default_dict = {key: value for key, value in sorted(default_dict.items())}
        self.default = max(sorted_default_dict, key=sorted_default_dict.get)

    def predict(self, test_file):
        f = open(test_file, "r")
        data = f.readlines()
        f.close()
        data = [line.strip().split(",") for line in data]
        data_final = []
        goal = data[0][-1]
        goal_values = []
        for row in data[1:]:
            dict = {}
            for i in range(len(row)):
                dict[data[0][i]] = row[i]
            data_final.append(dict)
            goal_values.append(row[-1])
        predictions = []
        for row in data_final:
            temp = prediction(self.tree, row, self.default)
            predictions.append(temp)
        goal_values = list(set(goal_values + predictions))
        goal_values.sort()
        confusion_matrix = [[0 for i in range(len(goal_values))] for j in range(len(goal_values))]
        to_print = "[PREDICTIONS]: "
        for i in predictions:
            to_print += i + " "
        print(to_print)
        correct = 0
        for i in range(len(predictions)):
            if (predictions[i] == data_final[i][goal]):
                correct += 1
            confusion_matrix[goal_values.index(data_final[i][goal])][goal_values.index(predictions[i])] += 1
        print("[ACCURACY]: " + "{:.5f}".format(correct/len(predictions), 5))
        print("[CONFUSION_MATRIX]:")
        for i in confusion_matrix:
            for j in i:
                print(j, end=" ")
            print()


alg = ID3()
if (len(sys.argv) == 3):
    depth = -1
    alg.fit(sys.argv[1], depth)
    alg.predict(sys.argv[2])
elif (len(sys.argv) == 4):
    depth = int(sys.argv[3])
    alg.fit(sys.argv[1], depth)
    alg.predict(sys.argv[2])

