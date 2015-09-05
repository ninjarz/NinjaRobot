import threading

class NinjaQueue(object):
    class Unit(object):
        def __init__(self, data=None, last=None, next=None):
            self.data = data
            self.last = last
            self.next = next

    def __init__(self):
        self.mutex = threading.Lock()
        self.list_head = None
        self.list_tail = None

    def empty(self):
        if self.list_head is None:
            return True
        return False

    def push(self, data):
        self.mutex.acquire()
        unit = self.Unit(data, None, self.list_tail)
        if self.empty():
            self.list_head = unit
            self.list_tail = unit
        else:
            self.list_tail = unit
        self.mutex.release()

    def pop(self):
        self.mutex.acquire()
        unit = self.list_head
        if unit is not None:
            self.list_head = unit.last
            if self.list_head is None:
                self.list_tail = None
            self.mutex.release()
            return unit.data
        self.mutex.release()
        return None