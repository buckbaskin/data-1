from trace_nums import setup_data_workspace, DataInt
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
    	if count <= 0:
    		return DataFloat(0.0)
    	return self.score*1.0/self.count



def main():
	c = Calculation()
	c.set_data(1,2,3)
	print 'c1: '+str(c.data_to_value())
	dia = DataInt(2)
	dib = DataInt(3)
	print 'c2: '+str(c.data_to_value())
	c.update(dia)
	print 'c3: '+str(c.data_to_value())
	c.update(dib)
	print 'c4: '+str(c.data_to_value())

	c.reverse(dia.unique_id)
	print 'c5: '+str(c.data_to_value())

if __name__ == '__main__':
	main()