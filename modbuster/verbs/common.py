import sys
from pymodbus.client import ModbusTcpClient


def connect_to_modbus_server(host, port=502):
    """
    Establish a Modbus TCP connection to the server.
    """
    client = ModbusTcpClient(host, port=port)
    if client.connect():
        return client
    else:
        print(f"Failed to connect to Modbus server at {host}:{port}")
        sys.exit(1)


def parse_modbus_address(address):
    if not isinstance(address, int):
        print(f"Error: Invalid Modbus address format. Address should be an integer: {address}")
        sys.exit(1)

    ranges = {
        'holding_register': (400001, 465535, 400001),
        'input_register': (300001, 365535, 300001),
        'discrete': (100001, 165535, 100001),
        'coil': (1, 65535, 1),
    }

    for addr_type, (start, end, offset) in ranges.items():
        if start <= address <= end:
            # Return the offset-adjusted address and the address type
            return address - offset, addr_type

    print(f"Error: Address out of valid range: {address}")
    sys.exit(1)

function_code_name = {
    1: "Read Coils",
    2: "Read Discrete Inputs",
    3: "Read Multiple Holding Registers",
    4: "Read Input Registers",
    5: "Write Single Coil",
    6: "Write Single Holding Register",
    7: "Read Exception Status",
    8: "Diagnostic",
    11: "Get Com Event Counter",
    12: "Get Com Event Log",
    15: "Write Multiple Coils",
    16: "Write Multiple Holding Registers",
    17: "Report Slave ID",
    20: "Read File Record",
    21: "Write File Record",
    22: "Mask Write Register",
    23: "Read/Write Multiple Registers",
    24: "Read FIFO Queue",
    43: "Read Device Identification"
    # Add more function codes if necessary
}


diagnostic_sub_functions = {
    0x00: "Return Query Data",  # Echoes the query data back to the client
    0x01: "Restart Communications Option",  # Toggles communication restart
    0x02: "Return Diagnostic Register",  # Returns the content of the diagnostic register
    0x03: "Change ASCII Input Delimiter",  # Changes the ASCII input delimiter
    0x04: "Force Listen Only Mode",  # Forces the slave to listen-only mode
    0x0A: "Clear Counters and Diagnostic Register",  # Clears diagnostic counters
    0x0B: "Return Bus Message Count",  # Returns the number of messages received
    0x0C: "Return Bus Communication Error Count",  # Returns the number of communication errors
    0x0D: "Return Bus Exception Error Count",  # Returns the number of exceptions
    0x0E: "Return Slave Message Count",  # Returns the number of messages processed
    0x0F: "Return Slave No Response Count",  # Returns the number of no-responses
    0x10: "Return Slave NAK Count",  # Returns the number of NAK responses
    0x11: "Return Slave Busy Count",  # Returns the number of busy responses
    0x12: "Return Bus Character Overrun Count",  # Returns the number of character overruns
    0x13: "Return IOP Overrun Count",  # Returns the number of IOP overruns
    0x14: "Clear Overrun Counter and Flag",  # Clears the overrun counter and flag
    0x15: "Get/Clear Modbus Plus Response",  # Clears and retrieves Modbus Plus diagnostics
}


_modbus_exceptions = {  
	1: "Illegal function",
	2: "Illegal data address",
	3: "Illegal data value",
	4: "Slave device failure",
	5: "Acknowledge",
	6: "Slave device busy",
	8: "Memory parity error",
	10: "Gateway path unavailable",
	11: "Gateway target device failed to respond"
}
