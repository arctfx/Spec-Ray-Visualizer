import pipe
import tkinter as tk
from PIL import Image, ImageTk

cnt = 1


def refresh_image():
    global cnt, img
    try:
        # print('refresh image')
        # Creating an image object 'img' from the NumPy array 'data', specifying the color mode as 'RGB'
        img = ImageTk.PhotoImage(Image.fromarray(client.data))
        panel.configure(image=img)
        cnt = cnt + 1
        label.configure(text=f"{cnt}")
        panel.image = img
        panel.update()
    except IOError:  # missing or corrupt image file
        print("ERROR")
        # img = None
    # repeat every half sec
    # canvas.after(200, refresh_image, canvas, img, image_id)
    panel.after(100, refresh_image)


# pipe.pipe_client()
if __name__ == '__main__':
    client = pipe.Client()
    client.start()

    window = tk.Tk()
    window.title("SpecRay Visualizer")
    img = ImageTk.PhotoImage(Image.fromarray(client.data))
    panel = tk.Label(window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    label = tk.Label(window, text=f"{cnt}", font=('Aerial 11'))
    label.pack()
    # canvas = tk.Canvas(window, height=img_h, width=img_w)
    # img = None  # initially only need a canvas image place-holder
    # image_id = canvas.create_image(img_w, img_h, image=img)
    # canvas.pack()

    refresh_image()
    window.mainloop()
