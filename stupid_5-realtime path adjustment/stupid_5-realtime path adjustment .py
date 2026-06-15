from controller import Robot, Motor, DistanceSensor,Gyro
import math
import time
from collections import deque
visited_cells = set()
###there are related to flood fill algorithm
maze_size =16
flood = [[999 for _ in range(maze_size)] for _ in range(maze_size)]
walls = [[[False, False, False, False] for _ in range(maze_size)] for _ in range(maze_size)] 

# [flood value, wall_N, wall_E, wall_S, wall_W]
maze_data = [[[999, False, False, False, False] for _ in range(maze_size)] for _ in range(maze_size)]

## we have to map upper and lower arrays of these 3d,2d ararays to x,y cordinate.
THRESHOLD = 500  # You can tune this threshold

robot_x = 0
robot_y = 0
robot_direction = 0  # 0=N, 1=E, 2=S, 3=W direction_labels = ["N", "E", "S", "W"]
# direction_vectors = [N, E, S, W]
#direction_vectors = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # original (Y increases down)
# Change to:
#direction_vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Y increases up

TIME_STEP = 8
SPEED = 5
robot = Robot()

# Get encoder devices
enL = robot.getDevice("enL")
enR = robot.getDevice("enR")
# Enable encoders
enL.enable(TIME_STEP)
enR.enable(TIME_STEP)

robot.step(TIME_STEP) 

start_L= enL.getValue()
start_R= enR.getValue()

# Motors
m1 = robot.getDevice("M1")
m2 = robot.getDevice("M2")
m3 = robot.getDevice("M3")
m4 = robot.getDevice("M4")

m1.setPosition(float('inf'))
m2.setPosition(float('inf'))
m3.setPosition(float('inf'))
m4.setPosition(float('inf'))

gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)
# Distance Sensors
DL = robot.getDevice("DL")
DR = robot.getDevice("DR")
DFLeft = robot.getDevice("DFLeft")
DFRight = robot.getDevice("DFRight")
DL45 = robot.getDevice("DL45")
DR45 = robot.getDevice("DR45")

# Enable the sensors
DL.enable(TIME_STEP)
DR.enable(TIME_STEP)
DFLeft.enable(TIME_STEP)
DFRight.enable(TIME_STEP)
DL45.enable(TIME_STEP)
DR45.enable(TIME_STEP)

def flood_fill(goalX, goalY):
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    for i in range(maze_size):
        for j in range(maze_size):
            flood[i][j] = 255  # Reset all
    flood[goalX][goalY] = 0
    queue = deque()                 # Create an empty queue
    queue.append((goalX, goalY)) 
    
    while queue:
        x, y = queue.popleft()    # dequeue from the front
        for dir in range(4):  # dir = 0,1,2,
            nx = x + dx[dir]
            ny = y + dy[dir]

            if nx < 0 or ny < 0 or nx >= maze_size or ny >= maze_size:
                continue
            if walls[x][y][dir]:  # block from this cell
                continue
            if walls[nx][ny][(dir + 2) % 4]:  # block from neighbor (optional but safer)
               # print(f"  Wall blocks from neighbor ({nx},{ny}) to ({x},{y}) in dir {(dir+2)%4}")
                continue

            if flood[nx][ny] > flood[x][y] + 1:
                flood[nx][ny] = flood[x][y] + 1
                queue.append((nx, ny))
                
