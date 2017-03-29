from abc import ABC, abstractmethod
import csv
import json
import collections as col

def csv_load(file: object) -> str:
    reader = csv.reader(file)
    stRes = ''
    listRes = []
    for row in reader:
        row = ''.join(row).split(';')
        stRes = stRes + ' '.join(row)
        listRes.append(' '.join(row))
    count = len(listRes)
    i = 0
    for i in range(0, count-1):
        listRes[i] = listRes[i] + '\n'
    stRes = ''.join(listRes)
    return stRes


def csv_save(s: str, file: object) -> None:
    Ls_line = s.split('\n')
    LsRes = [s.replace(' ', ';') for s in Ls_line]
    StRes = '\n'.join(LsRes).replace("'", '"')
    file.write(StRes)

def json_load(file: object) -> str:
    dicOrd = json.load(file, object_pairs_hook=col.OrderedDict)
    stRes = ""
    listRes = dicOrd["rows"]
    count = len(listRes)
    stRes = "\n".join(listRes)
    return stRes



def json_save(s: str, file: object) -> None:
    St = s.split("\n")
    DicOrder = col.OrderedDict()
    DicOrder["rows"] = St
    file.write(str(dict(DicOrder)).replace("'", '"'))


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
    dict_load = {'csv': csv_load, 'json':json_load}
    dict_save = {'csv': csv_save, 'json':json_save}
    class Converter(AbstractConverter):
        pass

    def create_converter(self, _from: str, _to: str) -> object:
        self._from = _from
        self._to = _to
        ConverterFabric.Converter = type('Converter', (),
                                         {'load':ConverterFabric.dict_load[self._from]
            , 'save':ConverterFabric.dict_save[self._to]})
        obj = ConverterFabric.Converter
        return obj



if __name__ == '__main__':

    fab = ConverterFabric()
    converter1 = fab.create_converter('csv', 'json')
    converter2 = fab.create_converter('json', 'csv')

    with open('csv.txt', 'r') as file:
        result = converter1.load(file)
        print(result,'1')
    print()


    with open('json.txt', 'w') as file:
        converter1.save(result, file)

    with open('json.txt', 'r') as file:
        result = converter2.load(file)
        print(result, '2')

    with open('csv.txt', 'w') as file:
        converter2.save(result, file)


