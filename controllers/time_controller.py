from controllers.sort_controller import *

'''
Function that counts overlap time
'''


def CalculateOverlapTime(t1, t2):
    hour1, minute1 = int(t1.split(':')[0]), int(t1.split(':')[1])
    hour2, minute2 = int(t2.split(':')[0]), int(t2.split(':')[1])
    min1, min2, min3 = 0, 0, 0
    for hrs in range(hour1, hour2+1):
        for mins in range(0, 60):
            if hour1 == hour2 and minute1 == minute2:
                minutes = 0
            elif mins >= minute1 and hrs == hour1:
                min1 += 1
            elif hour1 < hrs < hour2:
                min2 += 1
            elif mins < minute2 and hrs == hour2:
                min3 += 1
    minutes = min1 + min2 + min3
    return (minutes)


'''
Function to calculate available time-slots of a day
'''


def CalculateFreeTimeDay(l):
    time_range = []
    start_val, end_val = 830, 1730
    start_time, end_time = start_val, end_val
    # [i such that i belongs to length of courses] i.e 0->1->2->.. etc..
    for i in range(len(l)):
        course_start, course_end = l[i][0], l[i][1]
        # for all classes except for the last class
        if not course_end == end_val and i < len(l) - 1:
            # if that course has no-free-time before
            if course_start == start_time:
                start_time = course_end
            # if that course has free-time before
            elif course_start > start_time:
                checkpoint1, checkpoint2 = start_time, course_start
                time_range.append([checkpoint1, checkpoint2])
                start_time = course_end
            # handling duplicates
            elif i > 0 and course_start <= l[i-1][0] or course_end <= l[i-1][1]:
                start_time = l[i-1][1]
        # for last class or only class
        elif i == len(l) - 1:
            # if that course has no-free-time before & doesn't end at 17:30
            if course_start == start_time and course_end != end_time:
                checkpoint1, checkpoint2 = course_end, end_time
                time_range.append([checkpoint1, checkpoint2])
            # if that course has free-time before
            elif course_start > start_time:
                checkpoint1, checkpoint2 = start_time, course_start
                time_range.append([checkpoint1, checkpoint2])
                # & doesn't end at 17:30
                if course_end != end_time:
                    checkpoint3, checkpoint4 = course_end, end_time
                    time_range.append([checkpoint3, checkpoint4])
            # handling duplicates
            elif i > 0 and course_start <= l[i-1][0] or course_end <= l[i-1][1]:
                checkpoint1, checkpoint2 = l[i-1][1], end_time
                time_range.append([checkpoint1, checkpoint2])
            elif start_time > course_start and course_end != end_time:
                checkpoint1, checkpoint2 = course_end, end_time
                time_range.append([checkpoint1, checkpoint2])
    R_sort(time_range)
    return (time_range)


'''
extending that to calculate free-time-slots of the whole week
'''
test_results = {
    'Sat': [],
    'Sun': [],
    'Mon': [],
    'Tue': [],
    'Wed': []
}


def CalculateFreeTimeWeek(week):
    for day, times in week.items():
        test_results[day] = CalculateFreeTimeDay(times)
