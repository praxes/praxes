import weakref
import exceptions
import Queue
import time
#import threading

(UPDATEVALUE, FIREEVENT) = (1, 2)
#MAIN_THREAD = threading.currentThread()

class SpecClientDispatcherError(exceptions.Exception):
    def __init__(self, args=None):
        self.args = args


def robustApply(slot, arguments = ()):
    """Call slot with appropriate number of arguments"""
    if hasattr(slot, '__call__'):
        # Slot is a class instance ?
        if hasattr( slot.__call__, 'im_func'): # or hasattr( slot.__call__, 'im_code'): WARNING:im_code does not seem to exist?
            # Reassign slot to the actual method that will be called
            slot = slot.__call__

    if hasattr(slot, 'im_func'):
        # an instance method
        n_default_args = slot.im_func.func_defaults and len(slot.im_func.func_defaults) or 0
        n_args = slot.im_func.func_code.co_argcount - n_default_args - 1
    else:
        try:
            n_default_args = slot.func_defaults and len(slot.func_defaults) or 0
            n_args = slot.func_code.co_argcount - n_default_args
        except:
            raise SpecClientDispatcherError, 'Unknown slot type %s %s' % (repr(slot), type(slot))

    if len(arguments) < n_args:
        raise SpecClientDispatcherError, 'Not enough arguments for calling slot %s (need: %d, given: %d)' % (repr(slot), n_args, len(arguments))
    else:
        return slot(*arguments[0:n_args])


class Receiver:
    def __init__(self, weakReceiver, dispatchMode):
        self.weakReceiver = weakReceiver
        self.dispatchMode = dispatchMode


    def __call__(self, arguments):
        slot = self.weakReceiver() #get the strong reference

        if slot is not None:
            return robustApply(slot, arguments)


class Event:
    def __init__(self, sender, signal, arguments):
        self.receivers = []
        senderId = id(sender)
        signal = str(signal)
        self.args = arguments

        try:
            self.receivers = connections[senderId][signal]
        except:
            pass


class EventsQueue(Queue.Queue):
    def __init__(self):
        Queue.Queue.__init__(self, 0)


    def get(self):
        """Remove and return an item from the queue."""
        try:
            return Queue.Queue.get(self, False)
        except Queue.Empty:
            raise IndexError


    def put(self, event):
        """Put an event into the queue."""
        receiversList = event.receivers

        self.mutex.acquire()
        try:
            was_empty = not self._qsize()

            for r in receiversList:
                if not was_empty:
                    if r.dispatchMode == UPDATEVALUE:
                        for i in range(len(self.queue)):
                            _r, args = self.queue[i]
                            if r == _r:
                                del self.queue[i]
                                break

                self._put( (r, event.args) )
        finally:
            self.mutex.release()


class BoundMethodWeakRef(object):
        """'Safe' and reusable weak references to instance methods

        BoundMethodWeakRef objects provide a mechanism for
        referencing a bound method without requiring that the
        method object itself (which is normally a transient
        object) is kept alive.  Instead, the BoundMethodWeakref
        object keeps weak references to both the object and the
        function which together define the instance method.

        Attributes:
                key -- the identity key for the reference, calculated
                        by the class's calculateKey method applied to the
                        target instance method
                deletionMethods -- sequence of callable objects taking
                        single argument, a reference to this object which
                        will be called when *either* the target object or
                        target function is garbage collected (i.e. when
                        this object becomes invalid).  These are specified
                        as the onDelete parameters of safeRef calls.
                weakSelf -- weak reference to the target object
                weakFunc -- weak reference to the target function

        Class Attributes:
                _allInstances -- class attribute pointing to all live
                        BoundMethodWeakref objects indexed by the class's
                        calculateKey(target) method applied to the target
                        objects.  This weak value dictionary is used to
                        short-circuit creation so that multiple references
                        to the same (object, function) pair produce the
                        same BoundMethodWeakref instance.

        """
        _allInstances = weakref.WeakValueDictionary()
        def __new__( cls, target, onDelete=None, *arguments,**named ):
                """Create new instance or return current instance

                Basically this method of construction allows us to
                short-circuit creation of references to already-
                referenced instance methods.  The key corresponding
                to the target is calculated, and if there is already
                an existing reference, that is returned, with its
                deletionMethods attribute updated.  Otherwise the
                new instance is created and registered in the table
                of already-referenced methods.
                """
                key = cls.calculateKey(target)
                current =cls._allInstances.get(key)
                if current is not None:
                        current.deletionMethods.append( onDelete)
                        return current
                else:
                        base = super( BoundMethodWeakRef, cls).__new__( cls )
                        cls._allInstances[key] = base
                        base.__init__( target, onDelete, *arguments,**named)
                        return base
        def __init__(self, target, onDelete=None):
                """Return a weak-reference-like instance for a bound method

                target -- the instance-method target for the weak
                        reference, must have im_self and im_func attributes
                        and be reconstructable via:
                                target.im_func.__get__( target.im_self )
                        which is true of built-in instance methods.
                onDelete -- optional callback which will be called
                        when this weak reference ceases to be valid
                        (i.e. either the object or the function is garbage
                        collected).  Should take a single argument,
                        which will be passed a pointer to this object.
                """
                def remove(weak, self=self):
                    """Set self.isDead to true when method or instance is destroyed"""
                    methods = self.deletionMethods[:]
                    del self.deletionMethods[:]
                    try:
                        del self.__class__._allInstances[ self.key ]
                    except KeyError:
                        pass

                    for function in methods:
                        try:
                            if callable( function ):
                                function( self )
                        except:
                            pass

                self.deletionMethods = [onDelete]
                self.key = self.calculateKey( target )
                self.weakSelf = weakref.ref(target.im_self ,remove)
                self.weakFunc = weakref.ref(target.im_func, remove)
        def calculateKey( cls, target ):
                """Calculate the reference key for this reference

                Currently this is a two-tuple of the id()'s of the
                target object and the target function respectively.
                """
                return (id(target.im_self),id(target.im_func))
        calculateKey = classmethod( calculateKey )
        def __str__(self):
                """Give a friendly representation of the object"""
                return """%s( %s.%s )"""%(
                        self.__class__.__name__,
                        self.weakSelf(),
                        self.weakFunc().__name__,
                )
        __repr__ = __str__
        def __nonzero__( self ):
                """Whether we are still a valid reference"""
                return self() is not None

        def __cmp__( self, other ):
                """Compare with another reference"""
                if not isinstance (other,self.__class__):
                        return cmp( self.__class__, type(other) )
                return cmp( self.key, other.key)

        def __call__(self):
                """Return a strong reference to the bound method

                If the target cannot be retrieved, then will
                return None, otherwise returns a bound instance
                method for our object and function.

                Note:
                        You may call this method any number of times,
                        as it does not invalidate the reference.
                """
                target = self.weakSelf()
                if target is not None:
                    function = self.weakFunc()
                    if function is not None:
                        return function.__get__(target)
                return None


