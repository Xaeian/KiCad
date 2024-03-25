## KiCad Library

### Library Contents:

- `Symbols\` - Libraries containing symbols
  - Files in symbol format `.lib` and links to documentation in `.dcm` format
  - The folder should be linked to the system variable `LSB` in KiCad program
- `Footprints\` - Libraries containing footprints _(components)_
  - Folders with footprints in `.kicad_mod` format
  - The folder should be linked to the system variable `LFP` in KiCad program
- `Models\` - Libraries containing 3D models
  - Files in `.step` format, sometimes **FreeCAD** projects in `.FCStd` format
  - The folder should be linked to the system variable `3D` in KiCad program
- `frame.kicad_wks` - Empty frame for **eeschema** and **pcbnew** programs
- `sym-lib-table` - Table for symbol libraries
- `fp-lib-table` - Table for footprint libraries
- `kicad_common.json` - Kicad pathes
- `bom_csv_jlcpcb.py`, `bom_csv_xaeian.py` - Scripts for generate BOM files

### Placement:

Tables `sym-lib-table`, `fp-lib-table`, `kicad_common.json` should be placed in the location:

```
C:\Users\%USERNAME%\AppData\Roaming\kicad\8.0
```

Scripts  `bom_csv_jlcpcb.py`, `bom_csv_xaeian.py` should be placed in the location: 

```
C:\Program Files\KiCad\8.0\bin\scripting\plugins
```

Alternatively, you can use the following script to automate the process:

```bash
bash cp-lib-table.sh
```