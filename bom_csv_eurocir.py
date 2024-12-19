"""
@package
Output: CSV (comma-separated)
Grouped By: Manufacturer, Code
Sorted By: Manufacturer (asc), Code (asc)
Fields: Code(Manufacturer Part Number), Description,
  Reference(Reference Designator), Count(Quantity), Manufacturer

Command line:
python "pathToFile/bom_csv_eurocir.py" "%I" "%O.csv"
"""

import sys, os
import kicad_netlist_reader
import pandas as pd

net = kicad_netlist_reader.netlist(sys.argv[1])
components = net.getInterestingComponents(excludeBOM=True)
array = []

for comp in components:
  array.append([
    comp.getField("Manufacturer"),
    comp.getValue(),
    comp.getField("Code"),
    comp.getField("Description"),
    1,
    comp.getRef(),
    comp.getDNP()
  ])

df = pd.DataFrame(array, columns=["Manufacturer", "Value", "Code", "Description", "Count", "Reference", "DNP"])
df = df[(df["Code"].astype(str) != "")]
df = df[(df["DNP"].astype(bool) == False)]
df = df.drop(columns=["DNP"])

sys.argv[2]
df = df.groupby(["Manufacturer", "Code"]).agg({
  "Value": "first",
  "Description": "first",
  "Count": "sum",
  "Reference": lambda x: ",".join(x)
}).reset_index()

df = df[["Code", "Description", "Reference", "Count", "Manufacturer"]]
df = df.rename(columns={"Code": "Manufacturer Part Number", "Reference": "Reference Designator", "Count": "Quantity"})

name = os.path.splitext(sys.argv[2])[0] + "-bom-eurocir.csv"
df.to_csv(name, index=False)
os.remove(sys.argv[1])
