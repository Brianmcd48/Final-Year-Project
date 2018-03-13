import numpy as np
import os
import cv2
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)
from time import time

ttf = []
images=[]

df = pd.DataFrame(ttf)
ds = pd.Series(ttf)
dsImages=pd.Series(images)
#dfTarget=np.full((df.shape[0], df.shape[1]), '')
#dfTarget=dfTarget.flatten()
n_samples, n_features= df.shape
n_neighbors= 30
letter = 97
case="upper"
timer=0.0

# runs through folder and takes every png file for individual letters
def info():
    global df, ds, dsImages, n_samples, n_features, n_neighbors, ttf
    for root, dirs, files in os.walk('test_data'):

        for file in files:

            if file.endswith(chr(letter)+'.png'):

                img = cv2.imread(os.path.join('test_data', file[0:file.__len__()-12],file), 0)

                images.append(img)
                img=img.flatten()

                ttf.append(img)

    df=[]
    df= pd.DataFrame(ttf)
    ds=[]
    ds= pd.Series(ttf)
    dsImages=pd.Series(images)
    n_samples, n_features= df.shape
    n_neighbors= 30
    ttf=[]



# Scale and visualize the embedding vectors
def plot_embedding( X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    ax = plt.subplot(111)
    num = 0
    for i in range(X.shape[0]):

        plt.text(X[i, 0], X[i, 1], str(chr(letter)),
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

def embed():
    global timer
    print("Computing t-SNE embedding for "+case +"-case "+chr(letter))
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    t0 = time()
    X_tsne = tsne.fit_transform(df)

    plot_embedding(X_tsne,
                  "t-SNE embedding of the fonts (time %.2fs)" %
                  (time() - t0))

    print(time() - t0)
    timer += (time() - t0)
    if not os.path.exists("output_graphs"):
        os.makedirs("output_graphs")

    numpy.savetxt("output_graphs/"+case+"_"+chr(letter)+".txt",X_tsne.flatten() )
    plt.draw()


for i in range(0, 52):

    info()
    print(df.shape)

    embed()


    letter += 1

    if letter == 123:
        letter = 65
        case = "upper"
    elif letter == 91:
        letter = 122
        case = "lower"

print("Overall time(minutes):" +timer/60.0)
plt.show()