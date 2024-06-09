# Brenda’s Supply Allocation APP

Welcome to Brenda’s supply allocation app! This app assists you in creating an effective supply allocation plan based on the relative importance of sales channels when there is a shortage of product.

## APP Instructions

Move the sliders to set the relative importance of the three main sales channels/customers: online store, retail store, and reseller partners. Once you've set the importance for the reseller partner channel, distribute this importance among three regions (AMR, Europe, PAC). (Example: If you choose 4 for online store, 3 for retail store, 7 for retail partner, 1 for AMR, 2 for Europe, and 4 for PAC, then the final importance ratio between the 5 total channels will be 4:3:1:2:4. The importance of 7 for retail partner is shared among the three regions.)

Use an additional slider to adjust the importance multiplier in cases when the product is delayed for 2 or more weeks, which might impact customer retention. You can also use the checkbox to enable different importance multipliers for the 5 channels.

The app will use the relative importance you selected and calculate an optimal supply allocation strategy for you. The allocation plan table shows the exact quantities to allocate, the demand ask table shows the actual demand ask, and the forecasted shortage delta table shows the incremental change in shortage. 

## Code flow

Display sliders for users to input the relative importance of channels and regions.

Convert these slider inputs into weights for the optimization solver.

Create an optimization model, define the decision variables, set the optimization cost function, and lay out the constraints. The optimization solver automatically generates the optimal supply allocation plan based on the information above.

Generate and display tables based on the optimized allocation plan on the app’s webpage.
