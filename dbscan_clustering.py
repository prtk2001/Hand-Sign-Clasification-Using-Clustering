import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2

from alive_progress import alive_bar
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from rotate import normalise, rotate_3d

# pca params
n_PCA = 15
eps = 0.1

# file = "Basic words - Auslan"
# file = "Auslan COVID-19 Update - 29 Jan 2021"
# file = "WIN_20210418_10_11_51_Pro"
file = "WIN_20210422_17_16_38_Pro"

if not os.path.exists(file + "/dbscan_right_hand_clusters"):
    os.mkdir(file + "/dbscan_right_hand_clusters")

print("\nloading hand csv file...")
df = pd.read_csv(file + "/right_hand_keypoints.csv")
df = np.array(df)
df = df[:, 1:]
for i in range(len(df)):
    df[i][0::3] -=  df[i][0]
    df[i][1::3] -=  df[i][1]
    df[i][2::3] -=  df[i][2]
    
    pts = np.vstack([df[i][0::3], df[i][1::3], df[i][2::3]]).T
    pts = normalise(pts)

    df[i] = rotate_3d(pts).flatten()

paths = pd.read_csv(file + "/right_hand_paths.csv")
paths = np.array(paths)
paths = paths[:, 1:]
paths = paths.astype('str')
print("hand csv file loaded!\n")

n_components = min(n_PCA, min(df.shape[0], df.shape[1]))
print("performing PCA on hands for first {} components...".format(n_components))
pcaf = PCA(n_components=n_components)
df = pcaf.fit_transform(df)
var = round(np.sum(pcaf.explained_variance_ratio_[:n_components]) * 100, 2)
print(("{}"+'%'+" of variance explained with first {} components.").format(var, n_components))
print("PCA done.\n")

print("performing dbscan clustering on hand data...")
df = pcaf.fit_transform(df)
dbscan = DBSCAN(eps=eps, n_jobs=-1, metric='cosine')
dbscan.fit(df)
labels = dbscan.fit_predict(df)
print("predicted no clusters: {}\n".format(len(np.unique(labels)[1:])))

with alive_bar(len(np.delete(labels, np.where(labels == -1)))) as bar:

    for i in range(len(np.unique(labels)[1:])):
        cluster_folder_path = file + "/dbscan_right_hand_clusters/" + str(i)

        if not os.path.exists(cluster_folder_path):
            os.mkdir(cluster_folder_path)

        i_labels = np.where(labels == i)[0]

        for j in i_labels:
            image = cv2.imread(paths[j][0])
            no = np.where(np.char.find(paths, paths[j][0].split('/')[-1]) != -1)[0][0]
            cv2.imwrite(cluster_folder_path + '/' + str(no) + ".jpg", image)
            bar()

if not os.path.exists(file + "/dbscan_left_hand_clusters"):
    os.mkdir(file + "/dbscan_left_hand_clusters")

print("\nloading hand csv file...")
df = pd.read_csv(file + "/left_hand_keypoints.csv")
df = np.array(df)
df = df[:, 1:]
for i in range(len(df)):
    df[i][0::3] -=  df[i][0]
    df[i][1::3] -=  df[i][1]
    df[i][2::3] -=  df[i][2]
    df[i] = rotate_3d(np.vstack([df[i][0::3], df[i][1::3], df[i][2::3]]).T).flatten()
# df = df[:, 3:]

paths = pd.read_csv(file + "/left_hand_paths.csv")
paths = np.array(paths)
paths = paths[:, 1:]
paths = paths.astype('str')
print("hand csv file loaded!\n")

n_components = min(n_PCA, min(df.shape[0], df.shape[1]))
print("performing PCA on hands for first {} components...".format(n_components))
pcaf = PCA(n_components=n_components)
df = pcaf.fit_transform(df)
var = round(np.sum(pcaf.explained_variance_ratio_[:n_components]) * 100, 2)
print(("{}"+'%'+" of variance explained with first {} components.").format(var, n_components))
print("PCA done.\n")

print("performing dbscan clustering on hand data...")
df = pcaf.fit_transform(df)
dbscan = DBSCAN(eps=eps, n_jobs=-1, metric='cosine')
dbscan.fit(df)
labels = dbscan.fit_predict(df)
print("predicted no clusters: {}\n".format(len(np.unique(labels)[1:])))

with alive_bar(len(np.delete(labels, np.where(labels == -1)))) as bar:

    for i in range(len(np.unique(labels)[1:])):
        cluster_folder_path = file + "/dbscan_left_hand_clusters/" + str(i)

        if not os.path.exists(cluster_folder_path):
            os.mkdir(cluster_folder_path)

        i_labels = np.where(labels == i)[0]

        for j in i_labels:
            image = cv2.imread(paths[j][0])
            no = np.where(np.char.find(paths, paths[j][0].split('/')[-1]) != -1)[0][0]
            cv2.imwrite(cluster_folder_path + '/' + str(no) + ".jpg", image)
            bar()