def get_correct_path(start_x, start_y):
    # Directions: N, E, S, W
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    direction_labels = ["N", "E", "S", "W"]

    x, y = start_x, start_y
    sim_dir = robot_direction  # simulate robot's current facing direction
    path = [(x, y)]

    while maze_data[x][y][0] != 0:  # flood value 0 means goal reached
        dir_order = [
            sim_dir,                    # forward
            (sim_dir + 1) % 4,          # right
            (sim_dir + 3) % 4,          # left
            (sim_dir + 2) % 4           # back
        ]

        min_flood = float('inf')
        chosen_dir = -1
        next_cell = (x, y)

        for dir in dir_order:
            nx = x + dx[dir]
            ny = y + dy[dir]

            if 0 <= nx < maze_size and 0 <= ny < maze_size:
                if not maze_data[x][y][dir + 1]:  # dir+1 because index 0 is flood value
                    if maze_data[nx][ny][0] < min_flood:
                        min_flood = maze_data[nx][ny][0]
                        next_cell = (nx, ny)
                        chosen_dir = dir

        if next_cell == (x, y):
            print(f"Stuck at ({x}, {y}) - No better flood neighbor found.")
            break

        # Simulate robot turning
        turn_diff = (chosen_dir - sim_dir) % 4
        if turn_diff == 1:
            turn = "right"
        elif turn_diff == 3:
            turn = "left"
        elif turn_diff == 2:
            turn = "back"
        else:
            turn = "forward"

      #  print(f"At ({x},{y}), heading {direction_labels[sim_dir]} → move {turn} to ({next_cell[0]},{next_cell[1]})")

        # Update simulated direction and position
        sim_dir = chosen_dir
        x, y = next_cell
        path.append((x, y))
    return path      
    
def print_maze_with_path(path):
    path_set = set(path)
    for y in reversed(range(maze_size)):
        row_str = ""
        for x in range(maze_size):
            if (x, y) in path_set:
                row_str += "🟩 "
            else:
                row_str += "⬜ "
        print(row_str)


    

def get_lowest_flood_neighbor(x,y):
    # Directions: N, E, S, W
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    # Prefer front, then left/right, then back
    dir_order = [
        robot_direction,                 # front
        (robot_direction + 1) % 4,       # right
        (robot_direction + 3) % 4,       # left
        (robot_direction + 2) % 4        # back
    ]
    min_flood = 1000
    target = (x, y)  # Default to current position

    for dir in dir_order:
        nx = x + dx[dir]
        ny = y + dy[dir]

        if nx < 0 or ny < 0 or nx >= maze_size or ny >= maze_size:
            continue
        if walls[x][y][dir]:
            continue
        if flood[nx][ny] < min_flood:
            min_flood = flood[nx][ny]
            target = (nx, ny)
    print("Selected neighbor:", target)
    if min_flood == 255:
        return robot_x,robot_y        
    return target  # (x, y)
    
def flood_map_printer():
    ORANGE_BG = '\033[48;5;208m'  # Orange background
    RESET = '\033[0m'

    print("\nFlood Map:")
    for y in reversed(range(maze_size)):
        row = ""
        for x in range(maze_size):
            if x == robot_x and y == robot_y:
                row += f"{ORANGE_BG}   {RESET} "
            else:
                val = flood[x][y]
                row += f"{val if val != 999 else ' . ' :>3} "
        print(row)

def merge_flood_and_walls():
    global maze_data
    for i in range(maze_size):
        for j in range(maze_size):
            maze_data[i][j][0] = flood[i][j]
            for dir in range(4):
                maze_data[i][j][dir + 1] = walls[i][j][dir]
    return

def move_to_cell(target_x, target_y):
    global robot_x, robot_y

    dx = target_x - robot_x
    dy = target_y - robot_y

    if dx == 1 and dy == 0:
        print("Trying to turn East")
        face_direction("E")
    elif dx == -1 and dy == 0:
        print("Trying to turn West")
        face_direction("W")
    elif dx == 0 and dy == 1:
        print("Trying to turn North")
        face_direction("N")
    elif dx == 0 and dy == -1:
        print("Trying to turn South")
        face_direction("S")

    else:
        print("Invalid move: target cell is not adjacent.")
        return

    move_forward_one_cell()  # You already made this
    robot_x = target_x
    robot_y = target_y
    print(f"Moved to cell ({robot_x}, {robot_y})")
    
