from KMeans.KMeansNetwork import Network
from KMeans.KMeansConfig import Config
from Pickle.PKLInput import Input
from Pickle.PKLOutput import Output
from Run.Run import Run

netObj = Network()
confObj = Config()
inObj = Input()
outObj = Output()

run = Run(netObj, confObj, inObj, outObj)
run.getConfig('configs/KMconfig.cfg')
run.runConfig()

from KMplots import makePlots
makePlots(confObj, basename='KM')

from plot_mean_var import meanVarPlots
meanVarPlots(confObj)
