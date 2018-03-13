import sklearn.datasets as sk
from sklearn.manifold import TSNE
import numpy
from PIL import ImageFont, ImageDraw, Image,  ImageTk
import os
import FontManifold

if not os.path.exists("test_data"):
    os.makedirs("test_data")


ttf = []
for root, dirs, files in os.walk(r'fonts'):
    for file in files:
        if file.endswith('.ttf'):
            ttf.append(file)



i = 0
W,H=(15, 15)
test_data= 'a'

X_data = []
s=''
#open('.\\test_data', 'w').create('test.txt').write('this is a test')


for i in range(ttf.__len__()):
    letter = 65
    print(i)
    for iter in range(0, 2):
        append = "upper"
        if(letter==97):
            append="lower"

        for alpha in range(0, 26):

            im = Image.new("RGBA", (W, H), (255, 255, 255))
            draw = ImageDraw.Draw(im)
            try:

                font_name = str(ttf[int(i)])
                font_name = font_name[0:font_name.__len__() - 4]

                if not os.path.exists(os.path.join("test_data", font_name)):
                    os.makedirs(os.path.join("test_data",font_name))

                font = ImageFont.truetype(os.path.join('fonts', ttf[int(i)]), 15)
                w, h = draw.textsize(chr(alpha+letter), font=font)
                draw.text(((W-w)/2,((H-h)/2)-2), chr(letter+alpha), (0, 0, 0), font=font)


                im.save(os.path.join('test_data',font_name, "" + font_name +"_"+append+ "_"+chr(letter+alpha)+".png"), 'png')

                #pixels = numpy.asarray(im)
                #width, height = im.size
                #numpy.savetxt("pixel_data.csv", pixels, delimiter=",")
                width, height = im.size

                # open a file to write the pixel data

                #imarray = numpy.array(im)

            except OSError:
                pass
        letter = 97
FontManifold