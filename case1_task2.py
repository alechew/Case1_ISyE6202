import csv
import scipy.stats as stat
import numpy

demand = []                         # List of demand per year
amountFullfilledInAYear = []        # List of amount of demand/amount sold fulfilled per year
loss = []                           # list of loss per year.
serviceLevel = []                   # percentage of service level per year.

basePeriod = 1                  # Base Period in Days
serviceTargetLevel = 0.99          # Service Target Level for Demand
zNormalValue = zNormalValue = stat.norm.ppf(serviceTargetLevel)

mean = 1000
stdDev = 200
capacity = 1
numberPeriods = 1
orderToShipping = 1;

totalProductionYear = 1
numberScenarios = 100   # number of years we want to run.


def write_to_file(list_of_demand, list_of_loss, list_of_service_level):
    ofile = open('scenarios.csv', "wb")

    # writing the title of the columns
    row = "Scenarion #, Demand(Year), Production(Year), Sales Loss(Year), %Demand Satisfaction\n"
    ofile.write(row)

    totalProductionInAYear = str(totalProductionYear);
    for x in range(0, numberScenarios):
        row = str(x + 1) + "," + str(list_of_demand[x]) + "," + totalProductionInAYear + "," + str(list_of_loss[x]) + "," + str(list_of_service_level[x]) + "\n"
        ofile.write(row)


def ask_for_inputs():
    global orderToShipping
    orderToShipping = input('Enter order to shipping time: ')
    # serviceTargetLevel = float(input('Enter Service Target Level: '))


# Robust Demand Satisfaction requirements during target lead time give target service level.
def calculate_capacity():
    demand_satisfaction_capacity = (mean * orderToShipping/basePeriod) \
                                 + (zNormalValue * numpy.math.sqrt(stdDev * orderToShipping / basePeriod))
    return demand_satisfaction_capacity


ask_for_inputs()
capacity = calculate_capacity()
numberPeriods = int(round(365 / orderToShipping))
totalProductionYear = capacity * numberPeriods

print (capacity)

for j in range(numberScenarios): #sample comment

    totalDemandinPeriod = 0
    totalDemandFullfilledInOneYear = 0
    totalLoss = 0

    for i in range(numberPeriods):

        salesLoss = 0
        generatedPeriodDemand = orderToShipping * round(numpy.random.normal(mean, stdDev), 0)
        print("Generated period demand " + str(generatedPeriodDemand))
        if generatedPeriodDemand > capacity:

            salesLoss = generatedPeriodDemand - capacity
            demandFulfilled = capacity
            totalLoss += salesLoss                  # adding the loss for that day to the total loss of the year

        else:
            demandFulfilled = generatedPeriodDemand

        totalDemandinPeriod += generatedPeriodDemand                    # adding the total demand for the year
        totalDemandFullfilledInOneYear += demandFulfilled     # adding the total demand we were able to fulfill.

    demand.append(totalDemandinPeriod)
    amountFullfilledInAYear.append(totalDemandFullfilledInOneYear)
    loss.append(totalLoss)
    serviceLevel.append(totalDemandFullfilledInOneYear / totalDemandinPeriod)

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


