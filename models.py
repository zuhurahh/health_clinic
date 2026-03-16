from datetime import datetime
from collections import deque


class Patient:
    """Represents a patient registered at the clinic."""

    PRIORITY_ORDER = {"Emergency": 0, "Urgent": 1, "Normal": 2}

    def __init__(self, name, age, complaint, priority="Normal"):
        self.name = name
        self.age = age
        self.complaint = complaint
        self.priority = priority
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
            "priority": self.priority,
            "registered_at": self.registered_at.strftime("%d %b %Y, %I:%M %p"),
        }


class ClinicQueue:
    """
    Manages the clinic's patient queue using a priority-based FIFO.
    Emergency > Urgent > Normal. Within same priority, FIFO applies.
    Uses collections.deque for efficient front/back operations.
    """

    def __init__(self):
        self._waiting_queue = deque()   # patients waiting (priority-ordered)
        self._seen_today = []           # list of patients already attended to
        self._ticket_counter = 1        # auto-incrementing ticket number
        self._priority_counts = {"Emergency": 0, "Urgent": 0, "Normal": 0}
        self._undo_stack = []           # stack for undo functionality

    def register_patient(self, name, age, complaint, priority="Normal"):
        """Creates a new Patient and adds them to the queue based on priority."""
        patient = Patient(name, age, complaint, priority)
        patient.ticket_number = self._ticket_counter
        self._ticket_counter += 1
        
        self._insert_by_priority(patient)
        self._priority_counts[priority] += 1
        return patient

    def _insert_by_priority(self, patient):
        """Insert patient based on priority: Emergency first, Urgent second, Normal last."""
        priority = patient.priority
        if priority == "Emergency":
            self._waiting_queue.appendleft(patient)
        elif priority == "Urgent":
            insert_idx = self._priority_counts.get("Emergency", 0)
            self._waiting_queue.insert(insert_idx, patient)
        else:
            self._waiting_queue.append(patient)

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
            self._undo_stack.append(patient)
            return patient
        return None

    def undo_last_call(self):
        """
        Restores the last called patient to the front of the queue.
        Returns the patient if successful, None if nothing to undo.
        """
        if self._undo_stack:
            patient = self._undo_stack.pop()
            self._seen_today.remove(patient)
            delattr(patient, 'seen_at')
            self._waiting_queue.appendleft(patient)
            return patient
        return None

    def can_undo(self):
        """Returns True if there is a patient that can be restored."""
        return len(self._undo_stack) > 0

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
