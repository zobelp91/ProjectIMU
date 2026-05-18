import mathlib as ml
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D # Axes3D causes error notification 
import numpy as np

def plotVector(x, vector):
    """ plots 3x1 vector using subplots
    """
    y1, y2, y3 = ml.toValue(vector)
    symbol = 'ro'
    plt.subplot(311)
    plt.plot(x,y1,symbol)
    plt.subplot(312)
    plt.plot(x,y2,symbol)
    plt.subplot(313)
    plt.plot(x,y3,symbol)
    
def plotRGB(x,vector):
    """ plots 3x1 vector in 1 axis
    """
    y1, y2, y3 = ml.toValue(vector)
    handle1, = plt.plot(x,y1,'ro')
    handle2, = plt.plot(x,y2,'go')
    handle3, = plt.plot(x,y3,'bo')
    plt.grid(True)
    plt.legend([handle1, handle2, handle3], ['X','Y','Z'])
    

def plot3DFrame(s,ax):
    """ transforms and plots 3 orthognal vectors representing the orientation
        requires a strapdown-object and an 3D axis as argument
    """
    q = s.quaternion.getConjugatedQuaternion()
    xn = ml.toVector(0,1,0)
    yn = ml.toVector(1,0,0)
    zn = ml.toVector(0,0,-1)
    
    xb = q.vecTransformation(xn)
    yb = q.vecTransformation(yn)
    zb = q.vecTransformation(zn)
    
    x1, x2, x3 = ml.toValue(xb)
    y1, y2, y3 = ml.toValue(yb)
    z1, z2, z3 = ml.toValue(zb)
    xb = [x1,x2,x3]
    yb = [y1,y2,y3]
    zb = [z1,z2,z3]
    
    for i in range(3):
        ax.plot([0,xb[i]], [0,yb[i]], zs = [0,zb[i]])
        
    ax.auto_scale_xyz([-1,1],[-1,1],[-1,1])
    ax.set_xlabel('East')
    ax.set_ylabel('North')
    ax.set_zlabel('Down')
    
    phi, theta, psi = s.getOrientation()
    vx, vy, vz = s.getVelocity()
    px, py, pz = s.getPosition()
    s1 = ' Roll: %.4f\n Pitch: %.4f\n Yaw: %.4f\n\n' % (np.rad2deg(phi),np.rad2deg(theta),np.rad2deg(psi))
    s2 = ' vx: %.2f\n vy: %.2f\n vz: %.2f\n\n' % (vx, vy, vz)
    s3 = ' px: %.2f\n py: %.2f\n pz: %.2f\n' % (px,py,pz)
    plt.figtext(0, 0, s1+s2+s3)

def main():
    vec = ml.toVector(1.,2.,0.)
    plotVector(1,vec)
    plt.show()
    
if __name__ == "__main__":
    main()