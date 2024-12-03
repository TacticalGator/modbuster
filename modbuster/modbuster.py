#!/usr/bin/env python3
import sys
import argparse
from modbuster.verbs import read, write, getfunctions

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
        description=ASCII_ART + "\n  Busting ICS/SCADA over modbus\n\nExamples:\n"
                    "    modbuster read -s 1 127.0.0.1 400001 10\n"
                    "    modbuster write 127.0.0.1 300231 11 22 33 44 55\n"
                    "    modbuster getfunctions 127.0.0.1",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('command', choices=['read', 'write', 'getfunctions'], help="Command to execute: 'read', 'write', or 'getfunctions'")
    parser.add_argument('-s', '--slave', type=int, default=0, help="Slave ID (default: 0)")
    parser.add_argument('-p', '--port', type=int, default=502, help="Port to connect to (default: 502)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")

    args, remaining_args = parser.parse_known_args()

    if args.command == 'getfunctions':
        getfunctions_parser = argparse.ArgumentParser(description="Get supported Modbus function codes")
        getfunctions_parser.add_argument('host', help="Modbus server host (IP address or hostname)")
        getfunctions_args = getfunctions_parser.parse_args(remaining_args)
        args.host = getfunctions_args.host
        getfunctions.execute(args)
    else:
        parser.add_argument('host', help="Modbus server host (IP address or hostname)")
        parser.add_argument('address', type=int, help="Modbus address to read/write from")
        parser.add_argument('count_or_values', nargs='+', help="Number of registers/coils to read or values to write")
        args = parser.parse_args()

        if args.command == 'read':
            if len(args.count_or_values) != 1:
                print("Error: Read command requires a single count value.")
                sys.exit(1)
            args.count = int(args.count_or_values[0])
            read.execute(args)

        elif args.command == 'write':
            args.values = [int(value) for value in args.count_or_values]
            write.execute(args)

if __name__ == "__main__":
    main()
