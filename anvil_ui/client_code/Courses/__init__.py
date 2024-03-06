from ._anvil_designer import CoursesTemplate
from anvil import *
import anvil.server
import anvil.js
import anvil.media


class Courses(CoursesTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        global course_count
        course_count = 0

        count_label_msg = f"Selected: {course_count}"
        self.selected_count_label = Label(text=count_label_msg, font_size='16')

        self.load_courses()

    def update_selected_count(self):
        course_count = len(self.checked_values)
        count_label_msg = f"Selected: {course_count}"
        self.selected_count_label.text = count_label_msg
        self.count_panel.clear()
        self.count_panel.add_component(self.selected_count_label)

    def on_resize(self, **event_args):
        pass

    def load_courses(self):
        init_label = Label(
            text='List of all courses from Semester 1-8', font_size='20', bold=True)
        self.content_panel.add_component(init_label)

        self.count_panel = ColumnPanel(width="auto")
        self.count_panel.add_component(self.selected_count_label)

        self.content_panel.add_component(self.count_panel)

        self.checked_values = set()
        self.generate.visible = False

        semesters = range(1, 9)
        courses_by_semester = [[] for _ in semesters]
        current_semester = None
        items = anvil.server.call('get_all_courses')
        for item in items:
            if isinstance(item, int):
                current_semester = item
                continue
            if current_semester is not None:
                courses_by_semester[current_semester - 1].append(item)

        layout = FlowPanel(width="100%", spacing=(50, 0))

        columns = [ColumnPanel(width="auto") for _ in range(8)]
        for i, courses in enumerate(courses_by_semester):
            label = Label(text=f"Semester {i+1}",
                          font_size="16", align="center", bold=True)
            sem_title_panel = ColumnPanel(border="1px solid #90EE90")
            sem_title_panel.add_component(label)
            columns[i].add_component(sem_title_panel)
            course_title_panel = ColumnPanel(border="1px solid #90EE90")
            columns[i].add_component(course_title_panel)
            for course in courses:
                checkbox = anvil.CheckBox(text=course)
                checkbox.set_event_handler("change", self.check_box_changed)
                # columns[i].add_component(checkbox)
                course_title_panel.add_component(checkbox)

        for column in columns:
            layout.add_component(column)

        self.content_panel.add_component(layout)

    def check_box_changed(self, **event_args):
        sender = event_args['sender']

        if sender.checked:
            self.checked_values.add(sender.text)
        else:
            self.checked_values.discard(sender.text)

        self.update_selected_count()

        self.generate.visible = len(self.checked_values) > 0

    def get_total_courses(self):
        default_routine_init_label = Label(
            text="### Before analyzing ###", bold=True)
        global default_total_list
        default_total_list = []
        for checkbox_value in self.checked_values:
            default_total_list.append(checkbox_value)

        courses_str = ", ".join(default_total_list)

        courses_label_msg = f"Courses: {courses_str}"
        courses_label = Label(text=courses_label_msg)

        default_total_count = len(default_total_list)

        courses_count_msg = f"Total Courses = {default_total_count}"
        courses_count = Label(text=courses_count_msg)

        merged_list = overlapped_courses_1 + overlapped_courses_2
        output_list = []

        for sublist in merged_list:
            for item in sublist:
                if item not in output_list:
                    output_list.append(item)

        output_string = ', '.join(output_list)
        ov_msg_str = f"Overlapped Courses: {output_string}"

        ov_msg_label = Label(text=ov_msg_str)

        total_ov_crs = len(output_list)
        ov_crs_cnt_str = f"Total Overlapped Courses = {total_ov_crs}"
        ov_crs_cnt_label = Label(text=ov_crs_cnt_str)

        actual_crs_cnt = default_total_count - total_ov_crs
        actual_crs_str = f"Actual Courses = {actual_crs_cnt}"
        actual_crs_label = Label(text=actual_crs_str)

        global before_update_info_panel
        before_update_info_panel = ColumnPanel(
            border="1px solid black", width="100%")
        before_update_info_panel.add_component(default_routine_init_label)
        before_update_info_panel.add_component(courses_label)
        before_update_info_panel.add_component(courses_count)
        before_update_info_panel.add_component(ov_msg_label)
        before_update_info_panel.add_component(ov_crs_cnt_label)
        before_update_info_panel.add_component(actual_crs_label)

    def generate_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.content_panel.clear()
        self.load_responsive_routine()
        self.back_to_courses.visible = True
        self.generate.visible = False

    def load_responsive_routine(self):
        global unique_checked_values, dj_day, dj_course, dj_msg, final_routine, comparison_list, final_time_list, overlapped_courses_1, overlapped_courses_2
        dj_day, dj_course, dj_msg, final_routine, comparison_list, final_time_list, overlapped_courses_1, overlapped_courses_2 = anvil.server.call(
            'generate_default_routine', list(self.checked_values))

        self.get_total_courses()

        routine_panel = ColumnPanel(border="1px solid black", width="100%")
        routine_panel.tag.style = "resize: both; overflow: auto; border-collapse:collapse;"

        for day, course in zip(dj_day, dj_course):
            day_panel = FlowPanel()
            day_panel.width = "100%"
            day_panel.tag.style = "display: flex; border-bottom: 1px solid black;"

            day_label = Label(border="1px solid black", text=day,
                              width='80px', align="left", font_size="3", bold=True)
            day_label.tag.style = "border-right: 1px solid black;"
            day_panel.add_component(day_label)

            for c in course:
                course_panel = ColumnPanel(width="100%")
                course_panel.tag.style = "flex: 1;"
                
                q_course = f'{c.split()[0]} {c.split()[1]}'

                overlap = False
                for overlap_info in dj_msg[day]:
                    if q_course in overlap_info:
                        overlap = True
                        break

                if overlap:
                    course_panel.border = "1px solid red"
                else:
                    course_panel.border = "1px solid black"

                label = Label(text=c, align="center", font_size="3")
                course_panel.add_component(label)

                day_panel.add_component(course_panel)

            routine_panel.add_component(day_panel)

        routine_panel.tag.style = "resize: both; overflow: auto;"

        err_panel = ColumnPanel(border="1px solid black", width="80%")

        for key, val in dj_msg.items():
            if key in dj_day and dj_msg[key] != '':
                raw_msg = str(dj_msg[key])
                stripped_msg = raw_msg.replace('[', '')
                stripped_msg = stripped_msg.replace(']', '')
                final_msg = f'{key}: {stripped_msg}'
                ov_msg = Label(text=final_msg, align='left',
                               font_size="5", foreground="red")
                err_panel.add_component(ov_msg)

        if len(err_panel.get_components()) == 0:
            h_label = Label(text='Reports', align='left',
                            font_size="5", bold=True)
            h_msg = "You're routine is all set."
            healthy_label = Label(text=h_msg, align='left', font_size="5")
            report_section = ColumnPanel()
            report_section.add_component(h_label)
            report_section.add_component(healthy_label)
        else:
            h_label = Label(text='Overlaps', align='left',
                            font_size="5", bold=True)
            report_section = ColumnPanel()
            report_section.add_component(h_label)
            report_section.add_component(err_panel)
            fix_button = Button(text='Fix Routine')
            report_section.add_component(fix_button)
            fix_button_callback = lambda **event_args: self.fix_button_click(
                final_routine)
            fix_button.set_event_handler('click', fix_button_callback)

        self.checked_values = set()

        container_panel = ColumnPanel()
        container_panel.add_component(routine_panel)
        container_panel.add_component(report_section)
        self.content_panel.clear()
        self.content_panel.add_component(container_panel)

    def get_new_routine_info(self, schedule):
        global model_info_panel
        new_routine_values = []
        missing_courses = []
        for day in schedule:
            for item in schedule[day]:
                if item[0] not in new_routine_values:
                    new_routine_values.append(item[0])

        new_courses_str = ", ".join(new_routine_values)

        new_courses_label_msg = f"Courses: {new_courses_str}"
        new_courses_label = Label(text=new_courses_label_msg)

        missing_courses = [course for course in default_total_list if course.split(
        )[0] not in [c.split()[0] for c in new_routine_values]]
        if missing_courses != []:
            missing_courses_str = ", ".join(missing_courses)
            missing_courses_label_msg = f"Missing Courses: {missing_courses_str}"
            missing_courses_label = Label(
                text=missing_courses_label_msg, foreground="red")

        new_total_count = len(default_total_list) - len(missing_courses)
        new_courses_count_msg = f"Total Courses = {new_total_count}"
        new_crs_count_label = Label(text=new_courses_count_msg)

        model_info_panel = ColumnPanel(border="1px solid black", width="100%")
        model_info_panel.clear()
        model_info_panel.add_component(new_courses_label)
        if missing_courses != []:
            model_info_panel.add_component(missing_courses_label)
        model_info_panel.add_component(new_crs_count_label)
        self.content_panel.add_component(model_info_panel)

    def fix_button_click(self, final_routine, **event_args):
        self.content_panel.clear()

        self.content_panel.add_component(before_update_info_panel)

        trial_routine_1, trial_routine_2, comp_list_1, comp_list_2, fn_time_l_1, fn_time_l_2, test_res_1, test_res_2, dr_1, dr_2 = anvil.server.call(
            'create_structures', final_routine, comparison_list, final_time_list)

        trial_routine_1, test_res_1, comp_list_1 = anvil.server.call(
            'generate_updated_routine', trial_routine_1, overlapped_courses_1, comp_list_1, fn_time_l_1, test_res_1)

        model_1_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(model_1_panel)

        model_1_label = Label(
            text='Updated Routine from 1st Model', align='left', bold=True)
        model_1_panel.add_component(model_1_label)

        self.get_updated_routine(trial_routine_1, model_1_panel)
        self.get_new_routine_info(trial_routine_1)

        separator_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(separator_panel)

        trial_routine_2, test_res_2, comp_list_2 = anvil.server.call(
            'generate_updated_routine', trial_routine_2, overlapped_courses_2, comp_list_2, fn_time_l_2, test_res_2)

        model_2_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(model_2_panel)

        model_2_label = Label(
            text='Updated Routine from 2nd Model', align='left', bold=True)
        model_2_panel.add_component(model_2_label)

        self.get_updated_routine(trial_routine_2, model_2_panel)
        self.get_new_routine_info(trial_routine_2)

    def get_updated_routine(self, routine, c_panel):
        updated_data_row_panel = DataRowPanel()

        for day, courses in routine.items():
            day_panel = FlowPanel(width="100%")

            day_label = Label(border="1px solid black", text=day,
                              width='80px', align="left", font_size="3", bold=True)
            day_label.tag.style = "border-right: 1px solid black;"
            day_panel.add_component(day_label)

            for course in courses:
                course_panel = ColumnPanel(
                    border="1px solid black", width="100%")
                course_panel.tag.style = "flex: 1;"

                label = Label(
                    text=f"{course[0]} {course[1]}", align="center", font_size="3")
                course_panel.add_component(label)

                day_panel.add_component(course_panel)

            updated_data_row_panel.add_component(day_panel)

        c_panel.add_component(updated_data_row_panel)

    def back_to_courses_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.back_to_courses.visible = False
        self.content_panel.clear()
        self.count_panel.clear()
        self.selected_count_label.text = "Selected: 0"
        self.load_courses()
