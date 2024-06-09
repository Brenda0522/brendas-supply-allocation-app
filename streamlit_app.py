import streamlit as st
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np

st.set_page_config(page_title = 'Superman Plus Supply Allocation')

# User input
# w1 through w5 are the relative weights for the 5 channels
# w6 through w10 are the same weights but delayed for 2 weeks
st.write('Please choose importance (will allocate based on the importance ratio between channels):')
online = st.slider(label = 'Online Store', min_value = 0, max_value = 10, value = 10)
retail = st.slider(label = 'Retail Store', min_value = 0, max_value = 10, value = 10)
resell = st.slider(label = 'Reseller Partners', min_value = 0, max_value = 10, value = 10)
col1, col2 = st.columns(2)
with col2:
    amr = st.slider(label = 'AMR', min_value = 0, max_value = 10, value = 10)
    eu = st.slider(label = 'Europe', min_value = 0, max_value = 10, value = 10)
    pac = st.slider(label = 'PAC', min_value = 0, max_value = 10, value = 10)
w1 = float(online)
w2 = float(retail)
if amr + eu + pac == 0:
    w3, w4, w5 = 0., 0., 0.
else:
    w3 = float(amr) / (amr + eu + pac) * resell
    w4 = float(eu) / (amr + eu + pac) * resell
    w5 = float(pac) / (amr + eu + pac) * resell

st.header('')

st.write('Please choose importance multiplier if product is delayed for 2 weeks:')
if st.checkbox('Separate multiplier for channels/customers'):
    w6 = w1 * st.slider(label = 'Online Store', min_value = 1, max_value = 10, value = 2)
    w7 = w2 * st.slider(label = 'Retail Store', min_value = 1, max_value = 10, value = 2)
    w8 = w3 * st.slider(label = 'AMR Reseller', min_value = 1, max_value = 10, value = 2)
    w9 = w4 * st.slider(label = 'Europe Reseller', min_value = 1, max_value = 10, value = 2)
    w10 = w5 * st.slider(label = 'PAC Reseller', min_value = 1, max_value = 10, value = 2)
else:
    k = st.slider(label = 'Importance Multiplier', min_value = 1, max_value = 10, value = 2)
    w6 = k * w1
    w7 = k * w2
    w8 = k * w3
    w9 = k * w4
    w10 = k * w5


# Create a new model
m = gp.Model()

# Create variables
x1  = m.addVar(vtype = GRB.CONTINUOUS, name = "x1")
x2  = m.addVar(vtype = GRB.CONTINUOUS, name = "x2")
x3  = m.addVar(vtype = GRB.CONTINUOUS, name = "x3")
x4  = m.addVar(vtype = GRB.CONTINUOUS, name = "x4")
x5  = m.addVar(vtype = GRB.CONTINUOUS, name = "x5")
x6  = m.addVar(vtype = GRB.CONTINUOUS, name = "x6")
x7  = m.addVar(vtype = GRB.CONTINUOUS, name = "x7")
x8  = m.addVar(vtype = GRB.CONTINUOUS, name = "x8")
x9  = m.addVar(vtype = GRB.CONTINUOUS, name = "x9")
x10 = m.addVar(vtype = GRB.CONTINUOUS, name = "x10")
x11 = m.addVar(vtype = GRB.CONTINUOUS, name = "x11")
x12 = m.addVar(vtype = GRB.CONTINUOUS, name = "x12")
x13 = m.addVar(vtype = GRB.CONTINUOUS, name = "x13")
x14 = m.addVar(vtype = GRB.CONTINUOUS, name = "x14")
x15 = m.addVar(vtype = GRB.CONTINUOUS, name = "x15")

# Set objective
m.setObjective(w1 * (20 - x1 - x11) + w2 * (15 - x2 - x12) + w3 * (10 - x3 - x13) + w4 * (10 - x4 - x14) * w5 * (10 - x5 - x15) + w6 * (10 - x1 - x6) + w7 * (10 - x2 - x7) + w8 * (5 - x3 - x8) + w9 * (5 - x4 - x9) + w10 * (5 - x5 - x10), GRB.MINIMIZE)

# Add constraints
m.addConstr(x1  >= 0)
m.addConstr(x2  >= 0)
m.addConstr(x3  >= 0)
m.addConstr(x4  >= 0)
m.addConstr(x5  >= 0)
m.addConstr(x6  >= 0)
m.addConstr(x7  >= 0)
m.addConstr(x8  >= 0)
m.addConstr(x9  >= 0)
m.addConstr(x10 >= 0)
m.addConstr(x11 >= 0)
m.addConstr(x12 >= 0)
m.addConstr(x13 >= 0)
m.addConstr(x14 >= 0)
m.addConstr(x15 >= 0)
m.addConstr(x1  <= 10)
m.addConstr(x2  <= 10)
m.addConstr(x3  <= 5)
m.addConstr(x4  <= 5)
m.addConstr(x5  <= 5)
m.addConstr(x6  <= 10 - x1)
m.addConstr(x7  <= 10 - x2)
m.addConstr(x8  <= 5 - x3)
m.addConstr(x9  <= 5 - x4)
m.addConstr(x10 == 5 - x5) # must supply for any remaining demand from PAC reseller from wk3 for promotion
m.addConstr(x11 <= 10)
m.addConstr(x12 <= 5)
m.addConstr(x13 <= 5)
m.addConstr(x14 <= 5)
m.addConstr(x15 == 5) # wk4 allocation for PAC must be 5 for promotion
m.addConstr(x1 + x2 + x3 + x4 + x5 == 25)
m.addConstr(x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 == 30)

# Optimize model
m.optimize()

# Save results
x = []
if m.status == GRB.Status.OPTIMAL:
    for v in m.getVars():
        x.append(round(v.X, 2))
    # st.write(f'Optimal Value: {m.ObjVal}')
elif m.status == GRB.Status.INFEASIBLE:
    st.write('The model is infeasible.')
# st.write(x)

# Create DataFrames for results
allocation = pd.DataFrame(index = ['Online Store', 'Retail Store', 'Reseller Partners', 'AMR', 'Europe', 'PAC'], columns = ['Jan Wk2', 'Jan Wk3', 'Jan Wk4', 'Jan Wk5'])
allocation['Jan Wk2'] = [20, 15, 50, 20, 5, 25]
allocation['Jan Wk3'] = [x[0], x[1], x[2] + x[3] + x[4], x[2], x[3], x[4]]
allocation['Jan Wk4'] = [x[5] + x[10], x[6] + x[11], x[7] + x[8] + x[9] + x[12] + x[13] + x[14], x[7] + x[12], x[8] + x[13], x[9] + x[14]]
allocation['Jan Wk5'] = [50, 35, 90, 35, 15, 40] - allocation['Jan Wk2'] - allocation['Jan Wk3'] - allocation['Jan Wk4']

d = np.array([[20, 10, 10, 10],
              [15, 10, 5, 5],
              [50, 15, 15, 10],
              [20, 5, 5, 5],
              [5, 5, 5, 0],
              [25, 5, 5, 5]])
demand = pd.DataFrame(data = d, index = ['Online Store', 'Retail Store', 'Reseller Partners', 'AMR', 'Europe', 'PAC'], columns = ['Jan Wk2', 'Jan Wk3', 'Jan Wk4', 'Jan Wk5'])

# Display results
st.write('Allocation plan')
allocation
st.write('Demand ask')
demand
st.write('Forecasted shortage delta')
demand - allocation
