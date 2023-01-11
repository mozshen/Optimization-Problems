#%%

import pyomo.environ as pe
import numpy as np

#%%

def create_points(n_green, n_red, start, end):
    
    x= np.random.uniform(start[0], end[0], n_green)
    y= np.random.uniform(start[1], end[1], n_green)
    
    green_points= [(i, j) for i, j in zip(x, y)]
    
    x= np.random.uniform(start[0], end[0], n_red)
    y= np.random.uniform(start[1], end[1], n_red)
    
    red_points= [(i, j) for i, j in zip(x, y)]
    
    return {'green': green_points,
            'red': red_points
            }

#%%
    
n_green= np.random.randint(50, 200)
n_red= np.random.randint(50, 200)
start= (0, 0)
end= (20, 20)

points= create_points(n_green, n_red, start, end)

#%%

#basic parameters
model= pe.ConcreteModel()

model.R = pe.Var(bounds= (0, (start[1]+end[1])/ 2))

#data related to points
model.g= pe.Set(initialize= range(n_green))
model.r= pe.Set(initialize= range(n_red))

model.gf= pe.Var(model.g, within= 'Binary')
model.rf= pe.Var(model.r, within= 'Binary')

#%%

def point_distance(model, i):
    
    x0= (start[0]+ end[0])/ 2
    y0= (start[1]+ end[1])/ 2
    
    di= ((points['green'][i][0]- x0)**2+\
        (points['green'][i][1]- y0)**2)**0.5
    
    return di

model.gd= pe.Param(model.g, rule= point_distance)
model.rd= pe.Param(model.r, rule= point_distance)

#%%




