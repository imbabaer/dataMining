import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, 7.0, 0.1)
s = np.sin(0.32*np.pi*t)
line, = plt.plot(t, s, 'o')
plt.setp(line, color='r')

plt.ylabel('sin(x)')
plt.xlabel('x')
plt.title('Sinusfunktion')

plt.grid(True)

plt.ylim(-1,1)
plt.show()