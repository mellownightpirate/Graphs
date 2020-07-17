from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

reverse_dirs = {'n': 's',
                's': 'n',
                'e': 'w',
                'w': 'e'}
reverse_path = []
visited = {}

def get_random_dir(directions):
	i = random.randrange(0, len(directions))
	return directions[i]

# create adjacency list of current room and its exits
visited[player.current_room.id] = player.current_room.get_exits()

while len(visited) < len(room_graph) - 1:

    if player.current_room.id not in visited:
        # mark this room as visited and track its exits: use a list rather than a dict with ? for simplicity
        exits = player.current_room.get_exits()
        # shuffle our list of exits so we are not biased towards moving east
        random.shuffle(exits)
        visited[player.current_room.id] = exits

        if reverse_path is not None:
            last_room = reverse_path[-1]
            # we don't want to revisit the room we have just come from, so remove it
            visited[player.current_room.id].remove(last_room)

    # if we have no more exits available, time to backtrack using our reverse path
    while reverse_path is not None and len(visited[player.current_room.id]) < 1:
        prev_path = reverse_path.pop()
        traversal_path.append(prev_path)
        player.travel(prev_path)

    # travel to the next exit and keep track of our reverse path for backtracking
    else:
        exit = visited[player.current_room.id].pop()
        # append the reverse direction to reversed path
        reverse_path.append(reverse_dirs[exit])
        # append the exit to the traversal path
        traversal_path.append(exit)
        # move to the next room
        player.travel(exit)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
