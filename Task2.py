import Classes
import numpy
import random

demandDistribution = Classes.DemandVar(365000, 73000)

yearName = ["2018", "2019", "2020", "2021", "2022"]
dayName = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

years = 5
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

yearlyDemand = []
dailyDemandList = []

# Generate year random demands;
for x in range(years - 1):
    demand = demandDistribution.generate_random_demand()
    yearlyDemand.append(demand)


for x in range(years - 1):
    for i in range(weeks - 1):
        beta = numpy.random.normal(weeklyDemandAverage[i], weeklyDemandStandardDeviation[i])
        for j in range(days - 1):
            p = random.uniform(0, 1)
            raw = 0
            if p <= pConstraints[j]:
                raw = triangularMin[j] \
                         + numpy.math.sqrt(p(triangularMax[j] - triangularMin[j])(triangularAvg[j] - triangularMin[j]))
            else:
                raw = triangularMax[j] \
                         - numpy.math.sqrt((1 - p)(triangularMax[j] - triangularMin[j])(triangularMax[j] - triangularAvg[j]))
        dailyDemand = Classes.DailyDemand(yearName[x], str(i), dayName[j], raw)
