import pprint
pp=pprint.PrettyPrinter(indent='3')

import sys
sys.path.append('..')

from rugstk_v1.data import munroecorpus
from rugstk_v1.demos import tacl,semdial
from rugstk_v1 import LUX


#run demos
print "running tacl demo. close it to proceed with example"
tacl() 
print "running semdial demo. close it to proceed with example"
semdial()

#get  lists of full paths to data files
print "running munroe corpus interface example"
colorname = 'light blue'
training = munroecorpus.get_training_handles()
dev = munroecorpus.get_dev_handles()
test = munroecorpus.get_test_handles()
train_fn = munroecorpus.get_training_filename(colorname,dim=0) #supply dim = 0,1,2 for h,s,v
dev_fn = munroecorpus.get_dev_filename(colorname)
test_fn = munroecorpus.get_test_filename(colorname)

example_train_data = munroecorpus.open_datafile(train_fn)
example_dev_data = munroecorpus.open_datafile(dev_fn)
example_test_data = munroecorpus.open_datafile(test_fn)

print "Example Training Handles:\n %s" % pp.pformat(training[0].items()[:10])
print "Example Dev Handles:\n %s" % pp.pformat(dev.items()[:10])
print "Example Test Handles:\n %s" % pp.pformat(test.items()[:10])

print "Example Training Filename:\n %s" % pp.pformat(train_fn)
print "Example Dev Filename :\n %s" % pp.pformat(dev_fn)
print "Example Test Filename:\n %s" % pp.pformat(test_fn)

print "Example Training Data: \n%s" % pp.pformat(example_train_data[:10]) 
print "Example Dev Data: \n%s" % pp.pformat(example_dev_data[:10])
print "Example Test Data: \n%s" % pp.pformat(example_test_data[:10])


#get lux
print "running lux example"
lux=LUX()
hsv = (200,100,100) #must be H \in [0,360], S \in [0,100], V \in [0,100]
print "argmax P(Label|HSV=%s)=%s" % (hsv,lux.predict(hsv))
print "First 10 of full posterior: \n%s" % pp.pformat(lux.full_posterior(hsv)[:10])
colorname = 'light blue'
print "P(%s|%s)=%s" % (colorname,hsv,lux.posterior_likelihood(hsv,colorname))
