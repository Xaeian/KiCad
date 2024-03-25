"""
@package
Output: CSV (comma-separated)
Grouped By: Manufacturer, LCSC
Sorted By: LCSC
Fields: Comment(Value), Designator(Reference), Footprint(), LCSC

Command line:
python "pathToFile/bom_csv_jlcpcb.py" "%I" "%O.csv"
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
    comp.getField("Code"),
    comp.getValue(),
    comp.getRef(),
    comp.getFootprint(),
    comp.getField("LCSC")
  ])

df = pd.DataFrame(array, columns=["Manufacturer", "Code", "Comment", "Designator", "Footprint", "LCSC"])
df = df[(df["Code"].astype(str) != "") | (df["LCSC"].astype(str) != "")]

sys.argv[2]
df = df.groupby(["Manufacturer", "Code"]).agg({
    "Comment": "first",
    "Designator": lambda x: ",".join(x),
    "Footprint": "first",
    "LCSC": "first"
}).reset_index()

df = df.drop(columns=["Manufacturer", "Code"])
df = df.rename(columns={"LCSC": "JLCPCB Part #"})

df.to_csv(sys.argv[2], index=False)
os.remove(sys.argv[1])
