from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from .common import connect_to_modbus_server, parse_modbus_address

MAX_REGISTERS_PER_REQUEST = 125  # Max number of registers that can be written in a single Modbus request

def execute(args):
    """
    Executes the 'write' command for modbuster. It writes values to Modbus registers or coils
    based on the address provided.
    """
    slave_id = args.slave  # Slave ID (default 0 if not provided)
    host = args.host  # Host IP
    address = args.address  # Starting address
    values = args.values  # List of values to write (can be multiple values)

    # Check if values are provided for write operation
    if not values:
        print("Error: No values provided for write operation.")
        return

    # VERBOSE output
    if args.verbose:
        print(f"[VERBOSE] Connecting to {host}:{args.port} as slave {slave_id}")
        print(f"[VERBOSE] Writing values {values} starting at Modbus address {address}")

    # Offset
    #address -= 1


    # Determine if we are writing to coils or holding registers
    address, address_type = parse_modbus_address(address)
    

    # Ensure values are valid based on the address type
    if address_type == 'coil':
        # Coils expect boolean values
        values = [bool(value) for value in values]  # Convert values to boolean (True/False)
        if not all(isinstance(v, bool) for v in values):
            print("Error: Coils can only be written with boolean values (1/0).")
            return

    elif address_type == 'holding_register':
        # Holding registers expect integer values
        if not all(isinstance(value, int) for value in values):
            print("Error: Holding registers can only be written with integer values.")
            return

    else:
        print("Error: Invalid Modbus address range.")
        return

    # Establish connection to the Modbus server
    client = connect_to_modbus_server(host, port=args.port)

    try:
        if address_type == 'coil':
            # Write coils in chunks if necessary
            chunked_values = chunk_list(values, MAX_REGISTERS_PER_REQUEST)
            for i, chunk in enumerate(chunked_values):
                start_address = address + i * len(chunk)
                result = client.write_coils(start_address, chunk, slave=slave_id)
                if result.isError():
                    print(f"Error writing to coils starting at address {start_address + 1}.")
                    return

        elif address_type == 'holding_register':
            # Write registers in chunks if necessary
            chunked_values = chunk_list(values, MAX_REGISTERS_PER_REQUEST)
            for i, chunk in enumerate(chunked_values):
                start_address = address + i * len(chunk)
                result = client.write_registers(start_address, chunk, slave=slave_id)
                if result.isError():
                    print(f"Error writing to holding registers starting at address {start_address + 1}.")
                    return
        
    except ModbusIOException as e:
        print(f"Modbus communication error: {e}")
    finally:
        client.close()


def chunk_list(values, max_size):
    # Splits a list of values into chunks of a specified maximum size.
    return [values[i:i + max_size] for i in range(0, len(values), max_size)]













