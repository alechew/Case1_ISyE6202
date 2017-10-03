import Classes
import numpy
import random
import statistics

"""
    calculates the Estimate 2018 - 2023 demand satisfaction capacity requirements according to task2 Assumptions
    promising 15, 7, 5, 2 or 1 day-s for order-to-shipping time and service levels of 99%, 99.5% vs. 99.9%.
"""

filename = ""

yearName = ["2018", "2019", "2020", "2021", "2022", "2023"]
yearsOfGrowth = 5
dayName = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

factorySpecifications = Classes.FactorySpecificationsTask2
leadTimes = [15, 7, 5, 2, 1]

demandDistribution = Classes.DemandVar(365000, 73000)
growthYearlyDemand = []     # this can be said is the mean of every new year demand
growthStandardDeviation = []    # this can be said is the standardDeviation of every new year demand
yearlyDemand = []       # generated random demand from the calculated yearly mean demands.
dailyCapacityRequirements = []
yearlyBetas = []
yearlyPConstraints = [0.5, 0.714285714, 0.6, 0.6, 0.588235294, 0.65, 0.555555556]
yearlyTriangularMin = [0.10, 0.08, 0.06, 0.0, -0.1]
yearlyTriangularAvg = [0.20, 0.20, 0.15, 0.15, 0.12]
yearlyTriangularMax = [0.25, 0.25, 0.20, 0.20, 0.20]

totalDaysInYear = 364
years = 6
weeks = 52
days = 7
weeklyDemandAverage = [0.004612546,0.004612546,
0.005535055,0.006457565,0.006457565,0.013837638,0.032287823,0.006457565,0.006457565,0.008302583,0.008302583,0.009225092,
0.009225092,0.011070111,0.011070111,0.012915129,0.013837638,0.014760148,0.016605166,0.018450185,0.020295203,0.020295203,
0.022140221,0.023062731,0.031365314,0.036900369,0.036900369,0.009225092,0.009225092,0.009225092,0.009225092,0.023062731,
0.027675277,0.036900369,0.036900369,0.027675277,0.025830258,0.023062731,0.018450185,0.018450185,0.009225092,0.009225092,
0.009225092,0.009225092,0.009225092,0.009225092,0.064575646,0.027675277,0.027675277,0.036900369,0.064575646,0.036900369]
weeklyDemandStandardDeviation = [0.000138376,0.000138376,
0.000166052,0.000193727,0.000193727,0.000415129,0.000968635,0.000193727,0.000193727,0.000249077,0.000249077,0.000276753,
0.000276753,0.000332103,0.000332103,0.000387454,0.000415129,0.000442804,0.000498155,0.000553506,0.000608856,0.000608856,
0.000664207,0.000691882,0.000940959,0.001107011,0.001107011,0.000276753,0.000276753,0.000276753,0.000276753,0.000691882,
0.000830258,0.001107011,0.001107011,0.000830258,0.000774908,0.000691882,0.000553506,0.000553506,0.000276753,0.000276753,
0.000276753,0.000276753,0.000276753,0.000276753,0.001937269,0.000830258,0.000830258,0.001107011,0.001937269,0.001107011]
pConstraints = [0.5, 0.714285714, 0.6, 0.6, 0.588235294, 0.65, 0.555555556]
triangularMin = [0.04, 0.05, 0.06, 0.1, 0.08, 0.05, 0.02]
triangularAvg = [0.08, 0.1, 0.12, 0.22, 0.18, 0.18, 0.12]
triangularMax = [0.12, 0.12, 0.16, 0.30, 0.25, 0.25, 0.20]

weeklyDemand = []
dailyDemandList = []


