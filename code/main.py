import bisect
import csv
import time as tm
from simulation import Simulation
from process import Process
from event import Event
from analyze import Analyze


def simulate(waiting_time, service_rate, arrival_rate, problem_size, is_exponential=True):

    arrival = 0

    simulation = Simulation(arrival_rate)

    while simulation.process_count < problem_size:
        if not simulation.events or simulation.events[0] > arrival:
            simulation.processes.append(
            Process(
                pid=simulation.process_count,
                arrival=arrival,
                deadline_time=waiting_time,
                service_rate=service_rate,
                expo_deadline=is_exponential
                )
            )
            result_event = simulation.handleArrivalEvent(
                simulation.processes[simulation.process_count],
                arrival)
            if result_event:
                bisect.insort_left(simulation.events, result_event)
            arrival = simulation.nextArrivalTime()
            simulation.process_count += 1
        else:
            event = simulation.events.pop(0)
            if event.type == "Departure":
                # Handle Departure
                result_event = simulation.handleDepartureEvent(
                    simulation.processes[event.pid],
                    event.time)
                if result_event:
                    bisect.insort_left(simulation.events, result_event)
            elif event.type == "Deadline":
                # Handle Deadline
                simulation.handleDeadlineEvent(simulation.processes[event.pid],event.time)
        

    Pb = simulation.blockedProcess/problem_size
    Pd = simulation.deadProcess/problem_size
    return Pb, Pd


def writeDownResult(result: list):
    with open('result.csv', 'a', newline='') as csvfile:
        result_writer = csv.writer(csvfile, delimiter=',')
        result_writer.writerow(result)


if __name__ == "__main__":
    waiting_time = 2
    service_rate = 1
    # arrival_rates = [i/10 for i in range(1,201,1)]
    arrival_rates = [5,10,15]
    problem_size = 10**6
    print("Problem Size is : {}".format(problem_size))
    with open('result.csv', 'a', newline='') as csvfile:
        result_writer = csv.writer(csvfile, delimiter=',')
        result_writer.writerow(
            ["Waiting_Time_Type", "Teta", "Mu", "Lambda", "Analysis_type", "PB", "PD"])
    
    with open("parameters.conf", 'r') as reader:
        while True:
            try:
                waiting_time = int(reader.readline())
                service_rate = int(reader.readline())
            except:
                break

            for arrival_rate in arrival_rates:
                start = tm.time()
                simulation_pb, simulation_pd = simulate(waiting_time,
                                                        service_rate,
                                                        arrival_rate,
                                                        problem_size,
                                                        is_exponential=False)
                print("simulation process time for arrival-rate={}  and constant waiting time : {}".format(arrival_rate, tm.time() - start))
                writeDownResult(["constant", waiting_time, service_rate, arrival_rate,
                                 "Simulation", simulation_pb, simulation_pd])

                statistical_pb, statistical_pd = Analyze(mu=service_rate,
                                                         teta=waiting_time,
                                                         lam=arrival_rate,
                                                         is_expnential=False).analyze()

                writeDownResult(["constant", waiting_time, service_rate, arrival_rate,
                                 "Statistical", statistical_pb, statistical_pd])

                start = tm.time()
                simulation_pb, simulation_pd = simulate(waiting_time,
                                                        service_rate,
                                                        arrival_rate,
                                                        problem_size,
                                                        is_exponential=True)
                print("simulation process time for arrival-rate={} and exponential waiting time : {}".format(arrival_rate, tm.time() - start))
                writeDownResult(["exponential", waiting_time, service_rate, arrival_rate,
                                 "Simulation", simulation_pb, simulation_pd])

                statistical_pb, statistical_pd = Analyze(mu=service_rate,
                                                         teta=waiting_time,
                                                         lam=arrival_rate,
                                                         is_expnential=True).analyze()

                writeDownResult(["exponential", waiting_time, service_rate, arrival_rate,
                                 "Statistical", statistical_pb, statistical_pd])
            
    print("results are stored in result.csv")
