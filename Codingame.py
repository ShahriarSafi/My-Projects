import sys
import math

# Survive the invasion waves

# map parser, not needed to change at all
player_id = int(input())
width, height = [int(k) for i in input().split()]
game_map = []
for k in range(height):
    line = input()
    game_map.append(line)

# do not change if beginner, this takes all the game inputs and parses them for ease of use
def process_input():
    my_rupee, my_reside = [int(i) for i in input().split()]
    adversary_rupee, adversary_reside = [int(i) for i in input().split()]
    
    castles = []
    invader = []

    castle_count = int(input())
    for k in range(castle_count):
        inputs = input().split()
        castle_type = inputs[0]
        castle_id = int(inputs[1])
        owner = int(inputs[2])
        a = int(inputs[3])
        b = int(inputs[4])
        damage = int(inputs[5])
        invasion_range = float(inputs[6])
        reload = int(inputs[7])
        cool_down = int(inputs[8])
        castle = {
            "castleType": castle_type,
            "castleId": castle_id,
            "owner": owner,
            "a": a,
            "b": b,
            "damage": damage,
            "range": invasion_range,
            "reload": reload,
            "coolDown": cool_down
        }
        castles.append(castle)


    invader_count = int(input())
    for i in range(invader_count):
        inputs = input().split()
        invader_id = int(inputs[0])
        owner = int(inputs[1])
        a = float(inputs[2])
        b = float(inputs[3])
        hit_points = int(inputs[4])
        max_hit_points = int(inputs[5])
        current_speed = float(inputs[6])
        max_speed = float(inputs[7])
        slow_time = int(inputs[8])
        bounty = int(inputs[9])
        invader = {
            "invaderId": invader_id,
            "owner": owner,
            "a": a,
            "b": b,
            "hitPoints": hit_points,
            "maxHitPoints": max_hit_points,
            "currentSpeed": current_speed,
            "maxSpeed": max_speed,
            "slowTime": slow_time,
            "bounty": bounty
        }
        invaders.append(invader)

    return [ my_rupee, my_reside, adversary_rupee, adversary_reside, castle_count, castles, invaders ]


# prints some message in the console for debugging
def print_debug(message):
    print(f"{message}", file=sys.stderr, flush=True)


# checks if the block at (a,b) coordinate is a canyon or plateu
# return '#' for plateu and '.' for canyon
# Note that you can only build castles if a block is a canyon
def get_coordinate(a,b):

    if( width <= a ):
        print_debug(f"{a} is invalid because its greater than width={width}")
        raise Exception(f"{a} is invalid because its greater than width={width}")
    if( a < 0 ):
        print_debug(f"{a} is invalid because its negative")
        raise Exception(f"{a} is invalid because its negative")
    
    if( height <= b ):
        print_debug(f"{b} is invalid because its greater than height={height}")
        raise Exception(f"{b} is invalid because its greater than height={height}")
    if( b < 0 ):
        print_debug(f"{b} is invalid because its negative")
        raise Exception(f"{b} is invalid because its negative")
    
    return game_map[b][a]



# returns if the block at (a,b) coordinate already has a castle built at this location
# you can't build a castle on a block that already contains another castle
# Note that, you also have to pass the castles array into this function
def check_if_block_is_occupied(a,b, castles):
    for castle in castles:
        if castle["a"] == a and castle["b"] == b:
            return True
    return False


# This function prints all information about castles currently active in the map
def print_castles(castles):
    for castle in castles:
        print("Castle {index}:", file=sys.stderr, flush=True)
        print(castle, file=sys.stderr, flush=True)

        
# This function prints all information about invaders currently active in the map
def print_invaders(invaders):
    for invader in invaders:
        print("Invader {index}:", file=sys.stderr, flush=True)
        print(invader, file=sys.stderr, flush=True)


# print gamee map
def print_game_map(game_map):
    for i in game_map:
        print(i, file=sys.stderr, flush=True)



turn = 0


# castle_states contains information about which upgrade stage a castle is at
# castle_states = {
#     "{id}": {upgrade_stage (1/2/3) },
# }
castle_states = {}

# my_rupee, my_reside, adversary_rupee, adversary_reside, castle_count, castles, invaders = (0,0,0,0,0,[],[])

# game loop
while True:
    commands = []
    inputs = process_input()

    my_rupee, my_reside, adversary_rupee, adversary_reside, castle_count, castles, invaders = inputs

    def execute_commands():
        if len(commands) == 0:
            print("PASS")
        else:
            for i in range(len(commands)):
                if i == len(commands) - 1:
                    print(commands[i])
                else:
                    print(commands[i], end=";")
                
                
    # builds the desired castle  (a,b)
    def build_castle(a,b, castle_type):
        # print_debug(my_rupee)
        commands.append("BUILD " + str(a) + " " + str(b) + " " + castle_type)
        global my_rupee
        my_rupee -= 100 - ( 30 if castle_type == "GLUECASTLE" else 0 )


    # upgrades the desired castle at (a,b)
    # upgrade_type can be DAMAGE / RELOAD / RANGE
    def upgrade_castle(a,b, upgrade_type):
        built = False
        for castle in castles:
            if castle["a"] == a and castle["b"] == b:
                if castle["owner"] != player_id:
                    print_debug(f"The castle at ({a},{b}) is not yours")
                    raise Exception(f"The castle at ({a},{b}) is not yours")
                    
                built = True
                if castle["castleId"] in castle_states:
                    castle_states[castle["castleId"]] = castle_states[castle["castleId"]] + 1
                else:
                    castle_states[castle["castleId"]] = 1
                
                global my_rupee
                my_rupee -= castle_states[castle["castleId"]] * 50
                
                commands.append("UPGRADE " + str(castle["castleId"]) + " " + upgrade_type) # upgrade_type can be DAMAGE, RANGE or RELOAD
        
        
        if built == False:
            print_debug(f"There is no castle at ({a},{b})")
            raise Exception(f"There is no castle at ({a},{b})")


    # When castlecount > 5
    # Attempt block change



    # DEMO STRATEGY <You can remove this!>
    strategy = 1
    # this block of code finds 'empty' plateau at the immediate left side of a canyon and places a castle there
    if strategy == 1:
        for b in range(height):
            for a in range(width):
                if a+1 < width and get_coordinate(a, b) == '#' and get_coordinate(a+1, b) == '.' and not check_if_block_is_occupied(a,b,castles):
                    if my_rupee > 100:
                        build_castle(a, b, "CARBINECASTLE") # you can change this to CARBINECASTLE, INGLECASTLE, GLUECASTLE or HEALCASTLE as necessary
                
        if my_rupee >= 50 and turn >= 2:
            for castle in castles:   
                if castle["owner"] == player_id:
                    upgrade_castle(castle["a"], castle["b"], "DAMAGE")

    # in this elif statement you can check if castle_count > 5 and only activate your 2nd strategy
    # if castle_count is greater than 5
    elif strategy == 2:
        pass
        # You could make your own code strategy here!
        # remove the "pass" statement when writing your own strategy
    
    execute_commands()
    turn = turn + 1
    

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # BUILD a b CASTLE | UPGRADE id PROPERTY
    # print("BUILD 5 5 CARBINECASTLE")
