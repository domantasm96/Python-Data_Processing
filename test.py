import csv
import string
from copy import deepcopy
from collections import namedtuple
import operator as op
import pandas as pd

from s1513204 import DataManipulation

df = pd.read_csv("data10_small.csv")
df.reindex()

csvreader = csv.reader(open("data10_small.csv"))
dm = DataManipulation(csvreader)

aplhabet = string.ascii_uppercase + string.ascii_lowercase + string.digits

print("SELECT TEST")
select_list = ('int1', 'str4', 'date1', 'str1', 'float2', 'str2')
tmp_dm = deepcopy(dm)
tmp_dm.select(*select_list)
tmp_data = tmp_dm.get()
assert (select_list == tmp_data[10]._fields)
print("PASSED")

print("TYPES TEST")
tmp_dm = deepcopy(dm)
tmp_types = tmp_dm.get(types=True)
print(tmp_types)
# assert(select_list == tmp_data[10]._fields)
for key, val in tmp_types.items():
    assert (key[:-1] in str(val))
print("PASSED")

print("FILTER TEST")
for letter in aplhabet:
    notnull = df[df.str2.notnull()]
    filtered = notnull[notnull['str2'].str.contains(letter)]
    filtered_len = len(filtered)

    tmp_dm = deepcopy(dm)
    tmp_dm.filter('str2', op.contains, letter)
    tmp_data = tmp_dm.get()
    # print(letter)
    assert (len(filtered) == len(tmp_data))
print("PASSED")

print("SORT TEST")

csvreader = csv.reader(open("data10nonull_small.csv"))
dm = DataManipulation(csvreader)

df = pd.read_csv("data10nonull_small.csv")
df.reindex()

tmp_df = df.filter(['int1', 'str4', 'date1', 'str1', 'float2', 'str2'])
# tmp_df = tmp_df.dropna(axis=0)
result = tmp_df.sort_values(['int1', 'str4', 'date1'], ascending=[1, 0, 1])

header = list(result)
Row = namedtuple("Row", header)

tmp_dm = deepcopy(dm)
tmp_dm.select('int1', 'str4', 'date1', 'str1', 'float2', 'str2')

tmp_dm.sort('+int1', '-str4', '+date1')
tmp_data = tmp_dm.get()

assert (len(tmp_data) == len(result))

c = 0
for index, row in result.iterrows():
    my_row = Row._make(list(row))
    assert (my_row.str2 == tmp_data[c].str2)
    c += 1

print("PASSED")