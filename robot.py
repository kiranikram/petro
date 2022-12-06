import math

instructions = ['LEFT 3', 'UP 2' , 'DOWN 9', 'RIGHT 4']

def get_distance(instructions):
    """Takes as instructions a list of strings 
    and returns the euclidean distance from the origin"""
    sideways = 0
    updown = 0
    for move in instructions:
        dist = int(move[-2:])
        dir = move[:-2]

        if dir == 'LEFT':
            sideways -= dist
        elif dir == 'RIGHT':
            sideways += dist
        elif dir == "UP":
            updown += dist
        elif dir == 'DOWN':
            updown -= dist


    distance = math.sqrt( (sideways - 0)**2 + (updown - 0)**2 )

    return distance

    



