import Classes
import numpy
import random

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

daysInAYear = 365
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
    leadTime = input("Enter Lead Time")
    serviceLevel = input("Enter Service Level")
    factorySpecifications = Classes.FactorySpecificationsTask2(leadTimes, growthYearlyDemand,
                                                             growthStandardDeviation, serviceLevel, leadTime)
    for x in range(len(factorySpecifications.yearlyDemandRequirements)):
        leftSide = (factorySpecifications.yearlyDemandRequirements[x] * factorySpecifications.leadTime / 365)
        valueInsideSqrt = pow(factorySpecifications.yearlyStandardDeviations[x], 2) * (15/float(365))
        dailyCapacity = (leftSide + factorySpecifications.zNormalValue * numpy.sqrt(valueInsideSqrt)) / factorySpecifications.leadTime

        dailyCapacityRequirements.append(int(dailyCapacity))
    factorySpecifications.dailyCapacity = dailyCapacityRequirements


def calculate_year_growth_demand(iterations):

    for i in range(iterations):
        yearDemand = 0
        yearDeviation = 0
        if i == 0:
            yearDemand = 365000
            yearDeviation = 73000
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
    ofile = open('Task2-2018-2023.csv', "wb")

    # writing the title of the columns
    row = "Year,Week,Day,Demand\n"
    ofile.write(row)

    for i in range(0, len(dailyDemandList), 1):
        day = dailyDemandList[i]
        if isinstance(day, Classes.DailyDemand):
            row = day.year + "," + day.week + "," + day.day + "," + str(day.dailyDemand) + "\n"
        ofile.write(row)
    ofile.close()


# generate yearly growth demand and standard deviation
calculate_year_growth_demand(yearsOfGrowth)
# generates the daily capacity requirements for each lead time and service level.
calculate_daily_capacity()


# Generate year random demands;
count = 0
while count <= years:
    demand = demandDistribution.generate_random_demand()
    yearlyDemand.append(demand)

    if count < 5:
        demandDistribution = Classes.DemandVar(growthYearlyDemand[count], growthStandardDeviation[count])
    count = count + 1


for x in range(years):
    for i in range(weeks):
        beta = numpy.random.normal(weeklyDemandAverage[i], weeklyDemandStandardDeviation[i])
        weekDemand = beta * yearlyDemand[x]
        weeklyDemand.append(weekDemand)
        for j in range(days):
            p = random.uniform(0, 1)
            raw = 0
            if p <= pConstraints[j]:
                raw = triangularMin[j] \
                         + numpy.math.sqrt(p * (triangularMax[j] - triangularMin[j]) * (triangularAvg[j] - triangularMin[j]))
            else:
                raw = triangularMax[j] \
                         - numpy.math.sqrt((1 - p) * (triangularMax[j] - triangularMin[j]) * (triangularMax[j] - triangularAvg[j]))

            singleDayDemand = round(weeklyDemand[i] * raw, 0)
            dailyDemand = Classes.DailyDemand(yearName[x], str(i + 1), dayName[j], yearlyDemand[x], weeklyDemand[i]
                                              , singleDayDemand)
            dailyDemandList.append(dailyDemand)

for day in dailyDemandList:
    if isinstance(day, Classes.DailyDemand):
        print("Year: " + day.year + ", " + day.week + ", " + day.day + ", " + str(day.dailyDemand))

# write_to_file()

# def calculate_service_level():
#