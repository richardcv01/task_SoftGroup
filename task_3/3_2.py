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


with open('json.txt', 'r') as file:
    print( json_load(file))







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


class ConverterFabric(AbsConverterFabric):
 '''Complete the code'''