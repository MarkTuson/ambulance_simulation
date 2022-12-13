import ciw
import pandas as pd
import math
from collections import namedtuple
import numpy as np

def classify(row):
    if np.isnan(row['rrv_pick_up_time']):
        return 'RRV not deployed'
    if row['rrv_delay_at_site'] == 0.0:
        return 'RRV arrived too late'
    if row['rrv_pick_up_time'] > row['ambulance_pick_up_time']:
        return 'RRV arrived after ambulance'
    return 'RRV arrived before ambulance'

def convert_from_class(clss, params):
    k = clss % params["n_specialities"]
    p = (clss - k) / params["n_specialities"]
    return int(p), int(k)

def convert_to_class(p, k, params):
    clss = (p * params["n_specialities"]) + k
    return int(clss)


def get_delay_period(time, params, secondary=False):
    sffx = ""
    if secondary:
        sffx = "_secondary"
    for i in range(params["n_factors" + sffx]):
        if time >= params["delay_split" + sffx][i] and time < params["delay_split" + sffx][i + 1]:
            return i

def find_max_dist(start_time, params, secondary=False):
    sffx = ""
    if secondary:
        sffx = "_secondary"
    frac_part, int_part = math.modf(start_time)
    i = get_delay_period(frac_part, params, secondary)
    max_duration = params["delay_split" + sffx][i + 1] - frac_part
    max_distance = (max_duration * params["delay_factor" + sffx][i])
    return max_distance, max_duration


def final_leg(start_time, distance_left, params, secondary=False):
    sffx = ""
    if secondary:
        sffx = "_secondary"
    frac_part, int_part = math.modf(start_time)
    i = get_delay_period(frac_part, params, secondary)
    tx = (distance_left / (params["delay_factor" + sffx][i])) + frac_part
    return tx - frac_part


def journey_time(start_time, required_distance, params, secondary=False):
    dist_covered = 0
    time_taken = 0
    max_dist, duration = 0, 0
    while dist_covered + max_dist < required_distance:
        dist_covered += max_dist
        time_taken += duration
        max_dist, duration = find_max_dist(start_time + time_taken, params, secondary)
    time_taken += final_leg(
        start_time + time_taken, required_distance - dist_covered, params, secondary
    )
    return time_taken


def expected_pickup(initial_call_time, a, p, params, secondary=False):
    """
    The expected service time for ambulance a to service patient p in time period t.
    Consists of:
      - getting to the patient
    """
    pick_up_transit_time = journey_time(initial_call_time, params["amb_to_patient"][a][p], params, secondary)
    return pick_up_transit_time + initial_call_time


def get_service(initial_call_time, ind, params):
    """
    The expected service time for ambulance a to service patient p in time period t.
    Consists of:
      - getting to the patient
      - delay at site
      - taking patient to the hospital
      - delay at hospital
      - getting back to ambulance location from the hospital
    """
    a, p, k = ind.ambulance, ind.pick_up_location, ind.speciality
    expected_pick_up_transit_time = journey_time(initial_call_time, params["amb_to_patient"][a][p], params)
    ind.expected_pick_up_time = expected_pick_up_transit_time
    pick_up_transit_time = ciw.random.triangular(0.75, 1.25, 1) * expected_pick_up_transit_time
    ind.pick_up_time = pick_up_transit_time
    initial_call_time += pick_up_transit_time

    delay_at_site = ciw.random.lognormvariate(params["delay_at_site"][0], params["delay_at_site"][1]) / 24
    initial_call_time += delay_at_site
    ind.delay_at_site = delay_at_site

    hosp_probs = [params["prob_hosp"][p][h][k] for h in range(params['n_hospitals'])]
    hospital = ciw.random_choice(
        list(range(params['n_hospitals'])) + [-1],
       hosp_probs + [1 - sum(hosp_probs)]
    )

    if hospital == -1:
        ind.hospital = None
        ind.to_hospital_time = None
        ind.delay_at_hospital = None

        expected_return_to_loc_time = journey_time(initial_call_time, params["patient_to_amb"][p][a], params)
        return_to_loc_time = ciw.random.triangular(0.75, 1.25, 1) * expected_return_to_loc_time
        ind.return_to_loc_time = return_to_loc_time

        ind.refill_time = params['refill_time'][0]

        ind.complete_time = ind.pick_up_time + ind.delay_at_site + ind.return_to_loc_time + ind.refill_time

    else:
        ind.hospital = hospital
        expected_to_hosp_transit_time = journey_time(initial_call_time, params["patient_to_hosp"][p][hospital], params)
        to_hosp_transit_time = ciw.random.triangular(0.75, 1.25, 1) * expected_to_hosp_transit_time
        initial_call_time += to_hosp_transit_time
        ind.to_hospital_time = to_hosp_transit_time

        delay_at_hospital = ciw.random.uniform(params["delay_at_hosp"][k][0], params["delay_at_hosp"][k][1])
        initial_call_time += delay_at_hospital
        ind.delay_at_hospital = delay_at_hospital

        expected_return_to_loc_time = journey_time(initial_call_time, params["hosp_to_amb"][hospital][a], params)
        return_to_loc_time = ciw.random.triangular(0.75, 1.25, 1) * expected_return_to_loc_time
        ind.return_to_loc_time = return_to_loc_time

        ind.refill_time = params['refill_time'][0]

        ind.complete_time = ind.pick_up_time + ind.delay_at_site + ind.to_hospital_time + ind.delay_at_hospital + ind.return_to_loc_time + ind.refill_time


