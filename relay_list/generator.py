import smbus
from time import sleep

bus = smbus.SMBus(1)


def set_pin_direction(pin, device_address):
    # Determine which configuration register (0x06 or 0x07)
    if pin < 8:
        config_reg = 0x06
    else:
        config_reg = 0x07
        pin -= 8

    # Read current configuration
    current_config = bus.read_byte_data(device_address, config_reg)

    # Update the configuration for the specific pin
    new_config = current_config & ~(1 << pin)  # Clear the bit for output

    # Write the new configuration back
    bus.write_byte_data(device_address, config_reg, new_config)

# Set pin state (high or low)


def set_pin_state(pin, state, device_address):
    # Determine which output port register (0x02 or 0x03)
    if pin < 8:
        output_reg = 0x02
    else:
        output_reg = 0x03
        pin -= 8

    # Read current output state
    current_state = bus.read_byte_data(device_address, output_reg)

    # Update the state for the specific pin
    if state == "high":
        new_state = current_state | (1 << pin)  # Set the bit for high
    else:  # "low"
        new_state = current_state & ~(1 << pin)  # Clear the bit for low

    # Write the new state back
    bus.write_byte_data(device_address, output_reg, new_state)


boards = [0x20, 0x21, 0x22, 0x24]

output = []


for i, address in enumerate(boards):
    output.append(f"board{i+1}_address = {address}")

output.append("lockers_dict = {")

for i, address in enumerate(boards):
    print(f"Board {i+1} with address {address}")
    print("Enter locker identifier '/' to move to the next board")
    print("Enter locker identifier 'r' to open the locker and try again")
    number_of_lockers = 16
    try:
        number_of_lockers = int(input("Enter number of lockers: "))
    except:
        number_of_lockers = 16
        print("Number of lockers is 16")
    output.append(f"    # Board {i+1} ({number_of_lockers} lockers)")
    for j in range(number_of_lockers):
        lockerIdentifier = "r"
        # Identify the locker until the user is satisfied
        while lockerIdentifier == "r":
            # Open the locker
            set_pin_direction(j, address)
            set_pin_state(j, "high", address)
            sleep(1)
            set_pin_state(j, "low", address)
            # Enter locker identifier
            lockerIdentifier = input(
                f"Enter locker identifier for pin {j} on board {address}: ")

        if lockerIdentifier == "/":
            break

        output.append(f'    "{lockerIdentifier}": [board{i+1}_address, {j}],')

output.append("}")

file_name = input("Enter file name: ")

with open(file_name, "w") as f:
    for line in output:
        f.write(line + "\n")

print("Done!")
