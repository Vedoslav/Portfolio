import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import numpy as np

#Loading dataset about recommendations for crops growing in India

data_set = pd.read_csv('Crop_recommendation.csv')
print(data_set[['label']].nunique())
print(data_set[['label']].drop_duplicates())

#This dataset contains information about 22 different crops. Let`s create subset with two variables, useful for clusterization, - temperature and humidity.

data_crop = data_set[["temperature", "humidity"]]

#Using KMeans-method for chosen variables with expectation of 22 clusters

kmeans_crop = KMeans(
    n_clusters=22,
    random_state=31
)

kmeans_crop.fit(data_crop)
labels_crop = kmeans_crop.labels_

from sklearn.metrics import silhouette_score

#Calculation of "silhouette" score

silhouette_avg = silhouette_score(data_crop, labels_crop)
print(f'Average silhouette score: {silhouette_avg:.2f}')

plt.scatter(data_crop[["temperature"]], data_crop[["humidity"]], c=labels_crop, cmap='viridis')
plt.scatter(
    kmeans_crop.cluster_centers_[:, 0],
    kmeans_crop.cluster_centers_[:, 1],
    s=300,
    c='red',
    marker='X'
)
plt.title('Clusterization of crop recommendations')
plt.ylabel('temperature')
plt.xlabel('humidity')
plt.show()

#This plot seems rightly. Let`s use "elbow" methon to define optimal number of clusters from mathematic point of view.

distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 25)

for k in K:
    kmeanModel = KMeans(n_clusters=k, random_state=42).fit(data_set[["humidity"]])

    distortions.append(sum(np.min(cdist(data_set[["humidity"]], kmeanModel.cluster_centers_, 'euclidean'), axis=1)**2) / data_set[["humidity"]].shape[0])

    inertias.append(kmeanModel.inertia_)

    mapping1[k] = distortions[-1]
    mapping2[k] = inertias[-1]

print("Distortion values:")
for key, val in mapping1.items():
    print(f'{key} : {val}')
plt.plot(K, distortions, 'bx-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Distortion')
plt.title('The Elbow Method using Distortion')
plt.grid()
plt.show()

distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 25)

for k in K:
    kmeanModel = KMeans(n_clusters=k, random_state=42).fit(data_set[["temperature"]])

    distortions.append(sum(np.min(cdist(data_set[["temperature"]], kmeanModel.cluster_centers_, 'euclidean'), axis=1)**2) / data_set[["humidity"]].shape[0])

    inertias.append(kmeanModel.inertia_)

    mapping1[k] = distortions[-1]
    mapping2[k] = inertias[-1]

print("Distortion values:")
for key, val in mapping1.items():
    print(f'{key} : {val}')
plt.plot(K, distortions, 'bx-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Distortion')
plt.title('The Elbow Method using Distortion')
plt.grid()
plt.show()

#As we cab seem, the "elbow" method defines 3 or 5 as optimal number of clusters for humidity, 3 or 7 - for temperature. Let`s create plots for 3 and 5 clusters and estimate clusterization with the "silhouette" score.

kmeans_crop = KMeans(
    n_clusters=3,
    random_state=31
)

kmeans_crop.fit(data_crop)
labels_crop = kmeans_crop.labels_

from sklearn.metrics import silhouette_score

silhouette_avg = silhouette_score(data_crop, labels_crop)
print(f'Average silhouette score: {silhouette_avg:.2f}')


plt.scatter(data_crop[["temperature"]], data_crop[["humidity"]], c=labels_crop, cmap='viridis')
plt.scatter(
    kmeans_crop.cluster_centers_[:, 0],
    kmeans_crop.cluster_centers_[:, 1],
    s=300,
    c='red',
    marker='X'
)
plt.title('Clusterization of crop recommendations')
plt.ylabel('temperature')
plt.xlabel('humidity')
plt.show()

kmeans_crop = KMeans(
    n_clusters=4,
    random_state=31
)

kmeans_crop.fit(data_crop)
labels_crop = kmeans_crop.labels_

from sklearn.metrics import silhouette_score

# вичислення коефіцієнта силуета
silhouette_avg = silhouette_score(data_crop, labels_crop)
print(f'Average silhouette score: {silhouette_avg:.2f}')


plt.scatter(data_crop[["temperature"]], data_crop[["humidity"]], c=labels_crop, cmap='viridis')
plt.scatter(
    kmeans_crop.cluster_centers_[:, 0],
    kmeans_crop.cluster_centers_[:, 1],
    s=300,
    c='red',
    marker='X'
)
plt.title('Clusterization of crop recommendations')
plt.ylabel('temperature')
plt.xlabel('humidity')
plt.show()

""" The highest "silhouette" score is recognized with 3 clusters (0.63), but the plot seem quite questionable. 5 clusters (0.49) in the same time seem more rightly. 
However, real number of categories in this dataset (22) gives the lowest "silhouette" score (0.40). This score can be changed by varying the random state, but without significant influence on relationships between all three scores.  

It can be argue that clusterization of crops growind recommendations by temperature and humidity is justifiable. But for estimation of model, probably, another method should be used, not "silhouette" score."""
