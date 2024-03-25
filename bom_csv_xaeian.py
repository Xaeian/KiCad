"""
@package
Output: CSV (comma-separated)
Grouped By: Manufacturer, Code
Sorted By: Manufacturer (asc), Code (asc)
Fields: Manufacturer, Value, Code, Pacage, Description,
    Count Datasheet, Reference

Command line:
python "pathToFile/bom_csv_xaeian.py" "%I" "%O.csv"
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
    comp.getRef()
  ])

df = pd.DataFrame(array, columns=["Manufacturer", "Value", "Code", "Pacage", "Description", "Count", "Datasheet", "Reference"])
df = df[(df["Code"].astype(str) != "")]

sys.argv[2]
df = df.groupby(["Manufacturer", "Code"]).agg({
    "Value": "first",
    "Pacage": "first",
    "Description": "first",
    "Count": "sum",
    "Datasheet": "first",
    "Reference": lambda x: ",".join(x)
}).reset_index()

df.to_csv(sys.argv[2], index=False)
os.remove(sys.argv[1])
