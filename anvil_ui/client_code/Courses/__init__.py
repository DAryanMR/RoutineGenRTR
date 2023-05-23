from ._anvil_designer import CoursesTemplate
from anvil import *
import anvil.server
import anvil.js
import anvil.media


class Courses(CoursesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # define global course_count
        global course_count
        # Set course_count default 0
        course_count = 0

        # Set count label
        count_label_msg = f"Selected: {course_count}"
        self.selected_count_label = Label(text=count_label_msg, font_size='16')

        # Call the load_courses method on initialization
        self.load_courses()

    def update_selected_count(self):
        course_count = len(self.checked_values)
        count_label_msg = f"Selected: {course_count}"
        self.selected_count_label.text = count_label_msg
        self.count_panel.clear()
        self.count_panel.add_component(self.selected_count_label)

    def on_resize(self, **event_args):
        # Code for handling resize event goes here
        pass

    def load_courses(self):
        init_label = Label(
            text='List of all courses from Semester 1-8', font_size='20', bold=True)
        self.content_panel.add_component(init_label)

        # Add count label to count_panel
        self.count_panel = ColumnPanel(width="auto")
        self.count_panel.add_component(self.selected_count_label)

        # # Create the selected_count_label and add it to the content_panel
        # # self.selected_count_label = Label(text="Selected: 0", font_size='16')
        self.content_panel.add_component(self.count_panel)

        # Create an empty list to store the values of checked checkboxes
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
        # Get the sender checkbox using the 'sender' key in the event_args dictionary
        sender = event_args['sender']

        if sender.checked:
            self.checked_values.add(sender.text)
        else:
            self.checked_values.discard(sender.text)

        # # Update the selected_count_label with the number of checked boxes
        self.update_selected_count()

        # Set the visibility of the button based on whether a checkbox is checked
        self.generate.visible = len(self.checked_values) > 0

    def get_total_courses(self):
        default_routine_init_label = Label(
            text="### Before analyzing ###", bold=True)
        global default_total_list
        default_total_list = []
        for checkbox_value in self.checked_values:
            default_total_list.append(checkbox_value)

        # Convert the list to a string with comma-separated values
        courses_str = ", ".join(default_total_list)

        # Create a label widget with the formatted string
        courses_label_msg = f"Courses: {courses_str}"
        courses_label = Label(text=courses_label_msg)
        # print(courses_label.text)

        # Get length of default_total_list
        default_total_count = len(default_total_list)

        # Create a label widget for default count
        courses_count_msg = f"Total Courses = {default_total_count}"
        courses_count = Label(text=courses_count_msg)
        # print(courses_count.text)

        # Get overlapped courses
        merged_list = overlapped_courses_1 + overlapped_courses_2
        output_list = []

        for sublist in merged_list:
            for item in sublist:
                if item not in output_list:
                    output_list.append(item)

        output_string = ', '.join(output_list)
        ov_msg_str = f"Overlapped Courses: {output_string}"

        # Create a label widget to store ov_msg_str
        ov_msg_label = Label(text=ov_msg_str)
        # print(ov_msg_label.text)

        # Get ov_crs_count and store it on a label
        total_ov_crs = len(output_list)
        ov_crs_cnt_str = f"Total Overlapped Courses = {total_ov_crs}"
        ov_crs_cnt_label = Label(text=ov_crs_cnt_str)
        # print(ov_crs_cnt_label.text)

        # Add a label for actual courses
        actual_crs_cnt = default_total_count - total_ov_crs
        actual_crs_str = f"Actual Courses = {actual_crs_cnt}"
        actual_crs_label = Label(text=actual_crs_str)
        # print(actual_crs_label.text)

        # Create and store all these info on a ColumnPanel
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
        # Get the daily routine and error messages
        dj_day, dj_course, dj_msg, final_routine, comparison_list, final_time_list, overlapped_courses_1, overlapped_courses_2 = anvil.server.call(
            'generate_default_routine', list(self.checked_values))

        # Call the default_routine_msg function
        self.get_total_courses()

        # Create the daily routine panel
        routine_panel = ColumnPanel(border="1px solid black", width="100%")
        routine_panel.tag.style = "resize: both; overflow: auto; border-collapse:collapse;"

        for day, course in zip(dj_day, dj_course):
            # Create a new FlowPanel for the day
            day_panel = FlowPanel()
            day_panel.width = "100%"
            day_panel.tag.style = "display: flex; border-bottom: 1px solid black;"

            # Add a label for the day to the day panel
            day_label = Label(border="1px solid black", text=day,
                              width='80px', align="left", font_size="3", bold=True)
            day_label.tag.style = "border-right: 1px solid black;"
            day_panel.add_component(day_label)

            # Add a panel with a border for each course inline with the day label to the day panel
            for c in course:
                course_panel = ColumnPanel(width="100%")
                course_panel.tag.style = "flex: 1;"

                # Check if the current course is overlapping with another course
                overlap = False
                for msg in dj_msg[day]:
                    if c.split()[0] in msg and c.split()[1] in msg:
                        overlap = True
                        break

                # Set border color based on overlap status
                if overlap:
                    course_panel.border = "1px solid red"
                else:
                    course_panel.border = "1px solid black"

                # Add label to course panel
                label = Label(text=c, align="center", font_size="3")
                course_panel.add_component(label)

                day_panel.add_component(course_panel)

            routine_panel.add_component(day_panel)

        # Set the style of the routine panel using .tag
        routine_panel.tag.style = "resize: both; overflow: auto;"

        # Creating the Reports Section
        err_panel = ColumnPanel(border="1px solid black", width="80%")

        # Adding error messages for every overlapped day to err_panel
        for key, val in dj_msg.items():
            if key in dj_day and dj_msg[key] != '':
                raw_msg = str(dj_msg[key])
                stripped_msg = raw_msg.replace('[', '')
                stripped_msg = stripped_msg.replace(']', '')
                final_msg = f'{key}: {stripped_msg}'
                ov_msg = Label(text=final_msg, align='left',
                               font_size="5", foreground="red")
                err_panel.add_component(ov_msg)

        # If error panel is empty let user know that their routine is all set
        if len(err_panel.get_components()) == 0:
            h_label = Label(text='Reports', align='left',
                            font_size="5", bold=True)
            h_msg = "You're routine is all set."
            healthy_label = Label(text=h_msg, align='left', font_size="5")
            report_section = ColumnPanel()
            report_section.add_component(h_label)
            report_section.add_component(healthy_label)
        # else add the err_panel to reports section
        else:
            h_label = Label(text='Overlaps', align='left',
                            font_size="5", bold=True)
            report_section = ColumnPanel()
            report_section.add_component(h_label)
            report_section.add_component(err_panel)
            fix_button = Button(text='Fix Routine')
            report_section.add_component(fix_button)
            # Create a lambda function to call fix_button_click() with the required arguments
            fix_button_callback = lambda **event_args: self.fix_button_click(
                final_routine)
            # Add the event handler with the lambda function as the callback
            fix_button.set_event_handler('click', fix_button_callback)

        # Clear the list of checked values for the next submission
        self.checked_values = set()

        # Add both the routine panel and reports section to the content panel using a container panel
        container_panel = ColumnPanel()
        container_panel.add_component(routine_panel)
        container_panel.add_component(report_section)
        self.content_panel.clear()
        self.content_panel.add_component(container_panel)

    def get_new_routine_info(self, schedule):
        # Defining necessary global variables
        global model_info_panel
        # Extracting values from the dictionary
        new_routine_values = []
        missing_courses = []
        for day in schedule:
            for item in schedule[day]:
                if item[0] not in new_routine_values:
                    new_routine_values.append(item[0])
        # print(new_routine_values)

        # Convert the list to a string with comma-separated values
        new_courses_str = ", ".join(new_routine_values)

        # Create a label widget with the formatted string
        new_courses_label_msg = f"Courses: {new_courses_str}"
        new_courses_label = Label(text=new_courses_label_msg)
        # print(new_courses_label.text)

        # Create a label widget for missing courses
        missing_courses = [course for course in default_total_list if course.split(
        )[0] not in [c.split()[0] for c in new_routine_values]]
        if missing_courses != []:
            missing_courses_str = ", ".join(missing_courses)
            missing_courses_label_msg = f"Missing Courses: {missing_courses_str}"
            missing_courses_label = Label(
                text=missing_courses_label_msg, foreground="red")
            # print(missing_courses_label.text)

        # Create a label widget for new course count
        new_total_count = len(default_total_list) - len(missing_courses)
        new_courses_count_msg = f"Total Courses = {new_total_count}"
        new_crs_count_label = Label(text=new_courses_count_msg)
        # print(new_crs_count_label.text)

        # Add models' course info to Content Panel
        model_info_panel = ColumnPanel(border="1px solid black", width="100%")
        model_info_panel.clear()
        model_info_panel.add_component(new_courses_label)
        if missing_courses != []:
            model_info_panel.add_component(missing_courses_label)
        model_info_panel.add_component(new_crs_count_label)
        self.content_panel.add_component(model_info_panel)

    def fix_button_click(self, final_routine, **event_args):
        # Clear the content panel
        self.content_panel.clear()

        # Add the before_update_info_panel on content panel
        self.content_panel.add_component(before_update_info_panel)

        # Call the 'create_structures' server function to generate the required data structures
        trial_routine_1, trial_routine_2, comp_list_1, comp_list_2, fn_time_l_1, fn_time_l_2, test_res_1, test_res_2, dr_1, dr_2 = anvil.server.call(
            'create_structures', final_routine, comparison_list, final_time_list)

        # Generate the updated routine, comparison list, and final time list for the first model
        trial_routine_1, test_res_1, comp_list_1 = anvil.server.call(
            'generate_updated_routine', trial_routine_1, overlapped_courses_1, comp_list_1, fn_time_l_1, test_res_1)

        # Add a column panel with a border to contain the updated routine from the first model
        model_1_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(model_1_panel)

        # Add a label for the updated routine from the first model
        model_1_label = Label(
            text='Updated Routine from 1st Model', align='left', bold=True)
        model_1_panel.add_component(model_1_label)

        # Add the updated routine from the first model to the content panel using get_updated_routine
        self.get_updated_routine(trial_routine_1, model_1_panel)
        self.get_new_routine_info(trial_routine_1)

        # Add a column panel with a border to separate the two updated routines
        separator_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(separator_panel)

        # Generate the updated routine, comparison list, and final time list for the second model
        trial_routine_2, test_res_2, comp_list_2 = anvil.server.call(
            'generate_updated_routine', trial_routine_2, overlapped_courses_2, comp_list_2, fn_time_l_2, test_res_2)

        # Add a column panel with a border to contain the updated routine from the second model
        model_2_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(model_2_panel)

        # Add a label for the updated routine from the second model
        model_2_label = Label(
            text='Updated Routine from 2nd Model', align='left', bold=True)
        model_2_panel.add_component(model_2_label)

        # Add the updated routine from the second model to the content panel using get_updated_routine
        self.get_updated_routine(trial_routine_2, model_2_panel)
        self.get_new_routine_info(trial_routine_2)

    def get_updated_routine(self, routine, c_panel):
        # Create a new data row panel to hold the updated routine
        updated_data_row_panel = DataRowPanel()

        # Loop over each day in the routine
        for day, courses in routine.items():
            # Create a new flow panel for the day
            day_panel = FlowPanel(width="100%")

            # Add a label for the day to the day panel
            day_label = Label(border="1px solid black", text=day,
                              width='80px', align="left", font_size="3", bold=True)
            day_label.tag.style = "border-right: 1px solid black;"
            day_panel.add_component(day_label)

            # Loop over each course on this day
            for course in courses:
                # Create a new column panel for the course
                course_panel = ColumnPanel(
                    border="1px solid black", width="100%")
                course_panel.tag.style = "flex: 1;"

                # Add a label for the course to the course panel
                label = Label(
                    text=f"{course[0]} {course[1]}", align="center", font_size="3")
                course_panel.add_component(label)

                # Add the course panel to the day panel
                day_panel.add_component(course_panel)

            # Add the day panel to the updated data row panel
            updated_data_row_panel.add_component(day_panel)

        # Add the updated data row panel to the container panel
        c_panel.add_component(updated_data_row_panel)

    def back_to_courses_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.back_to_courses.visible = False
        self.content_panel.clear()
        self.count_panel.clear()
        self.selected_count_label.text = "Selected: 0"
        self.load_courses()
