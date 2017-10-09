# bin/bash/python
"""Module s1513204"""
# -*- coding: utf-8 -*-
import copy
from collections import namedtuple
from datetime import date
from datetime import datetime
from operator import attrgetter
from pydoc import locate
import math


def set_types(self):
    """Module s1513204"""
    for line in self.data:
        tmp_line = []
        for col in line._fields:
            if self.types[col] != 'date':
                value_type = locate(self.types[col])
            else:
                value_type = date
            value = getattr(line, col)
            if value == '':
                value = math.inf
            else:
                if self.types[col] == 'date':
                    values_list = value.split('-')
                    value = value_type(int(values_list[0]), int(values_list[1]), \
                                       int(values_list[2]))
                else:
                    value = value_type(value)
            tmp_line.append(value)
        data_tuple = namedtuple('data_tuple', self.header)
        line = data_tuple._make(tmp_line)
        self.data_tmp.append(line)


class DataManipulation():
    """Module s1513204"""

    def __init__(self, csvreader):

        self.header = next(csvreader)
        data_tuple = namedtuple('data_tuple', self.header)
        self.data = []
        self.types = dict()
        self.data_tmp = []
        prevent_empty = []
        for line in csvreader:
            if any(line):
                for value in line:
                    if value == '':
                        value = ''
                    prevent_empty.append(value)
                nrec = data_tuple._make(prevent_empty)
                prevent_empty = []
                self.data.append(nrec)
        for line in csvreader:
            nrec = data_tuple._make(line)
            self.data.append(nrec)
        get_float = {}
        get_date = {}
        for line in self.data:
            for name in line._fields:
                try:
                    int(getattr(line, name))
                    self.types[name] = "int"
                except ValueError:
                    try:
                        float(getattr(line, name))
                        get_float[name] = True
                    except ValueError:
                        try:
                            datetime.strptime(getattr(line, name), '%Y-%m-%d')
                            get_date[name] = "date"
                        except ValueError:
                            str(getattr(line, name))
                            self.types[name] = "str"
        for name in get_float:
            self.types[name] = 'float'
        for name in get_date:
            self.types[name] = 'date'
        set_types(self)
        self.data = copy.deepcopy(self.data_tmp)

    def select(self, *args):
        """Module s1513204"""
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
            for i in range(0, len(args)):
                temp_list.append(getattr(line, args[i]))
            temp_tuple.append(data_tuple._make(temp_list))

            temp_list = []
        self.data = temp_tuple
        self.header = args

    def filter(self, column, operator, value):
        """Module s1513204"""
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
        """Module s1513204"""
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
        """Module s1513204"""
        if types:
            return self.types
        return self.data

    def save(self, csvwriter):
        """Module s1513204"""
        csvwriter.writerow(self.header)
        for line in self.data:
            csvwriter.writerow(line)
