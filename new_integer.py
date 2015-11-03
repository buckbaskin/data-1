import hashlib
import time
import weakref

class GlobalIdTracker(object):
    def __init__(self):
        self.next_id = 1
        self.hashm = hashlib.sha1()

    def get_id(self):
        self.hashm.update("%.20f" % time.time())
        return self.hashm.hexdigest()

class DataInt(int):

    def __new__(cls, *args, **vargs):
        val = int.__new__(cls, *args, **vargs)
        if len(args) >= 2:
            val.__init__(args[0], args[1])
        else:
            val.__init__(args[0])
        val.strong_ref = val
        return weakref.proxy(val)
    
    def __init__(self, i_, local_id_tracker=None):
        super(DataInt, self).__init__(i_)
        if local_id_tracker:
            self.unique_id = [local_id_tracker.get_id()]

        try:
            self.unique_id = [gidt.get_id()]
        except NameError as ne:
            raise(EnvironmentError('Data Workspace not yet set'))

    def __repr__(self):
        return str(self.real)

    def __str__(self):
        return __repr__(self)

    def __abs__(self):
        if self.real >= 0:
            di = DataInt(self.real)
            di.unique_id = self.unique_id
            return di
        else:
            di = DataInt(-1*self.real)
            di.unique_id = self.unique_id
            return di

    def __add__(self, y):
        di = DataInt(self.real+y.real)
        di.unique_id = self.unique_id.extend(y.unique_id)
        return di

    def __sub__(self, y):
        di = DataInt(self.real-y.real)
        di.unique_id = self.unique_id.extend(y.unique_id)
        return di

    def __and__(self, y):
        di = DataInt(self.real&y.real)
        di.unique_id = self.unique_id.extend(y.unique_id)
        return di

    def __div__(self, y):
        di = DataInt(self.real / y.real)
        di.unique_id = self.unique_id.extend(y.unique_id)
        return di

    # TODO def __coerce__(self, y)
    # TODO(buckbaskin): implement coerce with more data types

    def __divmod__(self, y):
        dia = DataInt(self.real // y.real)
        dib = DataInt(self.real % y.real)
        dia.unique_id = self.unique_id.extend(y.unique_id)
        dib.unique_id = self.unique_id.extend(y.unique_id)
        return (dia, dib,)

    def __floordiv__(self, y):
        di = DataInt(self.real // y.real)
        di.unique_id = self.unique_id.extend(y.unique_id)
        return di

    def remove(self):
        del self

    # TODO def __float__(self):
    # TODO(buckbaskin): implement to DataFloat with more data types

def setup_data_workspace():
    global gidt
    gidt = GlobalIdTracker()

    return gidt
