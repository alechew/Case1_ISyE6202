import csv

import numpy

demand = []             # List of demand per year
sales = []              # List of amount of demand/amount sold fulfilled per year
loss = []               # list of loss per year.
serviceLevel = []       # percentage of service level per year.

mean = 1000
stdDev = 200
capacity = 1466
numberDays = 364
totalProductionYear = 1466 * 365
numberScenarios = 100   # number of years we want to run.


def write_to_file(list_of_demand, list_of_loss, list_of_service_level):
    ofile = open('scenarios.csv', "wb")

    # writing the title of the columns
    row = "Scenarion #, Demand(Year), Production(Year), Sales Loss(Year), %Demand Satisfaction\n"
    ofile.write(row)

    totalProductionInAYear = str(totalProductionYear);
    for x in range(0, numberScenarios):
        row = str(x) + "," + str(list_of_demand[x]) + "," + totalProductionInAYear + "," + str(list_of_loss[x]) + "," + str(list_of_service_level[x]) + "\n"
        ofile.write(row)


for j in range(numberScenarios):

    totalDemand = 0
    totalDemandFulfilled = 0
    totalLoss = 0

    for i in range(numberDays):

        salesLoss = 0
        randomVar = round(numpy.random.normal(mean, stdDev), 0)

        if randomVar > capacity:

            salesLoss = randomVar - capacity
            demandFulfilled = capacity
            totalLoss += salesLoss                  # adding the loss for that day to the total loss of the day

        else:
            demandFulfilled = randomVar

        totalDemand += randomVar                    # adding the total demand for the year
        totalDemandFulfilled += demandFulfilled     # adding the total demand we were able to fulfill.

    demand.append(totalDemand)
    sales.append(totalDemandFulfilled)
    loss.append(totalLoss)
    serviceLevel.append(totalDemandFulfilled/totalDemand)

write_to_file(demand, loss, serviceLevel)




# for k in demand:
#     print(k)
#
# for k in sales:
#     print(k)
#
# for k in loss:
#     print(k)
#
# for k in serviceLevel:
#     print(k)