def make_service_dist(params):
    class TransitTrip(ciw.dists.Distribution):
        def sample(self, t, ind):
            get_service(t, ind, params)
            return ind.complete_time

    return TransitTrip()


TransitDataRecord = namedtuple(
    "TransitRecord",
    [
        "id_number",
        "pick_up_location",
        "speciality",
        "hospital",
        "ambulance_location",
        "ambulance_id",
        "call_date",
        "ambulance_service_start_date",
        "ambulance_service_time",
        "ambulance_expected_pick_up_time",
        "ambulance_pick_up_time",
        "ambulance_delay_at_site",
        "ambulance_to_hospital_time",
        "ambulance_delay_at_hospital",
        "ambulance_return_to_loc_time",
        'ambulance_refill_time',
        "ambulance_service_end_date",
        "destination",
    ],
)


class TransitJob(ciw.Individual):
    def __init__(self, id_number, customer_class=0, priority_class=0, simulation=False):
        super().__init__(id_number, customer_class, priority_class, simulation)
        self.pick_up_time = False
        self.expected_pick_up_time = False
        self.delay_at_site = False
        self.to_hospital_time = False
        self.delay_at_hospital = False
        self.return_to_loc_time = False
        self.refill_time = False
        p, k = convert_from_class(customer_class, simulation.params)
        self.speciality = k
        self.pick_up_location = p
        self.hospital = False
        self.ambulance = False


class TransitNode(ciw.Node):
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
            choices = {
                a: expected_pickup(
                    self.simulation.current_time,
                    a,
                    ind.pick_up_location,
                    self.simulation.params,
                )
                for a in range(self.simulation.network.number_of_nodes - 1)
            }
            ordered_choices = sorted(choices.keys(), key=lambda x: choices[x])
            for choice in ordered_choices:
                node = self.simulation.nodes[choice + 2]
                for s in node.servers:
                    if not s.busy:
                        ind.ambulance = node.id_number - 2
                        return node
            return self.simulation.nodes[-1]

    def write_individual_record(self, individual):
        """
        Write a data record for an individual:
        - id_number
        - pick_up_location
        - speciality
        - hospital
        - ambulance_location
        - ambulance_id
        - arrival_date
        - service_start_date
        - service_time
        - expected_pick_up_time
        - pick_up_time
        - delay_at_site
        - to_hospital_time
        - delay_at_hospital
        - return_to_loc_time
        - refill_time
        - service_end_date
        - destination

        """
        if math.isinf(self.c):
            server_id = False
        else:
            server_id = individual.server.id_number

        record = TransitDataRecord(
            individual.id_number,
            individual.pick_up_location,
            individual.speciality,
            individual.hospital,
            individual.ambulance,
            f"L{individual.ambulance} V{server_id}",
            individual.arrival_date,
            individual.service_start_date,
            individual.service_end_date - individual.service_start_date,
            individual.expected_pick_up_time,
            individual.pick_up_time,
            individual.delay_at_site,
            individual.to_hospital_time,
            individual.delay_at_hospital,
            individual.return_to_loc_time,
            individual.refill_time,
            individual.service_end_date,
            individual.destination
        )
        individual.data_records.append(record)


class TransitSimulation(ciw.Simulation):
    def __init__(
        self,
        network,
        tracker=ciw.trackers.StateTracker(),
        node_class=None,
        arrival_node_class=None,
        individual_class=None,
        server_class=None,
        params=None,
    ):
        self.params = params
        super().__init__(
            network,
            exact=False,
            name="Simulation",
            tracker=tracker,
            deadlock_detector=ciw.deadlock.NoDetection(),
            node_class=node_class,
            arrival_node_class=arrival_node_class,
            individual_class=individual_class,
            server_class=server_class,
        )

