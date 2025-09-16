import pygame
import math
import random

# --- Initialize ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Parameters ---
gravity = 200  # pixels/s^2
restitution = 0.8  # bounciness
balls = []

# --- Ball Class ---
class Ball:
    def __init__(self, x, y, vx, vy, radius=20, mass=1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.mass = mass
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))

    def update(self, dt):
        # update velocity with gravity
        self.vy += gravity * dt

        # update position
        self.x += self.vx * dt
        self.y += self.vy * dt

        # collision with walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx * restitution
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx * restitution
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * restitution
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy * restitution

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        # draw velocity vector
        end_x = self.x + self.vx * 0.1
        end_y = self.y + self.vy * 0.1
        pygame.draw.line(surf, (255,255,255), (self.x, self.y), (end_x, end_y), 2)

# --- Main Loop ---
running = True
paused = False
while running:
    dt = clock.tick(60)/1000  # delta time in seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            vx = random.uniform(-200,200)
            vy = random.uniform(-200,0)
            balls.append(Ball(mx, my, vx, vy))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_UP:
                gravity += 50
            if event.key == pygame.K_DOWN:
                gravity -= 50

    if not paused:
        # update physics
        for ball in balls:
            ball.update(dt)

        # handle ball-ball collisions
        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                b1, b2 = balls[i], balls[j]
                dx = b2.x - b1.x
                dy = b2.y - b1.y
                dist = math.hypot(dx, dy)
                if dist < b1.radius + b2.radius:  # collision
                    overlap = 0.5 * (dist - b1.radius - b2.radius)
                    # separate balls
                    b1.x -= overlap * dx/dist
                    b1.y -= overlap * dy/dist
                    b2.x += overlap * dx/dist
                    b2.y += overlap * dy/dist
                    # compute normal
                    nx, ny = dx/dist, dy/dist
                    # relative velocity
                    tx, ty = -ny, nx
                    dpTan1 = b1.vx * tx + b1.vy * ty
                    dpTan2 = b2.vx * tx + b2.vy * ty
                    dpNorm1 = b1.vx * nx + b1.vy * ny
                    dpNorm2 = b2.vx * nx + b2.vy * ny
                    # conservation of momentum (equal mass for simplicity)
                    m1 = (dpNorm1 * (b1.mass - b2.mass) + 2 * b2.mass * dpNorm2) / (b1.mass + b2.mass)
                    m2 = (dpNorm2 * (b2.mass - b1.mass) + 2 * b1.mass * dpNorm1) / (b1.mass + b2.mass)
                    b1.vx = tx * dpTan1 + nx * m1
                    b1.vy = ty * dpTan1 + ny * m1
                    b2.vx = tx * dpTan2 + nx * m2
                    b2.vy = ty * dpTan2 + ny * m2

    # draw
    screen.fill((0,0,0))
    for ball in balls:
        ball.draw(screen)
    # HUD
    font = pygame.font.SysFont(None, 24)
    text = font.render(f'Gravity: {gravity} (UP/DOWN to change) | P to Pause', True, (255,255,255))
    screen.blit(text, (10,10))
    pygame.display.flip()

pygame.quit()
