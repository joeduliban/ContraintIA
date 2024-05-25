from constraint import Problem, AllDifferentConstraint

class AirportScheduling:
    def __init__(self, flights, gates):
        self.flights = flights
        self.gates = gates
        self.problem = Problem()
        self.solutions = {}

    def create_variables(self):
        for flight in self.flights:
            self.problem.addVariable(flight["id"], [gate["id"] for gate in self.gates])
            self.problem.addVariable(flight["id"] + "_hour", range(24))
            self.problem.addVariable(flight["id"] + "_minute", range(60))

    def add_constraints(self):
        # Ensure that each flight is assigned a unique gate
        self.problem.addConstraint(AllDifferentConstraint(), [flight["id"] for flight in self.flights])

        # Ensure that the aircraft size matches the gate size
        for flight in self.flights:
            for gate in self.gates:
                if flight["aircraft_size"] == gate["size"]:
                    self.problem.addConstraint(lambda g: g == gate["id"], (flight["id"],))

        # Ensure that international flights are assigned to gates with Customs and Immigration
        for flight in self.flights:
            if flight["country"] != "USA":
                for gate in self.gates:
                    if gate["customs_immigration"]:
                        self.problem.addConstraint(lambda g: g == gate["id"], (flight["id"],))

        # Ensure that a flight is not assigned to a gate until the previous flight has departed
        for i in range(len(self.flights)):
            for j in range(i + 1, len(self.flights)):
                if self.flights[i]["id"] != self.flights[j]["id"]:
                    self.problem.addConstraint(lambda h1, m1, h2, m2: h2 * 60 + m2 - (h1 * 60 + m1) >= 60,
                                               (self.flights[i]["id"] + "_hour", self.flights[i]["id"] + "_minute",
                                                self.flights[j]["id"] + "_hour", self.flights[j]["id"] + "_minute"))

    def solve(self):
        self.create_variables()
        self.add_constraints()
        self.solutions = self.problem.getSolutions()

    def print_solution(self):
        if self.solutions:
            print(len(self.solutions))
            for solution in self.solutions:
                for flight in self.flights:
                    gate = solution.get(flight["id"])
                    hour = solution.get(flight["id"] + "_hour")
                    minute = solution.get(flight["id"] + "_minute")
                    print(f"Flight {flight['id']} assigned to Gate {gate} at {hour:02d}:{minute:02d}")
        else:
            print("No solution found")

# Example usage
flights = [
    {"id": "FR1", "country": "France", "arrival": "10:00", "departure": "11:00", "aircraft_size": "large"},
    {"id": "BE1", "country": "Belgium", "arrival": "10:30", "departure": "11:30", "aircraft_size": "medium"},
    {"id": "CA1", "country": "Canada", "arrival": "11:00", "departure": "12:00", "aircraft_size": "small"},
    {"id": "US1", "country": "USA", "arrival": "11:30", "departure": "12:30", "aircraft_size": "large"},
    {"id": "DE1", "country": "Germany", "arrival": "12:00", "departure": "13:00", "aircraft_size": "medium"},
    {"id": "IT1", "country": "Italy", "arrival": "12:30", "departure": "13:30", "aircraft_size": "small"},
    {"id": "ES1", "country": "Spain", "arrival": "13:00", "departure": "14:00", "aircraft_size": "large"},
    {"id": "CH1", "country": "China", "arrival": "13:30", "departure": "14:30", "aircraft_size": "medium"},
    {"id": "JP1", "country": "Japan", "arrival": "14:00", "departure": "15:00", "aircraft_size": "small"},
    {"id": "UK1", "country": "United Kingdom", "arrival": "14:30", "departure": "15:30", "aircraft_size": "large"},
    {"id": "AU1", "country": "Australia", "arrival": "15:00", "departure": "16:00", "aircraft_size": "medium"},
]

gates = [
    {"id": "A2", "size": "large", "customs_immigration": True},
    {"id": "B39", "size": "large", "customs_immigration": True},
    {"id": "C14", "size": "medium", "customs_immigration": False},
    {"id": "D21", "size": "medium", "customs_immigration": False},
    {"id": "E25", "size": "small", "customs_immigration": False},
    {"id": "F31", "size": "small", "customs_immigration": False},
    {"id": "G37", "size": "large", "customs_immigration": True},
    {"id": "A21", "size": "medium", "customs_immigration": False},
    {"id": "D25", "size": "medium", "customs_immigration": False},
    {"id": "C31", "size": "small", "customs_immigration": False},
    {"id": "B37", "size": "small", "customs_immigration": False},
    {"id": "H41", "size": "large", "customs_immigration": True},
    {"id": "I43", "size": "medium", "customs_immigration": False},
    {"id": "J45", "size": "small", "customs_immigration": False},
]

scheduler = AirportScheduling(flights, gates)
scheduler.solve()
scheduler.print_solution()