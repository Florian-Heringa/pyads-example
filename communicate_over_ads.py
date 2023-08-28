import pyads
import argparse
from time import sleep
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--AmsNetID", default=pyads.get_local_address())
parser.add_argument("-n", "--num_heartbeat", default=3, type=int)

args = parser.parse_args()

address = pyads.AmsAddr(args.AmsNetID, pyads.PORT_TC3PLC1)

## ========================= Connect to PLC
print(f"Connecting to: {address}......")
plc = pyads.Connection(address.netid, address.port)
plc.open()
if not plc.is_open:
    print("\tConnection failed => closing..")
    exit()

print("\tConnection successful...")

## ======================== Get an overview of available symbols
print("\n========= Available Symbols ==============")
for _ in plc.get_all_symbols():
    print(_.name)
print("=========================================\n")

## ======================== Read unstructured data type
print("Printing Heartbeat....")
for i in range(args.num_heartbeat):
    print(f'\tiHeartbeat => {plc.read_by_name("MAIN.iHeartbeat")}')
    sleep(1)

## ======================= Write unstructured datatype
# Reset the heartbeat to 0
print("Reset heartbeat...")
plc.write_by_name("MAIN.iHeartbeat", 0)
print(f"New value of heartbeat after reset...")
print(f'\tiHeartbeat => {plc.read_by_name("MAIN.iHeartbeat")}')

## ======================= Read structured datatype
print("\nHandling structured data type...")
structure_def = (
    ("iInt", pyads.PLCTYPE_UINT, 1),
    ("fReal", pyads.PLCTYPE_LREAL, 1),
    ("aArray", pyads.PLCTYPE_INT, 11)
)

structured_data = plc.get_symbol("MAIN.st_comm", structure_def=structure_def)
print("The structure definition is:")
pprint(structured_data.structure_def)

structured_data.write({"iInt": 42, "fReal": 3.1415692, "aArray": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]})
print("\nAfter writing, the values in the PLC are:")
pprint(structured_data.read())

plc.close()