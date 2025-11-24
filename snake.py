import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x , y):
        self.x = x
        self.y = y  

#GAME WINDOW
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
canvas.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}") 

#initialize the game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)  #single tile, snake's head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)  #single tile, food
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
score = 0
paused = False

def reset_game():
    """Reset game state to initial values so the game can restart without rerunning the script."""
    global snake, food, snake_body, velocityX, velocityY, game_over, score
    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    # place food randomly to avoid immediate collision
    food = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0

def change_direction(event):
    global velocityX, velocityY, game_over, paused

    key = event.keysym.lower()

    # Toggle pause anytime with 'p'
    if key == 'p':
        paused = not paused
        return

    # allow restart when game is over by pressing 'r'
    if game_over:
        if key == 'r':
            reset_game()
        return

    if (event.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (event.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (event.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (event.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    

    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    #update snake body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    #update snake position
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score, paused

    # only update game state when not paused and not game over
    if not paused and not game_over:
        move()
 
    canvas.delete("all")

    # top score bar
    canvas.create_rectangle(0, 0, WINDOW_WIDTH, 30, fill="#111111", outline="")
    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if game_over:
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20, text=f"GAME OVER: {score}", fill="white", font=("Arial", 24))
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20, text="Press R to restart", fill="white", font=("Arial", 14))
    else:
        # show score in the top-left bar
        canvas.create_text(60, 15, font=("Arial", 12), text=f"Score: {score}", fill="white")
        # show pause hint top-right
        canvas.create_text(WINDOW_WIDTH - 80, 15, font=("Arial", 10), text="P: Pause/Resume", fill="white")

    if paused and not game_over:
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="PAUSED", fill="yellow", font=("Arial", 24))

    window.after(100, draw)  #redraw every 100 ms
    
draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()