import scipy.stats as stat
import numpy
import Classes


# demandRequirements = Classes.DemandVar
#
#
# def ask_for_inputs():
#     demandRequirements.mean = input('Enter your new mean: ')
#
#
# ask_for_inputs()
# print(demandRequirements.mean)

list = []

testClassA = Classes.TestClass()
testClassB = Classes.TestClass()
testClassC = Classes.TestClass()

list.append(testClassA)

testClassB.name = "felipe"
testClassB.age = 31
list.append(testClassB)
testClassC.name = "Mike"
testClassC.age = 26

list.append(testClassC)

for obj in list:
    if isinstance(obj, Classes.TestClass):
        print (obj.name + "," + str(obj.age))