def calculate_daily_capacity():
    """"Calculates the daily capacity based on the mean and standard deviation from the random generated
        daily demand following task 2 assumptions."""

    global filename
    leadTime = input("Enter Lead Time")
    serviceLevel = input("Enter Service Level")
    filename = "Lead_Time_" + str(leadTime) + "Service_Level" + str(serviceLevel)

    factorySpecifications = Classes.FactorySpecificationsTask2(leadTimes, growthYearlyDemand,
                                                             growthStandardDeviation, serviceLevel, leadTime)
    factorySpecifications.set_lead_time(leadTime)

    for x in range(len(factorySpecifications.yearlyDemandRequirements)):
        leftSide = (factorySpecifications.yearlyDemandRequirements[x] * factorySpecifications.leadTime / totalDaysInYear)
        valueInsideSqrt = pow(factorySpecifications.yearlyStandardDeviations[x], 2) * (15/float(totalDaysInYear))
        dailyCapacity = (leftSide + factorySpecifications.zNormalValue * numpy.sqrt(valueInsideSqrt)) / factorySpecifications.leadTime

        dailyCapacityRequirements.append(int(dailyCapacity))
    factorySpecifications.dailyCapacity = dailyCapacityRequirements
    return factorySpecifications


def calculate_year_growth_demand(iterations):
    """calculates the yearly mean and standard deviation considering the demand growth
        triangular distribution"""

    for i in range(iterations):
        yearDemand = 0
        yearDeviation = 0
        if i == 0:
            yearDemand = 365000
            yearDeviation = 73000
            growthYearlyDemand.append(365000)
            growthStandardDeviation.append(73000)
        else:
            yearDemand = growthYearlyDemand[i - 1]
            yearDeviation = growthStandardDeviation[i -1]

        p = random.uniform(0, 1)
        raw = 0
        if p <= yearlyPConstraints[i]:
            raw = triangularMin[i] \
                  + numpy.math.sqrt(p * (yearlyTriangularMax[i] - yearlyTriangularMin[i]) * (yearlyTriangularAvg[i] - yearlyTriangularMin[i]))
        else:
            raw = triangularMax[i] \
                  - numpy.math.sqrt(
                (1 - p) * (yearlyTriangularMax[i] - yearlyTriangularMin[i]) * (yearlyTriangularMax[i] - yearlyTriangularAvg[i]))

        yearlyBetas.append(raw)
        newYearDemand = (1 + raw) * yearDemand
        growthYearlyDemand.append(newYearDemand)
        newStandardDeviation = (1 + raw) * yearDeviation
        growthStandardDeviation.append(newStandardDeviation)


def write_to_file():
    """writes on a CSV value the randomly generated daily demands from year 2018 to 2023
    """
    ofile = open(filename + "_Generated-Random-Demand.csv", "wb")

    # writing the title of the columns
    row = "Year,Week,Day,Demand\n"
    ofile.write(row)

    for i in range(0, len(dailyDemandList), 1):
        day = dailyDemandList[i]
        if isinstance(day, Classes.DailyDemand):
            row = day.year + "," + day.week + "," + day.day + "," + str(day.dailyDemand) + "\n"
        ofile.write(row)
    ofile.close()


def generate_beta(index):
    """generates weekly demand ratio following normal distribution with
     mean and standard deviation for its respective year"""

    return numpy.random.normal(weeklyDemandAverage[index], weeklyDemandStandardDeviation[index])


def generate_raw(index):
    """randomly generates daily demand ratio following triangular distribution"""
    p = random.uniform(0, 1)
    raw = 0
    if p <= pConstraints[index]:
        raw = triangularMin[index] \
              + numpy.math.sqrt(p * (triangularMax[j] - triangularMin[index]) * (triangularAvg[index] - triangularMin[index]))
    else:
        raw = triangularMax[index] \
              - numpy.math.sqrt((1 - p) * (triangularMax[index] - triangularMin[index]) * (triangularMax[index] - triangularAvg[index]))
    return raw


yearMeanOfRandomDemand = []
yearDeviationOfRandomDemand = []


def calculate_mean_deviation():
    """calculating mean and standard deviation for the total of the random generated daily demand for each yearly demand."""

    for i in range(6):
        yearList = eachYearDailyDemandList[i]
        demand = []
        for j in range(len(yearList)):
            obj = yearList[j]
            if isinstance(obj, Classes.DailyDemand):
                demand.append(obj.dailyDemand)

        theStdDeviation = statistics.stdev(demand)
        theMean = statistics.mean(demand)
        yearMeanOfRandomDemand.append(theMean)
        yearDeviationOfRandomDemand.append(theStdDeviation)