def transpose_and_flatten(got):
    got_t = [[row[i] for row in got] for i in range(len(got[0]))]
    want = [r for row in got_t for r in row]
    return want

def create_transit_network(params, max_time):
    arrival_rates = transpose_and_flatten(params['loc_arrival_rates'])
    N = ciw.create_network(
        arrival_distributions={
            "Class "
            + str(c): [ciw.dists.PoissonIntervals(rates=r, endpoints=params["demand_split"], max_sample_date=max_time)]
            + [ciw.dists.NoArrivals() for a in range(params["n_ambulances"])]
            for c, r in enumerate(arrival_rates)
        },
        service_distributions={
            "Class "
            + str(c): [ciw.dists.Deterministic(0)]
            + [make_service_dist(params) for a in range(params["n_ambulances"])]
            for c in range(params["n_locations"] * params['n_specialities'])
        },
        number_of_servers=[float("Inf")] + params["allocation"],
        queue_capacities=[float("Inf")] + [0 for _ in range(params["n_ambulances"])],
        routing={
            "Class "
            + str(c): [
                [0 for _ in range(params["n_ambulances"] + 1)]
                for _ in range(params["n_ambulances"] + 1)
            ]
            for c in range(params["n_locations"] * params['n_specialities'])
        },
    )
    return N


class ResponseSimulation(ciw.Simulation):
    def __init__(
        self,
        network,
        tracker=ciw.trackers.StateTracker(),
        node_class=None,
        arrival_node_class=None,
        individual_class=None,
        server_class=None,
        params=None,
        initial_recs=None,
    ):
        self.params = params
        self.initial_recs = initial_recs
        super().__init__(
            network,
            exact=False,
            name="Simulation",
            tracker=tracker,
            deadlock_detector=ciw.deadlock.NoDetection(),
            node_class=node_class,
            arrival_node_class=arrival_node_class,
            individual_class=individual_class,
            server_class=server_class,
        )


class ResponseJob(ciw.Individual):
    def __init__(self, id_number, row, customer_class=0, priority_class=0, simulation=False):
        super().__init__(id_number, customer_class, priority_class, simulation)
        self.ambulance_pick_up_time = row['ambulance_pick_up_time']
        self.expected_ambulance_pick_up_time = row['ambulance_expected_pick_up_time']
        self.ambulance_delay_at_site = row['ambulance_delay_at_site']
        self.speciality = row['speciality']
        self.pick_up_location = row['pick_up_location']
        self.pick_up_time = False
        self.delay_at_site = False
        self.return_to_loc_time = False
        self.refill_time = False
        self.rrv = False


ResponseDataRecord = namedtuple(
    "ResponseRecord",
    [
        "id_number",
        "rrv_location",
        "rrv_id",
        "rrv_service_time",
        "rrv_pick_up_time",
        "rrv_delay_at_site",
        "rrv_return_to_loc_time",
        'rrv_refill_time'
    ],
)


class ResponseNode(ciw.Node):
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
            choices = {
                a: expected_pickup(
                    self.simulation.current_time,
                    a,
                    ind.pick_up_location,
                    self.simulation.params,
                    secondary=True
                )
                for a in range(self.simulation.network.number_of_nodes - 1)
            }
            ordered_choices = sorted(choices.keys(), key=lambda x: choices[x])
            for choice in ordered_choices:
                node = self.simulation.nodes[choice + 2]
                for s in node.servers:
                    if not s.busy:
                        ind.rrv = node.id_number - 2
                        return node
            return self.simulation.nodes[-1]

    def write_individual_record(self, individual):
        """
        Write a data record for an individual:
        - id_number
        - rrv_location
        - rrv_id
        - rrv_service_time
        - rrv_pick_up_time
        - rrv_delay_at_site
        - rrv_return_to_loc_time
        - rrv_refill_time
        """
        if math.isinf(self.c):
            server_id = False
        else:
            server_id = individual.server.id_number

        record = ResponseDataRecord(
            individual.id_number,
            self.id_number - 2,
            f"L{individual.rrv} V{server_id}",
            individual.service_end_date - individual.service_start_date,
            individual.pick_up_time,
            individual.delay_at_site,
            individual.return_to_loc_time,
            individual.refill_time
        )
        individual.data_records.append(record)


