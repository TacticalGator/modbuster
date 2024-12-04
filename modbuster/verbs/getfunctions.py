import socket
from struct import pack
from .common import *

MODBUS_TCP_HEADER_LEN = 7
MODBUS_TCP_PROTOCOL_ID = 0
DEFAULT_TIMEOUT = 2  # seconds
MAX_FUNCTION_CODES = 127

# Function to create a Modbus TCP connection
def connect_to_target(ip, port):
    try:
        sock = socket.create_connection((ip, port), timeout=DEFAULT_TIMEOUT)
        return sock
    except Exception as e:
        print(f"[-] Error connecting to {ip}:{port}: {e}")
        return None

# Function to build a Modbus request packet
def build_modbus_request(trans_id, unit_id, func_code):
    pdu = pack('B', func_code) + pack('>HH', 0x0000, 0x0001)  # Function Code + starting address + quantity
    pdu_length = len(pdu)

    adu_length = pdu_length + 1  # ADU length includes PDU and 1 byte for unit ID
    adu = pack('>HHHB', trans_id, MODBUS_TCP_PROTOCOL_ID, adu_length, unit_id) + pdu
    
    return adu

def parse_modbus_response(response):
    if len(response) < 9:
        return None, None  # Invalid response length

    # Convert the response to a hex string
    data = response.hex()

    # Extract the return code and exception code as in the original code
    # Since the .hex() produces a string, we can slice it as normal
    return_code = int(data[14:16], 16)  # Extract 2 hex characters for return code
    exception_code = int(data[17:18], 16)  # Extract 1 hex character for exception code

    return return_code, exception_code


def enumerate_function_codes(ip, port, unit_id, verbose=False):
    sock = connect_to_target(ip, port)
    if not sock:
        print(f"[-] Modbus is not running on: {ip}")
        return

    print(f"[+] Looking for supported function codes on {ip}")
    try:
        for func_code in range(MAX_FUNCTION_CODES):
            trans_id = func_code + 2  # Start Transaction ID from 2
            request = build_modbus_request(trans_id, unit_id, func_code)
            
            if verbose:
                print(f"[VERBOSE] OutBound Raw Bytes for {func_code}: {request.hex()}")
            try:
                sock.sendall(request)
                response = sock.recv(1024)
                if response:
                    if verbose:
                        print(f"[VERBOSE] Inbound Raw Bytes for {func_code}: {response.hex()}")

                    return_code, exception_code = parse_modbus_response(response)
                    
                    if verbose:
                        print(f"[VERBOSE] return_code: {return_code}, exception_code: {exception_code}")

                    # Checking if the return code > 127 and exception code == 0x01, it's not supported
                    if return_code > 127 and exception_code == 0x01:
                        #print(f"[-] Function Code {func_code} is not supported.")
                        a=1
                    else:
                        # Supported function codes
                        if func_code in function_code_name:
                            print(f"[+] Function Code {func_code} ({function_code_name[func_code]}) is supported.")
                        else:
                            print(f"[+] Function Code {func_code} is supported.")
                            
                            
						# If Function Code 8 is supported, list diagnostic sub-functions
                        if func_code == 8:
                            print("[└────────] Check for Diagnostic Sub-Functions:")
                            for sub_code, description in diagnostic_sub_functions.items():
                                print(f"\t[*] Sub-Function 0x{sub_code:02X}: {description}")
                                
                else:
                    print(f"[-] No response for Function Code {func_code}.")
            except socket.timeout:
                print(f"[-] Timeout for Function Code {func_code}.")
            except Exception as e:
                print(f"[-] Error testing function code {func_code}: {e}")
    finally:
        sock.close()



# The `execute` method to be called from the CLI
def execute(args):
    ip = args.host
    port = args.port
    unit_id = args.slave
    verbose = args.verbose if hasattr(args, 'verbose') else False
    enumerate_function_codes(ip, port, unit_id, verbose)
