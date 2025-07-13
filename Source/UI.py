import pygame as pg
import read_map as rm
import state_search as ss

maps = rm.load_all_maps()

pg.init()
origin = (261, 131)  # Original position for the blocks (x, y ) of first block
move = 70  # Move distance for each block in pixels

# Initialize the game window.
screen = pg.display.set_mode((1440,640))

# Set the title of the game window.
pg.display.set_caption("RUSH HOUR")


# Load the imagespip e 'pics' directory.
surface = pg.image.load('pics/map.png').convert()
ui1=pg.image.load('pics/bfs.png').convert()
ui2=pg.image.load('pics/dfs.png').convert()
ui3=pg.image.load('pics/ucs.png').convert()
ui4=pg.image.load('pics/a_.png').convert()
stopBut=pg.image.load('pics/stop.png').convert()
red=pg.image.load('pics/red.png').convert()
blue_hor=pg.image.load('pics/blue.png').convert()
yellow_hor=pg.image.load('pics/yellow.png').convert()
blue_vert=pg.transform.rotate(blue_hor, 90)  
yellow_vert=pg.transform.rotate(yellow_hor, 90) 

# Align game surface and UI surface
surface_rect = surface.get_rect(midleft=screen.get_rect().midleft)
ui = pg.Surface((420, 640))  # Create a surface for the UI
ui_rect = ui.get_rect(midright=screen.get_rect().midright)
text1_rect = pg.Rect(46, 330, 15, 360).move(ui_rect.topleft)  # Text area for displaying information
text2_rect = pg.Rect(46, 370, 15, 360).move(ui_rect.topleft)  # Text area for displaying information

# Areas for buttons in the UI
play_pause_area = pg.Rect(21, 21, 170, 170).move(ui_rect.topleft) 
restart_area = pg.Rect(231, 21, 170, 170).move(ui_rect.topleft) 
change_search_area = pg.Rect(21, 441, 380, 80).move(ui_rect.topleft) 
exit_area = pg.Rect(21, 541, 380, 80).move(ui_rect.topleft) 
map_area = pg.Rect(41, 221, 340, 60).move(ui_rect.topleft)
# Main game loop. 
game_running = False  #game running flag
search_algorithm = 0  # Default search algorithm
ui_show = [ui1, ui2, ui3, ui4]  # List of UI images for different search algorithms
play_map = 1 # Default play map
font = pg.font.SysFont("Arial", 30)  #set font for rendering text

# animate
Step = 0
paths = ["/" * 36]
cost = 0

def Render():
    if paths: 
        screen.blit(surface, surface_rect)
        #Read a string state to define the positions of the blocks.
        # This string can be modified to change the positions of the blocks.
        # 'a' for red, 'b' for blue horizontal, 'c' for blue vertical,
        # 'm' for yellow horizontal, 'n' for yellow vertical
        # Render the text for the map selection
        # The string is divided into 6 columns and 6 rows, with each character representing
        stringState = paths[Step]
        for index, char in enumerate(stringState):
            if char == 'a':
                red_rect = red.get_rect()
                red_rect.x = origin[0] + (index % 6 - 1)*move  # Horizontal position based on index
                red_rect.y = origin[1] + (index // 6)*move  # Vertical position
                screen.blit(red, red_rect)
            elif char == 'b':
                blue_rect = blue_hor.get_rect()
                blue_rect.x = origin[0] + (index % 6 - 1) * move  # Horizontal position based on index
                blue_rect.y = origin[1] + (index // 6) * move  # Vertical position
                screen.blit(blue_hor, blue_rect)
            elif char == 'c':
                blue_rect = blue_vert.get_rect()
                blue_rect.x = origin[0] + (index % 6) * move  # Horizontal position based on index
                blue_rect.y = origin[1] + (index // 6 - 1) * move  # Vertical position
                screen.blit(blue_vert, blue_rect)
            elif char == 'm':
                yelllow_rect = yellow_hor.get_rect()
                yelllow_rect.x = origin[0] + (index % 6 - 2) * move  # Horizontal position based on index
                yelllow_rect.y = origin[1] + (index // 6) * move  # Vertical position
                screen.blit(yellow_hor, yelllow_rect)
            elif char == 'n':
                yelllow_rect = yellow_vert.get_rect()
                yelllow_rect.x = origin[0] + (index % 6) * move  # Horizontal position based on index
                yelllow_rect.y = origin[1] + (index // 6 - 2) * move  # Vertical position
                screen.blit(yellow_vert, yelllow_rect)

def increament_Step():
    global Step
    if game_running and paths:
        Step = max(min (Step + 1, len(paths) - 1), 0)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    # Do logic when user clicks on the screen.
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            # Exit
            if (exit_area).collidepoint(mouse_pos):
                print("Exit clicked at:", mouse_pos)
                pg.quit()
                raise SystemExit
            
            # Play/Pause
            elif play_pause_area.collidepoint(mouse_pos):
                print("Play/Pause clicked at:", mouse_pos)
                game_running = not game_running
                if Step == 0:
                    m = maps[play_map - 1]
                    if search_algorithm == 0:
                        paths, cost = ss.bfs(m)
                    elif search_algorithm == 1:
                        paths, cost = ss.ids(m)
                    elif search_algorithm == 2:
                        paths, cost = ss.ucs(m)
                    elif search_algorithm == 3:
                        paths, cost = ss.a_star(m)

            # Restart
            elif restart_area.collidepoint(mouse_pos):
                print("Restart clicked at:", mouse_pos)
                Step = 0
                cost = 0
                game_running = False
                paths = [maps[play_map - 1]]
                Render()

            elif change_search_area.collidepoint(mouse_pos):
                # Search algo
                print("Change search algorithm clicked at:", mouse_pos)
                if search_algorithm < 3:
                    search_algorithm += 1
                else:
                    search_algorithm = 0
                
                # Choose map
            elif map_area.collidepoint(mouse_pos):
                print("Map clicked at:", mouse_pos)
                if mouse_pos[1] - map_area.y < 35:  
                    play_map = 1 + ((mouse_pos[0] - map_area.x)// 68)
                else:
                    play_map = 6 + ((mouse_pos[0] - map_area.x)// 68)
                print("Play map:", play_map)
                Step = 0
                cost = 0
                game_running = False
                paths = [maps[play_map - 1]]
                Render()
                
    # Main game logic

    screen.blit(ui_show[search_algorithm], ui_rect)  # Draw the UI image on the right side of the screen
    text1_surface = font.render(f"Steps: {Step}", True, (0,0,0))  # White text
    text2_surface = font.render(f"Costs: {cost}", True, (0,0,0))  # White text
    # Draw the text on the UI surface
    screen.blit(text1_surface, text1_rect) # Adjust position as needed
    screen.blit(text2_surface, text2_rect) # Adjust position as needed
    Render()
    if game_running and paths:
        screen.blit(stopBut, (21 + ui_rect.x, 21  + ui_rect.y))                 
    pg.display.flip()  # Refresh on-screen display
    pg.time.delay(300)
    increament_Step()