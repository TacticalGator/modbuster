# modbuster
![signal-2024-12-02-225241](https://github.com/user-attachments/assets/b8f6a24e-df4a-4a08-9b50-02aac4e9cc4e)
$~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ Art by **mel_arts.graphicdesign** <br>

<br>

> Busting ICS/SCADA over modbus

<br>
Modbuster is a pure Python 3 command-line tool, powered by pymodbus, specifically designed for penetration testers, red teamers, and security researchers. It enables precise Modbus TCP interactions, including single and multi-read operations for Coils, Discrete Input Ranges, Input Registers, and Holding Registers, as well as single and multi-write capabilities for Coils and Holding Registers. Beyond these operations, it facilitates enumeration of supported Modbus function codes, aiding in vulnerability assessments and device exploration. With its straightforward interface and advanced features, Modbuster is an essential tool for anyone investigating or auditing Modbus environments.
<br>
<br>
<br>

# INSTALLATION
1. Clone the repository
```sh
git clone https://github.com/TacticalGator/modbuster
```

2. Use pipx to install
```sh
cd modbuster && pipx install .
```
<br>
<br>

## Using pip
1. Clone the repository
```sh
git clone https://github.com/TacticalGator/modbuster
```

2. Set up a virtual environment (Recommended & Optional)
```sh
python3 -m venv myVenv && source ./myVenv/bin/activate
```

3. Install with pip
```sh
cd modbuster && pip3 install .
```
<br>
<br>
<br>

# USAGE
```sh
modbuster <OPTIONAL_FLAGS> {read,write,getfunctions,diag} <HOST> <ADDRESS> <VALUES>
```
<br>


```sh
# modbuster --help
usage: modbuster.py [-h] [-s SLAVE] [-p PORT] [-v] [--restart-comm] [--force-listen-only] [--clear-counter] [--clear-overrun]
                    [--getclear-res]
                    {read,write,getfunctions,diag}

  Busting ICS/SCADA over Modbus

examples:
       modbuster read -s 1 127.0.0.1 400001 10
       modbuster write 127.0.0.1 300231 11 22 33 44 55
       modbuster getfunctions 127.0.0.1
       modbuster diag --slave 2 127.0.0.1
       modbuster diag -s 1 127.0.0.1 --force-listen-only

positional arguments:
  {read,write,getfunctions,diag}
                        Command to execute:
                          read          Read holding & input registers, coils, or disecrete inputs from a Modbus server
                          write         Write values to registers or coils on a Modbus server
                          getfunctions  Enumerate supported Modbus function codes
                          diag          Perform diagnostic functions

options:
  -h, --help            show this help message and exit
  -s SLAVE, --slave SLAVE
                        Specify the slave ID (default: 0)
  -p PORT, --port PORT  Specify the Modbus server port (default: 502)
  -v, --verbose         Enable detailed output (verbose mode)

*DANGEROUS Diagnostic Command Flags (used exclusively with "diag" command):
  --restart-comm        Restart communication (toggle mode)
  --force-listen-only   Force the device into listen-only mode
  --clear-counter       Clear Modbus communication counters
  --clear-overrun       Clear character overrun counters
  --getclear-res        Retrieve and clear Modbus Plus responses
```
<br>
<br>

## ADDRESS RANGE
```
000001 - 065535: Coil Range
100001 - 165535: Discrete Input Range
300001 - 365535: Input Register Range
400001 - 465535: Holding Register Range
```
<br>

## EXAMPLES
➡️ 3 Verbs are currently supported
<br>
<br>
**IMPORTANT**:<br>
Both read and write operations use **0-based** addressing internally,<br>
However addresses are often represented as **1-based**
<br>
<br>
<br>
## read 📖
➡️ single/multi read across **all 4 address ranges**
<br>
<br>
![image](https://github.com/user-attachments/assets/ca776a29-fb1c-415e-85f6-91a41298b647)\
Reading 3 values of **Input Register**, starting from the address `300001`
<br>
<br>
<br>
![image](https://github.com/user-attachments/assets/e07f64a9-f0d4-4c31-8428-c3b11cf4fb12)\
Reading a single value of **Discrete Input**, at the address `101992`
<br>
<br>
<br>
![image](https://github.com/user-attachments/assets/9054237d-ba8e-45f2-bcf2-e23ff1979cbd)\
Reading 16 values of **Coil**, starting from the address `1`
<br>
<br>
<br>
![image](https://github.com/user-attachments/assets/e3d63694-dccc-4952-bf6d-83d3a871eaaf)\
Reading 10 values of **Holding Register**, starting from the address `400001`
<br>
<br>
<br>
## write ✍🏻
➡️ single/multi write to **coil** and **holding register**
<br>
<br>
![image](https://github.com/user-attachments/assets/e41ee352-7862-4684-8f1f-b531571189e8)\
![{03FAD36C-2A34-4080-9ACD-6FD4CADDF3D3}](https://github.com/user-attachments/assets/2c12264b-8ff6-4d0d-bf28-6ef6fe6fdb1e)\
Writing 10 of `1` to **coil**, starting from the address `1` 
<br>
<br>
<br>
![{F6FDB7DB-5D54-49DD-B0F5-E0BA01F67C2E}](https://github.com/user-attachments/assets/be1421d1-1622-469f-8457-56bb8c0bfcbb)\
![{FD76339B-820B-4676-BB19-6EE1C9AC7005}](https://github.com/user-attachments/assets/7caf651c-0691-4e55-942f-13f275ed9642)\
Writing a total of 5 values(`11`, `22`, `33`, `44`, `55`) to **Holding Register**, starting from thee address `400010`
<br>
<br>
<br>
## getfunctions ƒ
➡️ enumerate supported modbus function of a given target
<br>
<br>
![image](https://github.com/user-attachments/assets/e3828fba-4ccb-430f-a1d6-6c5c55fb3442)\
Enumerating supported modbus functions using `getfunctions` verb
<br>
<br>
<br>
## diag 🔧
➡️ enumerate a given target via diagnostic functions
<br>
<br>
![{AB71D51E-BD37-4938-A490-F3D213CF241C}](https://github.com/user-attachments/assets/e0e170fd-e780-46f6-b919-cb6f999998f5)
<br>
<br>
## Dangerous diag 🚩
```
DANGEROUS_FLAGS = {
    "--restart-comm": ("diag_restart_communication", "Restart Communication", {'toggle': True}),
    "--force-listen-only": ("diag_force_listen_only", "Force Listen-Only Mode", {'slave': 0}),
    "--clear-counter": ("diag_clear_counters", "Clear Counters", {'slave': 0}),
    "--clear-overrun": ("diag_clear_overrun_counter", "Clear Overrun Counter", {'slave': 0}),
    "--getclear-res": ("diag_getclear_modbus_response", "Get/Clear modbus plus", {'slave': 0}),
}
```
Use with Extreme Caution 
<br>
<br>
<br>
## ADVANCED USAGE
![{45924414-A748-41FE-B0A8-953805E328C8}](https://github.com/user-attachments/assets/9babe1c6-99df-4f95-8ca8-9bbe97770a1d)\
It can be combined with other command line tools such as `watch` or `proxychains4`
<br>
<br>
<br>
![{0D477EBD-95A4-4076-B4F7-74EF48DB87D7}](https://github.com/user-attachments/assets/d2c70957-ee09-49fa-9f79-44e2d200e7bd)\
Same goes for the write operation. Above example conduct a continuous write operation
<br>
<br>
<br>
# DISCLAIMER
This tool is provided strictly for educational and research purposes. Its primary objective is to assist security professionals, system administrators, and researchers in identifying and addressing potential vulnerabilities in Modbus-based systems.

The author(s) and contributors of this tool explicitly do not endorse, condone, or assume responsibility for the misuse of this tool for illegal, unethical, or unauthorized activities. By using this tool, you acknowledge, understand, and agree to the following terms:

1. Authorized Use Only
   - This tool is to be used only with explicit authorization from the owner or administrator of the target systems or networks.
   - Unauthorized access, testing, or any form of use against systems for which you lack proper permissions may constitute a violation of applicable laws and regulations, including but not limited to:
       - Computer Misuse Acts
       - Hacking or Unauthorized Access Laws
       - Industrial Control Systems (ICS) Security Standards
       - Privacy and Data Protection Regulations
   - You are solely responsible for obtaining the necessary permissions before engaging in any activities involving this tool.

2. Educational and Research Intent
   - This tool is intended to:
       - Foster understanding of the Modbus protocol and its implementation in industrial systems.
       - Aid in identifying and mitigating vulnerabilities within authorized systems.
       - Support security education, ethical hacking practices, and secure design in industrial environments.
   - It is not designed or intended for:
       - Malicious activities such as exploiting vulnerabilities, disrupting operations, or unauthorized surveillance.
       - Engaging in activities that violate ethical standards or professional guidelines.

3. No Warranties or Guarantees
   - This tool is provided "AS IS" without any express or implied warranties or guarantees. This includes but is not limited to:
       - Guarantees of accuracy, reliability, or performance in any environment.
       - Compatibility with all Modbus implementations or network setups.
       - Protection from unintended consequences, including potential system disruption or data loss.
   - Users assume all risks associated with deploying, running, or testing this tool.

4. Limitation of Liability
   - The author(s) and contributors disclaim all liability for any damages or losses, whether direct, indirect, incidental, or consequential, arising from the use or misuse of this tool. Examples include but are not limited to:
       - Disruption of operational systems or processes.
       - Loss of data or financial impacts resulting from testing activities.
       - Legal actions taken against users for unauthorized or unethical use.
   - Users bear full responsibility for understanding and mitigating any risks involved in using this tool.

5. Ethical and Legal Compliance
   - Users of this tool agree to act responsibly, ethically, and in accordance with all applicable laws, regulations, and standards in their jurisdiction.
   - Ethical guidelines include, but are not limited to:
       - Respecting the rights and privacy of system owners, operators, and users.
       - Reporting identified vulnerabilities responsibly, adhering to Coordinated Vulnerability Disclosure (CVD) practices or equivalent frameworks.
       - Avoiding activities that cause unnecessary harm, damage, or disruption to any system.

6. Contribution and Redistribution
   - Contributions to the development of this tool are welcomed and encouraged. However, contributors must adhere to the same principles outlined in this disclaimer.
   - Redistribution, modification, or sharing of this tool (including forks or derivatives) must retain this disclaimer to ensure that future users understand its intended purpose and limitations.

7. Reporting and Disclosure
   - If this tool reveals vulnerabilities in a Modbus-based system, the user is strongly encouraged to report these findings to the system owner, vendor, or a relevant security team in a responsible manner.
   - Follow industry standards for disclosure, such as:
       - Coordinated Vulnerability Disclosure (CVD) protocols.
       - Adhering to applicable government or industry frameworks for ICS security.

8. Acknowledgment of Risks
   - Users acknowledge that:
       - Testing Modbus systems, even with authorization, can carry inherent risks, including potential operational disruptions.
       - This tool does not include safeguards to prevent accidental harm to systems during its use. It is the user's responsibility to deploy the tool in a controlled, authorized, and secure manner.
       - The improper use of this tool may result in personal, legal, or financial consequences for which the author(s) bear no responsibility.

9. Acceptance of Terms
   - By downloading, cloning, or using this tool, you:
       - Affirm that you have read, understood, and agreed to this disclaimer.
       - Accept all risks and responsibilities associated with its use.
       - Agree to use the tool only for lawful, ethical, and authorized purposes.
   - If you do not agree to these terms, you are prohibited from using this tool in any capacity.
