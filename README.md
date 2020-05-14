# Stage SociauxAntenne

# OnlyMobile.py

! the script must be executed with pyton3 in his own dir

The script takes all *SUP_\** tables in tables dir and wrtite new ones *MOBILE_\** in the same dir.
New tables only include emitters with type is in *typeEMRfilter.txt* or other elements holding this type of emitter.

## File needed
| Files              | Description |
|--------------------|-------------|
| ./OnlyMobile.py    | Source code |
| Import (csv, time) | |
| ./tables/SUP_?.txt | Dir with all tables to sort (SUPPORT, ANTENNE, STATION, EMETTEUR) |
| *./tables/SUP_EXPLOITANT.txt* | Link between id and name of operator |
| ./typeEMRfilter    | File with all emitters types to filter (initialy mobile network)|
