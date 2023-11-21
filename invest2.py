# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 21:05:27 2023

@author: WM522AX
"""

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

#%% Formulation
# Obj: Max \sum_{inv} R_{inv} = 5% C_a + 10% C_b + 12% C_c + 1e-6(C_d)^2
# Constraints
# C1: 0 <= C_c <= 10% T
# C2: 0 <= C_b <= 20% T
# C3: 0 <= C_d <= 30% T
# C4: \sum_{inv} C_{inv} = T

# model.obj = pyo.Objective(expr=0.05*C['A']+0.1*C['B']+0.12*C['C']+1e-6*C['D']**2, sense=pyo.maximize)
# C[A]= 70000.0
# C[B]= 20000.0
# C[C]= 10000.0
# C[D]= 0.0
# objfun= 6700.0

# model.obj = pyo.Objective(expr=pyo.summation(R), sense=pyo.maximize)

# C[A]= 40000.0
# C[B]= 20000.0
# C[C]= 10000.0
# C[D]= 30000.0
# objfun= 104100.000000001

#%% Constants
# T = 1e5

#%% Create a model and declare components
model = pyo.ConcreteModel()

#%% Instantiate the Model

model.setInv = pyo.Set(initialize=['A', 'B', 'C', 'D'])

model.T = 1e5

model.C = pyo.Var(model.setInv, bounds=(0, model.T))

model.R = pyo.Var(model.setInv, bounds=(0, model.T))

C=model.C
R=model.R
model.C1 = pyo.Constraint(expr= C['C']<=0.1*model.T)
model.C2 = pyo.Constraint(expr=(C['B']<=0.2*model.T))
model.C3 = pyo.Constraint(expr=(C['D']<=0.3*model.T))

model.C4 = pyo.Constraint(expr= R['A']==0.05*C['A'])
model.C5 = pyo.Constraint(expr= R['B']==0.1*C['B'])
model.C6 = pyo.Constraint(expr= R['C']==0.12*C['C'])
model.C7 = pyo.Constraint(expr= R['D']==1e-6*C['D']**2)

# C=model.C

model.C4 = pyo.Constraint(expr= pyo.summation(C)==model.T)

model.obj = pyo.Objective(expr=pyo.summation(R), sense=pyo.maximize)
# model.obj = pyo.Objective(expr=0.05*C['A']+0.1*C['B']+0.12*C['C']+1e-6*C['D']**2, sense=pyo.maximize)

#%% Apply Solver
# print('scip = ', SolverFactory('scip').available() == True)
# print('glpk = ', SolverFactory('glpk').available() == True)

# solver_list = ['gurobi', 'scip', 'baron', 'ipopt', 'glpk', 'cbc', 'cplex']

# available_sol = [s for s in solver_list if SolverFactory(s).available()]

# for s in solver_list:
#     print(f'{s} = ', SolverFactory(s).available() == True)
    
# opt = SolverFactory('glpk')
opt = pyo.SolverFactory('scip')
# opt = pyo.SolverFactory('cbc')
opt.solve(model)

#%% Interrogate Solver Results
model.pprint()

# x_sol = pyo.value(ca)
# y_sol = pyo.value(cb)
# z_sol = pyo.value(cc)


for i in model.setInv:
    print('C['+i+']=', pyo.value(model.C[i]))


print('objfun=', pyo.value(model.obj))