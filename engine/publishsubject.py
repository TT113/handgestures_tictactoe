# subject observer pattern


class PublishSubject:
    def __init__(self, runloop):
        self._observers = set()
        self._subject_state = None
        self.runloop = runloop

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
            self.runloop.schedule_delayed_callback(0, lambda x: observer.update(x), [self._subject_state])#observer.update(self._subject_state)

    def update_subject(self, arg):
        self._subject_state = arg
        self._notify()


class PublishReceiver:
    def __init__(self, wrapped_fn):
        self.wrapped_fn = wrapped_fn

    def update(self, object):
        self.wrapped_fn(object)
