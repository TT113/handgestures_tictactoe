# subject observer pattern


class PublishSubject:
    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer, instant_update=False):
        observer._subject = self
        self._observers.add(observer)
        if instant_update:
            observer.update(self._subject_state)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    def update_subject(self, arg):
        self._subject_state = arg
        self._notify()