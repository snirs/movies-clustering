import json
import csv
import random
import math
import itertools
import random


N = 6040        # NUM_OF_USERS
k = 3952        # NUM_OF_MOVIES

# --- Data Objects --- 

# -- movies
movies = csv.DictReader(
    open("movies.csv"),
    fieldnames=["MovieID", "Title", "Genres"])

# -- users
users = csv.DictReader(
    open("users.csv"),
    fieldnames=["UserID", "Gender", "Age", "Occupation", "Zip-code"])

# -- ratings
ratings = csv.DictReader(
    open("ratings.csv"),
    fieldnames=["UserId", "MovieId", "Rating", "Timestamp"])


# --- Extra Users Data ---

Occupation = {
    "0" :  "other" or None,
    "1" :  "academic/educator",
    "2" :  "artist",
    "3" :  "clerical/admin",
    "4" :  "college/grad student",
    "5" :  "customer service",
    "6" :  "doctor/health care",
    "7" :  "executive/managerial",
    "8" :  "farmer",
    "9" :  "homemaker",
    "10":  "K-12 student",
    "11":  "lawyer",
    "12":  "programmer",
    "13":  "retired",
    "14":  "sales/marketing",
    "15":  "scientist",
    "16":  "self-employed",
    "17":  "technician/engineer",
    "18":  "tradesman/craftsman",
    "19":  "unemployed",
    "20":  "writer"
}

ages = {
     "1"  : "Under 18",
	 "18" : "18-24",
	 "25" : "25-34",
	 "35" : "35-44",
	 "45" : "45-49",
	 "50" : "50-55",
	 "56" : "56+"
}


# len of each cell = ni (for p(m) computation)
movies_per_users = [set() for i in range(6040)]
for row in ratings:
    # movies_per_users[i] = watched list for user i
    movies_per_users[int(row['UserId'])-1].add(row['MovieId'])

# calc inner p(m)
def watched_sum(movieId):
    sum = 0
    for user in range (N) :
        ni = len(movies_per_users[user])
        user_saw_movie = 0
        if str(movieId) in movies_per_users[user]:
            user_saw_movie = 1
        sum = sum + ((2 / ni) * user_saw_movie)
    return sum


# calc inner p(m1, m2)
def watched_sum2(movieId1, movieId2):
    sum = 0
    for user in range (N) :
        ni = len(movies_per_users[user])
        user_saw_movie = 0
        if (str(movieId1) in movies_per_users[user]) and (str(movieId2) in movies_per_users[user]) :
            user_saw_movie = 1
        sum = sum + ((2 / (ni * (ni -1))) * user_saw_movie)
    return sum
    
# calc p(m)    
def movie_prob_1(movieId):
    p = 1 / (N + 1)
    pm = p * ( (2 / k) + watched_sum(movieId))
    return pm

# calc p(m1, m2)    
def movie_prob_2(movieId1, movieId2):
    p = 1 / (N + 1)
    pm = p * ( (2 / (k * (k - 1))) + watched_sum2(movieId1, movieId2))
    return pm



def correleted_check(m1, m2):
    return movie_prob_2(m1, m2) >= (movie_prob_1(m1) * movie_prob_1(m2)) 


def build_E(movie_subset):
    E_plus, E_minus = [], []
    for i1, m1 in enumerate(movie_subset):
        for i2, m2 in enumerate(movie_subset):
            if not m1 == m2:
                correleted = correleted_check(m1, m2)
                if (m2, m1) in E_plus or (m2, m1) in E_minus:
                    continue 
                if(correleted):
                    E_plus.append((m1, m2))
                else:
                    E_minus.append((m1, m2))
    return {"E_plus": E_plus, "E_minus": E_minus}

def CCPivot_Algorithm(V, E_plus, E_minus):
    i = random.choice(V)
    C, v_tag = [i], []
    for j in V:
        if not i == j:
            if (i, j) in E_plus or (j, i) in E_plus:
                C.append(j)
            else:
                v_tag.append(j)
    # print("C:", C)
    clusters.append(C)
    # print(clusters)
    if len(v_tag) == 0:
        return 
    CCPivot_Algorithm(v_tag, E_plus, E_minus)

def single_cost(movie):
    cost = math.log(1 / movie_prob_1(movie))
    print(f"single cost ({movie}): ", cost)
    return cost

def multi_cost(m1, m2, c_size):
    cost = (1 / (c_size -1) ) * (math.log(1 / movie_prob_2(m1, m2)))
    print(f"multi cost ({m1}, {m2}): ", cost)    
    return cost

def clusters_cost(clusters):
    total_cost = 0
    for cluster in clusters:
        if len(cluster) == 1:
            total_cost += single_cost(cluster[0])
        else:
            for movie_pair in itertools.combinations(cluster, 2):
                total_cost += multi_cost(movie_pair[0], movie_pair[1], len(cluster))
    print(total_cost)
    return total_cost

#Generate 5 random numbers between 10 and 30
randomlist = random.sample(range(2, 1000), 100)
print(randomlist)


V = randomlist
clusters = []

E = build_E(randomlist)
E_plus = E["E_plus"]
E_minus = E["E_minus"]
# print("E_plus:\n", E_plus, "\n")
# print("E_minus:\n", E_minus, "\n")
CCPivot_Algorithm(V, E_plus, E_minus)
print("clusters: ", clusters)
clusters_cost(clusters)




