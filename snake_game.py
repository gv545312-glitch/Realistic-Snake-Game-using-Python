import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Snake 🐍")

clock = pygame.time.Clock()

BLACK = (15, 15, 15)
BODY_COLOR = (0, 180, 0)
HEAD_COLOR = (0, 255, 120)
FOOD_COLOR = (255, 60, 60)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Arial", 25)

SPEED = 4
SNAKE_WIDTH = 18


def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def game():
    snake = [pygame.Vector2(400, 300)]
    direction = pygame.Vector2(1, 0)
    score = 0

    food = pygame.Vector2(random.randint(50, WIDTH-50),
                          random.randint(50, HEIGHT-50))

    # 👅 Tongue control
    tongue_timer = 0
    tongue_visible = False

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)

        # ---- Events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            direction = pygame.Vector2(-1, 0)
        if keys[pygame.K_RIGHT]:
            direction = pygame.Vector2(1, 0)
        if keys[pygame.K_UP]:
            direction = pygame.Vector2(0, -1)
        if keys[pygame.K_DOWN]:
            direction = pygame.Vector2(0, 1)

        if direction.length() != 0:
            direction = direction.normalize()

        # ---- Move head ----
        head = snake[0] + direction * SPEED
        snake.insert(0, head)

        # ---- Smooth body length ----
        total_length = 0
        max_length = 120 + score * 10

        new_snake = [snake[0]]
        for i in range(1, len(snake)):
            segment = snake[i]
            prev = new_snake[-1]
            distance = prev.distance_to(segment)
            total_length += distance

            if total_length < max_length:
                new_snake.append(segment)
            else:
                break

        snake = new_snake

        # ---- Food collision ----
        if head.distance_to(food) < SNAKE_WIDTH:
            food = pygame.Vector2(random.randint(50, WIDTH-50),
                                  random.randint(50, HEIGHT-50))
            score += 1

        # ---- Wall collision ----
        if head.x < 0 or head.x > WIDTH or head.y < 0 or head.y > HEIGHT:
            running = False

        # ---- Self collision ----
        for segment in snake[15:]:
            if head.distance_to(segment) < SNAKE_WIDTH / 2:
                running = False

        # ---- Tongue animation ----
        tongue_timer += 1
        if tongue_timer > 90:   # every ~1.5 sec
            tongue_visible = not tongue_visible
            tongue_timer = 0

        # ---- Draw food ----
        pygame.draw.circle(screen, FOOD_COLOR,
                           (int(food.x), int(food.y)), 10)

        # ---- Draw smooth body ----
        if len(snake) > 1:
            points = [(int(p.x), int(p.y)) for p in snake]
            pygame.draw.lines(screen, BODY_COLOR, False, points, SNAKE_WIDTH)

        # ---- Draw head ----
        pygame.draw.circle(screen, HEAD_COLOR,
                           (int(head.x), int(head.y)),
                           SNAKE_WIDTH // 2)

        # ---- Eyes ----
        eye_offset = direction * 6
        left_eye = (int(head.x - eye_offset.y),
                    int(head.y + eye_offset.x))
        right_eye = (int(head.x + eye_offset.y),
                     int(head.y - eye_offset.x))

        pygame.draw.circle(screen, WHITE, left_eye, 3)
        pygame.draw.circle(screen, WHITE, right_eye, 3)

        # ---- 👅 Draw tongue ----
        if tongue_visible:
            tongue_length = 20
            tip = head + direction * tongue_length

            left_split = tip + pygame.Vector2(-direction.y, direction.x) * 5
            right_split = tip + pygame.Vector2(direction.y, -direction.x) * 5

            pygame.draw.line(screen, (255, 0, 0),
                             (int(head.x), int(head.y)),
                             (int(tip.x), int(tip.y)), 3)

            pygame.draw.line(screen, (255, 0, 0),
                             (int(tip.x), int(tip.y)),
                             (int(left_split.x), int(left_split.y)), 2)

            pygame.draw.line(screen, (255, 0, 0),
                             (int(tip.x), int(tip.y)),
                             (int(right_split.x), int(right_split.y)), 2)

        show_score(score)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
    
