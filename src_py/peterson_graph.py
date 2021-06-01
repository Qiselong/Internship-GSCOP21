import matplotlib.pyplot as plt
import numpy as np

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


# prepare some coordinates
x, y, z = np.indices((11,9,8))

# 
a = (x < 6) & (x >= 4 ) & (y < 4 ) & (y >= 3) & (z < 7) & (z >= 1)
b = (x < 9) & (x >= 2) & (y < 2) & (y >= 0) & (z < 5 ) & (z >= 3)
c = (x < 11) & (x >= 0) & (y < 9) & (y >= 0 ) & (z < 2 ) & (z >= 0 )
d = (x < 7) & (x >=5 ) & (y <8 ) & (y >=1 ) & (z <5  ) & (z >=3 )
e = (x < 3) & (x >= 1) & (y <6 ) & (y >= 1) & (z <5  ) & (z >=1 )

A = (x < 11) & (x >=0 ) & (y <9 ) & (y >=0 ) & (z <  8) & (z >=6 )
B = (x < 11) & (x >=8 ) & (y <4 ) & (y >=1 ) & (z <7  ) & (z >=3 )
C = (x < 10) & (x >=9 ) & (y <8 ) & (y >=3 ) & (z <5  ) & (z >=1 )
D = (x < 11) & (x >=1 ) & (y <9 ) & (y >= 7) & (z <5  ) & (z >=3 )
E = (x < 2) & (x >=0 ) & (y <8 ) & (y >=3 ) & (z <7  ) & (z >=3 )


# combine the objects into a single boolean array
voxels = a | b | c | d | e | A | B | C | D | E

# set the colors of each object
colors = np.empty(voxels.shape, dtype=object)
colors[a] = 'red'
colors[b] = 'blue'
colors[c] = 'green'
colors[d] = 'yellow'
colors[e] = 'cyan'

colors[B] = 'red'
colors[C] = 'blue'
colors[D] = 'green'
colors[E] = 'yellow'
colors[A] = 'cyan'

## for 2D verification
voxels2D = a | b | d | e | B | C | D | E

colors2D = np.empty(voxels2D.shape, dtype=object)

colors2D[a] = 'red'
colors2D[b] = 'blue'
colors2D[d] = 'yellow'
colors2D[e] = 'cyan'

colors2D[B] = 'red'
colors2D[C] = 'blue'
colors2D[D] = 'green'
colors2D[E] = 'yellow'



# and plot everything (2D)
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(voxels2D, facecolors=colors2D)
plt.title('2D reduction (A & c removed)')

plt.show()

# and plot everything (3Ds)
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(voxels, facecolors=colors)
plt.title('3D version ')

plt.show()
