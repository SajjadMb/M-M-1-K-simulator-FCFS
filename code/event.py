from process import Process

class Event:
    def __init__(self, etype, pid, time) -> None:
        super().__init__()
        # Arrival Deadline Departure
        self.type = etype
        self.pid = pid
        self.time = time

    def __lt__(self, other: object) -> bool:
        return self.time < other

    def __le__(self, other: object) -> bool:
        return self.time <= other

    def __gt__(self, other: object) -> bool:
        return self.time > other

    def __ge__(self, other: object) -> bool:
        return self.time >= other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Process):
            return self.pid == other.pid
        else:
            return self.time == other

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Process):
            return self.pid != other.pid
        else:
            return self.time != other

    def __repr__(self) -> str:
        return ("Event >>> Type = {0}\tProcess = {1}\tTime = {2}\n".format(
            self.type,
            self.pid,
            self.time
        ))
