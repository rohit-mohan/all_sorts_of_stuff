from FFN.FFNetwork import Network
from FFN.FFNConfig import Config
from Pickle.PKLInput import Input
from Pickle.PKLOutput import Output
from Run.Run import Run


netObj = Network()
confObj = Config()
inObj = Input()
outObj = Output()
run = Run(netObj, confObj, inObj, outObj)

run.getConfig('configs/FFNconfig50000.cfg')
#run.runConfig()



