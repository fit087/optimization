# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 21:05:27 2023

@author: WM522AX
"""

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

#%% Formulation
# Obj: Max \sum_{inv} R_{inv} = 5% C_a + 10% C_b + 12% C_c
# Constraints
# C1: 0 <= C_c <= 10% T
# C2: 0 <= C_b <= 20% T
# C3: \sum_{inv} C_{inv} = T

#%% Constants
T = 1e5

#%% Create a model and declare components
model = pyo.ConcreteModel()


#%% Instantiate the Model
model.x = pyo.Var(bounds=(0,10))
model.y = pyo.Var(bounds=(0,10))


x = model.x
y = model.y

model.C1 = pyo.Constraint(expr= -x+2*y<=8)
model.C2 = pyo.Constraint(expr=(2*x+y<=14))
model.C3 = pyo.Constraint(expr=(2*x-y<=10))

model.obj = pyo.Objective(expr=x+y, sense=pyo.maximize)

print('scip = ', SolverFactory('scip').available() == True)
print('glpk = ', SolverFactory('glpk').available() == True)

solver_list = ['gurobi', 'scip', 'baron', 'ipopt', 'glpk', 'cbc', 'cplex']

available_sol = [s for s in solver_list if SolverFactory(s).available()]

for s in solver_list:
    print(f'{s} = ', SolverFactory(s).available() == True)
    
opt = SolverFactory('glpk')
# opt = pyo.SolverFactory('scip')
opt.solve(model)

model.pprint()

x_sol = pyo.value(x)
y_sol = pyo.value(y)

print('x=', x_sol)
print('y=', y_sol)

#%% Apply Solver


#%% Interrogate Solver Results