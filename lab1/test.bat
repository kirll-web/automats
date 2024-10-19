python3 main.py mealy-to-moore 1mea.csv 1moo.csv
fc 1moo.csv 1_moore.csv

python3 main.py moore-to-mealy 1moo.csv 1mea.csv
fc 1mea.csv 1_mealy.csv

python3 main.py moore-to-mealy 6moo.csv 6mea.csv
fc 6mea.csv 6_rev_mealy.csv