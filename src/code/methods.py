import ciw
import pandas as pd
import math
from collections import namedtuple

def get_delay_period(time, params):
    for i in range(params['n_factors']):
        if time >= params['delay_split'][i] and time < params['delay_split'][i+1]:
            return i

def find_max_dist(start_time, params):
    frac_part, int_part = math.modf(start_time)
    i = get_delay_period(frac_part, params)
    max_duration = params['delay_split'][i+1] - frac_part
    max_distance = (max_duration * params['delay_factor'][i]) * params['speed']
    return max_distance, max_duration

def final_leg(start_time, distance_left, params):
    frac_part, int_part = math.modf(start_time)
    i = get_delay_period(frac_part, params)
    tx = (distance_left/(params['delay_factor'][i] * params['speed'])) + frac_part
    return tx - frac_part

def journey_time(start_time, required_distance, params):
    dist_covered = 0
    time_taken = 0
    max_dist, duration = 0, 0
    while dist_covered + max_dist < required_distance:
        dist_covered += max_dist
        time_taken += duration
        max_dist, duration = find_max_dist(start_time + time_taken, params)
    time_taken += final_leg(start_time + time_taken, required_distance-dist_covered, params)
    return time_taken

def expected_pickup(initial_call_time, a, p, params):
    """
    The expected service time for ambulance a to service patient p in time period t.
    Consists of:
      - getting to the patient
      - taking patient to the hospital
      - getting back to ambulance location from the hospital
    """
    pick_up_transit_time = journey_time(initial_call_time, params['amb_to_patient'][a][p], params)
    return pick_up_transit_time + initial_call_time

def expected_service(initial_call_time, a, p, params):
    """
    The expected service time for ambulance a to service patient p in time period t.
    Consists of:
      - getting to the patient
      - taking patient to the hospital
      - getting back to ambulance location from the hospital
    """
    pick_up_transit_time = journey_time(initial_call_time, params['amb_to_patient'][a][p], params)
    to_hosp_transit_time = journey_time(initial_call_time + pick_up_transit_time, params['patient_to_hosp'][p], params)
    return_to_loc_transit_time = journey_time(initial_call_time + pick_up_transit_time + to_hosp_transit_time, params['hosp_to_amb'][p][a], params)
    return pick_up_transit_time, to_hosp_transit_time, return_to_loc_transit_time

def make_service_dist(ambulance, params):
    class AmbulanceTrip(ciw.dists.Distribution):
        def sample(self, t, ind):
            pick_up, to_hosp, return_to_loc = expected_service(t, ambulance, ind.customer_class, params)
            ind.pick_up_time = ciw.random.expovariate(1/pick_up)
            ind.to_hospital_time = ciw.random.expovariate(1/to_hosp)
            ind.return_to_loc_time = ciw.random.expovariate(1/return_to_loc)
            return ind.pick_up_time + ind.to_hospital_time + ind.return_to_loc_time
    return AmbulanceTrip()

DataRecord = namedtuple('Record', [
    'id_number',
    'customer_class',
    'node',
    'arrival_date',
    'waiting_time',
    'service_start_date',
    'service_time',
    'pick_up_time',
    'to_hospital_time',
    'return_to_loc_time',
    'service_end_date',
    'time_blocked',
    'exit_date',
    'destination',
    'queue_size_at_arrival',
    'queue_size_at_departure'
    ])

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
            choices = {a: expected_pickup(self.simulation.current_time, a, ind.customer_class, self.simulation.params) for a in range(self.simulation.network.number_of_nodes - 1)}
            ordered_choices = sorted(choices.keys(), key=lambda x: choices[x])
            for choice in ordered_choices:
                node = self.simulation.nodes[choice+2]
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
        record = DataRecord(individual.id_number,
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
            individual.queue_size_at_departure)
        individual.data_records.append(record)

        individual.arrival_date = False
        individual.service_time = False
        individual.service_start_date = False
        individual.service_end_date = False
        individual.exit_date = False
        individual.queue_size_at_arrival = False
        individual.queue_size_at_departure = False
        individual.destination = False


class AmbulanceSimulation(ciw.Simulation):
    def __init__(self, network,
                 tracker=ciw.trackers.StateTracker(),
                 node_class=None,
                 arrival_node_class=None,
                 individual_class=None,
                 server_class=None,
                 params=None):
        self.params = params
        super().__init__(network,
                 exact=False,
                 name='Simulation',
                 tracker=tracker,
                 deadlock_detector=ciw.deadlock.NoDetection(),
                 node_class=node_class,
                 arrival_node_class=arrival_node_class,
                 individual_class=individual_class,
                 server_class=server_class)



def create_ambulance_network(params):
    N = ciw.create_network(
        arrival_distributions = {'Class ' + str(c): [ciw.dists.Exponential(r)] + [ciw.dists.NoArrivals() for _ in range(params['n_ambulances'])] for c, r in enumerate(params['loc_arrival_rates'])},
        service_distributions = {'Class ' + str(c): [ciw.dists.Deterministic(0)] + [make_service_dist(a, params) for a in range(params['n_ambulances'])] for c in range(params['n_locations'])},
        number_of_servers = [float('Inf')] + [1 for _ in range(params['n_ambulances'])],
        queue_capacities = [float('Inf')] + [0 for _ in range(params['n_ambulances'])],
        routing = {'Class ' + str(c): [[0 for _ in range(params['n_ambulances'] + 1)] for _ in range(params['n_ambulances'] + 1)] for c in range(params['n_locations'])}
    )
    return N
