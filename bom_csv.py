"""
@package
Output: CSV (comma-separated)
Grouped By: Manufacturer, Code
Sorted By: Manufacturer (asc), Code (asc)
Fields: Manufacturer, Value, Code, Pacage, Description,
  Count Datasheet, Reference

Command line:
python "pathToFile/bom_csv.py" "%I" "%O.csv"
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
    comp.getFootprint(),
    comp.getField("Description"),
    1,
    comp.getDatasheet(),
    comp.getRef(),
    comp.getDNP()
  ])

df = pd.DataFrame(array, columns=["Manufacturer", "Value", "Code", "Pacage", "Description", "Count", "Datasheet", "Reference", "DNP"])
df = df[(df["Code"].astype(str) != "")]
df = df[(df["DNP"].astype(bool) == False)]
df = df.drop(columns=["DNP"])

sys.argv[2]
df = df.groupby(["Manufacturer", "Code"]).agg({
  "Value": "first",
  "Pacage": "first",
  "Description": "first",
  "Count": "sum",
  "Datasheet": "first",
  "Reference": lambda x: ",".join(x)
}).reset_index()

name = os.path.splitext(sys.argv[2])[0] + "-bom.csv"
df.to_csv(name, index=False)
os.remove(sys.argv[1])
