from routine_db import base_routine
from controllers.sort_controller import *
from controllers.time_controller import *


def rem__ov__crs(routine, ov_crs_list, comp_list_, fn_time_list_):
    for day, val in routine.items():
        removing_crs_ = []
        for i in range(len(val)):
            curr_slot_, curr_crs_ = val[i], val[i][0]
            for j in range(len(ov_crs_list)):
                if curr_crs_ == ov_crs_list[j][0]:
                    removing_crs_.append(curr_slot_)
        for slots in removing_crs_:
            for k in range(len(routine[day])):
                if routine[day][k] == slots:
                    fr_rmv_ = routine[day][k]
                    cl_rmv_ = comp_list_[day][k]
                    ftl_rmv_ = fn_time_list_[day][k]
            routine[day].remove(fr_rmv_)
            comp_list_[day].remove(cl_rmv_)
            fn_time_list_[day].remove(ftl_rmv_)
    return routine, ov_crs_list, comp_list_, fn_time_list_


def copy_free_time_slots(routine, routine_copy):
    CalculateFreeTimeWeek(routine)
    for k, v in test_results.items():
        routine_copy[k] = []
        for i in range(len(v)):
            routine_copy[k].append(v[i])
    return routine_copy


def find_alt_section(ov_crs_list, free_time_list):
    rec_crs_ = {}
    curr_list_, cmp_list_ = [], []
    exception_list = []
    course_sections = {}  # Maintain a dictionary of course names and their sections
    for key, value in base_routine.items():
        for i in range(len(value)):  # track of day
            curr_day = value[i]
            for j in range(len(curr_day)):
                if curr_day[j][0] != ():
                    curr_crs, curr_time, curr_sec = curr_day[j][0][0], curr_day[j][0][1], key
                    curr_st_, curr_end_ = int(''.join(curr_time.split(
                        '-')[0].split(':'))), int(''.join(curr_time.split('-')[1].split(':')))
                    curr_tar_ = curr_crs + ' ' + curr_sec

                    # Check if the same course's other section is already present
                    if curr_crs in course_sections:
                        if curr_sec in course_sections[curr_crs]:
                            continue

                    # Add the course-section pair to the current list and dictionary
                    curr_list_.append(curr_tar_)
                    if curr_crs not in course_sections:
                        course_sections[curr_crs] = set()
                    course_sections[curr_crs].add(curr_sec)

                    for OCs in range(len(ov_crs_list)):
                        for oc in ov_crs_list[OCs]:
                            ov_crs, ov_sec = oc.split(' ')[0], oc.split(' ')[1]
                            if curr_crs == ov_crs and curr_sec != ov_sec:
                                for d, Ts in free_time_list.items():
                                    for t in range(len(Ts)):
                                        if free_time_list[d][t] != None:
                                            free_time_st_, free_time_end_ = int(
                                                free_time_list[d][t][0]), int(free_time_list[d][t][1])
                                            if d == i:
                                                if curr_st_ >= free_time_st_ and curr_end_ <= free_time_end_:
                                                    curr_tar_ = curr_crs + ' ' + curr_sec
                                                    cmp_list_.append(curr_tar_)
                                                    if curr_st_ == free_time_st_ and curr_end_ == free_time_end_:
                                                        # print('Perfect fit:', d, curr_tar_, free_time_list[d][t])
                                                        free_time_list[d].remove(
                                                            free_time_list[d][t])
                                                    else:
                                                        # print('Loose fit:', d, curr_crs, curr_sec, curr_st_, curr_end_, curr_tar_, free_time_list[d][t], [curr_end_, free_time_end_])
                                                        if curr_st_ > free_time_st_ and curr_end_ == free_time_end_:
                                                            free_time_list[d][t] = [
                                                                free_time_st_, curr_st_]
                                                        elif curr_st_ > free_time_st_ and curr_end_ < free_time_end_:
                                                            free_time_list[d][t] = [
                                                                free_time_st_, curr_st_]
                                                            free_time_list[d].append(
                                                                [curr_end_, free_time_end_])
                                                    break
    '''
    identifying recommended courses
    '''
    # For each courses in CountRecommend[course] and their counts
    for Cs in cmp_list_:
        fn_cnt = 0
        print("Comparing count..", Cs, cmp_list_.count(Cs), curr_list_.count(Cs))
        if cmp_list_.count(Cs) == curr_list_.count(Cs):
            rec_crs_[Cs] = True
        recs_list = list(rec_crs_.keys())
        for w in range(len(recs_list)):
            print("Finding duplicates..", w)
            if Cs.split(' ')[0] in recs_list[w].split(' ')[0]:
                fn_cnt += 1
        if fn_cnt > 1:
            del rec_crs_[Cs]
            print("Deleting duplicates..", Cs)
    print("Final Recommendation:\n", rec_crs_)
    return rec_crs_, curr_list_, cmp_list_, exception_list
# Adding updated courses


