class RateOfInterest():

    interest = 0.09

    def __init__(self, name, loan):
        self.name = name
        self.loan = loan

    def calcInterest(self):
         interest = self.loan * self.interest
         print(f"Total interest: {interest}")

p1 = RateOfInterest("fred", 300000)
p2 = RateOfInterest("mwaura", 30000)
# p2.interest = 0.01

p1.calcInterest()
p2.calcInterest()
