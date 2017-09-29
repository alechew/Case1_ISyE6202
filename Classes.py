import scipy.stats as stat
import numpy

# A class am creating to teach
from case1 import stdDev


class TestClass:
    name = "Alejandro"
    age = 24


# Define Demand
class DemandVar:
    standard_Deviation = 0
    mean = 0
    demandGenerated = 0

    def __init__(self, mean, standardDeviation):
        self.mean = mean
        self.standard_Deviation = standardDeviation

    def generate_random_demand(self):
        self.demandGenerated = round(numpy.random.normal(self.mean, self.standard_Deviation), 0)
        return self.demandGenerated


# Target level we want to satisfy
class FactoryRequirements:
    serviceTargetLevel = 0.99
    zNormalValue = zNormalValue = stat.norm.ppf(serviceTargetLevel)
    numberDays = 364
    numberScenarios = 100   # number Years we want to run
    leadTime = 10

    def __init__(self):
        print("Creating the scenario foe the case")

    # def calculate_capacity():
    #     demand_satisfaction_capacity = (meanInPeriod * orderToShipping / basePeriod) \
    #                                    + (zNormalValue * numpy.math.sqrt(
    #         stdDevInPeriod * orderToShipping / basePeriod))
    #     return demand_satisfaction_capacity


# Object that will have all the information of daily demand generated compared with our production capacity.
class DailyScenario:
    demand = 0
    demandSatisfied = 0
    demandNotSatisfied = 0

    def __init__(self):
        print("Daily Demand Scenario")


class DailyDemand:
    year = "2018"
    week = "1"
    day = "Monday"
    yearlyDemand = 0
    weeklyDemand = 0
    dailyDemand = 0

    def __init__(self, year, week, day, yearlyDemand, weeklyDemand, dailyDemand):





