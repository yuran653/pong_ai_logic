import turtle
import random

# Настройка окна
win = turtle.Screen()
win.title("Pong на Python с ИИ")
win.bgcolor("black")
win.setup(width=600, height=600)

# # Останавливаем обновление окна, чтобы управлять им самостоятельно
win.tracer(0)

# Ракетка A (игрок)
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=6, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-250, 0)

# Ракетка B (ИИ)
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=6, stretch_len=1)
paddle_b.penup()
paddle_b.goto(250, 0)

# Мяч
ball = turtle.Turtle()
ball.speed(40)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 3
ball.dy = -3

# Функции управления ракетками
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:
        paddle_a.sety(y + 20)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 20)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        paddle_b.sety(y + 20)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        paddle_b.sety(y - 20)

# ИИ логика
class PongAI:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball
        self.prediction = None
        self.reaction_time = 0.1
        self.error_margin = 30

    def move(self):
        if self.ball.dx > 0:  # Мяч движется в сторону ИИ
            self.predict()
            if self.prediction:
                if self.prediction > self.paddle.ycor() + self.error_margin:
                    paddle_b_up()
                elif self.prediction < self.paddle.ycor() - self.error_margin:
                    paddle_b_down()
        else:
            # Возвращаем ракетку в центр, когда мяч движется от неё
            if self.paddle.ycor() < -10:
                paddle_b_up()
            elif self.paddle.ycor() > 10:
                paddle_b_down()

    def predict(self):
        # Простое предсказание траектории мяча
        time_to_reach = (self.paddle.xcor() - self.ball.xcor()) / self.ball.dx
        self.prediction = self.ball.ycor() + self.ball.dy * time_to_reach
        # Добавляем небольшую погрешность
        self.prediction += random.uniform(-self.error_margin, self.error_margin)

# Создаем экземпляр ИИ
ai = PongAI(paddle_b, ball)

# Привязка клавиш
win.listen()
win.onkeypress(paddle_a_up, "Up")
win.onkeypress(paddle_a_down, "Down")

# Основной игровой цикл
while True:
    win.update()

    # Перемещение мяча
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # ИИ делает свой ход
    ai.move()

    # Проверка краев экрана
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 290:
        ball.goto(0, 0)
        ball.dx *= -1

    if ball.xcor() < -290:
        ball.goto(0, 0)
        ball.dx *= -1

    # Проверка столкновения с ракетками
    if (ball.xcor() > 240 and ball.xcor() < 250) and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(240)
        ball.dx *= -1

    if (ball.xcor() < -240 and ball.xcor() > -250) and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-240)
        ball.dx *= -1
