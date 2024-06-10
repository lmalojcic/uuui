import sys
import numpy as np


class nn_5s:
    def __init__(self, input_size):
        self.weights = np.random.normal(0, 0.01, (5, input_size))
        self.bias = np.random.normal(0, 0.01, (5, 1))
        self.weights_out = np.random.normal(0, 0.01, (1, 5))
        self.bias_out = np.random.normal(0, 0.01, (1))

    def output(self, x):
        t = np.dot(self.weights, x) + self.bias
        t_sigmoid = 1 / (1 + np.exp(-t))
        return np.dot(self.weights_out, t_sigmoid) + self.bias_out
    
    def error(self, X, y):
        err = 0
        for i in range(len(X)):
            err += (y[i] - self.output(X[i])) ** 2
        err /= len(X)
        return err[0,0]
    
    def get_props(self):
        return [self.weights, self.bias, self.weights_out, self.bias_out]
    
    def set_props(self, props):
        self.weights = props[0]
        self.bias = props[1]
        self.weights_out = props[2]
        self.bias_out = props[3]

      
class nn_20s:
    def __init__(self, input_size):
        self.weights = np.random.normal(0, 0.01, (20, input_size))
        self.bias = np.random.normal(0, 0.01, (20, 1))
        self.weights_out = np.random.normal(0, 0.01, (1, 20))
        self.bias_out = np.random.normal(0, 0.01, (1))

    def output(self, x):
        t = np.dot(self.weights, x) + self.bias
        t_sigmoid = 1 / (1 + np.exp(-t))
        return np.dot(self.weights_out, t_sigmoid) + self.bias_out
    
    def error(self, X, y):
        err = 0
        for i in range(len(X)):
            err += (y[i] - self.output(X[i])) ** 2
        err /= len(X)
        return err[0,0]
    
    def get_props(self):
        return [self.weights, self.bias, self.weights_out, self.bias_out]
    
    def set_props(self, props):
        self.weights = props[0]
        self.bias = props[1]
        self.weights_out = props[2]
        self.bias_out = props[3]


class nn_5s5s:
    def __init__(self, input_size):
        self.weights_1 = np.random.normal(0, 0.01, (5, input_size))
        self.bias_1 = np.random.normal(0, 0.01, (5, 1))
        self.weights_2 = np.random.normal(0, 0.01, (5, 5))
        self.bias_2 = np.random.normal(0, 0.01, (5, 1))
        self.weights_out = np.random.normal(0, 0.01, (1, 5))
        self.bias_out = np.random.normal(0, 0.01, (1))
    
    def output(self, x):
        t = np.dot(self.weights_1, x) + self.bias_1
        t_sigmoid = 1 / (1 + np.exp(-t))
        t_2 = np.dot(self.weights_2, t_sigmoid) + self.bias_2
        t_sigmoid_2 = 1 / (1 + np.exp(-t_2))
        return np.dot(self.weights_out, t_sigmoid_2) + self.bias_out
    
    def error(self, X, y):
        err = 0
        for i in range(len(X)):
            err += (y[i] - self.output(X[i])) ** 2
        err /= len(X)
        return err[0,0]
    
    def get_props(self):
        return [self.weights_1, self.bias_1, self.weights_2, self.bias_2, self.weights_out, self.bias_out]
    
    def set_props(self, props):
        self.weights_1 = props[0]
        self.bias_1 = props[1]
        self.weights_2 = props[2]
        self.bias_2 = props[3]
        self.weights_out = props[4]
        self.bias_out = props[5]


i = 0
while (i<len(sys.argv)):
    if (sys.argv[i] == "--train"):
        i+=1
        train_file = sys.argv[i]
    elif (sys.argv[i] == "--test"):
        i+=1
        test_file = sys.argv[i]
    elif (sys.argv[i] == "--nn"):
        i+=1
        nn = sys.argv[i]
    elif (sys.argv[i] == "--popsize"):
        i+=1
        popsize = int(sys.argv[i])
    elif (sys.argv[i] == "--elitism"):
        i+=1
        elitism = int(sys.argv[i])
    elif (sys.argv[i] == "--p"):
        i+=1
        p = float(sys.argv[i])
    elif (sys.argv[i] == "--K"):
        i+=1
        K = float(sys.argv[i])
    elif (sys.argv[i] == "--iter"):
        i+=1
        iter = int(sys.argv[i])
    i+=1


