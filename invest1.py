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
model.ca = pyo.Var(bounds=(0, T))
model.cb = pyo.Var(bounds=(0, 0.2*T))
model.cc = pyo.Var(bounds=(0, 0.1*T))

ca = model.ca
cb = model.cb
cc = model.cc

model.C1 = pyo.Constraint(expr= ca+cb+cc==T)

model.obj = pyo.Objective(expr=0.05*ca+0.1*cb+0.12*cc, sense=pyo.maximize)

#%% Apply Solver
print('scip = ', SolverFactory('scip').available() == True)
print('glpk = ', SolverFactory('glpk').available() == True)

solver_list = ['gurobi', 'scip', 'baron', 'ipopt', 'glpk', 'cbc', 'cplex']

available_sol = [s for s in solver_list if SolverFactory(s).available()]

for s in solver_list:
    print(f'{s} = ', SolverFactory(s).available() == True)
    
opt = SolverFactory('glpk')
# opt = pyo.SolverFactory('scip')
opt.solve(model)

#%% Interrogate Solver Results
model.pprint()

x_sol = pyo.value(ca)
y_sol = pyo.value(cb)
z_sol = pyo.value(cc)

print('x=', x_sol)
print('y=', y_sol)
print('y=', z_sol)

print('objfun=', pyo.value(model.obj))