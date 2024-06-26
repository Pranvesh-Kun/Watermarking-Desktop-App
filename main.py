from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont


def stretch(event):
    global img
    global canvas
    global re_tk
    width = event.width
    height = event.height
    if not isinstance(img, str):
        re_pic = img.resize((width, height))
        re_tk = ImageTk.PhotoImage(re_pic)
        canvas.create_image(0, 0, image=re_tk, anchor="nw")


def imageuploader():
    global canvas
    global img
    global pic

    filetypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = filedialog.askopenfilename(filetypes=filetypes)

    if len(path):
        img = Image.open(path)
        pic = ImageTk.PhotoImage(img.resize((canvas.winfo_width(), canvas.winfo_height())))
        canvas.create_image(0, 0, image=pic, anchor="nw")
        messagebox.showinfo('Info', "Image added successfully!")
    else:
        print("No file is chosen! Please choose a file.")
        imageuploader()


def watermark():
    global water
    global pic

    filetypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = filedialog.askopenfilename(filetypes=filetypes)

    wa = Image.open(path).resize((100, 100))
    water = ImageTk.PhotoImage(wa)

    w, h = img.size
    a, b = int(w) - 100, int(h) - 100

    if side == "4":
        img.paste(wa, (a, b))
    elif side == "3":
        img.paste(wa, (100, b))
    elif side == "2":
        img.paste(wa, (a, 100))
    else:
        img.paste(wa, (0, 100))
    pic = ImageTk.PhotoImage(img.resize((canvas.winfo_width(), canvas.winfo_height())))
    canvas.create_image(0, 0, image=pic, anchor="nw")
    messagebox.showinfo('Info', "Watermark added!")


def textentry():
    global text
    text = entry.get()
    write_text()


def sideentry():
    global side
    side = entry2.get()


def write_text():
    global pic
    sideentry()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    x, y = int(w / 2), int(h / 2)
    a, b = int(w) - 100, int(h) - 70
    if x > y:
        font_size = y / 2
    elif y > x:
        font_size = x / 2
    else:
        font_size = x / 2

    font = ImageFont.truetype("arial.ttf", int(font_size / 6))

    if side == "4":
        draw.text((a, b), text, fill=(0, 0, 0), font=font, anchor="ms")
    elif side == "3":
        draw.text((100, b), text, fill=(0, 0, 0), font=font)
    elif side == "2":
        draw.text((a, 100), text, fill=(0, 0, 0), font=font)
    else:
        draw.text((100, 100), text, fill=(0, 0, 0), font=font)

    pic = ImageTk.PhotoImage(img.resize((canvas.winfo_width(), canvas.winfo_height())))
    canvas.create_image(0, 0, image=pic, anchor="nw")
    messagebox.showinfo('Info', "Watermark added!")


def save_image():
    img.save("edited_img.jpg")
    messagebox.showinfo('Info', "Image successfully saved!")


window = Tk()
window.geometry("600x400")
window.title("Watermarker")

img = Image.open('image.png')
water = ""
text = ""
side = "4"

window.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
window.rowconfigure(0, weight=1)

button_frame = ttk.Frame(window)

text1 = ttk.Label(button_frame, text="Upload the img:")
text1.pack(pady=5)

upload = ttk.Button(button_frame, text="Upload", command=imageuploader)
upload.pack()

text2 = ttk.Label(button_frame, text="Upload the watermark:")
text2.pack(pady=5)

watermark1 = ttk.Button(button_frame, text="Upload", command=watermark)
watermark1.pack()

text3 = ttk.Label(button_frame, text="Or type in the text you\n want to watermark:")
text3.pack(pady=10)

entry = ttk.Entry(button_frame)
entry.pack()

enter = ttk.Button(button_frame, text="Submit", command=textentry)
enter.pack(pady=10)

text4 = ttk.Label(button_frame, text="Where do u want to place \n         the watermark: ")
text4.pack(pady=10)

entry2 = ttk.Entry(button_frame)
entry2.insert(0, "4")
entry2.pack()

enter2 = ttk.Button(button_frame, text="Submit", command=sideentry)
enter2.pack(pady=10)

download = ttk.Button(button_frame, text="Download image", command=save_image)
download.pack(pady=10)

button_frame.grid(row=0, column=0, sticky="nsew")

canvas = Canvas(window, background="black", highlightthickness=0, bd=0, relief='ridge')
canvas.grid(column=1, row=0, columnspan=3, sticky="nsew")

canvas.bind('<Configure>', stretch)

window.mainloop()
