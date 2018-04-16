from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
import numpy as np
import os
import cv2
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold)
from time import time

# #create the manifold to be embeded later



#set to 97 to start in lower case 65 for upper and preset case respectively
letter = 97
case = "lower"
timer = 0.0


# runs through folder and takes every png file for individual letters
def info( path, outpath):
    ttf = []
    images = []
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    for root, dirs, files in os.walk(path):

        x = []
        x.append(dirs)
        x[0].sort(key=str.lower)

        for file in x[0]:
            img = cv2.imread(os.path.join(path, file, file+"_"+case+"_"+chr(letter)+".png"), 0)

            images.append(file+".ttf")

            img=img.flatten()

            ttf.append(img)


    df = pd.DataFrame(ttf)

    dsImages = pd.Series(images)

    return df, dsImages

# Scale and visualize the embedding vectors and plots them
def plot_embedding( X, shape, dsImages, title=None):
    global letter
    print("graphing " + case + " " + chr(letter))
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    ax = plt.subplot(111)
    num = 0

    for i in range(X.shape[0]):
        #plots the point as the letter and gives a colour
        plt.text(X[i, 0], X[i, 1], chr(letter),
                color=plt.cm.Set1(num),
                 fontdict={'weight': 'bold', 'size': 9})
        #cycles through the color of labels
        num=num+1;
        if(num>8):
            num=0


    if hasattr(offsetbox, 'AnnotationBbox'):

        shown_images = np.array([[1., 1.]])  # just something big

        for i in range(int(shape)):
            dist = np.sum((X[i] - shown_images) ** 2, 1)
            if np.min(dist) < 4e-3:
                # don't show points that are too close
                continue
            shown_images = np.r_[shown_images, [X[i]]]

            W, H= (20, 20)
            img = Image.new("RGBA", (W, H), (255, 255, 255))
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype(os.path.join('fonts', dsImages[i]), 15)
            w, h = draw.textsize(chr(letter), font=font)
            draw.text(((W - w) / 2, ((H - h) / 2) - 2), chr(letter), (0, 0, 0), font=font)

            with BytesIO() as f:
                img.save(f, format='png')
                f.seek(0)
                file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, 0)
                f.close()

            imagebox = offsetbox.AnnotationBbox(offsetbox.OffsetImage(img, cmap=plt.cm.gray_r), X[i])
            ax.add_artist(imagebox)
    plt.xticks([]), plt.yticks([])

    if title is not None:
        plt.title(title)


#embedds the data
def embed(df, dsImages, case, letter, tsne, output_path, show):
    global timer
    print(df.shape)
    print("Computing t-SNE embedding for "+case + "-case "+chr(letter))

    t0 = time()
    X_tsne = tsne.fit_transform(df)

    numpy.savetxt(output_path+"/" + case + "_" + chr(letter) + ".txt", X_tsne)
    # #creates graphs for visulaization
    if show == True:
        plot_embedding(X_tsne, df.shape[0], dsImages,"t-SNE embedding of "+chr(letter) )  # " +(time %.2fs)" % (time() - t0))
        plt.draw()
    print(time() - t0)
    timer += (time() - t0)



# #the loop for each letter, set to 52 for a full loop(lower and uppercase)

if __name__ == '__main__':
    input_path = 'test_data'
    output_path = 'output_graphs'
    show=True
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)


    for i in range(0, 1):

        df, dsImages=info(input_path, output_path)
        #Set show value to true to display graph
        embed(df, dsImages, case, letter, tsne,  output_path, show)

        letter += 1

        if letter == 123:
            letter = 65
            case = "upper"
        elif letter == 91:
            letter = 97
            case = "lower"

    print("Overall time(minutes):" + str(timer/60.0))
    # #un-comment to display graphs
    if show==True:
     plt.show()
