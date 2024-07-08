import pulp as pl


class VehicleFinder:
    def __init__(self, packages):
        # Өгөгдлийг тохируулах (Set up the data)
        self.cars = {
            'A': {'capacity_kg': 500, 'volume_m3': 4, 'efficiency_km_per_l': 15},
            'B': {'capacity_kg': 300, 'volume_m3': 2.5, 'efficiency_km_per_l': 12},
            'C': {'capacity_kg': 200, 'volume_m3': 1.5, 'efficiency_km_per_l': 18}
        }

        # Багцын жагсаалт (List of packages)
        self.packages = packages
        self.total_weight_kg = sum(package['grossWeight'] * package['quantity'] for package in packages)
        self.total_volume_m3 = sum(package['volume'] * package['quantity'] for package in packages)
        self.total_price = sum(package['price'] * package['quantity'] for package in packages)

    def get(self):
        # Модел үүсгэх (Create the model)
        model = pl.LpProblem("Car_Selection_Problem", pl.LpMinimize)

        # Шийдвэр гаргах хувьсагчид (Decision variables)
        use_car = pl.LpVariable.dicts("Use", self.cars.keys(), cat='Binary')
        weight_carried = pl.LpVariable.dicts("Weight", self.cars.keys(), lowBound=0)
        volume_carried = pl.LpVariable.dicts("Volume", self.cars.keys(), lowBound=0)

        # Зорилго (Objective function)
        model += pl.lpSum([100 / self.cars[car]['efficiency_km_per_l'] * use_car[car] for car in self.cars])

        # Хязгаарлалтууд (Constraints)
        model += pl.lpSum([weight_carried[car] for car in self.cars]) >= self.total_weight_kg
        model += pl.lpSum([volume_carried[car] for car in self.cars]) >= self.total_volume_m3

        for car in self.cars:
            model += weight_carried[car] <= self.cars[car]['capacity_kg'] * use_car[car]
            model += volume_carried[car] <= self.cars[car]['volume_m3'] * use_car[car]

        # Моделийг шийдвэрлэх (Solve the model)
        model.solve()

        # Хариу гаргах (Return the solution)
        used_cars = []
        for car in self.cars:
            if pl.value(use_car[car]) == 1:
                used_cars.append({
                    'car': car,
                    'weight_carried': pl.value(weight_carried[car]),
                    'volume_carried': pl.value(volume_carried[car]),
                    'efficiency_km_per_l': self.cars[car]['efficiency_km_per_l']
                })

        return used_cars


if __name__ == '__main__':
    packages = [
        {
            "volume": 12,
            "quantity": 1,
            "grossWeight": 120,
            "price": 120123123,
        },
        {
            "volume": 123,
            "quantity": 13,
            "grossWeight": 23,
            "price": 12000000
        },
    ]

    vehicle_finder = VehicleFinder(packages=packages)
    used_cars = vehicle_finder.get()
    print(f'Cars : {used_cars}')
