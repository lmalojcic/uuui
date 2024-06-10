from queue import PriorityQueue
import sys
from collections import deque, defaultdict

#BFS
#algoritam preuzet iz predavanja
def bfs(file_name):
    print("# BFS")
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    filtered_lines = []
    for line in lines:
        if (line[0] != "#"and line != "\n"): #filtriranje komentara i praznih linija
            filtered_lines.append(line)
    s0 = filtered_lines[0].replace("\n", "")
    goal = filtered_lines[1].split(" ")
    goal[-1] = goal[-1].replace("\n", "")
    filtered_lines.pop(0)
    filtered_lines.pop(0)
    for i in range(len(filtered_lines)):
        filtered_lines[i] = filtered_lines[i].split(":")
        filtered_lines[i][1] = filtered_lines[i][1].split()
        for j in range(0, len(filtered_lines[i][1])):
            filtered_lines[i][1][j] = filtered_lines[i][1][j].replace("\n", "")
            filtered_lines[i][1][j] = filtered_lines[i][1][j].split(",")

    successors = {}
    for node, succs in filtered_lines: #izgradnja rjecnika za sljedbenike (sortirana abecednim redom)
        temp = []
        for succ in succs:
            temp.append(succ[0])
        temp.sort()
        successors[node] = temp
    path = {}
    found = False
    open_s = deque([s0])
    closed_s = set()
    while open_s != []: #provodjenje algoritma
        current = open_s.popleft()
        if (current in goal):
            found = True
            break
        if (current not in closed_s):
            closed_s.add(current)
            for succ in successors[current]:
                if (succ not in closed_s):
                    if (succ not in path):
                        path[succ] = current
                    open_s.append(succ)
    #ODREDJIVANJE PUTA
    path_length = 1
    length = 0
    path_print = current
    while (current != s0):
        last = path[current]
        path_print = last + " => " + path_print
        for line in filtered_lines:
                if (line[0] == last):
                    for succ in line[1]:
                        if (succ[0] == current):
                            length += int(succ[1])
                            path_length +=1
                    break
        current = last
    #ISPIS
    if found: 
        print("[FOUND_SOLUTION]: yes")  
        print("[STATES_VISITED]: " + str(len(closed_s) + 1))
        print("[PATH_LENGTH]: " + str(path_length))
        print("[TOTAL_COST]: " + "{:.1f}".format(length))
        print("[PATH]: " + path_print)
    else:
        print("[FOUND SOLUTION]: no")

#UCS
#algoritam preuzet iz predavanja
def ucs(file_name):
    print("# UCS")
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    filtered_lines = []
    for line in lines:
        if (line[0] != "#"): #filtriranje komentara
            filtered_lines.append(line)
    s0 = filtered_lines[0].replace("\n", "")
    goal = filtered_lines[1].split(" ")
    goal[-1] = goal[-1].replace("\n", "")
    filtered_lines.pop(0)
    filtered_lines.pop(0)
    for i in range(len(filtered_lines)):
        filtered_lines[i] = filtered_lines[i].split(":")
        filtered_lines[i][1] = filtered_lines[i][1].split()
        for j in range(0, len(filtered_lines[i][1])):
            filtered_lines[i][1][j] = filtered_lines[i][1][j].replace("\n", "")
            filtered_lines[i][1][j] = filtered_lines[i][1][j].split(",")
    successors = {}
    for node, succs in filtered_lines: #izgradnja rjecnika za sljedbenike pojedinog cvora
        successors[node] = [(succ[0], int(succ[1])) for succ in succs]

    path = defaultdict(lambda: ["default",sys.maxsize])
    found = False
    open_s = PriorityQueue()
    open_s.put((0, s0))
    closed_s = set()
    while open_s: #provodjenje algoritma
        currentCost, currentState = open_s.get()
        if (currentState in goal):
            found = True
            break
        if (currentState not in closed_s):
            closed_s.add(currentState)
            for succ, cost in successors[currentState]:
                if succ not in closed_s:
                    if (path[succ][1] > currentCost + cost):
                        path[succ] = [currentState, currentCost + cost]
                    open_s.put((currentCost + cost, succ))
    #ODREDJIVANJE PUTA             
    path_length = 1
    path_print = currentState
    current_temp = currentState
    while (current_temp != s0):
        last = path[current_temp][0]
        path_print = last + " => " + path_print
        for line in filtered_lines:
                if (line[0] == last):
                    for succ in line[1]:
                        if (succ[0] == current_temp):
                            path_length +=1
                    break
        current_temp = last
    #ISPIS
    if found: 
        print("[FOUND_SOLUTION]: yes")  
        print("[STATES_VISITED]: " + str(len(closed_s) + 1))
        print("[PATH_LENGTH]: " + str(path_length))
        print("[TOTAL_COST]: " + "{:.1f}".format(currentCost))
        print("[PATH]: " + path_print)
    else:
        print("[FOUND SOLUTION]: no")