def calculate_daily_capacity_v2():
    """Calculates the daily capacity required to fullfill yearly demand based on OTS and Service level."""

    global filename
    leadTime = input("Enter Lead Time")
    serviceLevel = input("Enter Service Level")
    filename = "Lead_Time_" + str(leadTime) + "_Service_Level_" + str(serviceLevel)

    factorySpecifications = Classes.FactorySpecificationsTask2(leadTimes, yearMeanOfRandomDemand,
                                                             yearDeviationOfRandomDemand, serviceLevel, leadTime)

    factorySpecifications.set_lead_time(leadTime)

    for x in range(len(factorySpecifications.yearlyDemandRequirements)):
        leftSide = (factorySpecifications.yearlyDemandRequirements[x] * factorySpecifications.leadTime)
        valueInsideSqrt = pow(factorySpecifications.yearlyStandardDeviations[x], 2) * factorySpecifications.leadTime
        dailyCapacity = (leftSide + factorySpecifications.zNormalValue * numpy.sqrt(valueInsideSqrt)) / factorySpecifications.leadTime

        dailyCapacityRequirements.append(int(dailyCapacity))
    factorySpecifications.dailyCapacity = dailyCapacityRequirements
    return factorySpecifications


# generate yearly growth demand and standard deviation
calculate_year_growth_demand(yearsOfGrowth)


# Generate yearly random demands;
count = 0
while count <= years:
    demand = demandDistribution.generate_random_demand()
    yearlyDemand.append(demand)

    if count < 5:
        demandDistribution = Classes.DemandVar(growthYearlyDemand[count], growthStandardDeviation[count])
    count = count + 1


for x in range(years):
    for i in range(weeks):
        beta = generate_beta(i)
        weekDemand = beta * yearlyDemand[x]
        weeklyDemand.append(weekDemand)
        for j in range(days):
            raw = generate_raw(j)

            singleDayDemand = round(weeklyDemand[i] * raw, 0)
            dailyDemand = Classes.DailyDemand(yearName[x], str(i + 1), dayName[j], yearlyDemand[x], weeklyDemand[i]
                                              , singleDayDemand, x, i, j)
            dailyDemandList.append(dailyDemand)

index = 0
eachYearDailyDemandList = []
totalYears = len(dailyDemandList) / totalDaysInYear
tempList = []

# separating each year.
for x in range(totalYears):
    tempList = [dailyDemandList[index]]
    index += 1
    while index % 364 != 0:
        tempList.append(dailyDemandList[index])
        index += 1
    eachYearDailyDemandList.append(tempList)


# calculating standard deviation for the random data generated.
calculate_mean_deviation()

# generates the daily capacity requirements for each lead time and service level.
factorySpecifications = calculate_daily_capacity_v2()


# outputs in console the daily demand generated for each year
count = 1
for day in dailyDemandList:
    if isinstance(day, Classes.DailyDemand):
        print("Year: " + day.year + ", " + day.week + ", " + day.day + ", " + str(day.dailyDemand))
        if count % 364 == 0:
            print("\n")
    count += 1

write_to_file()


# calculates the year demands daily demand and amount shipped and calculates the average of service satisfaction level.
def summarize_year_demands():
    for x in range(totalYears):
        totalDemand = 0
        totalProduced = 0
        totalCapacity = 0
        totalShipped = 0
        for obj in yearTotalDemand[x]:
            if isinstance(obj, Classes.DayManufactured):
                totalDemand += obj.demand
                totalProduced += obj.produced
                totalCapacity += factorySpecifications.dailyCapacity[factorySpecifications.scenario]
                totalShipped += obj.amountShipped

        satisfaction = totalShipped / float(totalDemand)
        currentYearSummary = Classes.YearSummary(totalDemand, totalCapacity, totalProduced, totalShipped,
                                                 satisfaction)
        yearSummarizeOverPeriod.append(currentYearSummary)


def write_yearly_summary():
    """writes into a CSV File the average of the daily demand fulfilled service level for each year"""

    file_name = filename + "_Yearly-Summary.csv"
    ofile = open(file_name, "wb")

    # writing the title of the columns
    row = "Year, Total Demand, Total Shipped, Satisfaction Level\n"
    ofile.write(row)

    count = 1
    for x in yearSummarizeOverPeriod:

        if isinstance(x, Classes.YearSummary):
            row = str(count) + "," + str(x.yearDemand) + "," + str(x.totalShipped) + "," \
                  + str(round(x.satisfactionLevel, 6)) + "\n"
            ofile.write(row)
        count = count + 1

    row = "Lead Time, Satisfaction Level\n"
    ofile.write(row)
    row = str(factorySpecifications.leadTime) + "," + str(factorySpecifications.serviceTargetLevel)
    ofile.write(row)
    ofile.close()


