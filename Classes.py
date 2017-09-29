import scipy.stats as stat


# A class am creating to teach
class TestClass:
    name = "Alejandro"
    age = 24


# Define Demand
class DemandVar:
    standard_Deviation = 200
    mean = 1000

    def __init__(self):
        print("Demand Generation Variables Created")


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

