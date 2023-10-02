import anvil.server
from routine_db import base_routine
from controllers.sort_controller import *
from controllers.time_controller import *
from controllers.course_controller import *


# Sending list of all courses to client-side


@anvil.server.callable
def get_all_courses():
    print("User at Generator's doorstep")
    sem_list = list(base_routine.keys())
    all_courses = []
    for i in range(8):
        sem = i+1
        all_courses.append(sem)
        if f"{sem}A" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}A"])):
                for time_steps in range(len(base_routine[f"{sem}A"][days])):
                    if not base_routine[f"{sem}A"][days][0][0] == ():
                        current_course = base_routine[f"{sem}A"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}A')
        if f"{sem}A1" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}A1"])):
                for time_steps in range(len(base_routine[f"{sem}A1"][days])):
                    if not base_routine[f"{sem}A1"][days][0][0] == ():
                        current_course = base_routine[f"{sem}A1"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}A1')
        if f"{sem}A2" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}A2"])):
                for time_steps in range(len(base_routine[f"{sem}A2"][days])):
                    if not base_routine[f"{sem}A2"][days][0][0] == ():
                        current_course = base_routine[f"{sem}A2"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}A2')
        if f"{sem}B" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}B"])):
                for time_steps in range(len(base_routine[f"{sem}B"][days])):
                    if not base_routine[f"{sem}B"][days][0][0] == ():
                        current_course = base_routine[f"{sem}B"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}B')
        if f"{sem}B1" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}B1"])):
                for time_steps in range(len(base_routine[f"{sem}B1"][days])):
                    if not base_routine[f"{sem}B1"][days][0][0] == ():
                        current_course = base_routine[f"{sem}B1"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}B1')
        if f"{sem}B2" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}B2"])):
                for time_steps in range(len(base_routine[f"{sem}B2"][days])):
                    if not base_routine[f"{sem}B2"][days][0][0] == ():
                        current_course = base_routine[f"{sem}B2"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}B2')
        if f"{sem}C" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}C"])):
                for time_steps in range(len(base_routine[f"{sem}C"][days])):
                    if not base_routine[f"{sem}C"][days][0][0] == ():
                        current_course = base_routine[f"{sem}C"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}C')
        if f"{sem}C1" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}C1"])):
                for time_steps in range(len(base_routine[f"{sem}C1"][days])):
                    if not base_routine[f"{sem}C1"][days][0][0] == ():
                        current_course = base_routine[f"{sem}C1"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}C1')
        if f"{sem}C2" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}C2"])):
                for time_steps in range(len(base_routine[f"{sem}C2"][days])):
                    if not base_routine[f"{sem}C2"][days][0][0] == ():
                        current_course = base_routine[f"{sem}C2"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}C2')
        if f"{sem}D" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}D"])):
                for time_steps in range(len(base_routine[f"{sem}D"][days])):
                    if not base_routine[f"{sem}D"][days][0][0] == ():
                        current_course = base_routine[f"{sem}D"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}D')
        if f"{sem}D1" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}D1"])):
                for time_steps in range(len(base_routine[f"{sem}D1"][days])):
                    if not base_routine[f"{sem}D1"][days][0][0] == ():
                        current_course = base_routine[f"{sem}D1"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}D1')
        if f"{sem}D2" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}D2"])):
                for time_steps in range(len(base_routine[f"{sem}D2"][days])):
                    if not base_routine[f"{sem}D2"][days][0][0] == ():
                        current_course = base_routine[f"{sem}D2"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}D2')
        if f"{sem}E" in sem_list:
            visited = []
            for days in range(len(base_routine[f"{sem}E"])):
                for time_steps in range(len(base_routine[f"{sem}E"][days])):
                    if not base_routine[f"{sem}E"][days][0][0] == ():
                        current_course = base_routine[f"{sem}E"][days][time_steps][0][0]
                        if current_course not in visited and not current_course == ():
                            visited.append(current_course)
                            all_courses.append(f'{current_course} {sem}E')
    return all_courses

# Generating default routine


