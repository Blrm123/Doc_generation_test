import turtle

screen = turtle.Screen()
screen.title("Ice Cream Cone")
screen.bgcolor("lightyellow")

pen = turtle.Turtle()
pen.speed(3)
pen.width(3)

# --------------------
# Cone
# --------------------
pen.penup()
pen.goto(-40, 0)
pen.pendown()

pen.color("brown", "burlywood")
pen.begin_fill()
pen.goto(40, 0)
pen.goto(0, -100)
pen.goto(-40, 0)
pen.end_fill()

# --------------------
# Ice Cream Scoop (Half Circle)
# --------------------
pen.penup()
pen.goto(-50, 0)
pen.setheading(0)
pen.pendown()

pen.color("deeppink", "pink")
pen.begin_fill()
pen.circle(50, 180)      # Half circle
pen.goto(-50, 0)         # Close the shape
pen.end_fill()

# --------------------
# Cherry
# --------------------
pen.penup()
pen.goto(0, 105)
pen.pendown()

pen.color("red", "red")
pen.begin_fill()
pen.circle(8)
pen.end_fill()

pen.hideturtle()
turtle.done()