#UCS ZA PROVJERU OPTIMISTICNOSTI
#ranija verzija drugog ucs, napisana prije optimizacija za vrijeme izvodjenja, ostavljena zato sto se izvodi dovoljno brzo
#nema koda za otvaranje datoteka i postavljanje pocetnog i ciljnih stanja
#vraca samo duljinu puta
def ucs_h(lines, s0, goal):
    path = {}
    found = False
    open_s = [[s0,0]]
    closed_s = []
    while open_s != []:
        current = open_s.pop(0)
        if (current[0] in goal):
            found = True
            break
        if (current[0] not in closed_s):
            closed_s.append(current[0])
            for line in lines:
                if (line[0] == current[0]):
                    for succ in line[1]:
                        if (succ[0] not in closed_s):
                            if ((succ[0] not in path) or (path[succ[0]][1] > (current[1]+int(succ[1])))):
                                path[succ[0]] = [current[0], current[1]+int(succ[1])]
                            open_s.append([succ[0], current[1]+int(succ[1])])
                    break
            #sortanje opena
            n = len(open_s)
            for i in range(n):
                for j in range(0, n-i-1):
                    if (open_s[j][1] > open_s[j+1][1]):
                        open_s[j], open_s[j+1] = open_s[j+1], open_s[j]
    if found:
        return current[1]
    else:
        return -1


