from tkinter import *
import math
import winsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"
reps = 0
timer = None
ALARM_SOUND = "alarm.wav"


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global reps
    screen.after_cancel(timer)
    timer_label.config(text="TIMER", fg=GREEN)
    canvas.itemconfig(promo_count, text="00:00")
    check_mark_label.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="LONG REST", fg=RED, font=(FONT_NAME, 40), bg=YELLOW)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="SHORT REST", fg=PINK)
    else:
        count_down(work_sec)
        timer_label.config(text="WORK", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"
    canvas.itemconfig(promo_count, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = screen.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for i in range(work_sessions):
            marks += CHECK_MARK
        check_mark_label.config(text=marks, fg=GREEN, bg=YELLOW, font=20)
        play_alarm()


# ---------------------------- PLAY ALARM SOUND ------------------------------- #
def play_alarm():
    winsound.PlaySound(ALARM_SOUND, winsound.SND_FILENAME)  # Frequency 440 Hz, duration 1000 ms


# ---------------------------- UI SETUP ------------------------------- #
screen = Tk()
screen.title('Pomodoro')
screen.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 40), bg=YELLOW)
timer_label.grid(column=1, row=0)

check_mark_label = Label(fg=GREEN, bg=YELLOW, font=20)
check_mark_label.grid(column=1, row=3)

canvas = Canvas(width=200, height=230, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(100, 115, image=tomato_img)
promo_count = canvas.create_text(100, 140, text="00:00", font=(FONT_NAME, 30, "bold"), fill="white")
canvas.grid(column=1, row=1)

start_button = Button(text="START", command=start_timer, highlightthickness=0, activebackground=GREEN)
start_button.grid(column=0, row=2)
reset_button = Button(text="RESET", command=reset, highlightthickness=0, activebackground=GREEN)
reset_button.grid(column=2, row=2)
screen.mainloop()
