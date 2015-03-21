import sys, getopt
import numpy as np
import pylab as plt
from matplotlib.patches import Rectangle



def getHelp():
    print 'plot_offenders.py -i <inputfile>'
    sys.exit(2)

def main(argv):

    point_file = "../data/all_points.txt"

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        getHelp()
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            point_file = arg
        else:
            getHelp()


    print "Loading data (takes a while)"
    d = np.loadtxt(point_file,usecols=[0,1])
    ids = np.loadtxt(point_file,usecols=[2],dtype='str')
    

    xlim=(-125,-120)
    ylim=(35,40)

    print "Finding bad nodes"
    notliv = ~((d[:,0]>xlim[0]) * (d[:,0]<xlim[1])) + ~((d[:,1]>ylim[0])*(d[:,1]<ylim[1]))
    bad_ids=np.unique( ids[notliv] )
    dim=np.ceil(np.sqrt(bad_ids.size)).astype(np.int64)

    print "Number of offenders: ",bad_ids.size
    print "Plotting ",dim,"x",dim," figure"
    plt.figure()
    for i in range(0,bad_ids.size):
        tmp=d[ids==bad_ids[i]]
        plt.subplot(dim,dim,i+1,aspect='equal')
        plt.plot(tmp[:,0],tmp[:,1],'.r')
        plt.xlim([-180,180])
        plt.ylim([-90,90])
    
        ax = plt.gca()
        ax.add_patch(Rectangle((xlim[0],-90),abs(xlim[1]-xlim[0]),180,edgecolor='none',facecolor='steelblue'))
        ax.add_patch(Rectangle((-180,ylim[0]),360,abs(ylim[1]-ylim[0]),edgecolor='none',facecolor='steelblue'))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.title(bad_ids[i])
    plt.show()
    
if __name__ == "__main__":
   main(sys.argv[1:])
