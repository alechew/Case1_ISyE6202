import csv
import scipy.stats as stat
import numpy

demand = []                         # List of demand per year
amountFullfilledInAYear = []        # List of amount of demand/amount sold fulfilled per year
loss = []                           # list of loss per year.
serviceLevel = []                   # percentage of service level per year.

demandMean = 1000               # Demand mean per Day
demandStandardDev = 200 ** 2
basePeriod = 1                  # Base Period in Days
serviceTargetLevel = 0          # Service Target Level for Demand
zNormalValue = 0

mean = 365000
stdDev = 73000
capacity = 1466
numberDays = 364
orderToShipping = 1;

totalProductionYear = 1466 * 365
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
    global serviceTargetLevel
    global zNormalValue
    orderToShipping = input('Enter order to shipping time: ')
    serviceTargetLevel = float(input('Enter Service Target Level: '))
    zNormalValue = stat.norm.ppf(serviceTargetLevel)


# Robust Demand Satisfaction requirements during target lead time give target service level.
def calculate_capacity():
    demand_satisfaction_capacity = (demandMean * orderToShipping/basePeriod) \
                                 + (zNormalValue * numpy.math.sqrt(demandStandardDev * orderToShipping / basePeriod))
    return demand_satisfaction_capacity


ask_for_inputs()
capacity = calculate_capacity()
print (capacity)

for j in range(numberScenarios): #sample comment

    totalDemandinOneDay = 0
    totalDemandFullfilledInOneYear = 0
    totalLoss = 0

    for i in range(numberDays):

        salesLoss = 0
        generatedDailyDemand = round(numpy.random.normal(mean, stdDev), 0)

        if generatedDailyDemand > capacity:

            salesLoss = generatedDailyDemand - capacity
            demandFulfilled = capacity
            totalLoss += salesLoss                  # adding the loss for that day to the total loss of the year

        else:
            demandFulfilled = generatedDailyDemand

        totalDemandinOneDay += generatedDailyDemand                    # adding the total demand for the year
        totalDemandFullfilledInOneYear += demandFulfilled     # adding the total demand we were able to fulfill.

    demand.append(totalDemandinOneDay)
    amountFullfilledInAYear.append(totalDemandFullfilledInOneYear)
    loss.append(totalLoss)
    serviceLevel.append(totalDemandFullfilledInOneYear / totalDemandinOneDay)

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


