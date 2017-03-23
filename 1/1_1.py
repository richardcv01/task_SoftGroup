def like(numbers: str, a_set: str, b_set: str):
    likes = 0
    number_list = numbers.split(' ')
    A_list = a_set.split(' ')
    B_list = b_set.split(' ')
    for x in number_list:
        if (x in A_list and x in B_list):
            pass
        elif x in A_list:
            likes +=1
        elif x in B_list:
            likes -=1
    return likes

if __name__ == '__main__':
    numbers = '1 4 10 20 1 11 12 100'
    a = '1 4 1 12 '
    b = '1 12 10 20 100'
    print(like(numbers, a, b))

