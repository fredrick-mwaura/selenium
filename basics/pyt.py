import datetime

s = "selenium for browser automation using webdrivers"

string = s[8:]
print(string)

x = 10
y = "training"

z = [1, 2, 3, 4, 5]
p = ["st", "rcv", "academy", "stm"]

currentDate = datetime.datetime.today().date()
print(currentDate)

""" Objects """
class Area:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calcArea(self):
        return self.length * self.width


rect = Area(10, 30)
print(rect.calcArea())


"""class and objects"""

class Employee:
    # pass

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def hello(self):
        print(f"hello {self.name} from py objs")


emp = Employee("fred", "fredrick@mail.com")
print(emp.hello())
print(emp.name)


class RateOfInterest:
    #class variables
    interest = 0.06


    def __init__(self, name, loan):
        self.name = name
        self.loan = loan

    def calc_interest(self):
        print(f"Total interest: {self.loan * self.interest}")

rt = RateOfInterest("fred", 5000)

rt.calc_interest()


class Student(RateOfInterest):
    interest = 0.02

s = Student("fred", 5000)

s.calc_interest()





