eventsToDispatch = EventsQueue()
connections = {} # { senderId0: { signal0: [receiver0, ..., receiverN], signal1: [...], ... }, senderId1: ... }
senders = {} # { senderId: sender, ... }


def callableObjectRef(object):
    """Return a safe weak reference to a callable object"""
    if hasattr(object, 'im_self'):
        if object.im_self is not None:
            # turn a bound method into a BoundMethodWeakReference instance
            return BoundMethodWeakRef(object, _removeReceiver)
    return weakref.ref(object, _removeReceiver)


def connect(sender, signal, slot, dispatchMode = UPDATEVALUE):
    if sender is None or signal is None:
        return

    if not callable(slot):
        return

    senderId = id(sender)
    signal = str(signal)
    signals = {}

    if senderId in connections:
        signals = connections[senderId]
    else:
        connections[senderId] = signals

    def remove(object, senderId=senderId):
        _removeSender(senderId)

    try:
        weakSender = weakref.ref(sender, remove)
        senders[senderId] = weakSender
    except:
        pass

    receivers = []

    if signal in signals:
        receivers = signals[signal]
    else:
        signals[signal] = receivers

    weakReceiver = callableObjectRef(slot)

    for r in receivers:
        if r.weakReceiver == weakReceiver:
            r.dispatchMode = dispatchMode
            return

    receivers.append(Receiver(weakReceiver, dispatchMode))


def disconnect(sender, signal, slot):
    if sender is None or signal is None:
        return

    if not callable(slot):
        return

    senderId = id(sender)
    signal = str(signal)

    try:
        signals = connections[senderId]
    except KeyError:
        return
    else:
        try:
            receivers = signals[signal]
        except KeyError:
            return
        else:
            weakReceiver = callableObjectRef(slot)

            toDel = None
            for r in receivers:
                if r.weakReceiver == weakReceiver:
                    toDel = r
                    break
            if toDel is not None:
                receivers.remove(toDel)

                _cleanupConnections(senderId, signal)


def emit(sender, signal, arguments = ()):
    eventsToDispatch.put(Event(sender, signal, arguments))
    #if threading.current_thread() == MAIN_THREAD:
    #    dispatch(-1)


def dispatch(max_time_in_s=1):
    t0 = time.time()
    while 1:
        try:
            receiver, args = eventsToDispatch.get()
        except IndexError:
            break
        else:
            receiver(args)
            if max_time_in_s < 0:
              continue
            elif (time.time()-t0) >= max_time_in_s:
              break


def _removeSender(senderId):
    try:
        del connections[senderId]
        del senders[senderId]
    except KeyError:
         pass


def _removeReceiver(weakReceiver):
    """Remove receiver from connections"""
    for senderId in connections.keys():
        for signal in connections[senderId].keys():
            receivers = connections[senderId][signal]

            for r in receivers:
                if r.weakReceiver == weakReceiver:
                    receivers.remove(r)
                    break

            _cleanupConnections(senderId, signal)


def _cleanupConnections(senderId, signal):
    """Delete any empty signals for sender. Delete sender if empty."""
    receivers = connections[senderId][signal]

    if len(receivers) == 0:
        # no more receivers
        signals = connections[senderId]
        del signals[signal]

        if len(signals) == 0:
            # no more signals
            _removeSender(senderId)

















