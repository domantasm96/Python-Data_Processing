from collections import namedtuple
from datetime import datetime
from operator import attrgetter


class DataManipulation():
    def __init__(self, csvreader):
        self.header = next(csvreader)
        data_tuple = namedtuple('data_tuple', self.header)
        self.data = []
        self.types = dict()
        prevent_empty = []
        for line in csvreader:
            if any(line):
                for value in line:
                    if value == '':
                        value = '0'
                    prevent_empty.append(value)
                nrec = data_tuple._make(prevent_empty)
                prevent_empty = []
                self.data.append(nrec)

        get_float = {}
        get_date = {}
        for line in self.data:
            for name in line._fields:
                try:
                    int(getattr(line, name))
                    # print(name + " = " + getattr(line, name) + ": int")
                    self.types[name] = "int"
                except:
                    try:
                        float(getattr(line, name))
                        get_float[name] = True
                    except:
                        try:
                            datetime.strptime(getattr(line, name), '%Y-%m-%d')
                            get_date[name] = "date"
                            # self.types[name] = "date"
                        except:
                            try:
                                str(getattr(line, name))
                                self.types[name] = "str"
                            except:
                                pass
        for name in get_float:
            self.types[name] = 'float'
        for name in get_date:
            self.types[name] = 'date'

    def select(self, *args):
        try:
            data_tuple = namedtuple('data_tuple', args)
        except:
            print("Repeating arguments")
            raise KeyError
        for key in args:
            if key not in self.header:
                print("This argument is not included in the header")
                raise KeyError
        temp_list = []
        temp_tuple = []
        for line in self.data:
            for key in line._fields:
                if key in args:
                    temp_list.append(getattr(line, key))
            temp_tuple.append(data_tuple._make(temp_list))
            temp_list = []
        self.data = temp_tuple
        self.header = args

    def filter(self, column, operator, value):
        if column not in self.header:
            print("This argument is not included in the header")
            raise KeyError
        tuple_list = []
        for line in self.data:
            if self.types[column] == 'int':
                if operator(int(getattr(line, column)), value):
                    tuple_list.append(line)
            if self.types[column] == 'float':
                if operator(float(getattr(line, column)), value):
                    tuple_list.append(line)
            if self.types[column] == 'date':
                if operator(datetime.strptime(getattr(line, column)), value):
                    tuple_list.append(line)
            if self.types[column] == 'str':
                if operator(getattr(line, column), value):
                    tuple_list.append(line)
        self.data = tuple_list

    def sort(self, *args):
        check = []
        for value in args:
            if value in check:
                print('Repeated arguments')
                raise KeyError
            check.append(value)
        for key in args:
            if key[1:] not in self.header:
                print("This argument is not included in the header")
                raise KeyError
        for values in reversed(args):
            self.data.sort(key=attrgetter(values[1:]), reverse=False if values[0] == '+' else True)

    def get(self, types=False):
        if types:
            return self.types
        else:
            return self.data

    def save(self, csvwriter):
        temp = []
        for title in self.header:
            temp.append(title + " ")
        temp.append('\n')
        csvwriter.writerow(temp)
        temp = []
        for line in self.data:
            for values in line._fields:
                temp.append(getattr(line, values) + " ")
            csvwriter.writerow(temp)
            temp = []
