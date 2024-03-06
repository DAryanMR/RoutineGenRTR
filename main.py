import anvil.server
from controllers.sort_controller import *
from controllers.time_controller import *
from controllers.course_controller import *
from controllers.gui_controller import *


anvil.server.connect("app_security_key_here")

anvil.server.wait_forever()
