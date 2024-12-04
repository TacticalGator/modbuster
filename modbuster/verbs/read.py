import sys
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from .common import connect_to_modbus_server, parse_modbus_address

def execute(args):
    """
    Executes the 'read' command for modbuster. It reads the Modbus registers or coils
    based on the address provided, and outputs the result in the specified format.
    """
    slave_id = args.slave  # Slave ID (default 0 if not provided)
    host = args.host  # Host IP
    address = args.address  # Starting address
    count = args.count  # Number of registers or coils to read

    # Verbose
    if args.verbose:
        print(f"[VERBOSE] Connecting to {host}:{args.port} as slave {slave_id}")
        print(f"[VERBOSE] Reading {count} values starting at Modbus address {address}")

    # Offset
    #address -= 1

    # Parsing the Modbus address to determine the type of register/coil
    address, address_type = parse_modbus_address(address)

    # Establishing connection to the Modbus server
    client = connect_to_modbus_server(host, port=args.port)

    try:
        # Based on the address type, read the respective register or coil
        if address_type == 'coil':
            result = client.read_coils(address, count, slave=slave_id)
            if not result.isError():
                print_result(address + 0, result.bits[:count])  # Fix: Slice result.bits to `count`
            else:
                print("Error reading coils.")

        elif address_type == 'discrete':
            result = client.read_discrete_inputs(address, count, slave=slave_id)
            if not result.isError():
                print_result(address + 100000, result.bits[:count])  # Fix: Slice result.bits to `count`
            else:
                print("Error reading discrete inputs.")

        elif address_type == 'input_register':
            result = client.read_input_registers(address, count, slave=slave_id)
            if not result.isError():
                print_result(address + 300000, result.registers)
            else:
                print("Error reading input registers.")

        elif address_type == 'holding_register':
            result = client.read_holding_registers(address, count, slave=slave_id)
            if not result.isError():
                print_result(address + 400000, result.registers)
            else:
                print(f"Error reading holding registers.")

        else:
            print("Error: Invalid address type.")
            sys.exit(1)

    except ModbusIOException as e:
        print(f"Modbus communication error: {e}")
    finally:
        client.close()

def print_result(start_address, values):
    """
    Print the result in the desired format.
    Displays the address and the corresponding values.
    """
    for i, value in enumerate(values):
        # Increment the start_address for 1-based Modbus addressing during printing
        address = start_address + i + 1
        formatted_value = int(value) if isinstance(value, bool) else value
        print(f"{address:06d}      {formatted_value}")
