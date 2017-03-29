import cgi
import html

def html_p(s: str) -> str:
    new_s = '<p>{}<p>'.format(s)
    return new_s

def html_b(s: str) -> str:
    new_s = '<b>{}<b>'.format(s)
    return new_s

def html_i(s: str) -> str:
    new_s = '<i>{}<i>'.format(s)
    return new_s

def html_u(s: str) -> str:
    new_s = '<u>{}<u>'.format(s)
    return new_s




def writer(html_escap):
    dicfun = {'p':html_p, 'b':html_b, 'i':html_i, 'u':html_u}
    def writer(func):
        def wrapped(*args, **kwargs):
            res = func(*args, **kwargs)
            for key in html_escap:
                if key in dicfun :
                    res = dicfun[key](res)
            res = (func(res))
            return res
        return wrapped
    return writer

@writer('')
def html_printer(s):
    new_s = html.escape(s)
    return new_s

if __name__ == "__main__":
    print(html_printer("I'll give you +++ cash for this -> stuff."))