# PaoWii
Making the Wii work like a switch
# PaoWii – CMPS 375 File Transfer Prototype

This project simulates a dock behavior:
- A "USB drive" folder is copied to a "USB-C connected device" folder
- No files are deleted
- By default, existing destination files are NOT overwritten

## Run (local demo)

From the project root:

```powershell
# default demo paths
python .\src\main.py

# custom paths
python .\src\main.py --src test_data/usb_source --dst test_data/usbc_destination

# overwrite existing destination files (optional)
python .\src\main.py --overwrite
