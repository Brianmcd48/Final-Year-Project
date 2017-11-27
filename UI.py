from tkinter import *
from PIL import ImageFont, ImageDraw, Image,  ImageTk
import os

ttf = []
for root, dirs, files in os.walk(r'fonts'):
    for file in files:
        if file.endswith('.ttf'):
            ttf.append(file)


window = Tk()
window.title("Font Picker")
loop=0
photo=0
label=Label()


def update(value):

    im = Image.new("RGBA", (300, 100), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join('fonts', ttf[int(value)]), 50)
   
    draw.text((60, 0), "Aa,Bb,Cc", (0, 0, 0), font=font)
    global label
    if loop == 0:
        return im
    else:
        photo = ImageTk.PhotoImage(im)
        label.configure(image=photo)
        label.image = photo


selectFont = Scale(window, length=500, from_=0, to=ttf.__len__()-1, orient=HORIZONTAL, command=update, showvalue=0)

if loop == 0:
    photo = ImageTk.PhotoImage(update(selectFont.get()))
    label = Label(window, image=photo)
    label.pack(side="bottom", fill="both", expand="yes")
    loop = 1

selectFont.pack()
label.pack()

window.bind("<Return>", update)
window.mainloop()