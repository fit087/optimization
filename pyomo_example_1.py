# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 09:53:28 2023

@author: WM522AX
"""

import pyomo.environ as pyo
# from pyomo.environ import *
from pyomo.opt import SolverFactory


#%%
model = pyo.ConcreteModel()

#%%

model.x = pyo.Var(bounds=(-float('inf'),3))
model.y = pyo.Var(bounds=(0,float('inf')))


x = model.x
y = model.y

model.C1 = pyo.Constraint(expr= x+y<=8)
model.C2 = pyo.Constraint(expr=(8*x+3*y>=-24))
model.C3 = pyo.Constraint(expr=(-6*x+8*y<=48))
model.C4 = pyo.Constraint(expr=(3*x+5*y<=15))

model.obj = pyo.Objective(expr=-4*x-2*y, sense=pyo.minimize)

print('scip = ', SolverFactory('scip').available() == True)
print('glpk = ', SolverFactory('glpk').available() == True)

solver_list = ['gurobi', 'scip', 'baron', 'ipopt', 'glpk', 'cbc', 'cplex']

available_sol = [s for s in solver_list if SolverFactory(s).available()]

for s in solver_list:
    print(f'{s} = ', SolverFactory(s).available() == True)
    
# opt = pyo.SolverFactory('glpk')
opt = pyo.SolverFactory('scip')
opt.solve(model)

model.pprint()

x_sol = pyo.value(x)
y_sol = pyo.value(y)

print('\n', '='*60, sep='')

print('x=', x_sol)
print('y=', y_sol)

#%%

# in python is there a way to plot the graphical representation of 
# linear programming problem done with pyomo?

# import matplotlib.pyplot as plt
# import numpy as np

# # Assuming you have a Pyomo model called 'model'

# # Extract the variable values from the Pyomo model
# x_values = np.array([model.x[i].value for i in model.x])
# y_values = np.array([model.y[i].value for i in model.y])

# # Ensure that the matplotlib backend is set correctly
# plt.switch_backend('TkAgg')

# # Plot the constraints (assuming there are two constraints)
# plt.plot([0, model.x[1].upper()], [model.c1.value, (-model.a[1].value*model.x[1].upper() + model.b.value)/model.a[2].value], 'r', label='Constraint 1')
# plt.plot([0, model.x[1].upper()], [model.c2.value, (-model.a[1].value

#%% Find Solvers availables
if False:
    import pyomo.environ as pyo
    from itertools import compress
    
    pyomo_solvers_list = pyo.SolverFactory.__dict__['_cls'].keys()
    solvers_filter = []
    for s in pyomo_solvers_list:
        try:
            solvers_filter.append(pyo.SolverFactory(s).available())
        # except (pyo.ApplicationError, NameError, ImportError) as e:
        # except (AttributeError, NameError, ImportError) as e:
        # except (NameError, ImportError) as e:
        except (Exception) as e:
            solvers_filter.append(False)
    pyomo_solvers_list = list(compress(pyomo_solvers_list,solvers_filter))

