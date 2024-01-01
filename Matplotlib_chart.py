from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()                        # create a figure
ax = fig.add_subplot(projection='3d')             # create a 3-dimensional axis
X = np.arange(-5, 5, 0.25)                # horizontal range
Y = np.arange(-5, 5, 0.25)                # vertical range
X, Y = np.meshgrid(X, Y)                  # create a special grid
R = np.sqrt(X**2 + Y**2)                  # calculate square root
Z = np.sin(R)                             # calculate sinus
## use #@UndefinedVariable below to ignore the error for cm.coolwarm
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                               cmap=cm.coolwarm, linewidth=0,
                               antialiased=False)
ax.set_zlim(-1.01, 1.01)                  # z-axis is third dimension
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()                                # display the figure
    
