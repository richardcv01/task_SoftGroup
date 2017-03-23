import types

print(type(len))

class PublicMeta(type):

    def __new__(Class, classname, superclasses, attributedict):
        new_dicattr = PublicMeta.rePrivat_Public(classname, attributedict)
        new_dicattr['do_things'] = PublicMeta.do_things
        new_dicattr['pretty_func'] = PublicMeta.pretty_func
        return type(classname, superclasses, new_dicattr)

    # Function rePrivat_Public return new dict where updated name privad attributes to public
    @staticmethod
    def rePrivat_Public(classname, attributedict):
        str_privat = '_' + classname + '__'
        end_Slices = len(classname) + 3
        for member_dic in attributedict:
            if (member_dic.startswith(str_privat)) and (not isinstance(attributedict[member_dic], types.FunctionType)):
                attributedict[member_dic[end_Slices:]] = attributedict[member_dic]
                attributedict.pop(member_dic)
        return attributedict

    def do_things(self):
        print(self.var)

    @staticmethod
    def pretty_func(self):
        print('Some useful message')


class A(metaclass=PublicMeta):
    __var = 12

    def __Met(self):
        pass
    def K(self):
        pass
    def __init__(self, x):
        self.x = x


if __name__ == '__main__':
    a = A(10)
    print(a.var)
    a.do_things()
    a.pretty_func()








#print(a.var)