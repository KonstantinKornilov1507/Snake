from tkinter import *
import random

width = 800
height = 600
size_of_segment = 20
playing = True
list = []

def create_block():
    global block
    posx = size_of_segment * random.randint(1, (width - size_of_segment) / size_of_segment)
    posy = size_of_segment * random.randint(1, (height - size_of_segment) / size_of_segment)
    block = canva.create_oval(posx, posy, posx + size_of_segment, posy + size_of_segment, fill="green")

def create_fence():
    global fence
    list1 = []
    posx = size_of_segment * random.randint(1, (width - size_of_segment) / size_of_segment)
    posy = size_of_segment * random.randint(1, (height - size_of_segment) / size_of_segment)
    fence = canva.create_rectangle(posx, posy, posx + size_of_segment, posy + size_of_segment, fill="red")
    list1.append(posx)
    list1.append(posy)
    list1.append(posx + size_of_segment)
    list1.append(posy + size_of_segment)
    list.append(list1)

class Score(object):
    def __init__(self):
        self.score = 0
        self.x = 55
        self.y = 15
        canva.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20", fill="Yellow", tag="score", state='hidden')

    def add_score(self):
        canva.delete("score")
        self.score += 1
        canva.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20", fill="Yellow", tag="score")

    def reset(self):
        canva.delete("score")
        self.score = 0


def game_center():
    global playing
    if playing:
        snake.movement()

        head_orient = canva.coords(snake.segments[-1].instance)
        x1, y1, x2, y2 = head_orient
        l = [x1,y1,x2,y2]
        if x2 > width or x1 < 0 or y1 < 0 or y2 > height:
            playing = False

        elif head_orient == canva.coords(block):
            snake.new_segment()
            canva.delete(block)
            create_block()
        elif l in list:
            playing = False

        else:
            for i in range(len(snake.segments) - 1):
                if head_orient == canva.coords(snake.segments[i].instance):
                    playing = False

        root.after(100, game_center)
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        set_state(close_but, 'normal')


class Segment(object):
    def __init__(self, x, y):
        self.instance = canva.create_rectangle(x, y, x + size_of_segment, y + size_of_segment, fill="green")


class Snake(object):

    def __init__(self, segments):
        self.segments = segments
        self.mapping = {"Down": (0, 1), "Right": (1, 0),"Up": (0, -1), "Left": (-1, 0)}
        self.vector = self.mapping["Right"]

    def movement(self):
        for i in range(len(self.segments) - 1):
            segment = self.segments[i].instance
            x1, y1, x2, y2 = canva.coords(self.segments[i + 1].instance)
            canva.coords(segment, x1, y1, x2, y2)
        x1, y1, x2, y2 = canva.coords(self.segments[-2].instance)
        canva.coords(self.segments[-1].instance,x1 + self.vector[0] * size_of_segment, y1 + self.vector[1] * size_of_segment,x2 + self.vector[0] * size_of_segment, y2 + self.vector[1] * size_of_segment)

    def new_segment(self):
        score.add_score()
        last_seg = canva.coords(self.segments[0].instance)
        x = last_seg[2] - size_of_segment
        y = last_seg[3] - size_of_segment
        self.segments.insert(0, Segment(x, y))

    def change_dir(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def new_snake(self):
        for segment in self.segments:
            canva.delete(segment.instance)


def set_state(item, state):
    canva.itemconfigure(item, state=state)
    canva.itemconfigure(block, state='hidden')


def clicked(event):
    global playing
    snake.new_snake()
    playing = True
    canva.delete(block)
    score.reset()
    canva.itemconfigure(restart_text, state='hidden')
    canva.itemconfigure(game_over_text, state='hidden')
    canva.itemconfigure(close_but, state='hidden')
    canva.itemconfigure(your_score, state='hidden')
    start_game()

def start_game():
    global snake
    x = random.randint(3,14)
    for i in range(0,x):
        create_fence()
    create_block()
    snake = create_snake()
    canva.bind("<KeyPress>", snake.change_dir)
    game_center()


def create_snake():
    segments = [Segment(size_of_segment, size_of_segment),Segment(size_of_segment * 2, size_of_segment),Segment(size_of_segment * 3, size_of_segment)]
    return Snake(segments)

def close_win(root):
    exit()


root = Tk()
root.title("Snake")
canva = Canvas(root, width=width, height=height, bg="#000000")
canva.grid()
canva.focus_set()
game_over_text = canva.create_text(width / 2, height / 2, text="Loose!",font='Arial 20', fill='Yellow',state='hidden')
restart_text = canva.create_text(width / 2, height - height / 3,font='Arial 25',fill='green',text="New Game",state='hidden')
close_but = canva.create_text(width / 2, height - height / 5, font='Arial 25',fill='White',text="Enter",state='hidden')
your_score = canva.create_text(width / 2, height - height / 7, font='Arial 25',fill='yellow',text="Your score: ",state='hidden')

canva.tag_bind(restart_text, "<Button-1>", clicked)
canva.tag_bind(close_but, "<Button-1>", close_win)
score = Score()
start_game()
root.mainloop()