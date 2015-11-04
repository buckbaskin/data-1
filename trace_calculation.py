from trace_nums import setup_data_workspace, DataInt

class Calculation(object):
    def __init__(self):
        self.diffs = {}

    def set_data(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def operation(self, data):
        # returns the new chng'd calculation object
        # original + data => changed
        # override this to implement functionality
        return Calculation(self.a+data.real, self.b+data.real, self.c+data.real)

    def update(self, data):
        # call this method with data to update in a reversible way
        new_state = self.operation(data)

        diff = Diff(self, new_state)
        data_id = data.unique_id

        self.store_diff(data_id, diff)
        
        return diff.apply(self)

    def reverse(self, unique_id):
        new_state = self
        for uid in unique_id:
            if uid in self.diffs:
                for diff in self.diffs[uid]:
                    new_state = diff.reverse(new_state)
        return new_state


    def store_diff(self, data_id_set, diff):
        for id_ in data_id_set:
            if id_ not in self.diffs:
                self.diffs[id_] = []
            self.diffs[id_].append(diff)

    def data_to_value(self):
        # calculate value from the data. This should still work even if data changes
        return self.a

class Diff(object):
    def __init__(self, orig, chng, debug=False):
        for attr in set(dir(orig)).union(dir(chng)):
            if hasattr(getattr(orig,attr),'__call__'):
                pass
            elif getattr(orig,attr) is None:
                pass
            # elif len(attr) > 2 and attr[0:2] == '__'
            elif attr in dir(orig) and attr in dir(chng):
                # this is a value update
                try:
                    diff = getattr(chng,attr) - getattr(orig,attr)
                    if debug:
                        print str(attr)+' diff: '+str(diff)
                    setattr(self,attr,diff)
                except TypeError:
                    if debug:
                        print str(attr)+" can't do simple diff"
            elif attr in dir(orig):
                # delete this attr
                # print 'attr '+str(attr)+' in old only'
                pass
            else: # attr in dir(chng)
                # add this value
                # print 'attr '+str(attr)+' in new only'
                pass

    def apply(self, orig, debug=False):
        # make stored changes to an original
        for attr in set(dir(self)).union(dir(orig)):
            if hasattr(self, attr) and hasattr(getattr(self,attr),'__call__'):
                pass
            elif hasattr(orig, attr) and hasattr(getattr(orig,attr),'__call__'):
                pass
            elif hasattr(self, attr) and getattr(self,attr) is None:
                pass
            elif hasattr(orig, attr) and getattr(orig,attr) is None:
                pass
            elif hasattr(orig, attr) and hasattr(self, attr):
                # this is a value update
                try:
                    # it was: diff = getattr(chng,attr) - getattr(orig,attr)
                    # now it is: getattr(chng,attr) = getattr(orig,attr) + diff
                    change = getattr(orig,attr) + getattr(self,attr)
                    if debug:
                        print str(attr)+' chng: '+str(change)
                    setattr(orig,attr,change)
                except TypeError:
                    if debug:
                        print str(attr)+" can't do simple diff"

        return orig

    def reverse(self, chng, debug=False):
        # remove stored changes from a changed object
        for attr in set(dir(self)).union(dir(chng)):
            if hasattr(self, attr) and hasattr(getattr(self,attr),'__call__'):
                pass
            elif hasattr(chng, attr) and hasattr(getattr(chng,attr),'__call__'):
                pass
            elif hasattr(self, attr) and getattr(self,attr) is None:
                pass
            elif hasattr(chng, attr) and getattr(chng,attr) is None:
                pass
            elif hasattr(chng, attr) and hasattr(self, attr):
                # this is a value update
                try:
                    # it was: diff = getattr(chng,attr) - getattr(chng,attr)
                    # now it is: getattr(orig,attr) = getattr(chng,attr) - diff
                    change = getattr(chng,attr) - getattr(self,attr)
                    if debug:
                        print str(attr)+' chng: '+str(change)
                    setattr(chng,attr,change)
                except TypeError:
                    if debug:
                        print str(attr)+" can't do simple diff"

        return chng