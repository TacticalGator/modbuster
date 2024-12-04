#!/usr/bin/env python3
import sys
import os
import argparse

# Adjust sys.path if running as a script
if __name__ == "__main__" and __package__ is None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(script_dir))

# Now imports work in both cases
from modbuster.verbs import read, write, getfunctions, diag

ASCII_ART = r"""
                       █    █                                                                       
                  ███                                                                               
                                                                                                    
               █                                                                                    
                                                                                                    
              █                                                                                     
                      █  ██  ██                                                                     
            █           █                                                                           
            █           █   ███                                                                     
            █           █                                                                           
            █           █                                                             █████         
            █                 █                                                   ████████ █        
           █       █     █    █                                                           █         
███████████   ████ █  █   ████████ ██████   ███  ███  ██████  ████████ ███████ ███████  █  █        
███ ██  ███  ██  █ █ █         ███    ███   ███  ███  ███       ███    ███         ███  █    █ █    
███     ███ ██ █       █   █   ███    ███   ███  ███  ████      ███    ██████     ████  █  █        
███     █████████ ███ ███████  ███     ███  ███  ███   ████     ███    ███       ███    █           
███     ███ ██ █       █       ███      ███ ███  ███     ████   ███    ███      ████    █  ██       
███     ███  ██  █ █ █         ███     ████ ███  ███      ███   ███    ███       ████   █           
███     ███   ███  █  ██   ███████ ███████   ███████  ██████    ███    ███████    ████  █           
                   █                                                                    █           
                                                                      ██  █████████████ █ █         
                                                                        █████████████   █           
                                                                                     █              
                                                                   
								Art by mel_arts.graphicdesign
"""

def main():
    parser = argparse.ArgumentParser(
        description=(
            ASCII_ART
            + "\n  Busting ICS/SCADA over Modbus\n\n"
            "examples:\n"
            "       modbuster read -s 1 127.0.0.1 400001 10\n"
            "       modbuster write 127.0.0.1 300231 11 22 33 44 55\n"
            "       modbuster getfunctions 127.0.0.1\n"
            "       modbuster diag --slave 2 127.0.0.1\n"
            "       modbuster diag -s 1 127.0.0.1 --force-listen-only\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        'command',
        choices=['read', 'write', 'getfunctions', 'diag'],
        help=(
            "Command to execute:\n"
            "  read          Read holding & input registers, coils, or disecrete inputs from a Modbus server\n"
            "  write         Write values to registers or coils on a Modbus server\n"
            "  getfunctions  Enumerate supported Modbus function codes\n"
            "  diag          Perform diagnostic functions\n"
        ),
    )
    parser.add_argument(
        '-s', '--slave',
        type=int,
        default=0,
        help="Specify the slave ID (default: 0)",
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=502,
        help="Specify the Modbus server port (default: 502)",
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable detailed output (verbose mode)",
    )

    # Diagnostic command flags
    diag_parser = parser.add_argument_group(
        '*DANGEROUS Diagnostic Command Flags (used exclusively with "diag" command)',
    )
    diag_parser.add_argument('--restart-comm', action='store_true', help="Restart communication (toggle mode)")
    diag_parser.add_argument('--force-listen-only', action='store_true', help="Force the device into listen-only mode")
    diag_parser.add_argument('--clear-counter', action='store_true', help="Clear Modbus communication counters")
    diag_parser.add_argument('--clear-overrun', action='store_true', help="Clear character overrun counters")
    diag_parser.add_argument('--getclear-res', action='store_true', help="Retrieve and clear Modbus Plus responses")

    # Parse arguments
    args, remaining_args = parser.parse_known_args()

    # Check exclusive flags for "diag"
    if args.command != 'diag' and any(
        [args.restart_comm, args.force_listen_only, args.clear_counter, args.clear_overrun, args.getclear_res]
    ):
        parser.error(
            "The flags (--restart-comm, --force-listen-only, --clear-counter, --clear-overrun, --getclear-res) "
            "can only be used with the 'diag' command."
        )

    # Handle commands
    if args.command == 'getfunctions':
        getfunctions_parser = argparse.ArgumentParser(description="Retrieve supported Modbus function codes")
        getfunctions_parser.add_argument('host', help="Specify the Modbus server IP or hostname")
        getfunctions_args = getfunctions_parser.parse_args(remaining_args)
        args.host = getfunctions_args.host
        getfunctions.execute(args)

    elif args.command == 'diag':
        diag_parser = argparse.ArgumentParser(description="Perform diagnostic functions on a Modbus server")
        diag_parser.add_argument('host', help="Specify the Modbus server IP or hostname")
        diag_args = diag_parser.parse_args(remaining_args)
        args.host = diag_args.host
        diag.execute(args)

    else:
        parser.add_argument('host', help="Specify the Modbus server IP or hostname")
        parser.add_argument('address', type=int, help="Starting Modbus address (register/coil)")
        parser.add_argument('count_or_values', nargs='+', help="Number of items to read or values to write")
        args = parser.parse_args()

        if args.command == 'read':
            if len(args.count_or_values) != 1:
                parser.error("The 'read' command requires a single count value.")
            args.count = int(args.count_or_values[0])
            read.execute(args)

        elif args.command == 'write':
            args.values = [int(value) for value in args.count_or_values]
            write.execute(args)

if __name__ == "__main__":
    main()
