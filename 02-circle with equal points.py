#%%

import pyomo.environ as pe
import numpy as np
import matplotlib.pyplot as plt

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
    
n_green= np.random.randint(100, 300)
n_red= np.random.randint(100, 300)
start= (0, 0)
end= (200, 200)

points= create_points(n_green, n_red, start, end)

#%%

#basic parameters
model= pe.ConcreteModel()

model.R = pe.Var(bounds= (0, (start[1]+ end[1])/ 2))

#data related to points
model.g= pe.Set(initialize= range(n_green))
model.r= pe.Set(initialize= range(n_red))

model.gf= pe.Var(model.g, within= pe.Binary)
model.rf= pe.Var(model.r, within= pe.Binary)

#%%

def green_point_distance(model, i):
    
    x0= (start[0]+ end[0])/ 2
    y0= (start[1]+ end[1])/ 2
    
    di= ((points['green'][i][0]- x0)**2+\
        (points['green'][i][1]- y0)**2)**0.5
    
    return di

model.gd= pe.Param(model.g, rule= green_point_distance)

def red_point_distance(model, i):
    
    x0= (start[0]+ end[0])/ 2
    y0= (start[1]+ end[1])/ 2
    
    di= ((points['red'][i][0]- x0)**2+\
        (points['red'][i][1]- y0)**2)**0.5
    
    return di

model.rd= pe.Param(model.r, rule= red_point_distance)

model.gd_positive= pe.Var(model.g, within= pe.PositiveReals)
model.gd_negative= pe.Var(model.g, within= pe.PositiveReals)

model.rd_positive= pe.Var(model.r, within= pe.PositiveReals)
model.rd_negative= pe.Var(model.r, within= pe.PositiveReals)

#%%

def gdi(model, i):
    return model.gd[i]- model.R== model.gd_positive[i]- model.gd_negative[i]

model.greensdistancerule = pe.Constraint(model.g, rule=gdi)

#%%

def rdi(model, i):
    return model.rd[i]- model.R== model.rd_positive[i]- model.rd_negative[i]

model.redsdistancerule = pe.Constraint(model.r, rule=rdi)

#%%

def gdi_limit_negative(model, i):
    return end[1]* model.gf[i]>= model.gd_negative[i]

def gdi_limit_positive(model, i):
    return end[1]* (1- model.gf[i])>= model.gd_positive[i]

model.greenincircle1 = pe.Constraint(model.g, rule=gdi_limit_negative)
model.greenincircle2 = pe.Constraint(model.g, rule=gdi_limit_positive)

#%%

def rdi_limit_negative(model, i):
    return end[1]* model.rf[i]>= model.rd_negative[i]

def rdi_limit_positive(model, i):
    return end[1]* (1- model.rf[i])>= model.rd_positive[i]

model.redincircle1 = pe.Constraint(model.r, rule=rdi_limit_negative)
model.redincircle2 = pe.Constraint(model.r, rule=rdi_limit_positive)

#%%

def equalredgreen(model):
    return sum([model.gf[i] for i in model.g])== sum([model.rf[i] for i in model.r])
    
model.equalredgreen = pe.Constraint(rule= equalredgreen)
    
#%%

def model_objective(model):
    return model.R

model.obj = pe.Objective(rule=model_objective, sense=pe.maximize)

#%%

import os
solver= pe.SolverFactory('glpk', executable= os.getcwd()+ '\\glpk-4.65\\w64\\glpsol')
results= solver.solve(model)

#%%

if (results.solver.status == pe.SolverStatus.ok) and (results.solver.termination_condition == pe.TerminationCondition.optimal):
    print('feasible')
elif (results.solver.termination_condition == pe.TerminationCondition.infeasible):
    print('infeasible')
else:
    print ('Solver Status:',  results.solver.status)

print('Objective:', model.R.value)

#%%

x0= (start[0]+ end[0])/ 2
y0= (start[1]+ end[1])/ 2
r= model.R.value

#%%

theta = np.linspace(0,2*np.pi,100)
X= x0+r*np.cos(theta)
Y= y0+r*np.sin(theta)

plt.figure(figsize= (5, 5))
plt.plot(X, Y, c='blue', lw=1, alpha = 1)

plt.scatter([x[0] for x in points['green']],
            [x[1] for x in points['green']],
            color= 'green')

plt.scatter([x[0] for x in points['red']],
            [x[1] for x in points['red']],
            color= 'red')

plt.xlim((start[0], end[0]))
plt.ylim((start[1], end[1]))
#%%

results.write()