def append_alt_crs(rec__crs__, routine, ftl):
    '''
    appending recommended-courses to the routine
    '''
    print("Appending alternate courses..")
    # For every courses marked as Recommended
    for k in rec__crs__.keys():
        # take that instance of course and section
        ap_crs_, ap_sec_ = k.split(' ')[0], k.split(' ')[1]
        # for each section and days in base__routine__
        for sec, val in base_routine.items():
            # for every course in each day
            for v in range(len(val)):
                # if course-slot is not empty and recommended course's section matches base__routine's section
                if not val[v][0][0] == () and ap_sec_ == sec:
                    # for each course in every day
                    for c in range(len(val[v])):
                        # take current instance of base__routine's course and time
                        br_crs_, br_time_ = val[v][c][0][0], val[v][c][0][1]
                        # split the time into start and end time
                        br_st_, br_end_ = int(''.join(br_time_.split(
                            '-')[0].split(':'))), int(''.join(br_time_.split('-')[1].split(':')))
                        # if recommended course matches base__routine's course
                        if ap_crs_ == br_crs_:
                            # whichever day matches append that course to model's final_routine's day and sort the values
                            if v == 0:
                                # Check if the new course overlaps with any existing courses in this day
                                overlaps = False
                                for existing_course in routine['Sat']:
                                    existing_time = existing_course[1]
                                    existing_st, existing_end = int(''.join(existing_time.split('-')[0].split(':'))), int(
                                        ''.join(existing_time.split('-')[1].split(':')))
                                    if br_end_ > existing_st and existing_end > br_st_:
                                        overlaps = True
                                        break
                                if not overlaps:
                                    routine['Sat'].append(
                                        [f'{br_crs_} {sec}', br_time_])
                                    ftl['Sat'].append([br_st_, br_time_])
                                    R_sort(ftl['Sat'])
                            if v == 1:
                                # Check if the new course overlaps with any existing courses in this day
                                overlaps = False
                                for existing_course in routine['Sun']:
                                    existing_time = existing_course[1]
                                    existing_st, existing_end = int(''.join(existing_time.split('-')[0].split(':'))), int(
                                        ''.join(existing_time.split('-')[1].split(':')))
                                    if br_end_ > existing_st and existing_end > br_st_:
                                        overlaps = True
                                        break
                                if not overlaps:
                                    routine['Sun'].append(
                                        [f'{br_crs_} {sec}', br_time_])
                                    ftl['Sun'].append([br_st_, br_time_])
                                    R_sort(ftl['Sun'])
                            if v == 2:
                                # Check if the new course overlaps with any existing courses in this day
                                overlaps = False
                                for existing_course in routine['Mon']:
                                    existing_time = existing_course[1]
                                    existing_st, existing_end = int(''.join(existing_time.split('-')[0].split(':'))), int(
                                        ''.join(existing_time.split('-')[1].split(':')))
                                    if br_end_ > existing_st and existing_end > br_st_:
                                        overlaps = True
                                        break
                                if not overlaps:
                                    routine['Mon'].append(
                                        [f'{br_crs_} {sec}', br_time_])
                                    ftl['Mon'].append([br_st_, br_time_])
                                    R_sort(ftl['Mon'])
                            if v == 3:
                                # Check if the new course overlaps with any existing courses in this day
                                overlaps = False
                                for existing_course in routine['Tue']:
                                    existing_time = existing_course[1]
                                    existing_st, existing_end = int(''.join(existing_time.split('-')[0].split(':'))), int(
                                        ''.join(existing_time.split('-')[1].split(':')))
                                    if br_end_ > existing_st and existing_end > br_st_:
                                        overlaps = True
                                        break
                                if not overlaps:
                                    routine['Tue'].append(
                                        [f'{br_crs_} {sec}', br_time_])
                                    ftl['Tue'].append([br_st_, br_time_])
                                    R_sort(ftl['Tue'])
                            if v == 4:
                                # Check if the new course overlaps with any existing courses in this day
                                overlaps = False
                                for existing_course in routine['Wed']:
                                    existing_time = existing_course[1]
                                    existing_st, existing_end = int(''.join(existing_time.split('-')[0].split(':'))), int(
                                        ''.join(existing_time.split('-')[1].split(':')))
                                    if br_end_ > existing_st and existing_end > br_st_:
                                        overlaps = True
                                        break
                                if not overlaps:
                                    routine['Wed'].append(
                                        [f'{br_crs_} {sec}', br_time_])
                                    ftl['Wed'].append([br_st_, br_time_])
                                    R_sort(ftl['Wed'])
    '''
    Converting time to human-readable format
    '''
    for day, time in routine.items():
        for time_steps in range(len(time)):
            current_course, current_time = routine[day][time_steps][0], int(
                ''.join(routine[day][time_steps][1].split('-')[0].split(':')))
            routine[day][time_steps][1] = current_time
        Sort(routine[day])

    for day, time in routine.items():
        for time_steps in range(len(time)):
            proper_time = ftl[day][time_steps][1]
            routine[day][time_steps][1] = proper_time

    return routine, ftl