@anvil.server.callable
def generate_default_routine(user_choice):
    print("Generating default routine for user")
    sections, courses = [], []
    dj_day, dj_course = [], []
    for items in user_choice:
        courses.append(items.split(' ')[0])
        sections.append(items.split(' ')[1])
    '''
    Creating blueprints
    '''
    final_routine = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    dummy_routine = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    final_time_list = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    comparison_list = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    overlap_list = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    overlap_days = {
        'Sat': False,
        'Sun': False,
        'Mon': False,
        'Tue': False,
        'Wed': False,
    }
    dj_msg = {
        'Sat': '',
        'Sun': '',
        'Mon': '',
        'Tue': '',
        'Wed': '',
    }
    '''
    Appending the courses while sorting them
    '''
    for section in range(len(sections)):
        for day in range(len(base_routine[sections[section]])):
            for course in range(len(base_routine[sections[section]][day])):
                if not base_routine[sections[section]][day][0][0] == ():
                    if courses[section] == base_routine[sections[section]][day][course][0][0]:
                        course_times = base_routine[sections[section]
                                                    ][day][course][0][1]
                        start_times = int(
                            "".join(course_times.split('-')[0].split(':')))
                        end_times = int(
                            "".join(course_times.split('-')[1].split(':')))
                        if day == 0:
                            final_routine['Sat'].append(
                                [f'{courses[section]} {sections[section]}', start_times])
                            Sort(final_routine['Sat'])
                            dummy_routine['Sat'].append(
                                [courses[section], start_times])
                            Sort(dummy_routine['Sat'])
                            final_time_list['Sat'].append(
                                [start_times, course_times])
                            R_sort(final_time_list['Sat'])
                            comparison_list['Sat'].append(
                                [start_times, end_times])
                            R_sort(comparison_list['Sat'])
                        elif day == 1:
                            final_routine['Sun'].append(
                                [f'{courses[section]} {sections[section]}', start_times])
                            Sort(final_routine['Sun'])
                            dummy_routine['Sun'].append(
                                [courses[section], start_times])
                            Sort(dummy_routine['Sun'])
                            final_time_list['Sun'].append(
                                [start_times, course_times])
                            R_sort(final_time_list['Sun'])
                            comparison_list['Sun'].append(
                                [start_times, end_times])
                            R_sort(comparison_list['Sun'])
                        elif day == 2:
                            final_routine['Mon'].append(
                                [f'{courses[section]} {sections[section]}', start_times])
                            Sort(final_routine['Mon'])
                            dummy_routine['Mon'].append(
                                [courses[section], start_times])
                            Sort(dummy_routine['Mon'])
                            final_time_list['Mon'].append(
                                [start_times, course_times])
                            R_sort(final_time_list['Mon'])
                            comparison_list['Mon'].append(
                                [start_times, end_times])
                            R_sort(comparison_list['Mon'])
                        elif day == 3:
                            final_routine['Tue'].append(
                                [f'{courses[section]} {sections[section]}', start_times])
                            Sort(final_routine['Tue'])
                            dummy_routine['Tue'].append(
                                [courses[section], start_times])
                            Sort(dummy_routine['Tue'])
                            final_time_list['Tue'].append(
                                [start_times, course_times])
                            R_sort(final_time_list['Tue'])
                            comparison_list['Tue'].append(
                                [start_times, end_times])
                            R_sort(comparison_list['Tue'])
                        elif day == 4:
                            final_routine['Wed'].append(
                                [f'{courses[section]} {sections[section]}', start_times])
                            Sort(final_routine['Wed'])
                            dummy_routine['Wed'].append(
                                [courses[section], start_times])
                            Sort(dummy_routine['Wed'])
                            final_time_list['Wed'].append(
                                [start_times, course_times])
                            R_sort(final_time_list['Wed'])
                            comparison_list['Wed'].append(
                                [start_times, end_times])
                            R_sort(comparison_list['Wed'])
    '''
    Converting course times back to their human readable format
    we did this before as well, nothing new..
    '''
    for day, info in final_routine.items():
        for readable_info in range(len(info)):
            final_routine[day][readable_info][1] = final_time_list[day][readable_info][1]
    '''
    Finally, checking for overlaps & printing the routine
    '''
    overlapped_courses_1 = []
    overlapped_courses_2 = []
    for day, time in comparison_list.items():
        for time_steps in range(len(time)):
            current_course = final_routine[day][time_steps][0]
            start_time, end_time = time[time_steps][0], time[time_steps][1]
            current_start_o, current_end_o = final_time_list[day][time_steps][1].split(
                '-')[0], final_time_list[day][time_steps][1].split('-')[1]
            if (time_steps > 0):
                for iterations in range(time_steps-1, -1, -1):
                    comparing_course = final_routine[day][iterations][0]
                    compare_start, compare_end = time[iterations][0], time[iterations][1]
                    compare_start_o, compare_end_o = final_time_list[day][iterations][1].split(
                        '-')[0], final_time_list[day][iterations][1].split('-')[1]
                    if compare_start <= start_time < compare_end:  # overlap detection
                        overlap_list[day].append([current_course, comparing_course, str(
                            CalculateOverlapTime(current_start_o, compare_end_o))])
                        if [comparing_course] not in overlapped_courses_1:
                            overlapped_courses_1.append([comparing_course])
                        if [current_course] not in overlapped_courses_2:
                            overlapped_courses_2.append(
                                [current_course])  # NEW !!
                        overlap_days[day] = True
            dummy_routine[day][time_steps] = final_routine[day][time_steps][0] + \
                ' ' + final_routine[day][time_steps][1]
        if overlap_days[day] == False:
            dj_day.append(day)
            dj_course.append(dummy_routine[day])
        else:
            for i in range(len(overlap_list[day])):
                overlap_list[day][i] = overlap_list[day][i][0] + ',' + \
                    overlap_list[day][i][1] + ' ' + \
                    overlap_list[day][i][2] + ' minutes'
            err_msg = overlap_list[day]
            dj_msg[day] = err_msg
            dj_day.append(day)
            dj_course.append(dummy_routine[day])
    print("Default routine:\n", final_routine)
    return dj_day, dj_course, dj_msg, final_routine, comparison_list, final_time_list, overlapped_courses_1, overlapped_courses_2

