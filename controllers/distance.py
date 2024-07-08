import googlemaps


class Distance:
    def __init__(self, starting_point, ending_point):
        self.startingPoint = starting_point
        self.endingPoint = ending_point

        self.distance = None
        self.pavedDistance = None
        self.unpavedDistance = None

    def get_distance(self):
        gmaps = googlemaps.Client(key='AIzaSyDpdnSslrswMjlFDtx1gE3_bjiFltFpIE8')
        result = gmaps.distance_matrix(origins=self.startingPoint, destinations=self.endingPoint)
        distance = result['rows'][0]['elements'][0]['distance']['value']
        self.distance = distance / 1000  # Convert to kilometers
        return self.distance

    def get_unpaved_distance(self):
        self.unpavedDistance = 10
        return self.unpavedDistance

    def get_paved_distance(self):
        if self.distance is None:
            self.get_distance()
        self.pavedDistance = self.distance - self.unpavedDistance
        return self.pavedDistance


if __name__ == '__main__':
    starting_point = 'UB'
    ending_point = 'Darkhan'

    distance_calculator = Distance(starting_point, ending_point)
    total_distance = distance_calculator.get_distance()
    unpaved_distance = distance_calculator.get_unpaved_distance()
    paved_distance = distance_calculator.get_paved_distance()

    print(f"Total distance from {starting_point} to {ending_point}: {total_distance} km")
    print(f"Unpaved distance: {unpaved_distance} km")
    print(f"Paved distance: {paved_distance} km")
