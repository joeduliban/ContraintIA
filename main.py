from constraint import Problem, AllDifferentConstraint

class AirportScheduling:
    def __init__(self, flights, gates):
        self.flights = flights
        self.gates = gates
        self.problem = Problem()
        self.solutions = []

    def create_variables(self):
        for flight in self.flights:
            self.problem.addVariable(flight["id"], [gate["id"] for gate in self.gates])
            '''self.problem.addVariable(flight["id"] + "_hour", range(8, 18))  # Reduce the range of hours
            self.problem.addVariable(flight["id"] + "_minute", range(0, 60, 30))  # Reduce the range of minutes'''

    def add_constraints(self):
        # No two planes can be on the same gate at the same time
        self.problem.addConstraint(AllDifferentConstraint(), [flight["id"] for flight in self.flights])

        # Priority for certain flights
        priority_flights = ["FR1", "BE1", "CA1"]
        priority_gates = ["A2", "B39", "C14"]
        for i, flight in enumerate(priority_flights):
            self.problem.addConstraint(lambda gate, g=priority_gates[i]: gate == g, (flight,))

        # Ensure flights are assigned to gates in the correct position
        gate_positions = {gate["id"]: gate["position"] for gate in self.gates}
        for flight in self.flights:
            self.problem.addConstraint(lambda gate_id, fp=flight["position"]: gate_positions[gate_id] == fp, (flight["id"],))

    def solve(self):
        self.create_variables()
        self.add_constraints()
        self.solutions = self.problem.getSolutions()

    def print_solution(self):
        if self.solutions:
            print(f"Number of solutions: {len(self.solutions)}")
        else:
            print("No solution found")

# Example usage
flights = [
    {"id": "FR1", "country": "France", "arrival": "10:00", "departure": "11:00", "position": "west"},
    {"id": "BE1", "country": "Belgium", "arrival": "10:30", "departure": "11:30", "position": "east"},
    {"id": "CA1", "country": "Canada", "arrival": "11:00", "departure": "12:00", "position": "north"},
    {"id": "US1", "country": "USA", "arrival": "11:30", "departure": "12:30", "position": "north"},
    {"id": "DE1", "country": "Germany", "arrival": "12:00", "departure": "13:00", "position": "east"},
    {"id": "IT1", "country": "Italy", "arrival": "12:30", "departure": "13:30", "position": "south"},
    {"id": "ES1", "country": "Spain", "arrival": "13:00", "departure": "14:00", "position": "west"},
]

gates = [
    {"id": "A1", "position": "west"},
    {"id": "A2", "position": "west"},
    {"id": "B2", "position": "north"},
    {"id": "B39", "position": "east"},
    {"id": "C14", "position": "north"},
    {"id": "D21", "position": "east"},
    {"id": "E5", "position": "south"},
    {"id": "E7", "position": "west"},
    {"id": "F11", "position": "north"},
    {"id": "F13", "position": "south"},
    {"id": "G4", "position": "west"},
    {"id": "G6", "position": "south"},
]

scheduler = AirportScheduling(flights, gates)
scheduler.solve()
scheduler.print_solution()