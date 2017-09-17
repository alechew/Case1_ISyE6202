import csv

import numpy

demand = []
sales = []
loss = []
serviceLevel = []

mean = 1000
stdDev = 200
capacity = 1466
numberDays = 364
numberScenarios = 2

for j in range(numberScenarios):

    totalDemand = 0
    totalDemandFulfilled = 0
    totalLoss = 0

    for i in range(numberDays):

        randomVar = round(numpy.random.normal(mean, stdDev), 0)

        if randomVar > capacity:

            salesLoss=randomVar-capacity
            demandFulfilled=capacity

        else:

            salesLoss = 0
            demandFulfilled=randomVar

        totalDemand=totalDemand+randomVar

        totalLoss=totalLoss+salesLoss

        totalDemandFulfilled=totalDemandFulfilled+demandFulfilled

    demand.append(totalDemand)
    sales.append(totalDemandFulfilled)
    loss.append(totalLoss)
    serviceLevel.append(totalDemandFulfilled/totalDemand)

for k in demand:
    print(k)

for k in sales:
    print(k)

for k in loss:
    print(k)

for k in serviceLevel:
    print(k)
