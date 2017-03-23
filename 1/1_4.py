def filer_func(emails):


    filtername = lambda ls:all([True if x.isdigit() or x.isalpha() or x=='_' else False for x in ls[:ls.find('@')]])
    filterdomen = lambda ls: all(True if len(x)>=2 else False for x in ls[ls.find('@')+1:].split('.'))


    objemail = filter(filtername, emails)
    emails = list(filter(filterdomen, objemail))
    emails.sort()

    return emails



if __name__ == '__main__':
    emails = ['1abc@gmail.com.ua', '*@ank.com',
     '_ny@us.gov.us', 'z@b.kk', 'zdddddddddddb.kk', 'aroma@com.ua.ua.kom.us']

    print(filer_func(emails))
