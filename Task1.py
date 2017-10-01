import Classes
import numpy

# this code is to generate data for Task 1 Part D.
# Input OTS times as float numbers with just 1 decimal value.


filename = " "


def write_to_file_per_year():
    global  filename
    ofile = open(filename + ".csv", "wb")

    # writing the title of the columns
    row = "Scenario, Backlog, Demand, Capacity, Production,Inventory,OrdersToShip,Actual Amount Shipped,Satisfaction Level\n"
    ofile.write(row)

    for x in yearTotalDemand:
        currentyear = x
        count = 1
        for obj in currentyear:
            if isinstance(obj, Classes.DayManufactured):
                row = str(count) + "," + str(obj.prevDayBacklog) + ","+ str(obj.demand) + "," \
                      + str(dailyManufacturingCapacity) + "," + str(obj.produced) + "," + str(obj.inventory) \
                      + "," + str(obj.ordersToShip) + "," + str(obj.amountShipped) + "," + str(obj.satisfactionPercentage) + "\n"
                ofile.write(row)
            count = count + 1
    ofile.close()


def write_yearly_summary():
    global filename
    ofile = open(filename + ".csv", "wb")

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
    ofile.close()


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


demandSpecifications = Classes.DemandVar(1000, 200)
factorySpecifications = Classes.FactorySpecifications()
totalYears = 100
daysInAYear = 365


yearTotalDemand = []
yearSummarizeOverPeriod = []
time = input("Enter Lead Time:")
filename = raw_input("Enter filename:")

# factorySpecifications.leadTime = input("Enter Lead Time:")
factorySpecifications.set_lead_time(time)


dailyManufacturingCapacity = factorySpecifications.dailyCapacity[factorySpecifications.scenario]

# running it for 100 years
for i in range(totalYears):

    listOfDaysProducing = []
    totalDemandInOneDay = 0
    totalDemandFulfilledInOneYear = 0
    totalLoss = 0
    backlog = 0  # very important variable as this temporarily store the missing parts produced previous day.

    for j in range(daysInAYear):

        generatedDailyDemand = int(round(numpy.random.normal(demandSpecifications.mean,
                                                         demandSpecifications.standard_Deviation), 0))
        if factorySpecifications.leadTime > 1:
            if j < factorySpecifications.leadTime - 1:
                ordersToShipToday = int(round(numpy.random.normal(demandSpecifications.mean, demandSpecifications.standard_Deviation), 0))
            else:
                if factorySpecifications.leadTime != 1 and j != 0:
                    index = int(j - (factorySpecifications.leadTime - 1))
                    ordersToShipToday = listOfDaysProducing[
                        index].demand  # of the item on the list of all saved dayManufactored L

        else:
            ordersToShipToday = generatedDailyDemand

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

        if dayManufactured.needToProduce > dailyManufacturingCapacity:
            dayManufactured.thisDayBackLog = dayManufactured.needToProduce - dailyManufacturingCapacity  # Calculating backlog
        else:
            dayManufactured.thisDayBackLog = 0

        dayManufactured.produced = min(dayManufactured.needToProduce, dailyManufacturingCapacity)

        if j == 0:
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
                dayManufactured.demandUnfilled = dayManufactured.ordersToShip - (dayManufactured.inventory + dayManufactured.produced)
                dayManufactured.inventory = 0
            else:
                dayManufactured.inventory = dayManufactured.inventory - dayManufactured.ordersToShip

            if dayManufactured.amountShipped == dayManufactured.ordersToShip:
                dayManufactured.satisfactionPercentage = 1.0
            else:
                dayManufactured.satisfactionPercentage = (dayManufactured.amountShipped / float(dayManufactured.ordersToShip))

        listOfDaysProducing.append(dayManufactured)
    yearTotalDemand.append(listOfDaysProducing)


summarize_year_demands()
write_yearly_summary()
# write_to_file_per_year()






