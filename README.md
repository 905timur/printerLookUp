
## Script Function 

The **printerLookUp** script is a tool designed to scan a specified subnet for active printers. It performs port scanning and gathers information from printers. The script utilizes concurrent threads to speed up the scanning process. 


### Prerequisites

Before using the **printerLookUp** script, ensure you have the following installed:

- Python (Version 3.x)

### Instructions

1. Open the `printerLookUp.py` script in a text editor.

2. Modify the `target_subnet` variable to specify the target subnet you want to scan. For example:

   ```python
   target_subnet = "192.168.1.0/24"

3.  (optional) The script is set to run on TCP port 9100, modify if needed.

4.  Execute the script in terminal by running `python printerLookUp.py`

## BASH

1.   Make it executable: chmod +x script.sh

2.   Run it with a subnet: ./script.sh 192.168.1.0/24

Requirements:

nc (netcat) for printer information retrieval

ipcalc for subnet calculations

timeout command (usually pre-installed)
