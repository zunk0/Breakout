import tkinter as tk
import random
import math
import time

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = "white"

class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout Game")
        
        # Constants
        self.WIDTH = 690
        self.HEIGHT = 600
        self.BALL_SPEED = 5
        self.PADDLE_SPEED = 30
        self.COLORS = ["#5078FF", "#FF5050", "#FFDC50", "#50DC78"]  # blue, red, yellow, green
        self.BROWN = "#78643C"
        self.LIGHT_BROWN = "#B48C50"
        self.BG_COLOR = "#181420"
        self.WHITE = "#FFFFFF"
        self.LIFE_COLOR = "#FFFFFF"
        self.GAME_OVER_COLOR = "#FF3C3C"
        self.WIN_COLOR = "#50FF50"
        self.DARK_COLORS = ["#283C80", "#802828", "#806E28", "#286E3C"]
        self.STONE_COLOR = "#503C1E"

        # Create canvas
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg=self.BG_COLOR)
        self.canvas.pack()

        # Game variables
        self.paddle_x = self.WIDTH // 2 - 50
        self.paddle_y = self.HEIGHT * 0.8
        self.paddle_width = 100
        self.paddle_height = 25
        self.paddle_speed = self.PADDLE_SPEED
        
        # Shrink variables
        self.shrink_start_time = 0
        self.is_shrunk = False
        self.original_width = self.paddle_width
        self.shrunken_width = 50

        # Lives
        self.lives = 3
        self.life_radius = 14
        self.life_margin = 10
        self.life_y = self.HEIGHT - 30
        self.life_x_start = 30

        # Game state
        self.balls = [Ball(self.WIDTH // 2, self.HEIGHT // 2, 0, self.BALL_SPEED)]
        self.spawn_timer = None
        self.won = False
        self.game_over = False
        self.start_time = time.time()
        self.final_time = None

        # Create rectangles
        self.create_rectangles()

        # Bind events
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Button-1>", self.check_restart)

        # Start game loop
        self.update()

    def create_rectangles(self):
        self.rectangles = []
        all_positions = list(range(28))
        plus_positions = random.sample(all_positions, 5)
        remaining_positions = [pos for pos in all_positions if pos not in plus_positions]
        brown_positions = random.sample(remaining_positions, 5)
        remaining_positions = [pos for pos in remaining_positions if pos not in brown_positions]
        shrink_positions = random.sample(remaining_positions, 3)

        x1, y1 = 0, 0
        for i in range(28):
            has_plus = i in plus_positions
            is_brown = i in brown_positions
            has_shrink = i in shrink_positions
            color = self.BROWN if is_brown else self.COLORS[i // 7]
            hits = 0
            self.rectangles.append([x1, y1, 90, 40, color, has_plus, is_brown, has_shrink, hits])
            x1 += 100
            if (i + 1) % 7 == 0:
                x1 = 0
                y1 += 50

    def normalize_speed(self, speed_x, speed_y, target_speed):
        current_speed = (speed_x ** 2 + speed_y ** 2) ** 0.5
        if current_speed > 0:
            return (speed_x / current_speed) * target_speed, (speed_y / current_speed) * target_speed
        return speed_x, speed_y

    def move_left(self, event):
        if not self.game_over and not self.won:
            if self.paddle_x > 0:
                self.paddle_x -= self.paddle_speed

    def move_right(self, event):
        if not self.game_over and not self.won:
            if self.paddle_x + self.paddle_width < self.WIDTH:
                self.paddle_x += self.paddle_speed

    def check_restart(self, event):
        if (self.game_over or self.won) and self.restart_rect:
            x, y = event.x, event.y
            # Check if click is within the restart button area
            button_x = self.WIDTH // 2
            button_y = self.HEIGHT // 2 + 60
            button_width = 100
            button_height = 40
            
            if (button_x - button_width//2 <= x <= button_x + button_width//2 and
                button_y - button_height//2 <= y <= button_y + button_height//2):
                self.reset_game()

    def reset_game(self):
        self.paddle_x = self.WIDTH // 2 - 50
        self.paddle_y = self.HEIGHT * 0.8
        self.paddle_width = 100
        self.paddle_height = 25
        self.paddle_speed = self.PADDLE_SPEED
        self.shrink_start_time = 0
        self.is_shrunk = False
        self.original_width = self.paddle_width
        self.shrunken_width = 50
        self.lives = 3
        self.balls = [Ball(self.WIDTH // 2, self.HEIGHT // 2, 0, self.BALL_SPEED)]
        self.spawn_timer = None
        self.won = False
        self.game_over = False
        self.final_time = None
        self.create_rectangles()
        self.start_time = time.time()

    def update(self):
        self.canvas.delete("all")

        if self.is_shrunk and time.time() - self.shrink_start_time >= 5:
            self.is_shrunk = False
            delta = (self.original_width - self.paddle_width) // 2
            self.paddle_x -= delta
            self.paddle_width = self.original_width

        # Draw lives
        for i in range(3):
            center_x = self.life_x_start + i * (self.life_radius * 2 + self.life_margin)
            if i < self.lives:
                self.canvas.create_oval(
                    center_x - self.life_radius, self.life_y - self.life_radius,
                    center_x + self.life_radius, self.life_y + self.life_radius,
                    fill=self.LIFE_COLOR
                )
            self.canvas.create_oval(
                center_x - self.life_radius, self.life_y - self.life_radius,
                center_x + self.life_radius, self.life_y + self.life_radius,
                outline=self.LIFE_COLOR, width=2
            )

        # Draw timer
        if not self.game_over and not self.won:
            elapsed = int(time.time() - self.start_time)
            self.canvas.create_text(
                self.WIDTH - 50, self.HEIGHT - 60,
                text=f"{elapsed}s",
                fill=self.WHITE,
                font=("Arial", 18)
            )

        # Draw rectangles
        for rect in self.rectangles:
            # Add rounded corners by adjusting coordinates and adding outline
            radius = 10  # Radius of the rounded corners
            self.canvas.create_rectangle(
                rect[0] + radius, rect[1],
                rect[0] + rect[2] - radius, rect[1] + rect[3],
                fill=rect[4], outline=rect[4]
            )
            self.canvas.create_rectangle(
                rect[0], rect[1] + radius,
                rect[0] + rect[2], rect[1] + rect[3] - radius,
                fill=rect[4], outline=rect[4]
            )
            # Draw the rounded corners
            self.canvas.create_arc(
                rect[0], rect[1],
                rect[0] + radius * 2, rect[1] + radius * 2,
                start=90, extent=90, fill=rect[4], outline=rect[4]
            )
            self.canvas.create_arc(
                rect[0] + rect[2] - radius * 2, rect[1],
                rect[0] + rect[2], rect[1] + radius * 2,
                start=0, extent=90, fill=rect[4], outline=rect[4]
            )
            self.canvas.create_arc(
                rect[0], rect[1] + rect[3] - radius * 2,
                rect[0] + radius * 2, rect[1] + rect[3],
                start=180, extent=90, fill=rect[4], outline=rect[4]
            )
            self.canvas.create_arc(
                rect[0] + rect[2] - radius * 2, rect[1] + rect[3] - radius * 2,
                rect[0] + rect[2], rect[1] + rect[3],
                start=270, extent=90, fill=rect[4], outline=rect[4]
            )
            if rect[5]:  # plus
                self.canvas.create_text(
                    rect[0] + rect[2] // 2, rect[1] + rect[3] // 2,
                    text="+", fill=self.DARK_COLORS[self.COLORS.index(rect[4]) if rect[4] in self.COLORS else 0],
                    font=("Arial", 22)
                )
            elif rect[6]:  # brown
                self.canvas.create_text(
                    rect[0] + rect[2] // 2, rect[1] + rect[3] // 2,
                    text="STONE", fill=self.STONE_COLOR,
                    font=("Arial", 16)
                )
            elif rect[7]:  # shrink
                self.canvas.create_text(
                    rect[0] + rect[2] // 2, rect[1] + rect[3] // 2,
                    text="><", fill=self.DARK_COLORS[self.COLORS.index(rect[4]) if rect[4] in self.COLORS else 0],
                    font=("Arial", 22)
                )

        # Draw paddle
        radius = 10  # Radius of the rounded corners
        self.canvas.create_rectangle(
            self.paddle_x + radius, self.paddle_y,
            self.paddle_x + self.paddle_width - radius, self.paddle_y + self.paddle_height,
            fill=self.WHITE, outline=self.WHITE
        )
        self.canvas.create_rectangle(
            self.paddle_x, self.paddle_y + radius,
            self.paddle_x + self.paddle_width, self.paddle_y + self.paddle_height - radius,
            fill=self.WHITE, outline=self.WHITE
        )
        # Draw the rounded corners
        self.canvas.create_arc(
            self.paddle_x, self.paddle_y,
            self.paddle_x + radius * 2, self.paddle_y + radius * 2,
            start=90, extent=90, fill=self.WHITE, outline=self.WHITE
        )
        self.canvas.create_arc(
            self.paddle_x + self.paddle_width - radius * 2, self.paddle_y,
            self.paddle_x + self.paddle_width, self.paddle_y + radius * 2,
            start=0, extent=90, fill=self.WHITE, outline=self.WHITE
        )
        self.canvas.create_arc(
            self.paddle_x, self.paddle_y + self.paddle_height - radius * 2,
            self.paddle_x + radius * 2, self.paddle_y + self.paddle_height,
            start=180, extent=90, fill=self.WHITE, outline=self.WHITE
        )
        self.canvas.create_arc(
            self.paddle_x + self.paddle_width - radius * 2, self.paddle_y + self.paddle_height - radius * 2,
            self.paddle_x + self.paddle_width, self.paddle_y + self.paddle_height,
            start=270, extent=90, fill=self.WHITE, outline=self.WHITE
        )

        if not self.game_over and not self.won:
            for ball in self.balls[:]:
                ball.x += ball.speed_x
                ball.y += ball.speed_y

                # Wall collisions
                if ball.x - ball.radius <= 0:
                    ball.x = ball.radius + 1
                    ball.speed_x *= -1
                    ball.speed_x, ball.speed_y = self.normalize_speed(ball.speed_x, ball.speed_y, self.BALL_SPEED)
                elif ball.x + ball.radius >= self.WIDTH:
                    ball.x = self.WIDTH - ball.radius - 1
                    ball.speed_x *= -1
                    ball.speed_x, ball.speed_y = self.normalize_speed(ball.speed_x, ball.speed_y, self.BALL_SPEED)
                if ball.y - ball.radius <= 0:
                    ball.y = ball.radius + 1
                    ball.speed_y *= -1
                    ball.speed_x, ball.speed_y = self.normalize_speed(ball.speed_x, ball.speed_y, self.BALL_SPEED)

                # Paddle collision
                if (ball.y + ball.radius >= self.paddle_y and ball.y - ball.radius <= self.paddle_y + self.paddle_height and
                    ball.x + ball.radius >= self.paddle_x and ball.x - ball.radius <= self.paddle_x + self.paddle_width):
                    bounce_angle = ((ball.x - self.paddle_x) / self.paddle_width - 0.5) * 2
                    ball.speed_x = bounce_angle * self.BALL_SPEED
                    ball.speed_y = -self.BALL_SPEED
                    ball.speed_x, ball.speed_y = self.normalize_speed(ball.speed_x, ball.speed_y, self.BALL_SPEED)

                # Ball lost
                if ball.y - ball.radius > self.paddle_y + self.paddle_height:
                    self.balls.remove(ball)
                    continue

                # Rectangle collisions
                for rect in self.rectangles[:]:
                    if (rect[0] < ball.x < rect[0] + rect[2] and 
                        rect[1] < ball.y < rect[1] + rect[3]):
                        dx = (ball.x - (rect[0] + rect[2]/2)) / (rect[2]/2)
                        dy = (ball.y - (rect[1] + rect[3]/2)) / (rect[3]/2)
                        ball.speed_x, ball.speed_y = self.normalize_speed(ball.speed_x, ball.speed_y, self.BALL_SPEED)
                        if abs(dx) > abs(dy):
                            ball.speed_x *= -1
                        else:
                            ball.speed_y *= -1
                        ball.speed_x, ball.speed_y = self.normalize_speed(ball.speed_x, ball.speed_y, self.BALL_SPEED)
                        
                        if rect[6]:  # brown
                            rect[8] += 1
                            if rect[8] == 1:
                                rect[4] = self.LIGHT_BROWN
                            elif rect[8] >= 2:
                                self.rectangles.remove(rect)
                        else:
                            if rect[5]:  # plus
                                angle = random.uniform(0, 2 * math.pi)
                                new_speed_x = self.BALL_SPEED * math.cos(angle)
                                new_speed_y = self.BALL_SPEED * math.sin(angle)
                                new_ball = Ball(ball.x, ball.y, new_speed_x, new_speed_y)
                                self.balls.append(new_ball)
                            elif rect[7]:  # shrink
                                self.is_shrunk = True
                                self.shrink_start_time = time.time()
                                delta = (self.paddle_width - self.shrunken_width) // 2
                                self.paddle_x += delta
                                self.paddle_width = self.shrunken_width
                            self.rectangles.remove(rect)

                # Draw ball
                self.canvas.create_oval(
                    ball.x - ball.radius, ball.y - ball.radius,
                    ball.x + ball.radius, ball.y + ball.radius,
                    fill=ball.color, outline=""
                )

        # Game state checks
        if not self.game_over and not self.won:
            if not self.balls:
                if self.lives > 0:
                    if self.spawn_timer is None:
                        self.lives -= 1
                        self.spawn_timer = time.time()
                    elif time.time() - self.spawn_timer >= 2:
                        self.balls.append(Ball(self.WIDTH // 2, self.HEIGHT // 2, 0, self.BALL_SPEED))
                        self.spawn_timer = None
                else:
                    self.game_over = True
                    self.final_time = int(time.time() - self.start_time)
            if not self.rectangles:
                self.won = True
                self.final_time = int(time.time() - self.start_time)

        # Game over screen
        if self.game_over:
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 - 60,
                text=f"{self.final_time}s",
                fill=self.WHITE,
                font=("Arial", 18)
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2,
                text="GAME OVER",
                fill=self.GAME_OVER_COLOR,
                font=("Arial", 40)
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 60,
                text="RESTART",
                fill=self.WHITE,
                font=("Arial", 20)
            )
            self.restart_rect = True

        # Win screen
        if self.won:
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 - 60,
                text=f"{self.final_time}s",
                fill=self.WHITE,
                font=("Arial", 18)
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2,
                text="YOU WON",
                fill=self.WIN_COLOR,
                font=("Arial", 40)
            )
            self.canvas.create_text(
                self.WIDTH // 2, self.HEIGHT // 2 + 60,
                text="RESTART",
                fill=self.WHITE,
                font=("Arial", 20)
            )
            self.restart_rect = True

        # Schedule next update
        self.root.after(16, self.update)  # Approximately 60 FPS

root = tk.Tk()
game = BreakoutGame(root)
root.mainloop()
