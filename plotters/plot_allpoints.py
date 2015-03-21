import sys, getopt
import numpy as np
import pylab as plt
from matplotlib.patches import Rectangle



def getHelp():
    print 'plot_allpoints.py -i <inputfile> -t [hist|points]'
    sys.exit(2)

def main(argv):

    point_file = "../data/all_points.txt"
    plot_type = "points"
    try:
        opts, args = getopt.getopt(argv,"hi:t:",["ifile=","type="])
    except getopt.GetoptError:
        getHelp()
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            point_file = arg
        if opt in ("-t", "--type"):
            plot_type = arg            
        else:
            getHelp()

    print "Loading data (takes a while)"
    d = np.loadtxt(point_file,usecols=[0,1])
    ids = np.loadtxt(point_file,usecols=[2],dtype='str')

    #Broad bounding box for Livermore area
    xlim=(-125,-120)
    ylim=(35,40)
    
    #Locate points outside of livermore
    notliv = ~((d[:,0]>xlim[0]) * (d[:,0]<xlim[1])) + ~((d[:,1]>ylim[0])*(d[:,1]<ylim[1]))
    dnot = d[notliv]
    bad_ids=np.unique( ids[notliv] )

    plt.figure()

    if(plot_type=="hist"):
        plt.subplot(211)
        plt.hist(d[:,0],bins=100,log=True)
        plt.subplot(212)
        plt.hist(d[:,1],bins=100,log=True)

    if(plot_type=="points"):
        ax = plt.gca()
        ax.add_patch(Rectangle((xlim[0],-90),abs(xlim[1]-xlim[0]),180,edgecolor='none',facecolor='steelblue'))
        ax.add_patch(Rectangle((-180,ylim[0]),360,abs(ylim[1]-ylim[0]),edgecolor='none',facecolor='steelblue'))

        ax.add_patch(Rectangle((ylim[0],-90),abs(ylim[1]-ylim[0]),180,edgecolor='none',facecolor='pink',label='Lon/Lat Swapped?'))
        ax.set_aspect('equal')

        plt.plot(d[:,0],d[:,1],'.b',lw=0)
        plt.plot(dnot[:,0],dnot[:,1],'.r',lw=0)

        plt.xlim([-180, 180])
        plt.ylim([-90,90])
        plt.legend(loc='lower right')

    #originally did some heat maps, but they didn't look right
    #if(plot_type=="heat"):
    #    heatmap, xedges, yedges = np.histogram2d(d[:,0], d[:,1], bins=64)
    #    #heatmap, xedges, yedges = np.histogram2d(dnot[:,0], dnot[:,1], bins=64)
    #    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    #    plt.clf()
    #    plt.imshow(heatmap, extent=extent)

    plt.show()


if __name__ == "__main__":
   main(sys.argv[1:])

