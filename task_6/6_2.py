import re

def print_list_string(st):
    list_st = st.split(', ')
    p = re.compile(r'[a-zA-Z]*fu$')
    for s in list_st:
        result_st = p.findall(s)
        if result_st:
            print(result_st[0])


if __name__ == "__main__":
    string = "fu, tofu, snafu, futz, fusillade, functional, discombobulated"
    print(string.split(', '))
    print_list_string(string)