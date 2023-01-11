#%%

import numpy as np
import pulp
import pandas as pd

#%%

def create_points(n_green, n_red, start, end):
    
    x= np.random.uniform(start[0], end[0], n_green)
    y= np.random.uniform(start[1], end[1], n_green)
    
    green_points= [(i, j) for i, j in zip(x, y)]
    
    x= np.random.uniform(start[0], end[0], n_red)
    y= np.random.uniform(start[1], end[1], n_red)
    
    red_points= [(i, j) for i, j in zip(x, y)]
    
    return green_points, red_points

#%%
    
n_green= np.random.randint(50, 200)
n_red= np.random.randint(50, 200)
start= (0, 0)
end= (100, 20)
points= create_points(n_green, n_red, start, end)
#mid_line= 0.3* (start[1]+ end[1])/ 2
mid_line= 2
#%%

problem = pulp.LpProblem('two_lines', pulp.LpMinimize)

R= pulp.LpVariable.dicts('R',\
                         indices= range(n_red),\
                         cat= 'Binary')

G= pulp.LpVariable.dicts('G',\
                         indices= range(n_green),\
                         cat= 'Binary')

delta_x= pulp.LpVariable('delta', start[1], end[1])

#%%


problem+=\
    (
    pulp.lpSum([R[i] for i in R])== pulp.lpSum([G[i] for i in G]),
    'equal red and green'    
    )

#%%

d_R_positive= pulp.LpVariable.dicts('d_R_positive',\
                         indices= range(n_red),\
                         lowBound=0
                             )

d_R_negetive= pulp.LpVariable.dicts('d_R_negetive',\
                         indices= range(n_red),\
                         lowBound=0
                             )

d_G_positive= pulp.LpVariable.dicts('d_G_positive',\
                         indices= range(n_green),\
                         lowBound=0
                             )

d_G_negetive= pulp.LpVariable.dicts('d_G_negetive',\
                         indices= range(n_green),\
                         lowBound=0
                         )


#%%

#greens
for i in range(len(points[0])):
    
    problem+=\
        (mid_line+ delta_x)- points[0][i][1]== d_G_positive[i]- d_G_negetive[i]
        
    problem+=\
        end[1]* G[i]>= d_G_positive[i]
    
    problem+=\
        end[1]* (1- G[i])>= d_G_negetive[i]

#reds
for i in range(len(points[1])):
    
    problem+=\
        (mid_line+ delta_x)- points[1][i][1]== d_R_positive[i]- d_R_negetive[i]
        
    problem+=\
        end[1]* R[i]>= d_R_positive[i]
        
    problem+=\
        end[1]* (1- R[i])>= d_R_negetive[i]


#%%

problem+= mid_line+ delta_x

#%%

#solver = pulp.getSolver(solver='PULP_CBC_CMD', msg=1, timeLimit=30, gapRel=0.0001, gapAbs=0)
print(problem.solve())
print(pulp.value(problem.objective))
Z= pulp.value(problem.objective)

#%%

import matplotlib.pyplot as plt

plt.scatter([x[0] for x in points[0]],
            [x[1] for x in points[0]],
            color= 'green')

plt.scatter([x[0] for x in points[1]],
            [x[1] for x in points[1]],
            color= 'red')

plt.hlines(y= pulp.value(problem.objective), xmin= start[0], xmax= end[0])

#%%

points_G= []
for i in G:
    points_G.append(
                  {'G':  G[i].varValue,
                  'point': (points[0][i]), 
                  'd_G_positive': d_G_positive[i].varValue,
                  'd_G_negetive': d_G_negetive[i].varValue,
                  'Z': Z}
)
points_G= pd.DataFrame(points_G)



points_R= []
for i in R:
    points_R.append(
                  {'R':  R[i].varValue,
                  'point': (points[1][i]), 
                  'd_R_positive': d_R_positive[i].varValue,
                  'd_R_negetive': d_R_negetive[i].varValue,
                  'Z': Z}
)
points_R= pd.DataFrame(points_R)

#%%