class ResponseArrivalNode(ciw.ArrivalNode):
    def have_event(self):
        """
        Finds a batch size. Creates that many Individuals and send
        them to the relevent node. Then updates the event_dates_dict.
        """
        batch = self.batch_size(self.next_node, self.next_class)
        for _ in range(batch):
            self.number_of_individuals += 1
            self.number_of_individuals_per_class[self.next_class] += 1
            priority_class = self.simulation.network.priority_class_mapping[
                self.next_class]
            row = self.simulation.initial_recs.iloc[self.number_accepted_individuals]
            next_individual = self.simulation.IndividualType(
                row['id_number'],
                row,
                self.next_class,
                priority_class,
                simulation=self.simulation)
            if self.simulation.network.process_based:
                next_individual.route = self.simulation.network.customer_classes[
                next_individual.customer_class].routing[self.next_node - 1](next_individual)
            next_node = self.simulation.transitive_nodes[self.next_node - 1]
            self.release_individual(next_node, next_individual)

        self.event_dates_dict[self.next_node][
            self.next_class] = self.increment_time(
            self.event_dates_dict[self.next_node][
            self.next_class], self.inter_arrival(
            self.next_node, self.next_class))
        self.find_next_event_date()


def get_service_response(initial_call_time, ind, params):
    """
    The expected service time for rrv a to service patient p in time period t.
    Consists of:
      - getting to the patient
      - delay at site
      - getting back to rrv location from the hospital
    """
    a, p, k = ind.rrv, ind.pick_up_location, ind.speciality
    expected_pick_up_transit_time = journey_time(initial_call_time, params["amb_to_patient"][a][p], params, secondary=True)
    ind.expected_pick_up_time = expected_pick_up_transit_time
    if ind.expected_pick_up_time > ind.expected_ambulance_pick_up_time:
        ind.complete_time = 0
    else:
        pick_up_transit_time = ciw.random.triangular(0.75, 1.25, 1) * expected_pick_up_transit_time
        ind.pick_up_time = pick_up_transit_time

        ind.delay_at_site = max(ind.ambulance_pick_up_time + ind.ambulance_delay_at_site - ind.pick_up_time, 0)
        
        expected_return_to_loc_time = journey_time(initial_call_time, params["patient_to_amb"][p][a], params, secondary=True)
        return_to_loc_time = ciw.random.triangular(0.75, 1.25, 1) * expected_return_to_loc_time
        ind.return_to_loc_time = return_to_loc_time

        ind.refill_time = params['refill_time'][1]
        
        ind.complete_time = ind.pick_up_time + ind.delay_at_site + ind.return_to_loc_time + ind.refill_time


def make_response_service_dist(params):
    class ResponseTrip(ciw.dists.Distribution):
        def sample(self, t, ind):
            get_service_response(t, ind, params)
            return ind.complete_time

    return ResponseTrip()


def create_response_network(params, initial_recs):
    arrivals = [list(initial_recs['call_date'])[0]] + list(initial_recs['call_date'].diff())[1:] + [float('inf')]
    N = ciw.create_network(
        arrival_distributions=[ciw.dists.Sequential(arrivals)] + [ciw.dists.NoArrivals() for _ in range(params['n_ambulances'])],
        service_distributions=[ciw.dists.Deterministic(0)] + [make_response_service_dist(params) for _ in range(params['n_ambulances'])],
        number_of_servers=[float("Inf")] + params["allocation_secondary"],
        routing=[[0 for _ in range(params["n_ambulances"] + 1)] for _ in range(params["n_ambulances"] + 1)]
    )
    return N



def run_full_simulation(params, max_time, trial):
    ciw.seed(trial)
    N_transit = create_transit_network(params, max_time)
    Q_transit = TransitSimulation(
        N_transit, node_class=TransitNode, individual_class=TransitJob, params=params
    )
    Q_transit.simulate_until_max_time(max_time, progress_bar=False)
    recs_transit = pd.DataFrame(Q_transit.get_all_records())
    recs_transit = recs_transit[recs_transit['destination'] == -1]
    
    initial_recs = recs_transit[recs_transit['ambulance_location'] != 'False'].sort_values('call_date').reset_index()
    N_response = create_response_network(params, initial_recs)
    Q_response = ResponseSimulation(
        N_response,
        arrival_node_class=ResponseArrivalNode,
        individual_class=ResponseJob,
        node_class=ResponseNode,
        params=params,
        initial_recs=initial_recs
    )
    Q_response.simulate_until_max_time(max_time)
    recs_response = Q_response.get_all_records()
    recs_response = pd.DataFrame(recs_response)
    recs_response = recs_response[recs_response['rrv_location'] != -1]
    
    recs_response = recs_response.set_index('id_number')
    recs_transit = recs_transit.set_index('id_number')
    recs = pd.concat([recs_transit, recs_response], axis=1)
    recs.replace(to_replace=False, value=np.NAN, inplace=True, method=None)
    recs['response_time'] = recs[['ambulance_pick_up_time', 'rrv_pick_up_time']].min(axis=1)
    recs['rrv_action'] = recs.apply(classify, axis=1)
    recs["trial"] = trial
    return recs
