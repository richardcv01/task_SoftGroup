from abc import ABC, abstractmethod
import csv
import json
import collections as col

def csv_load(file: object) -> str:
    reader = csv.reader(file)
    stRes = ''
    for row in reader:
        row = ''.join(row).split(';')
        stRes = stRes + ' '.join(row) + '\n'
    return stRes


def csv_save(s: str, file: object) -> None:
    s = 'Joe Doe Gree 77\nJoe Doe Gree 77'
    Ls_line = s.split('\n')
    LsRes = [s.replace(' ', ';') for s in Ls_line]
    StRes = '\n'.join(LsRes)
    file.write(StRes)



def json_load(file: object) -> str:
    dicOrd = json.load(file, object_pairs_hook=col.OrderedDict)
    stRes = ''
    for dicelement in dicOrd.values():
        st = '\n'.join(dicelement)
        stRes = stRes + '\n' + st
    return  stRes





def json_save(s: str, file: object) -> None:
 '''Complete the code'''


class AbsConverterFabric(ABC):
    @abstractmethod
    def create_converter(self, _from: str, _to: str) -> object:
        raise NotImplemented


class AbstractConverter(ABC):
    @abstractmethod
    def load(self, file: object) -> str:
        raise NotImplemented

    @abstractmethod
    def save(self, s: str, file: object) -> object:
        raise NotImplemented


class Converter(AbstractConverter):
    def __init__(self, _from: str, _to: str):
        self._from = _from
        self._to = _to

    def load(self, file: object) -> str:
        StRes = ''
        if self._from == 'csv':
            StRes = csv_load(file)
        elif self._from == 'json':
            StRes = json_load(file)
        return StRes

    def save(self, s: str, file: object) -> object:
        return file


class ConverterFabric(AbsConverterFabric):




    def create_converter(self, _from: str, _to: str) -> object:
        T = Converter(_from, _to)
        return T


fab = ConverterFabric()
con1 = fab.create_converter('csv', 'json')

with open('csv.txt', 'r') as file:
    print(con1.load(file))