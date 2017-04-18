import re

def print_list_string(st):
    list_st = st.split(', ')
    p = re.compile(r'^[a-zA-Z]*foo[a-zA-Z]*$|foster')
    for s in list_st:
        result_st = p.findall(s)
        if result_st:
            print(result_st[0])


if __name__ == "__main__":
    string = "afoot, catfoot, dogfoot, fanfoot, foody, foolery, foolish, foster, footage, foothot, footle, " \
             "footpad, footway, hotfoot, jawfoot, mafoo, nonfood, padfoot, prefool, sfoot, unfool, " \
             "Atlas, Aymoro, Iberic, Mahran, Ormazd, Silipan, altered, chandoo, crenel , crooked, fardo, " \
             "folksy, forest, hebamic, idgah, manlike, marly, palazzo, sixfold, tarrock, unfold"
    print(string.split(', '))
    print_list_string(string)
