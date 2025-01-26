import smbus

# Initialize the I2C bus
bus = smbus.SMBus(1)

# Define the addresses of the boards
board1_address = 0x20
board2_address = 0x21
board3_address = 0x22
board4_address = 0x23

lockers_dict = {
    "1": [board1_address, 1],
    "2": [board1_address, 2],
}

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

def setup():
    for locker_id in lockers_dict:
        locker = lockers_dict[locker_id]
        device_address = locker[0]
        pin = locker[1]
        set_pin_direction(pin, device_address)
        set_pin_state(pin, "low", device_address)

def board_controller(locker_id:str, action:str):
    if locker_id not in lockers_dict:
        print("Locker not found")
        return
    locker = lockers_dict[locker_id]
    pin = locker[1]
    device_address = locker[0]

    if action == "open":
        set_pin_state(pin, "high", device_address)
    else:
        set_pin_state(pin, "low", device_address)
