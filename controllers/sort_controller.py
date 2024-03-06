'''
functions to sort courses using time_steps
'''


def Sort(sub_li):
    sub_li.sort(key=lambda x: x[1])
    return sub_li


def R_sort(sub_li):
    sub_li.sort(key=lambda x: x[0])
    return sub_li
