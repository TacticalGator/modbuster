import sys
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from .common import connect_to_modbus_server, _modbus_exceptions

# Mapping of 13 non-distruptive diagnostic function handlers to more descriptive names
DIAGNOSTIC_FUNCTIONS = {
    "diag_read_diagnostic_register": "Diagnostic Register",
    "diag_change_ascii_input_delimeter": "Change ASCII Input Delimiter",
    "diag_read_bus_message_count": "Bus Message Count",
    "diag_read_bus_comm_error_count": "Bus Communication Error Count",
    "diag_read_bus_exception_error_count": "Bus Exception Error Count",
    "diag_read_slave_message_count": "Slave Message Count",
    "diag_read_slave_no_response_count": "Slave No Response Count",
    "diag_read_slave_nak_count": "Slave NAK Count",
    "diag_read_slave_busy_count": "Slave Busy Count",
    "diag_read_bus_char_overrun_count": "Bus Character Overrun Count",
    "diag_read_iop_overrun_count": "IOP Overrun Count",
    "diag_get_comm_event_counter": "Communication Event Counter",
    "diag_get_comm_event_log": "Communication Event Log",
}

# Optional flags for the `diag` verb with their corresponding pymodbus function names, descriptions, and default arguments
DANGEROUS_FLAGS = {
    "--restart-comm": ("diag_restart_communication", "Restart Communication", {'toggle': True}),
    "--force-listen-only": ("diag_force_listen_only", "Force Listen-Only Mode", {'slave': 0}),
    "--clear-counter": ("diag_clear_counters", "Clear Counters", {'slave': 0}),
    "--clear-overrun": ("diag_clear_overrun_counter", "Clear Overrun Counter", {'slave': 0}),
    "--getclear-res": ("diag_getclear_modbus_response", "Get/Clear modbus plus", {'slave': 0}),
}


def execute(args):
    """
    Executes the 'diag' command for modbuster. Runs diagnostic functions based on
    the flags provided (dangerous flags or non-disruptive diagnostic functions).
    """
    slave_id = args.slave  # Slave ID (default 0 if not provided)
    host = args.host  # Host IP

    if args.verbose:
        print(f"[VERBOSE] Connecting to {host}:{args.port} as slave {slave_id}")

    # Establish connection to the Modbus server
    client = connect_to_modbus_server(host, port=args.port)

    try:
        # Check if any dangerous flag is provided
        dangerous_flags_set = [flag for flag in DANGEROUS_FLAGS if getattr(args, flag.lstrip('-').replace('-', '_'), False)]

        if dangerous_flags_set:
            if args.verbose:
                print(f"[VERBOSE] Dangerous flags detected, skipping regular diagnostic functions.")

            # Run the dangerous flags functions
            for flag in dangerous_flags_set:
                function_name, description, default_args = DANGEROUS_FLAGS[flag]
                print(f"Attempting To {description}...")

                # Prepare the arguments to call the function
                kwargs = {**default_args, **{'slave': slave_id}}  # Add or override with slave_id
                func = getattr(client, function_name)
                result = func(**kwargs)  # Pass dynamic arguments to the function

                handle_modbus_result(result, description, args.verbose)

        else:
            # Run the regular 13 non-disruptive diagnostic functions
            if args.verbose:
                print(f"[VERBOSE] Running 13 non-disruptive diagnostic functions...")

            for func_name, description in DIAGNOSTIC_FUNCTIONS.items():
                try:
                    func = getattr(client, func_name)

                    # Handle the special case for functions that do not expect a slave ID
                    if func_name in ["diag_get_comm_event_counter", "diag_get_comm_event_log"]:
                        result = func()
                    else:
                        result = func(slave=slave_id)

                    # Process result
                    handle_modbus_result(result, description, args.verbose)

                except AttributeError:
                    print(f"[-] {description}: Not supported by the pymodbus client")
                except ModbusIOException as e:
                    print(f"[-] {description}: Communication error: {e}")

    finally:
        client.close()


def handle_modbus_result(result, description, verbose):
    """
    Handles the result of a Modbus operation. Checks for errors and prints relevant messages.
    """
    if result.isError():
        exception_code = getattr(result, 'exception_code', None)
        if exception_code in _modbus_exceptions:
            error_message = _modbus_exceptions[exception_code]
            if verbose:
                print(f"[VERBOSE] [-] {description}: Exception ({error_message}: {result.__dict__})")
            else:
                print(f"[-] {description}: Not supported ({error_message})")
        else:
            if verbose:
                print(f"[VERBOSE] [-] {description}: Unknown exception {result.__dict__}")
            else:
                print(f"[-] {description}: Not supported (unknown error)")
    else:
        # Print the `message` attribute or full JSON for debugging
        message = getattr(result, "message", None)
        if verbose:
            print(f"[VERBOSE] [+] {description}: {result.__dict__}")
        else:
            if message is not None:
                print(f"[+] {description}: {message}")
            else:
                print(f"[-] {description}: No relevant data found")
