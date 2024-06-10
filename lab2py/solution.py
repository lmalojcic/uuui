import sys
from collections import deque
import time

def zakljuci(file_name):
    f = open(file_name, "r") #ucitavanje datoteke
    lines = f.readlines()
    f.close()
    filtered_lines = []
    for line in lines:
        if (line[0] != "#" and line != "\n"): #filtriranje komentara i praznih linija
            filtered_lines.append(line.lower().replace("\n", ""))

    temp = filtered_lines.pop(-1)
    goal = temp
    temp_list = []
    if (len(temp.split(" v ")) == 1): #negiranje ciljne klauzule ako se ona sastoji od jednog atoma
        if (temp[0] == "~"):
            temp = temp[1:]
        else:
            temp = "~" + temp
        temp_list.append(temp)
    else:   #negiranje ciljne klauzule ako se ona sastoji od vise atoma koristenjem demorganovog pravila ~(x v y) => ~x ^ ~y
        for element in temp.split(" v "):
            if (element[0] == "~"):
                element = element[1:]
            else:
                element = "~" + element
            temp_list.append(element)

    clauses = set()
    support = set()
    for line in filtered_lines:     #dodavanje elemenata u setove kako bi se sprijecilo dupliciranje i ubrzao pristup
        temp1 = frozenset(line.split(" v "))
        clauses.add(temp1)
    
    for clause in clauses:
        temp = ""
        for atom in clause:
            temp = temp + atom + " v "
        temp = temp[:-3]
        print(temp)

    for line in temp_list:
        temp = frozenset(line.split(" v "))
        clauses.add(temp)
        support.add(temp)

    for clause in support:
        temp = ""
        for atom in clause:
            temp = temp + atom + " v "
        temp = temp[:-3]
        print(temp)
    print("===========")

    result = False
    path = dict()
    new = set()
    while 1:
        to_remove = set()   #strategija brisanja
        for clause1 in clauses: #uklanjanje redundantnih klauzula
            for clause2 in clauses:
                if clause1.issubset(clause2) and clause1 != clause2:
                    to_remove.add(clause2)
                    break
        for clause in clauses: #uklanjanje nevaznih klauzula
            found = False
            for atom1 in clause:
                if found:
                    break
                if atom1[0] == "~":
                    for atom2 in clause:
                        if ("~" + atom2 == atom1):
                            to_remove.add(clause)
                            found = True
                            break
                else:
                    for atom2 in clause:
                        if ("~" + atom1 == atom2):
                            to_remove.add(clause)
                            found = True
                            break

        for clause in to_remove:    #brisanje pronadjenih klauzula
            clauses.remove(clause)
            if clause in support:
                support.remove(clause)

    
        resolvents = set()  #izrada novih rezolvenata
        for i in clauses:
            for j in support:
                if i != j:
                    remove1 = set()
                    remove2 = set()
                    for atom1 in i:
                        for atom2 in j:
                            if (("~" + atom1) == atom2) or (("~" + atom2) == atom1):
                                remove1.add(atom1)
                                remove2.add(atom2)
                    if not (remove1 == set() and remove2 == set()):
                        resolvent = i.difference(remove1).union(j.difference(remove2))
                        if resolvent == frozenset():
                            resolvent = "NIL"
                        if resolvent not in path:
                            path[resolvent] = [i,j]
                        if resolvent == "NIL":
                            result = True
                            break
                        resolvents.add(resolvent)
            if result:
                break
        if result:
            break
        if resolvents == set():
            break
        new = new.union(resolvents)
        if new.issubset(clauses):
            break
        clauses = clauses.union(resolvents)
        support = support.union(resolvents)
    if result:
        current = ["NIL"]
        to_print = deque()
        while current:
            temp = current.pop(0)
            if temp == "NIL":
                print_temp1 = "NIL   "
            else:
                print_temp1 = ""
                for element in temp:
                    print_temp1 = print_temp1 + element + " v "
            print_temp2 = ""
            for element in path[temp][0]:
                print_temp2 = print_temp2 + element + " v "
            print_temp2 = print_temp2[:-3] + ", "
            for element in path[temp][1]:
                print_temp2 = print_temp2 + element + " v "
            to_print.append(print_temp1[:-3] + ": " + print_temp2[:-3])
            if path[temp][0] in path:
                current.append(path[temp][0])
            if path[temp][1] in path:
                current.append(path[temp][1])
        while to_print:
            print(to_print.pop())
        print("===========")
        print("[CONCLUSION]: " + goal + " is true")
    else:
        print("[CONCLUSION]: " + goal + " is unknown")


