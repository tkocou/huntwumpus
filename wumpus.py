## An adaption of the original 'Hunt The Wumpus' written in basic
##
## Includes some modifications to make hunting the wumpus more challenging
##
## Coded by Thomas Kocourek 2022, Released on the GPL3 license
##


import random

cave = {1: {'tunnels':[2,3,4], 'selected':False}, 2: {'tunnels':[1,5,6], 'selected':False}, 3: {'tunnels':[1,7,8],'selected':False}, 
        4: {'tunnels':[1,9,10],'selected':False}, 5: {'tunnels':[2,9,11],'selected':False}, 6: {'tunnels':[2,7,12],'selected':False}, 
        7: {'tunnels':[3,6,13],'selected':False}, 8: {'tunnels':[3,10,14],'selected':False}, 9: {'tunnels':[4,5,15],'selected':False}, 
        10: {'tunnels':[4,8,16],'selected':False}, 11: {'tunnels':[5,12,17],'selected':False}, 12: {'tunnels':[6,11,18],'selected':False}, 
        13: {'tunnels':[7,14,18],'selected':False}, 14: {'tunnels':[8,13,19],'selected':False}, 15: {'tunnels':[9,16,17],'selected':False}, 
        16: {'tunnels':[10,15,19],'selected':False}, 17: {'tunnels':[11,20,15],'selected':False}, 18: {'tunnels':[12,13,20],'selected':False},
        19: {'tunnels':[14,16,20],'selected':False}, 20: {'tunnels':[17,18,19],'selected':False}
        }

## There is no room # 0, assign room 0 to all 
pit = {1: 0, 2: 0}
bat = {1: 0, 2: 0}
wumpus = 0
player = 0

visible_tunnels = []
choice = ""
random_tunnel = 0
arrows = 0
#debug = False

def get_room_number():
    global cave
    while True:
        try:
            new_room = random.randint(1,20)
            selected_room = cave[new_room]['selected']
            if selected_room == False:
                cave[new_room]['selected'] = True
                break
        except:
            print("error for room Number: ",new_room)
            quit()
    #if debug:
        #print("new room: {}".format(new_room))
    return new_room

def setup_game():
    global player, wumpus, arrows
    random.seed()
    pit[1] = get_room_number()
    pit[2] = get_room_number()
    bat[1] = get_room_number()
    bat[2] = get_room_number()
    wumpus = get_room_number()
    player = get_room_number()
    #if debug:
    #    print("pit[1]: {}, pit[2]: {}, bat[1]: {}, bat[2]: {}, wumpus: {}, player: {}".format(pit[1],pit[2],bat[1],bat[2],wumpus,player))
    arrows = 5

def you_died(condition):
    if condition == 'arrows':
        print("As you grasp at your empty quiver,")
        print("you hear a large beast approaching...")
    print("You find yourself face to face with the wumpus.")
    print("It eats you whole.")
    print()
    print("You have met your demise.")

def another_game():
    choice = input("Do you want to hunt the wumpus again (Y/N)?")
    if isinstance(choice, str):
        if choice.upper() == 'Y':
            print()
            setup_game()
            return
        else:
            print("Come back again to hunt the wumpus.")
    quit()

def banner():
    print('\n\n')
    print("*******************")
    print("* Hunt the Wumpus *")
    print("*******************")
    print()
    choice = input("Do you want to hunt the big, smelly wumpus? (Y/N)?")
    if isinstance(choice, str):
        if choice.upper() == 'Y':
            print()
            return
        else:
            print("Come back again to hunt the wumpus.")
    quit()

def move_the_wumpus():
    global player, wumpus, cave, debug
    move_wumpus = random.random()
    if move_wumpus < 0.5 :
        print("== The wumpus woke up from its slumber and is moving. ==")
    else:
        print("== The wumpus is searching for its food. ==")
    count = 0
    while True:
        count += 1
        # create a random index for a list
        random_tunnel = random.randint(0,2)
        # get the list of tunnels based on wumpus location
        possible_tunnels = cave[wumpus]['tunnels']
        # get the room number from the indexed list
        selected_room = possible_tunnels[random_tunnel]
        # get the flag for the same room
        stat_room = cave[selected_room]['selected']
        # If the wumpus has selected the room of the player, player dies
        if selected_room == player:
            you_died('wumpus')
            another_game()
            return
        # otherwise move the wumpus
        elif stat_room == False:
            cave[selected_room]['selected'] = True
            cave[wumpus]['selected'] = False
            wumpus = selected_room
            #if debug:
            #    print("wumpus is now at {}".format(wumpus))
            return
        if count > 20:
            # wumpus does not have a clear room to move to
            # use a giant bat to move the wumpus
            print("A giant bat grabs the wumpus and drops it into a new room.")
            old_room = wumpus
            wumpus = get_room_number()
            cave[old_room]['selected'] = False
            break
    return

def game_loop():
    global player, wumpus, arrows, cave, debug
    setup_game()
    bad_room = True
    while True:
        print()
        #if debug:
        #    print("pit[1]: {}, pit[2]: {}, bat[1]: {}, bat[2]: {}, wumpus: {}, player: {}".format(pit[1],pit[2],bat[1],bat[2],wumpus,player))
        if arrows == 0:
            you_died('arrows')
            another_game()
        if player == wumpus:
            you_died('wumpus')
            another_game()
        if player == bat[1] or player == bat[2]:
            print("You have entered the lair of a large bat.")
            print("It picks you up and drops you into a new room")
            print()
            old_room = player
            player = get_room_number()
            cave[old_room]['selected'] = False
        if player == pit[1] or player == pit[2]:
            print("The ground gives way beneath your feet.")
            print("You fall into a deep abyss.")
            print()
            print("You have met your demise.")
            another_game()
        visible_tunnels = cave[player]['tunnels']
        vt = visible_tunnels
        for tunnel in visible_tunnels:
            if tunnel == wumpus:
                print("=-> You smell something terrible nearby.")
            if tunnel == bat[1] or tunnel == bat[2]:
                print("=-> You hear a rustling.")
            if tunnel == pit[1] or tunnel == pit[2]:
                print("=-> You feel a cold wind blowing from a nearby cavern.")
        print("** Status **")
        print("You are in room {}. ".format(player))
        print("Tunnels lead to {}; {}; and {}.".format(vt[0],vt[1],vt[2]))
        print("You have {} arrows.".format(arrows))
        move_wumpus = random.random()
        if move_wumpus < 0.25 :
            move_the_wumpus()
            continue
        choice = input("M)ove, S)hoot or Q)uit? ")

        if choice.upper() == 'Q':
            print()
            print("Come back again to hunt the wumpus.")
            quit()
        #if choice.upper() == 'D':
            ## toggle debug mode
            #debug = not(debug)
            #continue
        if choice.upper() == 'M' or choice.upper() == 'S':
            selected_room = int(input("Which room? "))
            bad_room == True
            for tunnel in visible_tunnels:
                if tunnel == selected_room:
                    bad_room = False
            if bad_room:
                print("Cannot get there from here.")
            else:
                if choice.upper() == 'M':
                    player = selected_room
                if choice.upper() == 'S':
                    if selected_room == wumpus:
                        move_wumpus = random.random()
                        # 50/50 chance to kill the wumpus
                        if move_wumpus < 0.5 :
                            print("Congratulations! You shot the wumpus!")
                            another_game()
                            continue
                    print()
                    print("=-> You missed.")
                    arrows -= 1
                    move_wumpus = random.random()
                    if move_wumpus > 0.25 :
                        move_the_wumpus()


def main():
    banner()
    game_loop()

if __name__ == "__main__":
    main()