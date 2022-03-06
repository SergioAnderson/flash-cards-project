from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}

window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card

    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    canvas.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


def correct_words():
    to_learn.remove(current_card)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526)
canvas_img = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

correct_button = Button()
correct_button.config(image=right, highlightthickness=0, bd=0, command=correct_words)
correct_button.grid(column=1, row=1)

wrong_button = Button()
wrong_button.config(image=wrong, highlightthickness=0, bd=0, command=next_card)
wrong_button.grid(column=0, row=1)
canvas.after(3000, flip_card)

next_card()

window.mainloop()
