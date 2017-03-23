def fine_print(n:int):

    long = lambda n: len(str(n)) - 1
    probel_count = 10

    sep_n = probel_count + long(n)
    sep_n_o = probel_count + long(oct(n))
    sep_n_X = probel_count + long(hex(n))

    for x in range(1, n+1):

        sep = ' ' * (sep_n - long(x))
        sepo = ' '* (sep_n_o - long(oct(x)))
        sepX = ' '* (sep_n_X - long(hex(x)))

        print('{0}{1}'.format(x, sep), '{0:o}{1}'.format(x, sepo),  '{0:X}{1}'.format(x, sepX), '{0:b}'.format(x)  )


if __name__ == '__main__':
     fine_print(13)

