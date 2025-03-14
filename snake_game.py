from tkinter import *
import random

# Game Constants
WIDTH, HEIGHT = 400, 400  # Game Size
SPEED = 100
SPACE = 25
SNAKE_COLOR = "#007BFF"
APPLE_COLOR = "#FF0000"
GRID_COLOR = "#404040"
BACKGROUND_COLOR = "#000000"
INITIAL_LENGTH = 3
BUTTON_BUFFER = 70


def center_window(window):
    window.update()
    x = (window.winfo_screenwidth() - window.winfo_width()) // 2
    y = (window.winfo_screenheight() - window.winfo_height()) // 2 - BUTTON_BUFFER
    window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{x}+{y}")


def draw_grid():
    for i in range(0, WIDTH, SPACE):
        canvas.create_line(i, 0, i, HEIGHT, fill=GRID_COLOR)
    for j in range(0, HEIGHT, SPACE):
        canvas.create_line(0, j, WIDTH, j, fill=GRID_COLOR)


def start_screen():
    canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, font=('consolas', 30), text="Snake Game", fill="white")
    canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, font=('consolas', 20), text="Press Start to Play", fill="gray")
    start_button.pack()  # Button Display


class Snake:
    def __init__(self):
        self.body = [[WIDTH//2, HEIGHT//2 + i * SPACE] for i in range(INITIAL_LENGTH)]
        self.squares = [canvas.create_line(x + SPACE//2, y + SPACE//2, x + SPACE//2, y + SPACE//2, width=SPACE, fill=SNAKE_COLOR, capstyle=ROUND, tag="snake") for x, y in self.body]

    def move(self, new_x, new_y):
        self.body.insert(0, [new_x, new_y])
        self.squares.insert(0, canvas.create_line(new_x + SPACE//2, new_y + SPACE//2, self.body[1][0] + SPACE//2, self.body[1][1] + SPACE//2, width=SPACE, fill=SNAKE_COLOR, capstyle=ROUND))

    def remove_tail(self):
        canvas.delete(self.squares.pop())
        self.body.pop()


class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        canvas.delete("food")
        while True:
            x, y = random.randint(0, (WIDTH // SPACE) - 1) * SPACE, random.randint(0, (HEIGHT // SPACE) - 1) * SPACE
            if [x, y] not in snake.body:
                self.coordinates = [x, y]
                canvas.create_oval(x, y, x + SPACE, y + SPACE, fill=APPLE_COLOR, tag="food")
                break


def next_turn():
    x, y = snake.body[0]
    if direction == "up":
        y -= SPACE
    elif direction == "down":
        y += SPACE
    elif direction == "left":
        x -= SPACE
    elif direction == "right":
        x += SPACE

    if check_collisions(x, y):
        update_highscore()
        return

    snake.move(x, y)
    
    if [x, y] == food.coordinates:
        global score
        score += 1
        label.config(text=f"Score: {score}  Highscore: {highscore}")
        food.respawn()
    else:
        snake.remove_tail()
    
    window.after(SPEED, next_turn)


def change_direction(new_dir):
    global direction
    if new_dir != {"left": "right", "right": "left", "up": "down", "down": "up"}.get(direction):
        direction = new_dir


def check_collisions(x, y):
    return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or [x, y] in snake.body


def update_highscore():
    global highscore
    if score > highscore:
        highscore = score
    canvas.delete("all")
    draw_grid()
    canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, font=('consolas', 30), text=f"Highscore: {highscore}", fill="white")
    canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, font=('consolas', 20), text="Press Restart to Play Again", fill="gray")
    start_button.pack_forget()  # Hide Start
    restart_button.pack()  # Show Restart


def restart_game():
    global snake, food, score, direction
    canvas.delete("all")
    draw_grid()
    snake = Snake()
    food = Food()
    score = 0
    direction = 'up'
    label.config(text=f"Score: {score}  Highscore: {highscore}")
    next_turn()
    restart_button.pack_forget()  # Hide Restart


# Window Setup
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text=f"Score: 0  Highscore: 0", font=('consolas', 20), fg="white", bg=BACKGROUND_COLOR)
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

draw_grid()


frame = Frame(window)
frame.pack()

start_button = Button(frame, text="Start", command=restart_game, font=('consolas', 15))
restart_button = Button(frame, text="Restart", command=restart_game, font=('consolas', 15))

start_screen()

center_window(window)

# Key Bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Initialize Game
score = 0
highscore = 0
direction = 'up'
snake = Snake()
food = Food()

window.mainloop()
