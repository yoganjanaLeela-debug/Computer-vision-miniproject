import cv2
import random
WIDTH = 1200
HEIGHT = 700
background = cv2.imread("nature_bg.jpg")
background = cv2.resize(background, (WIDTH, HEIGHT))

girl = cv2.imread("girl.jpeg")
girl = cv2.resize(girl, (180, 250))
girl_x = 500
girl_y = 400

move_speed = 30
ball_radius = 20
ball_x = random.randint(50, WIDTH - 50)
ball_y = 0
ball_speed = 8
score = 0
lives = 3
gray = cv2.cvtColor(girl, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
while True:
    frame = background.copy()
    ball_y += ball_speed

    cv2.circle(
        frame,
        (ball_x, ball_y),
        ball_radius,
        (0, 0, 255),
        -1
    )
    h, w = girl.shape[:2]

    if girl_x >= 0 and girl_y >= 0 and girl_x + w <= WIDTH and girl_y + h <= HEIGHT:

        roi = frame[girl_y:girl_y+h, girl_x:girl_x+w]

        bg_part = cv2.bitwise_and(roi, roi, mask=mask_inv)
        girl_part = cv2.bitwise_and(girl, girl, mask=mask)

        result = cv2.add(bg_part, girl_part)

        frame[girl_y:girl_y+h, girl_x:girl_x+w] = result
    bag_left = girl_x + 80
    bag_right = girl_x + 150

    if ball_y >= girl_y + 50:

        if bag_left <= ball_x <= bag_right:
            score += 1
        else:
            lives -= 1

        ball_x = random.randint(50, WIDTH - 50)
        ball_y = 0
    cv2.putText(
        frame,
        f"Score: {score}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Lives: {lives}",
        (30, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "A = Left   D = Right   Q = Quit",
        (700, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )
    if lives <= 0:

        cv2.putText(
            frame,
            "GAME OVER",
            (350, 350),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            4
        )

        cv2.imshow("Catch The Ball", frame)
        cv2.waitKey(3000)
        break
    cv2.imshow("Catch The Ball", frame)

    key = cv2.waitKey(30)
    if key == ord('a'):
        girl_x -= move_speed
    elif key == ord('d'):
        girl_x += move_speed
    girl_x = max(0, min(WIDTH - w, girl_x))

    # QUIT
    if key == ord('q'):
        break

cv2.destroyAllWindows()