# Starter code for an adventure type game.
# University of Utah, David Johnson, 2017.
# This code, or code derived from this code, may not be shared without permission.

# Aaron Morgan (u0393600)
# Bridger Smith (u0667202)

import sys, pygame, math

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames,10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())

    return frame_counts

def load_tiles_and_make_dict_and_rect():
    # Load the tiles
    black = pygame.image.load("Map/Black_sprite_0.png").convert_alpha() # (19, 13, 13, 255)
    tile_rect = black.get_rect()
    blue = pygame.image.load("Map/Blue_sprite_0.png").convert_alpha() # (58, 27, 223, 255)
    dark_red = pygame.image.load("Map/DarkRed_sprite_0.png").convert_alpha() # (69,12,5,255)
    green = pygame.image.load("Map/Green_sprite_0.png").convert_alpha() # (43,70,30,255)
    light_red = pygame.image.load("Map/Light_Red_sprite_0.png").convert_alpha() # (235, 52, 37, 255)
    red = pygame.image.load("Map/Red_sprite_0.png").convert_alpha() # (130, 30, 18, 255)
    water_tile = pygame.image.load('Map/Water_sprite_0.png').convert_alpha() # (27, 199, 223, 255)
    white = pygame.image.load('Map/White_sprite_0.png').convert_alpha() #(255, 255, 255, 255)
    yellow = pygame.image.load('Map/Yellow_sprite_0.png').convert_alpha() #(234, 235, 37, 255)


    # Make a dictionary of the tiles for easy access
    tiles = {}
    tiles[(19, 13, 13, 255)] = black
    tiles[(58, 27, 223, 255)] = blue
    tiles[(69, 12, 5, 255)] = dark_red
    tiles[(43, 70, 30, 255)] = green
    tiles[(235, 52, 37,255)] = light_red
    tiles[(130, 30, 18,255)] = red
    tiles[(27, 199, 223, 255)] = water_tile
    tiles[(255, 255, 255, 255)] = white
    tiles[(234, 235, 37, 255)] = yellow

    return (tiles, tile_rect)

