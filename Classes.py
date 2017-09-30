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
class FactorySpecifications:
    leadTimes = [30.0, 15.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.25, 0.1]
    demandRequirements = [32549, 16802, 11472, 6041, 2658, 1466, 829, 483, 248]
    dailyCapacity = [1085, 1120, 1147, 1208, 1329, 1466, 1658, 1932, 2480]
    serviceTargetLevel = 0.99
    zNormalValue = zNormalValue = stat.norm.ppf(serviceTargetLevel)
    numberDays = 364
    numberScenarios = 100   # number Years we want to run
    leadTime = 10
    scenario = 0
    scenarioValues = {30: 0,
                      15: 1,
                      10: 2,
                      5: 3,
                      2: 4,
                      1: 5,
                      0.5: 6,
                      0.25: 7,
                      0.1: 8}

    def __init__(self):
        print("Creating the scenario foe the case")

    def set_lead_time(self, leadtime):
        self.leadTime = leadtime

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
        self.year = year
        self.week = week
        self.day = day
        self.yearlyDemand = yearlyDemand
        self.weeklyDemand = weeklyDemand
        self.dailyDemand = dailyDemand


class DayManufactured:
    prevDayBacklog = 0
    thisDayBackLog = 0
    demand = 0
    produced = 0
    inventory = 0
    ordersToShip = 0
    amountShipped = 0
    demandUnfilled = 0
    satisfactionPercentage = 0.0

    def __init__(self, backlog, produced, inventory, orderstoship):
        self.prevDayBacklog = backlog
        self.produced = produced
        self.demand = self.thisDayBackLog + self.produced
        self.inventory = inventory
        self.ordersToShip = orderstoship







