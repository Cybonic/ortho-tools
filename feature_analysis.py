


import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# add project root to path
import os
import sys


# Get the absolute path of the root directory of your package
ROOT = os.path.abspath(os.path.dirname("../../"))
print(ROOT)
# Append the root directory to the system path
sys.path.append(ROOT)


import pandas as pd

spot_data = pd.read_csv(f"dataset/sentinel_data_4classes_2024.csv")
print(spot_data.head())

X = spot_data.drop('label', axis=1)
Y = spot_data['label']

print(X.shape)


from mpl_toolkits.mplot3d import Axes3D

# Assuming X is your data and Y are your labels
X_tsne = TSNE(n_components=3, random_state=42).fit_transform(X)

fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, projection='3d')

for i, label in enumerate(set(Y)):
    ax.scatter(X_tsne[Y == label, 0], X_tsne[Y == label, 1], X_tsne[Y == label, 2], label=label)

plt.legend()
plt.show()

