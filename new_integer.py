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

    def __init__(self, i_, local_id_tracker=None, source={}):
        super(DataInt, self).__init__(i_)
        
        self.unique_id = set()

        if local_id_tracker:
            self.unique_id.update([local_id_tracker.get_id()])
        else:
            try:
                self.unique_id.update([gidt.get_id()])
            except NameError:
                raise EnvironmentError('Data Workspace not yet set')
        self.unique_id.union(source)

    def __repr__(self):
        return str(self.real)

    def __str__(self):
        return self.__repr__()

    def __abs__(self):
        if self.real >= 0:
            return DataInt(self.real, source=self.unique_id)
        else:
            return DataInt(-1*self.real, source=self.unique_id)

    def __add__(self, y):
        return DataInt(self.real+y.real, 
            source=self.unique_id.union(y.unique_id))

    def __and__(self, y):
        return DataInt(self.real&y.real, 
            source=self.unique_id.union(y.unique_id))

    def __div__(self, y):
        # TODO(buckbaskin): check if y is DataFloat, float, and convert
        return DataInt(self.real / y.real, 
            source=self.unique_id.union(y.unique_id))

    # TODO def __coerce__(self, y)
    # TODO(buckbaskin): implement coerce with more data types

    def __divmod__(self, y):
        dia = DataInt(self.real // y.real,
            source=self.unique_id.union(y.unique_id))
        dib = DataInt(self.real % y.real,
            source=self.unique_id.union(y.unique_id))
        return (dia, dib,)

    # TODO def __float__(self):
    # TODO(buckbaskin): implement to DataFloat with more data types

    def __floordiv__(self, y):
        return DataInt(self.real // y.real, 
            source=self.unique_id.union(y.unique_id))

    # TODO def __hash__(self):
    # TODO(buckbaskin): possibly implement a new hash function

    def __invert__(self):
        return DataInt(-1*self.real - 1, 
            source=self.unique_id.union(y.unique_id))

    # TODO def __long__(self):
    # TODO(buckbaskin): implement to DataLong with more data types

    def __lshift__(self, y):
        return DataInt(self.real << y.real, 
            source=self.unique_id.union(y.unique_id))

    def __mod__(self, y):
        return DataInt(self.real % y.real, 
            source=self.unique_id.union(y.unique_id))

    def __mul__(self, y):
        # TODO(buckbaskin): check if y is DataFloat, float, and convert
        return DataInt(self.real * y.real, 
            source=self.unique_id.union(y.unique_id))

    def __neg__(self):
        return DataInt(-1*, source=self.unique_id)

    # TODO def __nonzero__(self, y):
    # TODO(buckbaskin): update this when there is a DataBool

    def __or__(self, y):
        return DataInt(self.real | y.real, 
            source=self.unique_id.union(y.unique_id))

    def __pow__(self, y, z=None):
        if z is not None:
            return DataInt(pow(self.real, y.real, z.real), 
                source=self.unique_id.union(y.unique_id).union(z.unique_id))
        else:
            return DataInt(pow(self.real, y.real), 
                source=self.unique_id.union(y.unique_id))

    def __radd__(self, y):
        return DataInt(y.real+self.real, 
            source=self.unique_id.union(y.unique_id))

    def __rand__(self, y):
        return DataInt(y.real&self.real, 
            source=self.unique_id.union(y.unique_id))

    def __rdiv__(self, y):
        # TODO(buckbaskin): check if y is DataFloat, float, and convert
        return DataInt(y.real / self.real, 
            source=self.unique_id.union(y.unique_id))

    def __rdivmod__(self, y):
        dia = DataInt(y.real // self.real, source=self.unique_id.union(y.unique_id))
        dib = DataInt(y.real % self.real, source=self.unique_id.union(y.unique_id)))
        return (dia, dib,)

    def __rfloordiv__(self, y):
        return DataInt(y.real // self.real, source=self.unique_id.union(y.unique_id))

    def __rlshift__(self, y):
        return DataInt(y.real << self.real, source=self.unique_id.union(y.unique_id))

    def __rmod__(self, y):
        return DataInt(y.real % self.real, source=self.unique_id.union(y.unique_id))

    def __rmul__(self, y):
        # TODO(buckbaskin): check if y is DataFloat, float, and convert
        return DataInt(y.real * self.real, source=self.unique_id.union(y.unique_id))

    def __ror__(self, y):
        return DataInt(y.real | self.real, source=self.unique_id.union(y.unique_id))

    def __rpow__(self, x, z=None):
        if z is not None:
            return DataInt(pow(x.real, self.real, z.real), source=self.unique_id.union(y.unique_id).union(z.unique_id)))
        else:
            return DataInt(pow(x.real, self.real), source=self.unique_id.union(y.unique_id))

    def __rrshift__(self, y):
        return DataInt(y.real >> self.real, source=self.unique_id.union(y.unique_id))

    def __rshift__(self, y):
        return DataInt(self.real >> y.real, source=self.unique_id.union(y.unique_id))

    def __rsub__(self, y):
        return DataInt(y.real - self.real, source=self.unique_id.union(y.unique_id))

    def __rtruediv__(self, y):
        return DataInt(1.0*y.real / self.real, source=self.unique_id.union(y.unique_id))

    def __rxor__(self, y):
        return DataInt(y.real^self.real, source=self.unique_id.union(y.unique_id))

    def __sub__(self, y):
        return DataInt(self.real - y.real, source=self.unique_id.union(y.unique_id))

    def __truediv__(self, y):
        return DataInt(1.0*self.real / y.real, source=self.unique_id.union(y.unique_id))

    def __trunc__(self):
        return DataInt(self.real, source=self.unique_id)

    def __xor__(self, y):
        return DataInt(self.real^y.real, source=self.unique_id.union(y.unique_id))

    def conjugate(self):
        return DataInt(self.real, source=self.unique_id)

    def remove(self):
        # take steps to remove this data point
        # TODO(buckbaskin): define what this operation should do
        pass

def setup_data_workspace():
    global gidt
    gidt = GlobalIdTracker()

    return gidt
