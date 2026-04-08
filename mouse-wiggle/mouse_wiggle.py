import pyautogui
import time
import random

def create_move_list(move_count = 15, x_limit = 100, y_limit = 50):
    move_list = []
    for i in range(move_count):
        move_list.append((random.randint(-x_limit, x_limit), random.randint(-y_limit, y_limit)))
    print(move_list)
    return move_list

def jiggle_mouse(interval=60, wiggle_move_count=15, cursor_move_duration=0.9):
    print("Mouse jiggler started. Press Ctrl+C to stop.")
    try:
        while True:
            # Move the mouse by a small random amount
            x = random.randint(400, 500)
            y = random.randint(-50, 50)
 
            x1 = random.randint(-50, 50)
            y1 = random.randint(-500, 500)
            x2 = -x1
            # y2 = -y-random.randint(-25, 25)
            y2 = -y1
            print(x1,x2)
            print(y1,y2)
            
            # Use relative movement
            move_list = create_move_list()
            for move_xy in move_list:
            # for i in range(wiggle_move_count):
                print(move_xy)
                print(-move_xy[0], -move_xy[1])
                pyautogui.moveRel(move_xy[0], move_xy[1], cursor_move_duration)

            for move_xy in move_list:
            # for i in range(wiggle_move_count):
                pyautogui.moveRel(-move_xy[0], -move_xy[1], cursor_move_duration)
                # pyautogui.moveRel(x2, y2, cursor_move_duration)
            # Wait for the specified interval

            # # for i in range(wiggle_move_count):
            #     pyautogui.moveRel(x1, y1, cursor_move_duration)
            #     pyautogui.moveRel(x2, y2, cursor_move_duration)
            # # Wait for the specified interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    # Runs every 60 seconds by default, wiggles mouse 15 times with 0.1 seconds between each cursor move
    jiggle_mouse(3)