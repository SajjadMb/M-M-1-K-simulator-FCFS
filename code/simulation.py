from numpy import random
from typing import List

from process import Process
from event import Event

class Simulation:
    def __init__(self, arrival_rate) -> None:
        # Mu
        self.arrival_rate = arrival_rate
        # time
        self.time = 0
        # count of processes passed deadline
        self.deadProcess = 0
        # process count
        self.process_count = 0
        # count of processes dropped out because queue is full
        self.blockedProcess = 0
        # queue to serve process if server is full
        self.queue : List[Process] = []
        # list of events
        self.events : List[Event] = []
        # list of processes
        self.processes : List[Process] = []
        

    def increaseDeads(self) -> None:
        self.deadProcess += 1
    
    def increaseBlocked(self) -> None:
        self.blockedProcess += 1

    def nextArrivalTime(self) -> float:
        self.time += random.exponential(1/self.arrival_rate)
        return self.time

    def handleArrivalEvent(self, process:Process, event_time) -> Event:
        self.time = event_time
        if len(self.queue) == 12 :
            # Queue is Full Block Process
            self.increaseBlocked()
            return None
        elif 0 < len(self.queue) < 12:
            # Put process end of queue
            self.queue.append(process)
            return Event(
                etype = "Deadline",
                pid = process.pid,
                time = self.time + process.deadline
            )
        else:
            self.queue.append(process)
            return Event(
                etype = "Departure",
                pid = process.pid,
                time = self.time + process.service
            )

    def handleDepartureEvent(self, process:Process, event_time):
        self.time = event_time
        self.queue.remove(process)
        # delete deadline event
        if process in self.events:
            self.events.remove(process)
        if len(self.queue) > 0:
            if self.queue[0] in self.events:
                self.events.remove(self.queue[0])
            return Event(
                etype = "Departure",
                pid = self.queue[0].pid,
                time = self.time + self.queue[0].service
            )
        else:
            return None

    def handleDeadlineEvent(self, process:Process, event_time) -> None:
        self.time = event_time
        self.queue.remove(process)
        try:
            self.events.remove(process)
        except:
            pass
        self.increaseDeads()