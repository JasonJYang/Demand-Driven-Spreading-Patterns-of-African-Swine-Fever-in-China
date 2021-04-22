# Demand-Driven-Spreading-Patterns-of-African-Swine-Fever-in-China
## This is the data, code, and corresponding results for our paper *Demand-Driven-Spreading-Patterns-of-African-Swine-Fever-in-China*.

The data includes the locations of province capitals, the road network, the locations of slaughter houses in mainland China, and the pork consumption and export (import) ratio for each province in mainland China.

The transportation distance and the counting of slaughter houses are computed by ArcMap 10.2. The corresponding distance processing is implemented in `/code/distance.py` by Python.

The results of three kinds of spread mechanisms are in `/results/` where res_NDS.csv contains the result of the natural distance spreading, res_TDS.csv contains the result of the transportation distance spreading, and res_DaTDS.csv contains the result of the demand-adjusted transport distance spreading.
