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
            self.problem.addConstraint(lambda gate_id, fp=flight["position_departure"]: gate_positions[gate_id] == fp, (flight["id"],))
        
        # Ensure that the aircraft size matches the gate size
        gate_size = {gate["id"]: gate["size"] for gate in self.gates}
        for flight in self.flights:
            self.problem.addConstraint(lambda gate_id, fs=flight["aircraft_size"]: gate_size[gate_id] >= fs, (flight["id"],))

        # Connection times for passengers
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

    def solve(self):
        self.create_variables()
        self.add_constraints()
        self.solutions = self.problem.getSolutions()

    def print_solution(self):
        if self.solutions:
            print(f"Number of solutions: {len(self.solutions)}")
            for i,solution in enumerate(self.solutions):
                print(f"Solution {i+1}:")
                for flight in self.flights:
                    gate = solution.get(flight["id"])
                    departure = flight["departure"]
                    print(f"Flight {flight['id']} assigned to Gate {gate} at {departure}")
        else:
            print("No solution found")

# Example usage
flights = [
    {"id": "FR1", "country": "France", "arrival": "10:00", "departure": "11:00", "position_departure": "west", "aircraft_size": 3},
    {"id": "BE1", "country": "Belgium", "arrival": "10:30", "departure": "11:30", "position_departure": "east", "aircraft_size": 2},
    {"id": "CA1", "country": "Canada", "arrival": "11:00", "departure": "12:00", "position_departure": "north", "aircraft_size": 3},
    {"id": "US1", "country": "USA", "arrival": "11:30", "departure": "12:30", "position_departure": "north", "aircraft_size": 3},
    {"id": "DE1", "country": "Germany", "arrival": "12:00", "departure": "13:00", "position_departure": "east", "aircraft_size": 1},
    {"id": "IT1", "country": "Italy", "arrival": "12:30", "departure": "13:30", "position_departure": "south", "aircraft_size": 2},
    {"id": "ES1", "country": "Spain", "arrival": "13:00", "departure": "14:00", "position_departure": "west", "aircraft_size": 1},
]

gates = [
    {"id": "A1", "position": "west", "size": 3},    # 3 : Large, 2 : medium, 1 : small
    {"id": "A2", "position": "west", "size": 3},
    {"id": "B2", "position": "north", "size": 2},
    {"id": "B39", "position": "east", "size": 2},
    {"id": "C14", "position": "north", "size": 3},
    {"id": "D21", "position": "east", "size": 1},
    {"id": "E5", "position": "south", "size": 1},
    {"id": "E7", "position": "west", "size": 2},
    {"id": "F11", "position": "north", "size": 3},
    {"id": "F13", "position": "south", "size": 1},
    {"id": "G4", "position": "west", "size": 1},
    {"id": "G6", "position": "south", "size": 3},
]

scheduler = AirportScheduling(flights, gates)
scheduler.solve()
scheduler.print_solution()