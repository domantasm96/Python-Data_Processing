import csv
import operator
from DataManipulation import DataManipulation

csvreader = csv.reader(open('input00.csv'))
dm = DataManipulation(csvreader)
dm.select('vardas', 'pavarde', 'amzius')
dm.filter('amzius', operator.ge, 18)
# dm.filter('vardas', operator.eq, 'Domantas')
dm.sort('+amzius', '-vardas', '+pavarde')
data = dm.get()
types = dm.get(types=True)
print(data)
print(types)
# csvfilew = open()
csvwriter = csv.writer(open('output01.csv', 'w'), lineterminator='\n')
dm.save(csvwriter)