# Calculates the daily satisfaction level based on randomly generated demand.
yearTotalDemand = []
yearSummarizeOverPeriod = []
currentYearIndex = 0
for i in range(totalYears):

    listOfDaysProducing = []
    totalDemandInOneDay = 0
    totalDemandFulfilledInOneYear = 0
    totalLoss = 0
    backlog = 0  # very important variable as this temporarily store the missing parts produced previous day.

    dailyManufacturingCapacity = factorySpecifications.dailyCapacity[currentYearIndex]

    yearList = eachYearDailyDemandList[i]

    for k in range(len(yearList)):
        dayDemandGenerated = yearList[k]
        if isinstance(dayDemandGenerated, Classes.DailyDemand):
            generatedDailyDemand = dayDemandGenerated.dailyDemand

            if factorySpecifications.leadTime > 1:
                if k < factorySpecifications.leadTime - 1:
                    ordersToShipToday = round(dayDemandGenerated.weeklyDemand * generate_raw(dayDemandGenerated.dayNumber), 0)
                else:
                    if factorySpecifications.leadTime != 1 and k != 0:
                        index = int(k - (factorySpecifications.leadTime - 1))
                        ordersToShipToday = listOfDaysProducing[
                            index].demand  # of the item on the list of all saved dayManufactored
            else:
                ordersToShipToday = round(dayDemandGenerated.weeklyDemand * generate_raw(dayDemandGenerated.dayNumber), 0)

            if k == 0:
                backlog = 0
                prevDayInventory = min(generatedDailyDemand, dailyManufacturingCapacity)
                prevDayAmountShipped = round(dayDemandGenerated.weeklyDemand * generate_raw(dayDemandGenerated.dayNumber), 0)
            else:
                if isinstance(listOfDaysProducing[k - 1], Classes.DayManufactured):
                    prevDayInventory = listOfDaysProducing[k - 1].inventory
                    backlog = listOfDaysProducing[k - 1].thisDayBackLog

            dayManufactured = Classes.DayManufactured(backlog, generatedDailyDemand, prevDayInventory, ordersToShipToday)

            if dayManufactured.needToProduce > dailyManufacturingCapacity:
                dayManufactured.thisDayBackLog = dayManufactured.needToProduce - dailyManufacturingCapacity  # Calculating backlog
            else:
                dayManufactured.thisDayBackLog = 0

            dayManufactured.produced = min(dayManufactured.needToProduce, dailyManufacturingCapacity)

            if k == 0:
                dayManufactured.amountShipped = min(dayManufactured.ordersToShip, dayManufactured.inventory)
                dayManufactured.satisfactionPercentage = 1.0
                if dayManufactured.ordersToShip > dayManufactured.inventory:
                    dayManufactured.inventory = 0
                else:
                    dayManufactured.inventory = dayManufactured.needToProduce - dayManufactured.ordersToShip
            else:
                dayManufactured.inventory = dayManufactured.inventory + dayManufactured.produced
                dayManufactured.amountShipped = min(dayManufactured.inventory, dayManufactured.ordersToShip)
                if dayManufactured.inventory < dayManufactured.ordersToShip:
                    dayManufactured.demandUnfilled = dayManufactured.ordersToShip - (
                    dayManufactured.inventory + dayManufactured.produced)
                    dayManufactured.inventory = 0
                else:
                    dayManufactured.inventory = dayManufactured.inventory - dayManufactured.ordersToShip

                if dayManufactured.amountShipped == dayManufactured.ordersToShip:
                    dayManufactured.satisfactionPercentage = 1.0
                else:
                    dayManufactured.satisfactionPercentage = (
                    dayManufactured.amountShipped / float(dayManufactured.ordersToShip))

            listOfDaysProducing.append(dayManufactured)
    currentYearIndex += 1
    yearTotalDemand.append(listOfDaysProducing)


summarize_year_demands()
write_yearly_summary()