#turn an specific angle
def turn_robot(target_angle_deg, robot, gyro, m1, m2, m3, m4):
    """
    Rotates the robot by target_angle_deg degrees using gyro integration.
    Positive = left turn, Negative = right turn.
    """
    direction = 1 if target_angle_deg > 0 else -1
    target = abs(target_angle_deg)
    # Initialize local angle integration
    angle_accum = 0.0
    previous_time = robot.getTime()

    Kp = 0.25
    max_speed = 6.0
    min_speed = 0.5
    print(f"Turning... Target: {target:.2f}° ")
    while robot.step(TIME_STEP) != -1:
        current_time = robot.getTime()
        dt = current_time - previous_time
        previous_time = current_time
        # Read angular velocity (rad/s)
        angular_velocity = gyro.getValues()[2]
        # Integrate angle in degrees
        angle_accum += math.degrees(angular_velocity * dt)
        turned_angle = abs(angle_accum)
        error = target - turned_angle

        if error <= 0.4:
            break
        speed = max(min_speed, min(Kp * error, max_speed))
        if direction > 0:
            motorLR(m1, m2, m3, m4, -speed, speed)  # Turn left
        else:
            motorLR(m1, m2, m3, m4, speed, -speed)  # Turn right
       # print(f"Turning... Angle: {turned_angle:.2f}° / Target: {target:.2f}° / Error: {error:.2f}° / Speed: {speed:.2f}")
    motorLR(m1, m2, m3, m4, 0, 0)  # Stop at end

   
def motorLR(m1, m2, m3, m4, L, R):
    m1.setVelocity(L)
    m2.setVelocity(L)
    m3.setVelocity(R)
    m4.setVelocity(R)
    
def get_encoder_values():
    left_value = enL.getValue()
    right_value = enR.getValue()
    return left_value, right_value
        
def move_forward_one_cell():
    # --- Direction labels for debug ---
    direction_labels = ['N', 'E', 'S', 'W']
    print("Current direction:", direction_labels[robot_direction])

    # --- Encoder Setup ---
    start_L = enL.getValue()
    start_R = enR.getValue()
    target_distance = 36.0  # cm

    # --- PID Constants (local) ---
    Kp = 0.0003
    Ki = 0.000
    Kd = 0.06

    # --- PID variables ---
    integral = 0
    previous_error = 0

    # --- Distance sensor threshold (above = no wall) ---
    wall_threshold = 430  # Adjust as needed
    front_t = 500

    while robot.step(TIME_STEP) != -1:
        # --- Encoder Distance Check ---
        left_enc, right_enc = get_encoder_values()
        total_distance = ((left_enc - start_L) + (right_enc - start_R)) * 2.2 / 2.0
        if total_distance >= target_distance:
            break

        # --- Read Side Distances ---
        left_dist = DL45.getValue()
        right_dist = DR45.getValue()
        l = DL.getValue()
        r = DR.getValue()
        
        
        # If wall is too far (no reference), skip PID and just go straight
        if left_dist < wall_threshold or right_dist < wall_threshold or l < front_t or r <  front_t:
            motorLR(m1, m2, m3, m4, SPEED, SPEED)
            continue

        # --- PID Error: try to equalize left and right sensor values ---
        error =  right_dist - left_dist   # Positive = too close to left wall
        integral += error
        derivative = error - previous_error
        correction = Kp * error + Ki * integral + Kd * derivative
        previous_error = error

        # --- Adjust Speeds ---
        base_speed = SPEED
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Optional: Clamp speeds
        max_speed = 10.0
        left_speed = max(min(left_speed, max_speed), 0)
        right_speed = max(min(right_speed, max_speed), 0)

        motorLR(m1, m2, m3, m4, left_speed, right_speed)
     
    # --- Stop motors after one cell ---
    motorLR(m1, m2, m3, m4, 0, 0)

    
def update_logical_direction(turn):
    global robot_direction
    if turn == "left":
        robot_direction = (robot_direction - 1) % 4
    elif turn == "right":
        robot_direction = (robot_direction + 1) % 4
    
def face_direction(target_dir):
    global robot_direction

    direction_map = {"N": 0, "E": 1, "S": 2, "W": 3}
    target = direction_map[target_dir]
    diff = (target - robot_direction) % 4

    if diff == 0:
        return  # already facing
    elif diff == 1:
        turn_robot(-90, robot, gyro, m1, m2, m3, m4)  # right
        update_logical_direction("right")
    elif diff == 2:
        turn_robot(180, robot, gyro, m1, m2, m3, m4)  # back
        update_logical_direction("right")
        update_logical_direction("right")
    elif diff == 3:
        turn_robot(90, robot, gyro, m1, m2, m3, m4)   # left
        update_logical_direction("left")
    robot_direction = target
    print("Now facing:", target_dir)

