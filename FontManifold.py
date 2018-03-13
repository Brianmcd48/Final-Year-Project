import sklearn.datasets as sk
import numpy as np
import scipy as sc
from PIL import ImageFont, ImageDraw, Image,  ImageTk
import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)
from time import time
ttf = []
images=[]
counter=0

for  dirs in os.walk('test_data'):
    counter+=1

# runs through folder and takes every png file and create array of images

for root, dirs, files in os.walk('test_data'):



    for file in files:

        if file.endswith('a.png'):

            img = cv2.imread(os.path.join('test_data', file[0:file.__len__()-12],file), 0)

            images.append(img)
            img=img.flatten()

            ttf.append(img)


df = pd.DataFrame(ttf)
ds = pd.Series(ttf)
dsImages=pd.Series(images)
dfTarget=np.full((df.shape[0], df.shape[1]), '')
dfTarget=dfTarget.flatten()
n_samples, n_features= df.shape
n_neighbors= 30
letter=97
for i in range(0, dfTarget.__len__()):
    dfTarget[i]=chr(letter)
    letter+=1
    if letter==133:
        letter=65
    elif letter==90:
        letter=97

# Scale and visualize the embedding vectors
def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    ax = plt.subplot(111)
    num = 0
    for i in range(X.shape[0]):

        plt.text(X[i, 0], X[i, 1], str(dfTarget[0]),
                color=plt.cm.Set1(num),
                 fontdict={'weight': 'bold', 'size': 9})
        num=num+1;
        if(num>8):
            num=0
    if hasattr(offsetbox, 'AnnotationBbox'):
        # only print thumbnails with matplotlib > 1.0
        shown_images = np.array([[1., 1.]])  # just something big
        for i in range(ds.shape[0]):
            dist = np.sum((X[i] - shown_images) ** 2, 1)
            if np.min(dist) < 4e-3:
                # don't show points that are too close
                continue
            shown_images = np.r_[shown_images, [X[i]]]
            imagebox = offsetbox.AnnotationBbox(
                offsetbox.OffsetImage(dsImages[i], cmap=plt.cm.gray_r),
                X[i])
            ax.add_artist(imagebox)
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)

n_img_per_row = 30
img = np.zeros(((10 * n_img_per_row) +7, (10 * n_img_per_row )+7))

for i in range(n_img_per_row):
    ix = 10 * i +1

    for j in range(n_img_per_row):
        iy = 10 * j+1

        img[ix:ix + 15, iy:iy + 15] = ds[i * n_img_per_row + j].reshape((15, 15))

#plt.imshow(img, cmap=plt.cm.binary)
#plt.xticks([])
#plt.yticks([])
#plt.title('A selection from the 64-dimensional digits dataset')



#print("Computing random projection")
#rp = random_projection.SparseRandomProjection(n_components=2, random_state=42)
#X_projected = rp.fit_transform(df)
#plot_embedding(X_projected, "Random Projection of the digits")


print("Computing t-SNE embedding")
tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
t0 = time()
X_tsne = tsne.fit_transform(df)

plot_embedding(X_tsne,
               "t-SNE embedding of the fonts (time %.2fs)" %
               (time() - t0))

print(X_tsne)

plt.plot(X_tsne)
n
plt.show()