from .gasPrice import GasPriceScraper
from .vehicleFinder import VehicleFinder


class Calculator:
    def __init__(self, starting_point, ending_point, package_category, package_insurance, packages):
        self.starting_point = starting_point
        self.ending_point = ending_point
        self.package_category = package_category
        self.package_insurance = package_insurance
        self.packages = packages

        # Distance
        self.totalDistance = None
        self.totalRoute = None
        self.totalPavedDistance = None
        self.totalUnpavedDistance = None

        # Price
        # gas = GasPriceScraper()
        # self.gasPrice = gas.calculate_average()['ДТ']
        self.gasPrice = 3884
        # Total
        self.totalPrice = 0.0  # Initialize as a float

    def calculate(self):
        # Distance
        if self.totalPavedDistance is None:
            self.totalPavedDistance = 486
        if self.totalUnpavedDistance is None:
            self.totalUnpavedDistance = 10
        if self.totalDistance is None:
            self.totalDistance = self.totalPavedDistance + self.totalUnpavedDistance

        # Find Vehicle and gas usage price
        vehicles = VehicleFinder(packages=self.packages).get()
        gas_usage_price = 0

        for vehicle in vehicles:
            gas_usage_price += (self.totalPavedDistance / vehicle['efficiency_km_per_l'] +
                                self.totalUnpavedDistance / vehicle['efficiency_km_per_l']) * self.gasPrice

        self.totalPrice += gas_usage_price

        # Insurance
        if self.package_insurance:
            self.totalPrice += (self.totalDistance * 10 * sum(package['price'] * package['quantity']
                                                              for package in self.packages))

        # Usage price
        self.totalPrice += (self.totalPavedDistance * 5985) + (self.totalUnpavedDistance * 6930)

        # Extra price
        # something
        return self.totalPrice, self.totalPrice / self.totalDistance

    def __str__(self):
        return f'Total Price: {self.totalPrice}'
