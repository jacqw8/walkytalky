"""
returns a list ex. [{'day': 'Monday', 'beg': '12 to 13'}]
check if times are unique
"""

def check_cal(list1):
    list2 = list1.copy()
    for idx in range(len(list1)):
        for idx1 in range(idx+1, len(list1)):
            if list1[idx] == list1[idx1] and list1[idx1] in list2:
                list2.remove(list1[idx1])

    return list2