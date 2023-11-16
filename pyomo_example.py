# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 09:41:22 2023

@author: WM522AX
"""

import pyomo.environ as pyo
# from pyomo.environ import *
from pyomo.opt import SolverFactory


#%%
model = pyo.ConcreteModel()

#%%

model.x = pyo.Var(bounds=(0,10))
model.y = pyo.Var(bounds=(0,10))


x = model.x
y = model.y

model.C1 = pyo.Constraint(expr= -x+2*y<=8)
model.C2 = pyo.Constraint(expr=(2*x+y<=14))
model.C3 = pyo.Constraint(expr=(2*x-y<=10))

model.obj = pyo.Objective(expr=x+y, sense=pyo.maximize)

opt = pyo.SolverFactory('glpk')
opt.solve(model)

model.pprint()

x_sol = pyo.value(x)
y_sol = pyo.value(y)

print('x=', x_sol)
print('y=', y_sol)