# Creating structures for calculation


@anvil.server.callable
def create_structures(fr, cl, ftl):
    '''
    creating blueprints to store the 'main-routine', 'comparison-list', 'final-time-list' & test-results to cross-check both ends of overlap
    '''
    # trial_routine_1, trial_routine_2, comp_list_1, comp_list_2, comp_list_2, fn_time_l_1, fn_time_l_2, test_res_1, test_res_2, dr_1, dr_2
    trial_routine_1 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    trial_routine_2 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }

    comp_list_1 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    comp_list_2 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }

    fn_time_l_1 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    fn_time_l_2 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }

    test_res_1 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    test_res_2 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }

    dr_1 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    dr_2 = {
        'Sat': [],
        'Sun': [],
        'Mon': [],
        'Tue': [],
        'Wed': [],
    }
    '''
    copying values to the blueprints
    '''
    for k, v in fr.items():
        for i in range(len(v)):
            trial_routine_1[k].append(v[i])
            trial_routine_2[k].append(v[i])

    for k, v in cl.items():
        for i in range(len(v)):
            comp_list_1[k].append(v[i])
            comp_list_2[k].append(v[i])

    for k, v in ftl.items():
        for i in range(len(v)):
            fn_time_l_1[k].append(v[i])
            fn_time_l_2[k].append(v[i])

    return trial_routine_1, trial_routine_2, comp_list_1, comp_list_2, fn_time_l_1, fn_time_l_2, test_res_1, test_res_2, dr_1, dr_2

# Generating updated routine (One for All)


@anvil.server.callable
def generate_updated_routine(trout, oc, cl, ftl, tres):
    print("Generating updated routine for user")
    trout, oc, cl, ftl = rem__ov__crs(trout, oc, cl, ftl)
    tres = copy_free_time_slots(cl, tres)
    copy_tres = {}
    for i in range(5):
        copy_tres[i] = tres[list(tres.keys())[i]]
    rec_crs_, curr_list_, cmp_list_, exception_list = find_alt_section(
        oc, copy_tres)
    trout, ftl = append_alt_crs(rec_crs_, trout, ftl)
    print("Updated routine:\n", trout)
    return trout, tres, cl
