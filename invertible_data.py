

class Triple(object):
    def __init__(self, data, id_):
        self.data = data
        if isinstance(id_, list):
            self.id_ = id_
        else:
            self.id_ = [int(id)]
        self.inv = self.remove()

    def get_data(self):
        return self.data

    def get_ids(self):
        return self.id_

    def remove(self):
        # call this method to remove the Triple from data store
        print 'Removed '+str(self)+''

# class ID(object):
#     def __init__(self, i):
#         self.set_id(i)

#     def set_id(self, i):
#         self.id = int(i)

#     def id(self):
#         return self.id

class Calculation(object):
    # calculation is a mapping from old calculated value triple to new value 
    # triple
    def __init__(self):
        pass

    def __call__(self, new_data_triple):
        return self.operate(new_data_triple)

    def operate(self, new_data_triple):
        return new_data_triple


class CalculationInverse(object):
    # calculation inverse is a generator that creates a function based on a 
    # unique/user idthat takes in a old calculated value triple and maps it to a
    # new calculated value triple that doesn't include the original data in the 
    # calculation.
    def __init__(self):
        pass

    def __call__(self, id_):
        self.generate_inverse(id_)

    def generate_inverse(self, id_):
        def inverse_function(calc_triple):
            # do something with the id in here
            pass

        return inverse_function

class StudentScore(Triple):
    def __init__(self, test_score, student_id):
        super(StudentScore, self).__init__(int(test_score), int(student_id))

class CalcClassAvg(Calculation):
    def __init__(self):
        super(CalcClassAvg, self).__init__()

    def operate(self, new_data_triple, old_calc_triple):
        new_score = new_data_triple.get_data()
        new_ids = new_data_triple.get_ids()

        old_avg = old_calc_triple.get_data()
        old_count = old_calc_triple.class_size()
        old_ids = old_calc_triple.get_ids()

        new_avg = (old_avg*old_count+new_score)*1.0/(old_count+1)

        new_calc_triple = ClassAverage(avg=new_avg, count=old_count+1, ids=old_ids.extend(new_ids))
        new_calc_triple.inv = InvClassAvg(new_data_triple, old_calc_triple)

        return new_calc_triple


class ClassAverage(Triple):
    def __init__(self, avg=0, count=0, ids=0):
        # data is stored as a tuple of (average, class size)
        super(ClassAverage, self).__init__((float(avg),int(count),), ids)

    def get_data(self):
        # return averae
        return self.data[0]

    def class_size(self):
        return self.data[1]

class InvClassAvg(CalculationInverse):
    def __init__(self, input_triple, current_calc_triple):
        def generate_inverse(id_):
            if id_ in input_triple.get_ids():
                def inverse_function(calc_triple):
                    # remove data frokm previous operations:
                    # for example, if students have taken multiple tests included
                    # in the class average for a semester
                    calc_triple = current_calc_triple.generate_inverse(id_)(calc_triple)

                    # if there's still data to be removed (from this step)
                    # there should be, this is removing the the single test
                    if id_ in calc_triple.get_ids():
                        # remove previous data from the user/id
                        rm_score = input_triple.get_data()

                        old_avg = calc_triple.get_data()
                        old_count = calc_triple.class_size()
                        old_ids = calc_triple.get_ids()
                        
                        # remove the id from the list of ids that are in this calc
                        del old_ids[old_ids.index(id_)]

                        new_avg = (old_avg*old_count-rm_score)*1.0/(old_count-1)

                        new_calc_triple = ClassAverage(avg=new_avg, count=old_count+1, ids=old_ids)
                        def new_generate_inverse(id2):
                            if id2 == id_: # stop all previous inverse operations
                                def inverse_function(calc_triple):
                                    return calc_triple
                                return inverse_function
                            else:
                                return generate_inverse(id2)
                        new_calc_triple.inv = new_generate_inverse

                        return new_calc_triple
                    else:
                        # the given id was not a part of the data
                        return calc_triple

                return inverse_function
            else:
                # the id is not from this data
                return current_calc_triple.generate_inverse(id_)
        self.call_this = generate_inverse

    def __call__(self, id_):
        return self.call_this(id_)