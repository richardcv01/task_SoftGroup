class A(type):
    pass

class B(A):
    pass

class C(A):
    pass

class D(B):
    pass

class E(D, B):
    pass

class F(C):
    pass

class G(C):
    pass

class MetaMRO(type):
    def mro(cls):
        return (cls, F, E, G, D, C, B, A, type, object)

class H(F, E, G, metaclass = MetaMRO):
    pass

if __name__ == '__main__':
    print(H.__mro__)

