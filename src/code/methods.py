import ciw
import pandas as pd
from collections import namedtuple

"""
SETUP:
There are 3 ambulance locations, A0, A1, and A2.
There are 5 patient locations, P0, P1, P2, P3, and P4.
Let loc_arrival_rates be a vector of arrival rates to each of the patient locations.
Let hosp_to_amb be a vector of distasnces from the nearest hospital to the ambulance locations.
Let patient_to_hosp be a vector of distances from the patient locations to the nearest hospital.
Let amb_to_patient be a matrix of distances between the ambulance locations and the patient locations.
Let delay_factor be a vector of time delay factors for each time of day (here every 6 hrs).
Let speed be a very crude conversion between distance and time
"""

n_ambulances = 3
n_locations = 5
loc_arrival_rates = [0.5, 0.9, 0.4, 0.7, 0.9]
hosp_to_amb = [10, 20, 25]
patient_to_hosp = [35, 30, 15, 22, 40]
amb_to_patient = [[55, 52, 25, 10, 30], [28, 25, 8, 18, 15], [12, 10, 15, 48, 35]]
delay_factor = [1.5, 1, 0.8, 1.4]
speed = 0.01

"""
Patient arrives to a patient location.
Out of all free ambulances, caluculate the expected time to pick up patient.
Choose ambulance with the shortest expected time to pick up patient.
"Service" begins immediately. Expected service time = (time from ambulance location to patient location + time from patient location to hospital + time from hospital to ambulance location) * (delay due to time of day). Actual service time add some randomness.
"""


def expected_pickup(a, p, t):
    """
    The expected service time for ambulance a to pick up patient p in time period t.
    """
    return amb_to_patient[a][p] * delay_factor[t] * speed


"""
Now let's make Ciw distribution objects to account for the randomness:
"""


def make_service_dist(ambulance):
    class AmbulanceTrip(ciw.dists.Distribution):
        def sample(self, t, ind):
            tperiod = int((t % 1) * 4)
            pick_up, to_hosp, return_to_loc = expected_service(
                ambulance, ind.customer_class, tperiod
            )
            ind.pick_up_time = ciw.random.expovariate(1 / pick_up)
            ind.to_hospital_time = ciw.random.expovariate(1 / to_hosp)
            ind.return_to_loc_time = ciw.random.expovariate(1 / return_to_loc)
            return ind.pick_up_time + ind.to_hospital_time + ind.return_to_loc_time

    return AmbulanceTrip()


"""
Here we manipulate the Ciw objects
Manipulate the routing. We want to route from the first node (where everyone arrives together) and send to an ambulance. Decide where to send them based on who's free, and who's going to get there quickest.
"""


DataRecord = namedtuple(
    "Record",
    [
        "id_number",
        "customer_class",
        "node",
        "arrival_date",
        "waiting_time",
        "service_start_date",
        "service_time",
        "pick_up_time",
        "to_hospital_time",
        "return_to_loc_time",
        "service_end_date",
        "time_blocked",
        "exit_date",
        "destination",
        "queue_size_at_arrival",
        "queue_size_at_departure",
    ],
)


class Patient(ciw.Individual):
    def __init__(self, id_number, customer_class=0, priority_class=0, simulation=False):
        super().__init__(id_number, customer_class, priority_class, simulation)
        self.pick_up_time = False
        self.to_hospital_time = False
        self.return_to_loc_time = False


class AmbulanceNode(ciw.Node):
    def next_node(self, ind):
        """
        Decides on the next node.

        If this is the first node:
          - find all the free ambulances
          - if no free ambulances, leave
          - calculate expected pick up time for each free ambulance
          - 'book' the closest ambulance, e.g. choose that node
        """
        if self.id_number != 1:
            return self.simulation.nodes[-1]
        else:
            tperiod = int((self.simulation.current_time % 1) * 4)
            choices = {
                a: expected_pickup(a, ind.customer_class, tperiod)
                for a in range(self.simulation.network.number_of_nodes - 1)
            }
            ordered_choices = sorted(choices.keys(), key=lambda x: choices[x])
            for choice in ordered_choices:
                node = self.simulation.nodes[choice + 2]
                if any(not s.busy for s in node.servers):
                    return node
            return self.simulation.nodes[-1]

    def write_individual_record(self, individual):
        """
        Write a data record for an individual:
            - Arrival date
            - Wait
            - Service start date
            - Service time
            - Pick up time
            - To hospital time
            - Reutrn to location time
            - Service end date
            - Blocked
            - Exit date
            - Node
            - Destination
            - Previous class
            - Queue size at arrival
            - Queue size at departure
        """
        record = DataRecord(
            individual.id_number,
            individual.previous_class,
            self.id_number,
            individual.arrival_date,
            individual.service_start_date - individual.arrival_date,
            individual.service_start_date,
            individual.service_end_date - individual.service_start_date,
            individual.pick_up_time,
            individual.to_hospital_time,
            individual.return_to_loc_time,
            individual.service_end_date,
            individual.exit_date - individual.service_end_date,
            individual.exit_date,
            individual.destination,
            individual.queue_size_at_arrival,
            individual.queue_size_at_departure,
        )
        individual.data_records.append(record)

        individual.arrival_date = False
        individual.service_time = False
        individual.service_start_date = False
        individual.service_end_date = False
        individual.exit_date = False
        individual.queue_size_at_arrival = False
        individual.queue_size_at_departure = False
        individual.destination = False


"""
Here we build a simulation
"""

N = ciw.create_network(
    arrival_distributions={
        "Class "
        + str(c): [ciw.dists.Exponential(r)]
        + [ciw.dists.NoArrivals() for _ in range(n_ambulances)]
        for c, r in enumerate(loc_arrival_rates)
    },
    service_distributions={
        "Class "
        + str(c): [ciw.dists.Deterministic(0)]
        + [make_service_dist(a) for a in range(n_ambulances)]
        for c in range(n_locations)
    },
    number_of_servers=[float("Inf")] + [1 for _ in range(n_ambulances)],
    queue_capacities=[float("Inf")] + [0 for _ in range(n_ambulances)],
    routing={
        "Class "
        + str(c): [
            [0 for _ in range(n_ambulances + 1)] for _ in range(n_ambulances + 1)
        ]
        for c in range(n_locations)
    },
)

Q = ciw.Simulation(N, node_class=AmbulanceNode, individual_class=Patient)

Q.simulate_until_max_time(100)

recs = pd.DataFrame(Q.get_all_records())

"""
Now lets analyse some results (from one trial only for now)
"""
"""
# How busy are the ambulances?
Q.nodes[2].server_utilisation
Q.nodes[3].server_utilisation
Q.nodes[4].server_utilisation

# Which patient locations (customer classes) are using each ambulance location (nodes)
recs[recs['node']!=1].groupby('customer_class')['node'].value_counts().unstack()

# How many patients were lost?
recs[recs['node']==1]['destination'].value_counts()
recs[recs['node']==1]['destination'].value_counts()[-1] / recs[recs['node']==1]['destination'].count()

# How long were they waiting on average?
recs[recs['node']!=1]['pick_up_time'].mean()
"""
