"""An observable, settable value interface."""

from eventemitter import EventEmitter


class Value(EventEmitter):
    """
    A property value.

    This is used for communicating between the Thing representation and the
    actual physical thing implementation.

    Notifies all observers when the underlying value changes through an
    external update (command to turn the light off) or if the underlying sensor
    reports a new value.
    """

    def __init__(self, initial_value, setter=None):
        """
        Initialize the object.

        initial_value -- the initial value
        setter -- the method that updates the actual value on the thing
        """
        EventEmitter.__init__(self)
        self.last_value = initial_value

        if setter is None:
            def fn(_):
                raise AttributeError('Read-only value')

            self.setter = fn
        else:
            self.setter = setter

    def set(self, value):
        """
        Set a new value for this thing.

        value -- value to set
        """
        self.setter(value)
        self.notify_of_external_update(value)

    def get(self):
        """Return the last known value from the underlying thing."""
        return self.last_value

    def notify_of_external_update(self, value):
        """
        Notify observers of a new value.

        value -- new value
        """
        if value is not None and value != self.last_value:
            self.last_value = value
            self.emit('update', value)