#A-STAR
#algoritam preuzet iz predavanja
def astar(file_states, file_heuristic):
    print("# A_STAR " + file_heuristic)
    #OTVARANJE I FILTRIRANJE DATOTEKE SA STANJIMA
    f = open(file_states, "r")
    lines = f.readlines()
    f.close()
    filtered_lines = []
    for line in lines:
        if (line[0] != "#" and line != "\n"): #filtriranje komentara i praznih linija
            filtered_lines.append(line)
    s0 = filtered_lines[0].replace("\n", "")
    goal = filtered_lines[1].split(" ")
    goal[-1] = goal[-1].replace("\n", "")
    filtered_lines.pop(0)
    filtered_lines.pop(0)
    for i in range(len(filtered_lines)):
        filtered_lines[i] = filtered_lines[i].split(":")
        filtered_lines[i][1] = filtered_lines[i][1].split()
        for j in range(0, len(filtered_lines[i][1])):
            filtered_lines[i][1][j] = filtered_lines[i][1][j].replace("\n", "")
            filtered_lines[i][1][j] = filtered_lines[i][1][j].split(",")
    
    #OTVARANJE DATOTEKE S HEURISTIKOM
    f = open(file_heuristic, "r")
    lines = f.readlines()
    f.close()
    heuristic1 = []
    heuristic = {}
    for line in lines:
        if (line[0] != "#" and line != "\n"): #filtriranje komentara i praznih linija
            heuristic1.append(line)
    for i in range(len(heuristic1)):
        heuristic1[i] = heuristic1[i].split(":")
        heuristic[heuristic1[i][0]] = int(heuristic1[i][1].strip().replace("\n", ""))
    
    #PROVODJENJE ALGORITMA
    path = {}
    found = False
    open_s = [[s0,0,0]]
    closed_s = []
    while open_s != []:
        current = open_s.pop(0)
        if (current[0] in goal):
            found = True
            break
        if (current[0] not in closed_s):
            closed_s.append(current[0])
            for line in filtered_lines:
                if (line[0] == current[0]):
                    for succ in line[1]:
                        if (succ[0] not in closed_s):
                            if ((succ[0] not in path) or (path[succ[0]][1] > (current[1]+int(succ[1])))):
                                path[succ[0]] = [current[0], current[1]+int(succ[1])]
                            open_s.append([succ[0], current[1]+int(succ[1]), current[1]+int(succ[1]) + heuristic[succ[0]]])
                    break
            #sortanje opena (bubble sort)
            n = len(open_s)
            for i in range(n):
                for j in range(0, n-i-1):
                    if (open_s[j][2] > open_s[j+1][2]):
                        open_s[j], open_s[j+1] = open_s[j+1], open_s[j]
    path_length = 1
    path_print = current[0]
    current_temp = current[0]
    while (current_temp != s0):
        last = path[current_temp][0]
        path_print = last + " => " + path_print
        for line in filtered_lines:
                if (line[0] == last):
                    for succ in line[1]:
                        if (succ[0] == current_temp):
                            path_length +=1
                    break
        current_temp = last
    if found: 
        print("[FOUND_SOLUTION]: yes")  
        print("[STATES_VISITED]: " + str(len(closed_s) + 1))
        print("[PATH_LENGTH]: " + str(path_length))
        print("[TOTAL_COST]: " + "{:.1f}".format(current[1]))
        print("[PATH]: " + path_print)
    else:
        print("[FOUND SOLUTION]: no")


#PROVJERA OPTIMISTICNOSTI HEURISTIKE
def optimistic(file_states, file_heuristic):
    print("# HEURISTIC-OPTIMISTIC " + file_heuristic)
    #OTVARANJE DATOTEKE SA STANJIMA
    f = open(file_states, "r")
    lines = f.readlines()
    f.close()
    filtered_lines = []
    for line in lines:
        if (line[0] != "#" and line != "\n"): #filtriranje komentara i praznih linija
            filtered_lines.append(line)
    s0 = filtered_lines[0].replace("\n", "")
    goal = filtered_lines[1].split(" ")
    goal[-1] = goal[-1].replace("\n", "")
    filtered_lines.pop(0)
    filtered_lines.pop(0)
    for i in range(len(filtered_lines)):
        filtered_lines[i] = filtered_lines[i].split(":")
        filtered_lines[i][1] = filtered_lines[i][1].split()
        for j in range(0, len(filtered_lines[i][1])):
            filtered_lines[i][1][j] = filtered_lines[i][1][j].replace("\n", "")
            filtered_lines[i][1][j] = filtered_lines[i][1][j].split(",")
    
    #OTVARANJE DATOTEKE S HEURISTIKOM
    f = open(file_heuristic, "r")
    lines = f.readlines()
    f.close()
    heuristic = []
    for line in lines: #filtriranje komentara i praznih linija
        if (line[0] != "#" and line != "\n"):
            heuristic.append(line)
    for i in range(len(heuristic)):
        heuristic[i] = heuristic[i].split(":")
        heuristic[i][1] = int(heuristic[i][1].strip().replace("\n", ""))

    optimistic = True
    for case in heuristic:
        real_distance = ucs_h(filtered_lines, case[0], goal)
        if (case[1] <= real_distance):
            print("[CONDITION]: [OK] h(" +  case[0] + ") <= h*: " + "{:.1f}".format(case[1]) + " <= " + "{:.1f}".format(real_distance))
        else:
            optimistic = False
            print("[CONDITION]: [ERR] h(" +  case[0] + ") <= h*: " + "{:.1f}".format(case[1]) + " <= " + "{:.1f}".format(real_distance))
    if optimistic:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")


