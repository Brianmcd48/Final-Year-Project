from PIL import ImageFont, ImageDraw, Image
import os, shutil
import sys
from time import time, gmtime, strftime

class Data:


    def ready_data(self, w, h, path, testing):

        # #check if folder exists if its doesn't create it and if it does
        # #delete and make it a new

        if not os.path.exists('fonts'):
            raise ValueError("please provide input directory of fonts")


        if w<15 or h<15:
            raise ValueError("please provide height and weight >15")


        if not os.path.exists(path):
            os.makedirs(path)
            print("path created")


        # #populate array with .ttf files
        ttf = []
        print("populating data")
        for root, dirs, files in os.walk(r'fonts'):
            if(testing==False):
                for file in files:
                    if file.endswith('.ttf'):
                        ttf.append(file)
            else:
                ttf.append(files[0])


        # #declare Width and Height Parameters

        self.build_data(ttf, w, h, path)

    def build_data(self, ttf, W, H, path):

        for i in range(0, ttf.__len__()):
            letter = 65

            font_name = str(ttf[int(i)])
            font_name = font_name[0:font_name.__len__() - 4]

            print("Drawing images for "+font_name)
            for iter in range(0, 2):
                append = "upper"
                if(letter==97):
                    append="lower"

                for alpha in range(0, 26):

                    im = Image.new("RGBA", (W, H), (255, 255, 255))

                    draw = ImageDraw.Draw(im)

                    try:

                        if not os.path.exists(os.path.join(path, font_name)):
                            os.makedirs(os.path.join(path,font_name))

                        font = ImageFont.truetype(os.path.join('fonts', ttf[int(i)]), H-10)

                        w, h = draw.textsize(chr(alpha+letter), font=font)

                        draw.text(((W-w)/2,((H-h)/2)-2), chr(letter+alpha), (0, 0, 0), font=font)

                        im.save(os.path.join(path,font_name, font_name +"_"+append+ "_"+chr(letter+alpha)+".png"), 'png')

                    except OSError:
                        pass
                        shutil.rmtree(os.path.join(path,font_name))
                letter = 97

        #uncomment below to have the manifold run
        #FontManifold




if __name__ == '__main__':
    print("program starting at: " + strftime(" %H:%M:%S", gmtime()))
    t0 = time()
    Data().ready_data(60, 60, "test_data", False)
    print("finished after " + str((time() - t0) / 60.0) + " minutes")
    print("program program finished at: " + strftime(" %H:%M:%S", gmtime()))