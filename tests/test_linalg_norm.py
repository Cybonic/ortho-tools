import numpy as np

a = np.arange(18) - 4
b = a.reshape((3, 3,2))

#b_prime = np.linalg.norm(b,axis=0,keepdims=True)
b_prime = (b - np.min(b))/np.ptp(b)

for d in b_prime:
    print(np.max(d))
    print(np.min(d))