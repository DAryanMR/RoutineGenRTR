from ._anvil_designer import CoursesTemplate
from anvil import *
import anvil.server
import anvil.js
import anvil.media

class Courses(CoursesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.load_courses()

    def on_resize(self, **event_args):
        # Code for handling resize event goes here
        pass
    
    def load_courses(self):
        init_label = Label(text='List of all courses from Semester 1-8', font_size='20')
        self.content_panel.add_component(init_label)
    
        self.checked_values = set() # Create an empty list to store the values of checked checkboxes
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
            label = Label(text=f"Semester {i+1}", font_size="16", align="center")
            columns[i].add_component(label)
            for course in courses:
                checkbox = anvil.CheckBox(text=course)
                checkbox.set_event_handler("change", self.check_box_changed)
                columns[i].add_component(checkbox)
    
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
    
        # Set the visibility of the button based on whether a checkbox is checked
        self.generate.visible = len(self.checked_values) > 0

    def generate_click(self, **event_args):
        """This method is called when the button is clicked""" 
        self.content_panel.clear()
        self.load_responsive_routine()
        self.back_to_courses.visible = True
        self.generate.visible = False

    def load_responsive_routine(self):
        global unique_checked_values, dj_day, dj_course, dj_msg, final_routine, comparison_list, final_time_list, overlapped_courses_1, overlapped_courses_2
        # Get the daily routine and error messages
        dj_day, dj_course, dj_msg, final_routine, comparison_list, final_time_list, overlapped_courses_1, overlapped_courses_2 = anvil.server.call('generate_default_routine', list(self.checked_values))
        
        # Create the daily routine panel
        routine_panel = ColumnPanel(border="1px solid black", width="100%")
        routine_panel.tag.style = "resize: both; overflow: auto; border-collapse:collapse;"
    
        for day, course in zip(dj_day, dj_course):
            # Create a new FlowPanel for the day
            day_panel = FlowPanel()
            day_panel.width = "100%"
            day_panel.tag.style = "display: flex; border-bottom: 1px solid black;"
    
            # Add a label for the day to the day panel
            day_label = Label(border="1px solid black", text=day, width='80px', align="left", font_size="3")
            day_label.tag.style = "border-right: 1px solid black;"
            day_panel.add_component(day_label)
    
            # Add a panel with a border for each course inline with the day label to the day panel
            for c in course:
                course_panel = ColumnPanel(border="1px solid black", width="100%")
                course_panel.tag.style = "flex: 1;"
                label = Label(text=c, align="center", font_size="3")
                course_panel.add_component(label)
                day_panel.add_component(course_panel)
    
            # Add the day panel to the routine panel
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
                ov_msg = Label(text=final_msg, align='left', font_size="5", foreground="red")
                err_panel.add_component(ov_msg)
    
        # If error panel is empty let user know that their routine is all set
        if len(err_panel.get_components()) == 0:
            h_label = Label(text='Reports', align='left', font_size="5")
            h_msg = "You're routine is all set."
            healthy_label = Label(text=h_msg, align='left', font_size="5")
            report_section = ColumnPanel()
            report_section.add_component(h_label)
            report_section.add_component(healthy_label)
        # else add the err_panel to reports section
        else:
            h_label = Label(text='Overlaps', align='left', font_size="5")
            report_section = ColumnPanel()
            report_section.add_component(h_label)
            report_section.add_component(err_panel)
            fix_button = Button(text='Fix Routine')
            report_section.add_component(fix_button)
            # Create a lambda function to call fix_button_click() with the required arguments
            fix_button_callback = lambda **event_args: self.fix_button_click(final_routine)
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

    def fix_button_click(self, final_routine, **event_args):
        # Clear the content panel
        self.content_panel.clear()
    
        # Call the 'create_structures' server function to generate the required data structures
        trial_routine_1, trial_routine_2, comp_list_1, comp_list_2, fn_time_l_1, fn_time_l_2, test_res_1, test_res_2, dr_1, dr_2 = anvil.server.call('create_structures', final_routine, comparison_list, final_time_list)
    
        # Generate the updated routine, comparison list, and final time list for the first model
        trial_routine_1, test_res_1, comp_list_1 = anvil.server.call('generate_updated_routine', trial_routine_1, overlapped_courses_1, comp_list_1, fn_time_l_1, test_res_1)
        
        # Add a column panel with a border to contain the updated routine from the first model
        model_1_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(model_1_panel)
    
        # Add a label for the updated routine from the first model
        model_1_label = Label(text='Updated Routine from 1st Model', align='left')
        model_1_panel.add_component(model_1_label)
        
        # Add the updated routine from the first model to the content panel using get_updated_routine
        self.get_updated_routine(trial_routine_1, model_1_panel)
    
        # Add a column panel with a border to separate the two updated routines
        separator_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(separator_panel)
    
        # Generate the updated routine, comparison list, and final time list for the second model
        trial_routine_2, test_res_2, comp_list_2 = anvil.server.call('generate_updated_routine', trial_routine_2, overlapped_courses_2, comp_list_2, fn_time_l_2, test_res_2)
        
        # Add a column panel with a border to contain the updated routine from the second model
        model_2_panel = ColumnPanel(border="1px solid black")
        self.content_panel.add_component(model_2_panel)
    
        # Add a label for the updated routine from the second model
        model_2_label = Label(text='Updated Routine from 2nd Model', align='left')
        model_2_panel.add_component(model_2_label)
        
        # Add the updated routine from the second model to the content panel using get_updated_routine
        self.get_updated_routine(trial_routine_2, model_2_panel)

    def get_updated_routine(self, routine, c_panel):
        # Create a new data row panel to hold the updated routine
        updated_data_row_panel = DataRowPanel()
    
        # Loop over each day in the routine
        for day, courses in routine.items():
            # Create a new flow panel for the day
            day_panel = FlowPanel(width="100%")
    
            # Add a label for the day to the day panel
            day_label = Label(border="1px solid black" , text=day, width='80px', align="left", font_size="3")
            day_label.tag.style = "border-right: 1px solid black;"
            day_panel.add_component(day_label)
    
            # Loop over each course on this day
            for course in courses:
                # Create a new column panel for the course
                course_panel = ColumnPanel(border="1px solid black", width="100%")
                course_panel.tag.style = "flex: 1;"
    
                # Add a label for the course to the course panel
                label = Label(text=f"{course[0]} {course[1]}", align="center", font_size="3")
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
      self.load_courses()
      

