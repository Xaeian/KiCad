NAME=$('whoami')
URL="C:/Users/$NAME/AppData/Roaming/kicad/8.0"
SCR="C:/Program Files/KiCad/8.0/bin/scripting/plugins"
cp fp-lib-table $URL/fp-lib-table
cp sym-lib-table $URL/sym-lib-table
cp kicad_common.json $URL/kicad_common.json
cp bom_csv_jlcpcb.py "$SCR/bom_csv_jlcpcb.py"
cp bom_csv_xaeian.py "$SCR/bom_csv_xaeian.py"
