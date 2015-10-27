from platypus.algorithms import *
from platypus.problems import DTLZ2
from platypus.indicators import hypervolume
from multiprocessing import Pool
import matplotlib.pyplot as plt

# setup the comparison
problem = DTLZ2()
algorithms = [NSGAII(problem),
              NSGAIII(problem, divisions_outer=24),
              CMAES(problem, epsilons=[0.01]),
              GDE3(problem),
              IBEA(problem),
              MOEAD(problem),
              OMOPSO(problem, epsilons=[0.01]),
              SMPSO(problem),
              SPEA2(problem),
              EpsilonMOEA(problem, epsilons=[0.01])]

# run the algorithms in parallel
#pool = Pool(processes=8)
map(operator.methodcaller("run", 1000), algorithms)
    
# generate the result plot
hyp = hypervolume(minimum=[0,0], maximum=[1,1])
fig, axarr = plt.subplots(2, 5, sharex=True, sharey=True)

for i in range(len(algorithms)):
    ax = axarr[i/5, i%5]
    ax.scatter([s.objectives[0] for s in algorithms[i].result],
               [s.objectives[1] for s in algorithms[i].result])
    ax.set_title(algorithms[i].__class__.__name__)
    ax.annotate("Hyp: " + str(round(hyp(algorithms[i].result), 3)),
                xy=(0.9, 0.9),
                xycoords='axes fraction',
                horizontalalignment='right',
                verticalalignment='bottom')

fig.text(0.5, 0.04, '$f_1(x)$', ha='center', va='center')
fig.text(0.04, 0.5, '$f_2(x)$', ha='center', va='center', rotation='vertical')

plt.locator_params(nbins=4)
plt.show()