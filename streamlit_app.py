import streamlit as st
import gurobipy as gp
from gurobipy import GRB

# User input
w1, w2, w3 = 2, 3, 5
k = 2

# Create a new model
m = gp.Model()

# Create variables
x1 = m.addVar(vtype = GRB.CONTINUOUS, name = "x1")
x2 = m.addVar(vtype = GRB.CONTINUOUS, name = "x2")
x3 = m.addVar(vtype = GRB.CONTINUOUS, name = "x3")
x4 = m.addVar(vtype = GRB.CONTINUOUS, name = "x4")
x5 = m.addVar(vtype = GRB.CONTINUOUS, name = "x5")
x6 = m.addVar(vtype = GRB.CONTINUOUS, name = "x6")
x7 = m.addVar(vtype = GRB.CONTINUOUS, name = "x7")
x8 = m.addVar(vtype = GRB.CONTINUOUS, name = "x8")
x9 = m.addVar(vtype = GRB.CONTINUOUS, name = "x9")

# Set objective
m.setObjective(w1 * (20 - x1 - x7) + w2 * (20 - x2 - x8) + w3 * (30 - x3 - x9) + k * w1 * (10 - x1 - x4) + k * w2 * (10 - x2 - x5) + k * w3 * (15 - x3 - x6), GRB.MINIMIZE)

# Add constraints
m.addConstr(x1 >= 0)
m.addConstr(x2 >= 0)
m.addConstr(x3 >= 0)
m.addConstr(x4 >= 0)
m.addConstr(x5 >= 0)
m.addConstr(x6 >= 0)
m.addConstr(x7 >= 0)
m.addConstr(x8 >= 0)
m.addConstr(x9 >= 0)
m.addConstr(x1 <= 10)
m.addConstr(x2 <= 10)
m.addConstr(x3 <= 15)
m.addConstr(x4 <= 10 - x1)
m.addConstr(x5 <= 10 - x2)
m.addConstr(x6 <= 15 - x3)
m.addConstr(x7 <= 10)
m.addConstr(x8 <= 5)
m.addConstr(x9 <= 15)
m.addConstr(x1 + x2 + x3 <= 25)
m.addConstr(x4 + x5 + x6 + x7 + x8 + x9 <= 30)

# Optimize model
m.optimize()

# Display results
if m.status == GRB.Status.OPTIMAL:
    for v in m.getVars():
        print(f'{v.VarName} {v.X}')
    print(f'Optimal Value: {m.ObjVal}')
elif m.status == GRB.Status.INFEASIBLE:
    print('The model is infeasible.')