#PROVJERA KONZISTENTNOSTI HEURISTIKE
def consistent(file_states, file_heuristic):
    print("# HEURISTIC-CONSISTENT " + file_heuristic)
    #OTVARANJE DATOTEKE SA STANJIMA
    f = open(file_states, "r")
    lines = f.readlines()
    f.close()
    filtered_lines = []
    for line in lines:  #filtriranje komentara i praznih linija
        if (line[0] != "#" and line != "\n"):
            filtered_lines.append(line)
    s0 = filtered_lines[0].replace("\n", "")
    goal = filtered_lines[1].split(" ")
    goal[-1] = goal[-1].replace("\n", "")
    filtered_lines.pop(0)
    filtered_lines.pop(0)
    for i in range(len(filtered_lines)):
        filtered_lines[i] = filtered_lines[i].split(":")
        filtered_lines[i][1] = filtered_lines[i][1].split()
        for j in range(0, len(filtered_lines[i][1])):
            filtered_lines[i][1][j] = filtered_lines[i][1][j].replace("\n", "")
            filtered_lines[i][1][j] = filtered_lines[i][1][j].split(",")

    #OTVARANJE DATOTEKE S HEURISTIKOM
    f = open(file_heuristic, "r")
    lines = f.readlines()
    f.close()
    heuristic1 = []
    heuristic = {}
    for line in lines: #filtriranje komentara i praznih linija
        if (line[0] != "#" and line != "\n"):
            heuristic1.append(line)
    for i in range(len(heuristic1)):
        heuristic1[i] = heuristic1[i].split(":")
        heuristic[heuristic1[i][0]] = int(heuristic1[i][1].strip().replace("\n", ""))
    
    #PROVODJENJE ALGORITMA
    consistent = True
    for key in heuristic:
        for line in filtered_lines:
            if (line[0] == key):
                for follower in line[1]:
                    if (heuristic[key] <= (heuristic[follower[0]] + int(follower[1]))):
                        print("[CONDITION]: [OK] h(" + key + ") <= h(" + follower[0] + ") + c: " + "{:.1f}".format(heuristic[key]) + " <= " + "{:.1f}".format(heuristic[follower[0]]) + " + " + "{:.1f}".format(int(follower[1])))
                    else:
                        print("[CONDITION]: [ERR] h(" + key + ") <= h(" + follower[0] + ") + c: " + "{:.1f}".format(heuristic[key]) + " <= " + "{:.1f}".format(heuristic[follower[0]]) + " + " + "{:.1f}".format(int(follower[1])))
                        consistent = False
                break
    if consistent:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")

#CITANJE ARGUMENATA IZ POZIVA PROGRAMA
i = 1
check_consistent = False
check_optimistic = False
alg = ""
while (i < len(sys.argv)):
    if (sys.argv[i] == "--alg"):
        alg = sys.argv[i+1]
        i+=1
    elif(sys.argv[i] == "--ss"):
        file_states = sys.argv[i+1]
        i+=1
    elif(sys.argv[i] == "--h"):
        file_heuristic = sys.argv[i+1]
        i+=1
    elif(sys.argv[i] == "--check-optimistic"):
        check_optimistic = True
    elif(sys.argv[i] == "--check-consistent"):
        check_consistent = True
    i+=1
#ZVANJE ZADANOG ALGORITMA
if (alg == "bfs"):
    bfs(file_states)
elif(alg == "ucs"):
    ucs(file_states)
elif(alg == "astar"):
    astar(file_states, file_heuristic)
#ZVANJE POTREBNIH PROVJERA ZA HEURISTIKU
if check_optimistic:
    optimistic(file_states, file_heuristic)
if check_consistent:
    consistent(file_states, file_heuristic)