f = open(train_file, "r")
train_data = f.readlines()
f.close()
header = train_data[0].split(",")
train_data = train_data[1:]
goals = []
for i in range(len(train_data)):
    train_data[i] = train_data[i].split(",")
    for j in range(len(train_data[i])-1):
        train_data[i][j] = [float(train_data[i][j])]
    goals.append(float(train_data[i][-1]))
    train_data[i] = train_data[i][:-1]
    train_data[i] = np.array(train_data[i])

#fitness === 1 / error
population = []
for i in range(popsize):
    if (nn == "5s"):
        population.append(nn_5s(len(header)-1))
    elif (nn == "20s"):
        population.append(nn_20s(len(header)-1))
    elif (nn == "5s5s"):
        population.append(nn_5s5s(len(header)-1))

for i in range(1, iter + 1):
    results = []
    errors = []
    for j in range(len(population)):
        x = population[j].error(train_data, goals)
        errors.append(x)
        results.append(1 / x)
    results = np.array(results)
    to_keep = np.argsort(results)[-elitism:]
    new_population = []
    for j in range(elitism):
        new_population.append(population[to_keep[j]])
    results_sum = np.sum(results)
    for j in range(popsize-elitism): #gradnja nove populacije
        rand = np.random.uniform(0, results_sum) #biranje roditelja
        seek = 0
        for k in range(len(results)):
            seek += results[k]
            if (seek >= rand):
                parent1 = population[k]
                break
        parent2 = parent1
        while (parent2 == parent1):
            rand = np.random.uniform(0, results_sum)
            seek = 0
            for k in range(len(results)):
                seek += results[k]
                if (seek >= rand):
                    parent2 = population[k]
                    break
        props1 = parent1.get_props()
        props2 = parent2.get_props()
        new_props = []
        for k in range(len(props1)):
            new_props.append((props1[k] + props2[k]) / 2)
        for k in range(len(new_props)):
            if (len(new_props[k].shape) == 1):
                for l in range(len(new_props[k])):
                        if (np.random.uniform(0, 1) < p):
                            new_props[k][l] += np.random.normal(0, K)
            else:
                rows, cols = new_props[k].shape
                for l in range(rows):
                    for m in range(cols):
                        if (np.random.uniform(0, 1) < p):
                            new_props[k][l][m] += np.random.normal(0, K)
        if (nn == "5s"):
            new_nn = nn_5s(len(header)-1)
        elif (nn == "20s"):
            new_nn = nn_20s(len(header)-1)
        elif (nn == "5s5s"):
            new_nn = nn_5s5s(len(header)-1)
        new_nn.set_props(new_props)
        new_population.append(new_nn)
    population = new_population
    if (i % 2000 == 0):
        print("[Train error @" +  str(i) + "]: " + str(round(errors[to_keep[-1]], 6)))
        

results = []
errors = []
for j in range(len(population)):
    x = population[j].error(train_data, goals)
    errors.append(x)
    results.append(1 / x)
results = np.array(results)
best_index = np.argsort(results)[-1:]
best = population[best_index[0]]

f = open(test_file, "r")
test_data = f.readlines()
f.close()
header = test_data[0].split(",")
test_data = test_data[1:]
goals = []
for i in range(len(test_data)):
    test_data[i] = test_data[i].split(",")
    for j in range(len(test_data[i])-1):
        test_data[i][j] = [float(test_data[i][j])]
    goals.append(float(test_data[i][-1]))
    test_data[i] = test_data[i][:-1]
    test_data[i] = np.array(test_data[i])

test_error = best.error(test_data, goals)
print("[Test error]: " + str(round(test_error,6)))