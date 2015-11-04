from trace_nums import setup_data_workspace, DataInt, DataFloat
from trace_calculation import Calculation

setup_data_workspace()

class StudentAverage(Calculation):

    def __init__(self):
        super(StudentAverage, self).__init__()
        self.set_data(0,0)

    def set_data(self, score, count):
        self.score = score
        self.count = count

    def operation(self, new_score):
        sa = StudentAverage()
        sa.set_data(self.score+new_score, self.count+1)
        return sa

    def data_to_value(self):
        if self.count <= 0:
            return DataFloat(0.0)
        return self.score*1.0/self.count



def main():
    s = StudentAverage()
    print 's1: '+str(s.data_to_value())
    
    studenta = DataInt(75)
    studentb = DataInt(25)
    studentc = DataInt(100)
    studentd = DataInt(50)

    print 'add student a: score 75'
    s.update(studenta)
    print 's3: '+str(s.data_to_value())
    
    print 'add student b: score 25'
    s.update(studentb)
    print 's4: '+str(s.data_to_value())

    print 'add student c: score 100'
    s.update(studentc)
    print 's4c: '+str(s.data_to_value())

    print 'remove student a data:'
    s.reverse(studenta.unique_id)
    print 's5: '+str(s.data_to_value())

    print 'add student d: score 50'
    s.update(studentd)
    print 's6: '+str(s.data_to_value())


if __name__ == '__main__':
    main()