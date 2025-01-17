
board1 = "neki1"
board2 = "neki2"
board3 = "neki3"
board4 = "neki4"

lockers_dict = {
    "A1": [board1, 0],
    "A2": [board1, 1],
}

def board_controller(locker_id:str, action:str):
    if locker_id not in lockers_dict:
        print("Locker not found")
        return
    board = lockers_dict[locker_id][0]
    relay = lockers_dict[locker_id][1]
    print("Controlling board:", board, "relay:", relay)
    if action == "open":
        print("Opening relay")
        # TODO: Open relay
    else:
        print("Closing relay")
        #TODO: Close relay
