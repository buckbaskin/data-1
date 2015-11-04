from trace_nums import setup_data_workspace, DataInt, DataFloat
from trace_calculation import Calculation

setup_data_workspace()

df = DataFloat(-1.5)

dg = df.__abs__()

print 'dg type: '+str(type(dg))

print str(dg.unique_id)