def zakljuci_kuharica(filtered_lines, goal):
    clauses = set()
    support = set()
    for line in filtered_lines:     #dodavanje elemenata u setove kako bi se sprijecilo dupliciranje i ubrzao pristup
        temp1 = frozenset(line.split(" v "))
        clauses.add(temp1)

    temp_list = []
    if (len(goal.split(" v ")) == 1): #negiranje ciljne klauzule ako se ona sastoji od jednog atoma
        if (goal[0] == "~"):
            temp = goal[1:]
        else:
            temp = "~" + goal
        temp_list.append(temp)
    else:   #negiranje ciljne klauzule ako se ona sastoji od vise atoma koristenjem demorganovog pravila ~(x v y) => ~x ^ ~y
        for element in temp.split(" v "):
            if (element[0] == "~"):
                element = element[1:]
            else:
                element = "~" + element
            temp_list.append(element)
    
    for line in temp_list:
        temp = frozenset(line.split(" v "))
        clauses.add(temp)
        support.add(temp)


    result = False
    path = dict()
    new = set()
    while 1:
        to_remove = set()   #strategija brisanja
        for clause1 in clauses: #uklanjanje redundantnih klauzula
            for clause2 in clauses:
                if clause1.issubset(clause2) and clause1 != clause2:
                    to_remove.add(clause2)
                    break
        for clause in clauses: #uklanjanje nevaznih klauzula
            found = False
            for atom1 in clause:
                if found:
                    break
                if atom1[0] == "~":
                    for atom2 in clause:
                        if ("~" + atom2 == atom1):
                            to_remove.add(clause)
                            found = True
                            break
                else:
                    for atom2 in clause:
                        if ("~" + atom1 == atom2):
                            to_remove.add(clause)
                            found = True
                            break

        for clause in to_remove:    #brisanje pronadjenih klauzula
            clauses.remove(clause)
            if clause in support:
                support.remove(clause)

        resolvents = set()  #izrada novih rezolvenata
        for i in clauses:
            for j in support:
                if i != j:
                    remove1 = set()
                    remove2 = set()
                    for atom1 in i:
                        for atom2 in j:
                            if (("~" + atom1) == atom2) or (("~" + atom2) == atom1):
                                remove1.add(atom1)
                                remove2.add(atom2)
                    if not (remove1 == set() and remove2 == set()):
                        resolvent = i.difference(remove1).union(j.difference(remove2))
                        if resolvent == frozenset():
                            resolvent = "NIL"
                        if resolvent not in path:
                            path[resolvent] = [i,j]
                        if resolvent == "NIL":
                            result = True
                            break
                        resolvents.add(resolvent)
            if result:
                break
        if result:
            break
        if resolvents == set():
            break
        new = new.union(resolvents)
        if new.issubset(clauses):
            break
        clauses = clauses.union(resolvents)
        support = support.union(resolvents)


    if result:
        current = ["NIL"]
        to_print = deque()
        while current:
            temp = current.pop(0)
            if temp == "NIL":
                print_temp1 = "NIL   "
            else:
                print_temp1 = ""
                for element in temp:
                    print_temp1 = print_temp1 + element + " v "
            print_temp2 = ""
            for element in path[temp][0]:
                print_temp2 = print_temp2 + element + " v "
            print_temp2 = print_temp2[:-3] + ", "
            for element in path[temp][1]:
                print_temp2 = print_temp2 + element + " v "
            to_print.append(print_temp1[:-3] + ": " + print_temp2[:-3])
            if path[temp][0] in path:
                current.append(path[temp][0])
            if path[temp][1] in path:
                current.append(path[temp][1])
        while to_print:
            print(to_print.pop())
        print("===========")
        print("[CONCLUSION]: " + goal + " is true")
    else:
        print("[CONCLUSION]: " + goal + " is unknown")

    
    


def kuhaj(file_clauses, file_user):
    f = open(file_clauses, "r") #ucitavanje datoteke
    lines = f.readlines()
    f.close()
    filtered_lines = []
    for line in lines:
        if (line[0] != "#" and line != "\n"): #filtriranje komentara i praznih linija
            filtered_lines.append(line.lower().replace("\n", ""))

    print("Constructed with knowledge:")
    for line in filtered_lines:
        print(line)
    print("")

    f = open(file_user, "r") #ucitavanje datoteke
    lines = f.readlines()
    f.close()
    commands = []
    for line in lines:
        if (line[0] != "#" and line != "\n"): #filtriranje komentara i praznih linija
            commands.append(line.lower().replace("\n", ""))
    
    for command in commands:
        print("User's command: " + command)
        if command[-1] == "?":
            zakljuci_kuharica(filtered_lines, command[:-2])
        elif command[-1] == "+":
            filtered_lines.append(command[:-2])
        elif command[-1] == "-":
            if command[:-2] in filtered_lines:
                filtered_lines.remove(command[:-2])
        print("")
    

if sys.argv[1] == "resolution":
    zakljuci(sys.argv[2])
elif sys.argv[1] == "cooking":
    kuhaj(sys.argv[2], sys.argv[3])
