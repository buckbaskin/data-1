from trace_nums import setup_data_workspace, DataInt

class Calculation(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def set_data(self):
        pass

    def data_to_value(self):
        # calculate value from the data. This should still work even if data changes
        pass

class Diff(object):
    def __init__(self, orig, chng):
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
                    print str(attr)+' diff: '+str(diff)
                    setattr(self,attr,diff)
                except TypeError:
                    print str(attr)+" can't do simple diff"
            elif attr in dir(orig):
                # delete this attr
                # print 'attr '+str(attr)+' in old only'
                pass
            else: # attr in dir(chng)
                # add this value
                # print 'attr '+str(attr)+' in new only'
                pass

    def apply(self, orig):
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
                    print str(attr)+' chng: '+str(change)
                    setattr(orig,attr,change)
                except TypeError:
                    print str(attr)+" can't do simple diff"

        return orig

    def reverse(self, chng):
        # remove stored changes from a changed object
        for attr in set(dir(orig)).union(dir(chng)):
            if hasattr(getattr(orig,attr),'__call__'):
                pass
            elif getattr(orig,attr) is None:
                pass
            elif attr in dir(orig) and attr in dir(chng):
                # this is a value update
                try:
                    # it was: diff = getattr(chng,attr) - getattr(orig,attr)
                    # now it is: getattr(orig,attr) = getattr(chng,attr) - diff
                    change = getattr(chng,attr) - getattr(self,attr)
                    print str(attr)+' chng: '+str(change)
                    setattr(chng,attr,change)
                except TypeError:
                    print str(attr)+" can't do simple diff"

        return chng