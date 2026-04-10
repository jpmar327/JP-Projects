import pyautogui
import time
import random
import datetime



def create_move_list(move_count = 15, x_limit = 100, y_limit = 50):
    """
    The function intakes or uses inputs by default and generates a list of the path the mouse cursor will follow
    - Input
        - move_count: the amount of forward moves that will be generated and then the amount that will walk back the first path
        - x_limit: the number used to create the range limit (-x_limit,x_limit) of the randomized number generated for the x offset
        - y_limit: the number used to create the range limit (-y_limit,y_limit) of the randomized number generated for the y offset
    - Output
        - move_list: the path list that the cursor will move in the  & y direction
        - Output Format: [(x1,y1),(x2,y2),(x3,y3),...,(xn,yn)]
    """
    move_list = []
    for i in range(move_count):
        # Move the mouse by a small random amount using the limits given numbers or default numbers
        move_list.append((random.randint(-x_limit, x_limit), random.randint(-y_limit, y_limit)))
    return move_list


def jiggle_mouse(interval=60, move_count=15, cursor_move_duration=0.005):
    """
    The function moves the mouse at every interval and will move at another interval.
    - Input
        - interval: time between the mouse jiggle
        - move_count: the amount of forward moves that will be generated and then the amount that will walk back the first path
        - cursor_move_duration: the intervals between the cursor movement when jiggling the cursor
    The function also utilizes a helper function above -> create_move_list(move_count = 15, x_limit = 100, y_limit = 25)
        - create_move_list(): The function intakes or uses inputs by default and generates a list of the path the mouse cursor will follow
    """
    
    print("Mouse jiggler started. Press Ctrl+C to stop.")
    
    try:
        while True:
            # print(datetime.datetime.now())
            # Move the mouse by a small random amount
            move_list = create_move_list(move_count)
            print(f'\n{str(datetime.datetime.now())}\n{move_list}\n')
            # FORWARD PATHING - Moves the mouse by a random amount forward
            for move_xy in move_list:
                pyautogui.moveRel(move_xy[0], move_xy[1], cursor_move_duration)
            # BACKWARD PATHING - Moves the mouse by a random amount backwards to original point
            for move_xy in move_list:
                pyautogui.moveRel(-move_xy[0], -move_xy[1], cursor_move_duration)

            # Wait for the specified interval
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")

def app_ui():
    """
    TO-DO: Create a UI to adjust scales and to show a button. Also want to package it like a regular app (with no download -> IMPORTANT!!!)
    """
    print()

if __name__ == "__main__":
    # Runs every 60 seconds by default, wiggles mouse 15 times with 0.1 seconds between each cursor move
    jiggle_mouse()