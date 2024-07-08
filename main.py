from controllers import Calculator

if __name__ == '__main__':
    # Test Input of user
    startingPoint = 'UB'
    endingPoint = 'Arkhangai'
    packageCategory = 1
    packageInsurance = False
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

    priceCalculator = Calculator(startingPoint, endingPoint, packageCategory, packageInsurance, packages)
    print(priceCalculator.calculate())
