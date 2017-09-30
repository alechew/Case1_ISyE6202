import Classes
import numpy

demandSpecifications = Classes.DemandVar(1000, 200)
factorySpecifications = Classes.FactorySpecifications()
totalYears = 2
daysInAYear = 365


yearTotalDemand = []
factorySpecifications.leadTime = input("Enter Lead Time:")
factorySpecifications.scenario = factorySpecifications.scenarioValues.get(factorySpecifications.leadTime, 30)

dailyManufacturingCapacity = factorySpecifications.dailyCapacity[factorySpecifications.scenario]

# running it for 100 years
for i in range(totalYears):

    listOfDaysProducing = []
    totalDemandInOneDay = 0
    totalDemandFulfilledInOneYear = 0
    totalLoss = 0
    backlog = 0  # very important variable as this temporarily store the missing parts produced previous day.

    for j in range(daysInAYear):
        if j < factorySpecifications.leadTime:
            ordersToShipToday = int(round(numpy.random.normal(demandSpecifications.mean,
                                                          demandSpecifications.standard_Deviation), 0))  # this will be the position (current position - lead time)
        else:
            ordersToShipToday = listOfDaysProducing[
                int(j - factorySpecifications.leadTime)]  # of the item on the list of all saved dayManufactored List to

        generatedDailyDemand = int(round(numpy.random.normal(demandSpecifications.mean,
                                                         demandSpecifications.standard_Deviation), 0))
        if j == 0:
            backlog = 0
            prevDayInventory = min(generatedDailyDemand, dailyManufacturingCapacity)
            prevDayAmountShipped = round(numpy.random.normal(demandSpecifications.mean,
                                                         demandSpecifications.standard_Deviation), 0)
        else:
            if isinstance(listOfDaysProducing[j - 1], Classes.DayManufactured):
                prevDayInventory = listOfDaysProducing[j - 1].inventory
                backlog = listOfDaysProducing[j - 1].thisDayBackLog

        dayManufactured = Classes.DayManufactured(backlog, generatedDailyDemand, prevDayInventory, ordersToShipToday)

        if dayManufactured.demand > dailyManufacturingCapacity:
            dayManufactured.thisDayBackLog = dayManufactured.demand - dailyManufacturingCapacity  # Calculating backlog
        else:
            dayManufactured.thisDayBackLog = 0

        dayManufactured.produced = min(dayManufactured.prevDayBacklog + dayManufactured.demand, dailyManufacturingCapacity)

        if j == 0:
            dayManufactured.amountShipped = min(dayManufactured.ordersToShip, dayManufactured.inventory)
            if dayManufactured.ordersToShip > dayManufactured.inventory:
                dayManufactured.inventory = 0
            else:
                dayManufactured.inventory = dayManufactured.demand - dayManufactured.ordersToShip
        else:
            dayManufactured.inventory = dayManufactured.inventory + dayManufactured.produced
            dayManufactured.amountShipped = min(dayManufactured.inventory, dayManufactured.ordersToShip)
            if dayManufactured.inventory < dayManufactured.ordersToShip:
                dayManufactured.demandUnfilled = dayManufactured.ordersToShip - (dayManufactured.inventory + dayManufactured.produced)
                dayManufactured.inventory = 0
            else:
                temp = dayManufactured.inventory
                dayManufactured.inventory = temp - dayManufactured.ordersToShip

            if dayManufactured.amountShipped == dayManufactured.ordersToShip:
                dayManufactured.satisfactionPercentage = 1.0
            else:
                dayManufactured.satisfactionPercentage = (dayManufactured.amountShipped / dayManufactured.ordersToShip)

        # if dayManufactured.inventory > dayManufactured.ordersToShip:
        #     dayManufactured.inventory = dayManufactured.inventory - dayManufactured.ordersToShip
        #     dayManufactured.amountShipped = dayManufactured.ordersToShip
        #     dayManufactured.satisfactionPercentage = 1.00
        # else:
        #     dayManufactured.inventory = 0
        #     dayManufactured.demandUnfilled = dayManufactured.ordersToShip - dayManufactured.inventory
        #     dayManufactured.amountShipped = dayManufactured.ordersToShip
        #     dayManufactured.satisfactionPercentage = 1 - (dayManufactured.demandUnfilled / dayManufactured.ordersToShip)

        listOfDaysProducing.append(dayManufactured)
    yearTotalDemand.append(listOfDaysProducing)

for x in yearTotalDemand:
    currentYear = x
    count = 1
    for obj in currentYear:
        print("Scenario, " + "Backlog, " + "Demand, " + "Capacity, " + "Production, " + "Inventory, " + "OrdersToShip, " + "Actual Amount Shipped, " + "Satisfaction Level")
        if isinstance(obj, Classes.DayManufactured):
            print(str(count) + " , " + str(x.backlog) + " , " + str(x.demand) + " , " + str(dailyManufacturingCapacity)
              + " , " + str(x.produced) + " , " + str(x.inventory)
              + " , " + str(x.ordersToShip) + " , " + str(x.amountShipped) + " , " + str(x.satisfactionPercentage))

    count = count + 1




