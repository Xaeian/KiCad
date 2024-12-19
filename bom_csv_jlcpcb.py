"""
@package
Output: CSV (comma-separated)
Grouped By: Manufacturer, Code2
Sorted By: Code2 (asc)
Fields: Comment(Value), Designator(Reference), Footprint(), Code2

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
    comp.getField("Code2"),
    comp.getDNP()
  ])

df = pd.DataFrame(array, columns=["Manufacturer", "Code", "Comment", "Designator", "Footprint", "Code2", "DNP"])
df = df[(df["Code"].astype(str) != "") & (df["Code2"].astype(str) != "")]
df = df[(df["DNP"].astype(bool) == False)]
df = df.drop(columns=["DNP"])


sys.argv[2]
df = df.groupby(["Manufacturer", "Code"]).agg({
  "Comment": "first",
  "Designator": lambda x: ",".join(x),
  "Footprint": "first",
  "Code2": "first"
}).reset_index()

df = df.drop(columns=["Manufacturer", "Code"])
df = df.rename(columns={"Code2": "JLCPCB Part #"})

name = os.path.splitext(sys.argv[2])[0] + "-bom-jlcpcb.csv"
df.to_csv(name, index=False)
os.remove(sys.argv[1])
