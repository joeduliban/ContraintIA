from constraint import Problem, AllDifferentConstraint

class AirportScheduling:
    def __init__(self, flights, gates):
        self.flights = flights
        self.gates = gates
        self.problem = Problem()
        self.solutions = {}

    def create_variables(self):
        for flight in self.flights:
            self.problem.addVariable(flight["id"], self.gates)
            self.problem.addVariable(flight["id"] + "_hour", range(24))
            self.problem.addVariable(flight["id"] + "_minute", range(60))

    def add_constraints(self):
        # Pas deux avions sur la même porte en même temps
        self.problem.addConstraint(AllDifferentConstraint(), [flight["id"] for flight in self.flights])

        # Temps de correspondance pour les passagers
        def correspondance_possible(f1, f2):
            heure_arrivee_f1 = next((flight["arrival"] for flight in self.flights if flight["id"] == f1), None)
            heure_depart_f2 = next((flight["departure"] for flight in self.flights if flight["id"] == f2), None)
            if heure_arrivee_f1 and heure_depart_f2:
                h1, m1 = map(int, heure_arrivee_f1.split(":"))
                h2, m2 = map(int, heure_depart_f2.split(":"))
                time1 = h1 * 60 + m1
                time2 = h2 * 60 + m2
                return (time2 - time1) >= 30
            return True

        for i in range(len(self.flights)):
            for j in range(i + 1, len(self.flights)):
                self.problem.addConstraint(correspondance_possible, (self.flights[i]["id"], self.flights[j]["id"]))

        # Pas plus de trois vols du même pays dans la même journée
        for country in set(flight["country"] for flight in self.flights):
            country_flights = [flight["id"] for flight in self.flights if flight["country"] == country]
            self.problem.addConstraint(lambda *flights: len([f for f in flights if f is not None]) <= 3, country_flights)

        # Priorité des portes pour certains vols
        priority_flights = ["FR1", "BE1", "CA1"]
        priority_gates = ["A2", "B39", "C14"]
        for i, flight in enumerate(priority_flights):
            self.problem.addConstraint(lambda gate, f=flight, g=priority_gates[i]: gate == g, (flight,))

        # Respect des heures de départ
        for flight in self.flights:
            departure_hour, departure_minute = map(int, flight["departure"].split(":"))
            arrival_hour, arrival_minute = map(int, flight["arrival"].split(":"))
            self.problem.addConstraint(lambda h, m, dh=departure_hour, dm=departure_minute: h == dh and m == dm, 
                                       (flight["id"] + "_hour", flight["id"] + "_minute"))

    def solve(self):
        self.create_variables()
        self.add_constraints()
        self.solutions = self.problem.getSolutions()

    def print_solution(self):
        if self.solutions:
            print(len(self.solutions))
            '''for solution in self.solutions:
                for flight in self.flights:
                    gate = solution.get(flight["id"])
                    hour = solution.get(flight["id"] + "_hour")
                    minute = solution.get(flight["id"] + "_minute")
                    print(f"Flight {flight['id']} assigned to Gate {gate} at {hour:02d}:{minute:02d}")'''
        else:
            print("No solution found")

# Example usage
flights = [
    {"id": "FR1", "country": "France", "arrival": "10:00", "departure": "11:00"},
    {"id": "BE1", "country": "Belgium", "arrival": "10:30", "departure": "11:30"},
    {"id": "CA1", "country": "Canada", "arrival": "11:00", "departure": "12:00"},
    {"id": "US1", "country": "USA", "arrival": "11:30", "departure": "12:30"},
    {"id": "DE1", "country": "Germany", "arrival": "12:00", "departure": "13:00"},
    {"id": "IT1", "country": "Italy", "arrival": "12:30", "departure": "13:30"},
    {"id": "ES1", "country": "Spain", "arrival": "13:00", "departure": "14:00"},
]

gates = ["A2", "B39", "C14", "D21", "E25", "F31", "G37", "A21", "D25", "C31", "B37"]
scheduler = AirportScheduling(flights, gates)
scheduler.solve()
scheduler.print_solution()