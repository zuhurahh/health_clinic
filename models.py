from datetime import datetime
from collections import deque


class Patient:
    """Represents a patient registered at the clinic."""

    def __init__(self, name, age, complaint):
        self.name = name
        self.age = age
        self.complaint = complaint
        self.registered_at = datetime.now()
        self.ticket_number = None  # assigned by the queue manager

    def get_summary(self):
        """Returns a short summary string for this patient."""
        return (
            f"Ticket #{self.ticket_number} | {self.name} (Age {self.age}) "
            f"— {self.complaint} | Registered: {self.registered_at.strftime('%I:%M %p')}"
        )

    def to_dict(self):
        """Converts patient data to a dictionary for passing to HTML templates."""
        return {
            "ticket_number": self.ticket_number,
            "name": self.name,
            "age": self.age,
            "complaint": self.complaint,
            "registered_at": self.registered_at.strftime("%d %b %Y, %I:%M %p"),
        }


class ClinicQueue:
    """
    Manages the clinic's patient queue using a FIFO (Queue) data structure.
    Uses collections.deque for efficient front/back operations.
    """

    def __init__(self):
        self._waiting_queue = deque()   # FIFO queue — patients waiting
        self._seen_today = []           # list of patients already attended to
        self._ticket_counter = 1        # auto-incrementing ticket number

    def register_patient(self, name, age, complaint):
        """Creates a new Patient and adds them to the back of the queue."""
        patient = Patient(name, age, complaint)
        patient.ticket_number = self._ticket_counter
        self._ticket_counter += 1
        self._waiting_queue.append(patient)   # enqueue (FIFO: add to back)
        return patient

    def call_next_patient(self):
        """
        Removes and returns the next patient from the front of the queue.
        This is the FIFO dequeue operation.
        Returns None if the queue is empty.
        """
        if self._waiting_queue:
            patient = self._waiting_queue.popleft()  # dequeue (FIFO: remove from front)
            patient.seen_at = datetime.now()
            self._seen_today.append(patient)
            return patient
        return None

    def get_waiting_list(self):
        """Returns a list of dicts for all patients currently waiting."""
        return [p.to_dict() for p in self._waiting_queue]

    def get_seen_today(self):
        """Returns a list of dicts for all patients seen today."""
        result = []
        for p in self._seen_today:
            d = p.to_dict()
            d["seen_at"] = p.seen_at.strftime("%I:%M %p")
            result.append(d)
        return result

    def waiting_count(self):
        return len(self._waiting_queue)

    def seen_count(self):
        return len(self._seen_today)
