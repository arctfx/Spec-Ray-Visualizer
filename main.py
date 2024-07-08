import pipe
import tkinter as tk
from PIL import Image, ImageTk

# global time in milliseconds
cnt = 1


def refresh_image():
    global cnt, img
    try:
        img = ImageTk.PhotoImage(Image.fromarray(client.data))
        panel.configure(image=img)
        cnt = cnt + 1
        label.configure(text=f"{cnt}")
        panel.image = img
        panel.update()
    except IOError:  # missing or corrupt image file
        print("ERROR")
        # img = None
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

    refresh_image()
    window.mainloop()