# The main loop handles most of the game
def main():

    # Initialize pygame
    pygame.init()

    screen_size = width, height = (700, 500)
    screen = pygame.display.set_mode(screen_size)

    # Mostly used to cycle the animation of sprites
    frame_count = 0;

    # create the hero character
    hero = load_piskell_sprite("HeroCard",25)
    hero_rect = hero[0].get_rect()
    hero_rect.center = (350, 250)

    # Enemy character
    enemy = load_piskell_sprite("Enemy Card", 16)
    enemy_rect = enemy[0].get_rect()
    enemy_rect.center = (3700, -1900)

    # Map
    world = pygame.image.load("Map/casino_map.png").convert_alpha()
    world_rect = world.get_rect()
    (mapx, mapy) = (0,0)

    # Game Over screen
    game_over = pygame.image.load('WinScreenPygame.png').convert_alpha()
    game_over_rect = game_over.get_rect()
    game_over_rect.topleft = (0,0)

    tiles, tile_rect = load_tiles_and_make_dict_and_rect()

    map_tile_width = (width // tile_rect.width)+1
    map_tile_height = (height // tile_rect.height)+1

    # Map starting position
    mapx = 10
    mapy = 499

    # Loading of images

    # Water Bucket
    water = pygame.image.load("WaterBucket.png").convert_alpha()
    water_rect = water.get_rect()
    water_rect.center = (3800, -1900)

    # Ace of Diamonds
    ace = load_piskell_sprite("AceD", 41)
    ace_rect = ace[0].get_rect()
    ace_rect.center = (2000, -1900)

    # Three of Diamonds
    threeD = load_piskell_sprite("ThreeD", 41)
    threeD_rect = threeD[0].get_rect()
    threeD_rect.center = (600, -1900)

    # Four of Diamonds
    fourD = load_piskell_sprite("FourD", 41)
    fourD_rect = fourD[0].get_rect()
    fourD_rect.center = (3800, -4000)

    # Five of Diamonds
    fiveD = load_piskell_sprite("FiveD", 41)
    fiveD_rect = fiveD[0].get_rect()
    fiveD_rect.center = (4000, 0)

    # Six of Diamonds
    sixD = load_piskell_sprite("SixD", 41)
    sixD_rect = sixD[0].get_rect()
    sixD_rect.center = (600, -3400)

    # Fire
    fire = load_piskell_sprite("Fire", 15)
    fire_rect = fire[0].get_rect()
    fire_rect.center = (600, -3400)

    # Ace of Clubs
    ace_club = pygame.image.load('ace of clubs.png').convert_alpha()
    ace_club_rect = ace_club.get_rect()
    ace_club_rect.center = (750, -150)

    # Seven of Diamonds
    sevenD = pygame.image.load('7 of diamonds.png').convert_alpha()
    sevenD_rect = sevenD.get_rect()
    sevenD_rect.center = (750, -150)

    # Shuffler
    shuffler = load_piskell_sprite("Card Shuffler",12)
    larger_shuffler = pygame.transform.scale2x(shuffler[frame_count%len(shuffler)])
    larger_shuffler_rect = larger_shuffler.get_rect()
    larger_shuffler_rect.center = (750, -200)

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # variable to show if we are still playing the game
    playing = True
    map_on = False

    # variable for hero direction
    is_facing_left = True

    # Variable to track text on the screen. If you set the dialog string to something and set the position and the
    # counter, the text will show on the screen for dialog_counter number of frames.
    dialog_counter = 0
    dialog = ''

    # Load font
    pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)


    # create the inventory and make it empty
    inventory = {}

    # This list should hold all the sprite rectangles that get shifted with a key press.
    rect_list = [water_rect, ace_rect, threeD_rect, fourD_rect, fiveD_rect, sixD_rect, ace_club_rect,
                fire_rect, sevenD_rect, larger_shuffler_rect, enemy_rect]

    # Loop while the player is still active
    while playing:
        # start the next frame
        screen.fill((170,190,190))

        # Initial starting dialog
        time = (pygame.time.get_ticks())/1000
        if time < 5:
            dialog = 'I need to go find the rest of the Diamonds!'
            dialog_counter = 10

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if map_on == True and event.key == pygame.K_SPACE:
                    map_on = False
                elif event.key == pygame.K_SPACE:
                    map_on = True

        # check for keys that are pressed
        # Note the indent makes it part of the while playing but not part of the for event loop.
        keys = pygame.key.get_pressed()
        # check for specific keys
        # movement says how the world should shift. Pressing keys changes the value in the movement variables.
        movement_x = 0
        movement_y = 0

        if keys[pygame.K_LEFT]:
            is_facing_left = True
            movement_x -= tile_rect.width
            mapx -= 1
        if keys[pygame.K_RIGHT]:
            is_facing_left = False
            movement_x += tile_rect.width
            mapx += 1
        if keys[pygame.K_UP]:
            movement_y -= tile_rect.height
            mapy -=1
        if keys[pygame.K_DOWN]:
            movement_y += tile_rect.height
            mapy +=1

        if mapx < 0:
            mapx = 0
            movement_x = 0
        if mapx > world.get_width()-1 - (map_tile_width-1):
            mapx = world.get_width()-1 - (map_tile_width-1)
            movement_x = 0
        if mapy < 0:
            mapy = 0
            movement_y = 0
        if mapy > world.get_height()-1 - (map_tile_height-1):
            mapy = world.get_height()-1 - (map_tile_height-1)
            movement_y = 0

        # Acquisition of Water
        if hero_rect.colliderect(water_rect) and "water" not in inventory:
            inventory["water"] = True
            dialog = "Acquired some water"
            dialog_counter = 40

        # Acquisition of Ace of Diamonds
        if hero_rect.colliderect(ace_rect) and "Ace of Diamonds" not in inventory:
            inventory["Ace of Diamonds"] = True
            dialog = "Acquired Ace of Diamonds"
            dialog_counter = 40

        # Acquistion of Three of Diamonds
        if hero_rect.colliderect(threeD_rect) and "Three of Diamonds" not in inventory:
            inventory["Three of Diamonds"] = True
            dialog = "Acquired Three of Diamonds"
            dialog_counter = 40

        # Acquisition of Four of Diamonds
        if hero_rect.colliderect(fourD_rect) and "Four of Diamonds" not in inventory:
            inventory["Four of Diamonds"] = True
            dialog = "Acquired Four of Diamonds"
            dialog_counter = 40

        # Acquisition of Five of Diamonds
        if hero_rect.colliderect(fiveD_rect) and "Five of Diamonds" not in inventory:
            inventory["Five of Diamonds"] = True
            dialog = "Acquired Five of Diamonds"
            dialog_counter = 40

        # Acquisition of Six of Diamonds
        if hero_rect.colliderect(fire_rect) and "water" in inventory and "Six of Diamonds" not in inventory:
            inventory["Six of Diamonds"] = True
            dialog = "Acquired Six of Diamonds"
            dialog_counter = 40
        elif hero_rect.colliderect(sixD_rect) and "Six of Diamonds" not in inventory:
            dialog = "Fire bad!"
            dialog_counter = 40

        # Acquisition of Seven of Diamonds
        if hero_rect.colliderect(sevenD_rect) and "Seven of Diamonds" not in inventory:
            inventory["Seven of Diamonds"] = True
            dialog = "Acquired Seven of Diamonds"
            dialog_counter = 40

        # Dialog depending on collision with other images
        if hero_rect.colliderect(enemy_rect):
            dialog = "I'll show you!"
            dialog_counter = 30

        if hero_rect.colliderect(ace_club_rect) and (frame_count/10)%10 <= 4:
            dialog = "Ouch, that hurts!"
            dialog_counter = 40

        if hero_rect.colliderect(larger_shuffler_rect):
            dialog = "Ouch, that hurts!"
            dialog_counter = 40

        # Creation of sprite variables needed for drawing the images onto the screen
        hero_sprite = hero[frame_count%len(hero)]
        ace_sprite = ace[frame_count%len(ace)]
        threeD_sprite = threeD[frame_count%len(threeD)]
        fourD_sprite = fourD[frame_count%len(fourD)]
        fiveD_sprite = fiveD[frame_count%len(fiveD)]
        sixD_sprite = sixD[frame_count%len(sixD)]
        fire_sprite = fire[frame_count%len(fire)]
        enemy_sprite = enemy[frame_count%len(enemy)]
        larger_shuffler = pygame.transform.scale2x(shuffler[frame_count%len(shuffler)])

        for y in range(0 ,map_tile_height):
            # offset y
            y_index = y + mapy
            for x in range(0, map_tile_width):
                # offset x
                x_index = x + mapx
                pixelColor = world.get_at((x_index,y_index))
                # The tile is draw at the pixel location scaled up
                tile_rect.topleft = (x * tile_rect.width), (y * tile_rect.height)
                screen.blit(tiles[tuple(pixelColor)],tile_rect)

        # Draws non-collectible images
        screen.blit(larger_shuffler, larger_shuffler_rect)
        screen.blit(enemy_sprite, enemy_rect)

        # Only draw the collected items if they haven't been picked up
        if "water" not in inventory:
            screen.blit(water, water_rect)

        if "Six of Diamonds" not in inventory:
            screen.blit(sixD_sprite, sixD_rect)
            screen.blit (fire_sprite, fire_rect)

        if "Ace of Diamonds" not in inventory:
            screen.blit(ace_sprite, ace_rect)

        if "Three of Diamonds" not in inventory:
            screen.blit(threeD_sprite, threeD_rect)

        if "Four of Diamonds" not in inventory:
            screen.blit(fourD_sprite, fourD_rect)

        if "Five of Diamonds" not in inventory:
            screen.blit(fiveD_sprite, fiveD_rect)

        # Card Shuffler projectiles
        if (frame_count/10)%10 <= 4:
            screen.blit(ace_club, ace_club_rect)
        if (frame_count/10)%5 == 0:
            ace_club_rect.move_ip(0, 75)
        if (frame_count/10)%5 == 1:
            ace_club_rect.move_ip(0, 75)
        if (frame_count/10)%5 == 2:
            ace_club_rect.move_ip(0, 75)
        if (frame_count/10)%5 == 3:
            ace_club_rect.move_ip(0, 75)
        if (frame_count/10)%5 == 4:
            ace_club_rect.move_ip(0, -300)

        if (frame_count/10)%10 >4 and (frame_count/10)%10 <=9 and "Seven of Diamonds" not in inventory:
            screen.blit(sevenD, sevenD_rect)
        if (frame_count/10)%10 == 5:
            sevenD_rect.move_ip(0, 75)
        if (frame_count/10)%10 == 6:
            sevenD_rect.move_ip(0, 75)
        if (frame_count/10)%10 == 7:
            sevenD_rect.move_ip(0, 75)
        if (frame_count/10)%10 == 8:
            sevenD_rect.move_ip(0, 75)
        if (frame_count/10)%10 == 9:
            sevenD_rect.move_ip(0, -300)

        # Flip the sprite depending on direction
        if not is_facing_left:
            hero_sprite = pygame.transform.flip(hero_sprite, True, False)

        # Draw the hero last, so it overlaps the others
        screen.blit(hero_sprite, hero_rect)

        # Draws minimap, which is turned on/off if the space bar is pressed
        if map_on:
            world_rect.topright = (699, 0)
            screen.blit(world, world_rect)
            pygame.draw.rect(screen, (255, 0, 0), (mapx+549, mapy, map_tile_width, map_tile_height), 2)

        if not map_on:
            space_bar = myfont.render("Press Space to show Map", True, (255, 255, 255))
            screen.blit(space_bar, (0, 0))

        # Used to acquire what color the player is on
        tile_position = (mapx +(map_tile_width//2)), (mapy +(map_tile_height//2))
        color_at_position = world.get_at(tile_position)

        # Prevents movement if on black tiles
        if color_at_position == (19, 13, 13, 255) and keys[pygame.K_UP]:
            movement_y += tile_rect.height + tile_rect.height
            mapy +=2
        if color_at_position == (19, 13, 13, 255) and keys[pygame.K_DOWN]:
            movement_y -=tile_rect.height + tile_rect.height
            mapy -=2
        if color_at_position == (19, 13, 13, 255) and keys[pygame.K_RIGHT]:
            movement_x -= tile_rect.width + tile_rect.width
            mapx -=2
        if color_at_position == (19, 13, 13, 255) and keys[pygame.K_LEFT]:
            movement_x += tile_rect.width + tile_rect.width
            mapx +=2

        # Prevents access to upper right room unless all other cards have been collected
        if color_at_position == (235, 52, 37, 255) and keys[pygame.K_UP]:
            if 'Ace of Diamonds' in inventory and\
            'Three of Diamonds' in inventory and 'Five of Diamonds' in inventory and\
            'Six of Diamonds' in inventory and 'Seven of Diamonds' in inventory:
                movement_y -=tile_rect.height
                mapy -=1
                dialog = 'Access Granted'
                dialog_counter = 30
            elif keys[pygame.K_UP]:
                movement_y += tile_rect.height + tile_rect.height
                mapy +=2
                dialog = 'Maybe I should collect more cards'
                dialog_counter = 40

        # Slower movement on "Water" tiles
        if color_at_position == (27, 199, 223, 255):
            clock.tick(10)
        else:
            # Runs at 30fps at all other points
            clock.tick(30)

        # Shifts all images a given amount. In order for the "movement prevention" code to work, this needs to be
        # done last.
        for rect in rect_list:
            rect.move_ip(-movement_x, -movement_y)

        # Dialog within a box at the bottom of the screen
        if dialog:
            pygame.draw.rect(screen, (200, 220, 220), [25, 425, 650, 50])
            textsurface = myfont.render(dialog, False, (0, 0, 0))
            screen.blit(textsurface, (30, 430))

            # Track how long the dialog is on screen
            dialog_counter -= 1
            if dialog_counter == 0:
                dialog = ''

        # Game is over once Four of Diamonds is collected:
        if 'Four of Diamonds' in inventory:
            screen.blit(game_over, game_over_rect)

        # Bring drawn changes to the front
        pygame.display.update()

        frame_count += 1

    # loop is over
    pygame.quit()
    sys.exit()

# Start the program
main()

