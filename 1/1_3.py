def decorator(fun):

    def inner(*args, **kwargs):
        res = None
        try:
            fun(*args, **kwargs)
        except Exception as e:
            print('Exception occurred in {0}: '.format(fun.__name__), e)
            print('Input args:' , ' '.join(map(str,args)))
            print('Input kwargs:' ,kwargs)
            print(res)
        else:
            res =  fun(*args, **kwargs)
        finally:
            return res

        #print(res)


    return inner

if __name__ == '__main__':

    @decorator
    def function(x, y, **kwargs):
        return x / y

    function(10, 'f', op='division', base=10)
    function(10, 2, op='division', base=10)