def record_wall_status(x, y):
    global walls

    front = DFRight.getValue() > THRESHOLD
    left = DL.getValue() > THRESHOLD
    right = DR.getValue() > THRESHOLD

    if robot_direction == 0:  # Facing North
        walls[x][y][3] = left   # WW
        walls[x][y][0] = front  # NW
        walls[x][y][1] = right  # EW

    elif robot_direction == 1:  # Facing East
        walls[x][y][0] = left   # NW
        walls[x][y][1] = front  # EW
        walls[x][y][2] = right  # SW

    elif robot_direction == 2:  # Facing South
        walls[x][y][1] = left   # EW
        walls[x][y][2] = front  # SW
        walls[x][y][3] = right  # WW

    elif robot_direction == 3:  # Facing West
        walls[x][y][2] = left   # SW
        walls[x][y][3] = front  # WW
        walls[x][y][0] = right  # NW

    # Print wall statuses
    print(f"[{x},{y}] Wall Status (N,E,S,W):", walls[x][y])

def get_first_unvisited_cell_in_path(path):
    for cell in path:
        if cell not in visited_cells:
            return cell
    return None  # All cells in path are already visited

def is_on_correct_path(correct_path):
    return (robot_x, robot_y) in correct_path
        
moving = True
step = 0

goal_x = 8
goal_y = 8

flood_fill(goal_x ,goal_y )
visited_cells.add((robot_x,robot_y))
while robot.step(TIME_STEP) != -1 and moving:
    record_wall_status(robot_x,robot_y)
    flood_fill(goal_x ,goal_y)
    flood_map_printer()
    x,y = get_lowest_flood_neighbor(robot_x,robot_y)
    move_to_cell(x,y)
    visited_cells.add((x, y))
    merge_flood_and_walls()
    correct_path=get_correct_path(0,0)
    ## what we are going to do is if the correct path has un visited cells we go there first.    
    unvisited_cell= get_first_unvisited_cell_in_path(correct_path)  
    print_maze_with_path(correct_path)
     
    if unvisited_cell==None:
        record_wall_status(robot_x,robot_y)#just to get final flood map
        flood_fill(goal_x ,goal_y)# just to get final flood map
        flood_map_printer()#just to get final flood map
        motorLR(m1, m2, m3, m4, 0, 0) 
        break
    if not is_on_correct_path(correct_path):
        tx,ty=unvisited_cell
        while robot.step(TIME_STEP) != -1 and moving:
            print("robot is currently not on the best path,Hedding that way...,")
            record_wall_status(robot_x,robot_y)
            flood_fill(tx,ty)
            flood_map_printer()
            _x,_y = get_lowest_flood_neighbor(robot_x,robot_y)
            if (_x, _y) == (robot_x, robot_y):
                print("Stuck — can't find valid next move.")
                break
            move_to_cell(_x,_y) 
            visited_cells.add((_x,_y))
            if robot_x ==tx and robot_y ==ty :
                break
            #now lets re check flood for real goal if the correct path has changed 
            #due to new wall data.
            flood_fill(goal_x ,goal_y)
            merge_flood_and_walls()
            new_correct_path=get_correct_path(0,0)
            #this condition checks if by any chance due to new wall data, robot in the correct path, then
            #dont follow the old correct path.
            if correct_path != new_correct_path:
                print ("A new Best path found>>>>>>>>>>>>>>>>>>>>oo<<<<<<<<<<<<<<<<<<")
                print_maze_with_path(new_correct_path)
                new_unvisited_cell = get_first_unvisited_cell_in_path(new_correct_path)
                if new_unvisited_cell is None:
                    print("All cells in the new best path have already been visited.")
                    break
                else:
                    tx, ty = new_unvisited_cell      
    else:
        print("robot is currently on the best path.......")                   
       # move_to_cell(0, 0)      # Move to (0, 0) → dwn (back to start)
       # record_wall_status(0, 0)
        #for _ in range(int(300 / TIME_STEP)):
          #      robot.step(TIME_STEP)
    