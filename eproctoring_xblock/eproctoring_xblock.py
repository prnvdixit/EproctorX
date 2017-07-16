"""TO-DO: Write a description of what this XBlock is."""

import MySQLdb

import database

import pkg_resources
import raw
import json

import os
from time import gmtime, strftime
import profile_pic
import sub_analyse
import subprocess
import base64
import time

from xblock.core import XBlock
from xblock.fields import Scope, Integer, Dict, Float, String
from xblock.fragment import Fragment

import logging
from django.template import Context, Template
log = logging.getLogger(__name__)

def load_resource(resource_path):  # pragma: NO COVER
    """
    Gets the content of a resource
    """
    resource_content = pkg_resources.resource_string(__name__, resource_path)
    return unicode(resource_content)

def render_template(template_path, context={}):  # pragma: NO COVER
    """
    Evaluate a template by resource path, applying the provided context
    """
    template_str = load_resource(template_path)
    template = Template(template_str)
    return template.render(Context(context))

class EproctoringXBlock(XBlock):
	
    """
    The main function being called every time page gets loaded or refreshed.
    """
    
  
    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    
    # PATH set by ADMIN - To save all the suspicious-attempts' proofs
    path = "/home/edx/suspicious_images"

    # Self-Explanatory
    student_name = String(
		default="", scope = Scope.user_state,
		help="Name of user",
    )

    # Self-Explanatory => TEST VALUE
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )


    sum_time = Float(
        default=0.0, scope=Scope.user_state,
        help="A counter storing time between last web-cheating attempt",
    )
	
    time_dict = Dict(
                default={},
                scope=Scope.user_state
        )

    content_id = String(
		default="",
		scope=Scope.user_state
	)

    course_name = String(
   		  default="",
    		  scope = Scope.user_state
    	)

    def get_all_courses(self):
		
	"""
	This function returns a boolean value telling if the Subsection is timed or not.
	It is called if the user is "instructor" or "staff".
	"""

	sql_user = 'root'
	database = 'edxapp'
	sql_passwd = ""


    	try:
        	db_mysql = MySQLdb.connect(user=sql_user,passwd=sql_passwd, db=database) # Establishing MySQL connection
   	except:
        	print "MySQL connection not established"
        	#return HttpResponse("MySQL connection not established") # MySQL could not be connected

    	name = self.content_id
    	query = "select is_active from proctoring_proctoredexam where content_id = %s"

    	mysql_cursor = db_mysql.cursor()
    	mysql_cursor.execute(query, (name,))
    	courses = mysql_cursor.fetchall()
    	try :
        	is_active_or_not = courses[0][0]
        	if(is_active_or_not):
                	return 1
        	else:
                	return 0
    	except:
        	return 0

        directory = path + "/" + course_name

        if not os.path.exists(directory):
            os.makedirs(directory)

        directory += "/" + block_id

        if not os.path.exists(directory):
            os.makedirs(directory)

        directory += "/" + student_name

        if not os.path.exists(directory):
            os.makedirs(directory)

        return directory + "/"


    def get_path_calling(self):
	path_webimg = self.get_path(self.path, self.xmodule_runtime.xqueue['default_queuename'], self.location.block_id, database.get_user(self.xmodule_runtime.user_id)) + "web_img"
	if not os.path.exists(path_webimg):
            os.makedirs(path_webimg)

	path_webimg += "/"

	return path_webimg + str(len(os.listdir(path_webimg))) + "_web.png"

    def resource_string(self, path):
		
        """Handy helper for getting resources from our kit."""
	
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")
   
    def is_instructor(self):
        return self.xmodule_runtime.get_user_role() == 'instructor'
    
    def studio_view(self,request, context=None):
	
        """
        The primary view of the EproctoringXBlock, shown to students
        when viewing courses.
        """
	
        html = self.resource_string("templates/eproctoring_xblock2.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/eproctoring_xblock2.css"))
        frag.initialize_js('EproctoringXBlock')
        return frag

    def student_view(self, request, context=None):
		
        """
        The primary view of the EproctoringXBlock, shown to students
        when viewing courses.
        """
	
 	self.sum_time = 0.0
        
	if self.xmodule_runtime.get_user_role() == 'student':
		
                # This block should run only if the current module is timed
		context = {
			"student_name" : database.get_user(self.xmodule_runtime.user_id),
			}


		html = self.resource_string("templates/eproctoring_xblock.html")
       		frag = Fragment()
		frag.add_content(
            		render_template(
               			"templates/eproctoring_xblock.html",
                		context
            			)
       		)
        	frag.add_css(self.resource_string("static/css/eproctoring_xblock.css"))
        	frag.add_javascript(self.resource_string("static/js/src/eproctoring_xblock.js"))
       		frag.initialize_js('EproctoringXBlock')
       		return frag

        else:
            if self.xmodule_runtime.get_user_role() == 'instructor' :
		#If the user is instructor, we are finding if the subsection is timed or not.
		#"reload_page" won't be relevant at the first alert (since request won't exist without reloading the page)
		#But at the second alert, we don't need to reload it again.
		
                if(request['root_xblock']) :
	        	self.content_id = str(request['root_xblock'].parent)
			is_active_bool = self.get_all_courses()
			reload_page = 0
		else :
			reload_page = 1
			is_active_bool = 0

	    #Analogous to request['root_xblock'].parent for insructor is request['activate_block_id'] for staff
	    if self.xmodule_runtime.get_user_role() == 'staff' :
		self.content_id = str(request['activate_block_id'])
		is_active_bool = self.get_all_courses()
		reload_page = 0
	    
            #Passing the boolean variables as context to eproctoring_xblock2.html
	    context = {
		"is_active_bool" : is_active_bool,
		"reload_page" : reload_page,
		}

	    html = self.resource_string("templates/eproctoring_xblock2.html")
            frag = Fragment()
            frag.add_content(
            render_template(
               "templates/eproctoring_xblock2.html",
                context
            )
        )
	    frag.add_css(self.resource_string("static/css/eproctoring_xblock2.css"))
            frag.add_javascript(self.resource_string("static/js/src/eproctoring_xblock2.js"))
            frag.initialize_js('EproctoringXBlock')	
	    return frag


    @XBlock.json_handler
    def send_img(self, image_string, suffix = '') :
        
        file = open(self.get_path(self.path, self.xmodule_runtime.xqueue['default_queuename'], self.location.block_id, database.get_user(self.xmodule_runtime.user_id)) + "json_data.txt", "w")
        file.write(image_string)
        file.close()

    	sub_analyse.sub_process(self.path, database.get_user(self.xmodule_runtime.user_id), self.xmodule_runtime.xqueue['default_queuename'], self.location.block_id)


    @XBlock.json_handler
    def reset_handler(self, data, suffix = ''):
	database.reset_table()

    @XBlock.json_handler
    def update_handler(self, data, suffix = ''):
	database.update_total()

    @XBlock.json_handler
    def save_student_handler(self, data, suffix = ''):

	parent_string = str(self.parent)
	
	index_colon = parent_string.find(':')
	column_dir_name = ""
	
	plus_count = 0

	for index in xrange(index_colon+1, len(parent_string)) :
		if(plus_count == 2):
			break
		if(parent_string[index] == '+'):
			if(plus_count == 0):
				column_dir_name += '-'
			plus_count += 1
		else:
			column_dir_name += parent_string[index]


	file = open(self.path + "/" + column_dir_name + ".txt", "w")
	
        desc_array = database.final_result(column_dir_name)
	
        for student_name in desc_array :
		file.write(student_name + "\n")

	file.close()
		
		

    @XBlock.json_handler
    def compare_image(self, data,suffix=''):
		
        """
        An handler, which compares the new image with the profile image.
        """
	
        path_compareimg1 = self.get_path(self.path, self.xmodule_runtime.xqueue['default_queuename'], self.location.block_id, database.get_user(self.xmodule_runtime.user_id)) + "compare_img"
        
        if not os.path.exists(path_compareimg1):
            os.makedirs(path_compareimg1)

        path_compareimg1 += "/"
	
	path_compareimg2 = path_compareimg1 + str(len(os.listdir(path_compareimg1))) + "_compare.png"
        
	path_compareimg1 += "profile_pic"
	
        compare_image_string = data
        
        file = open("/edx/app/edxapp/venvs/proctor/lib/python2.7/site-packages/compare_image/" + "json_data1.txt", "w")
        file.write(compare_image_string)

        file.close()
	image2path =  profile_pic.get_pic_path(database.get_user(self.xmodule_runtime.user_id))
	
	command = ['python', '/edx/app/edxapp/venvs/proctor/lib/python2.7/site-packages/compare2.py',str(image2path),str(path_compareimg1),str(path_compareimg2),str(self.xmodule_runtime.user_id),str( self.xmodule_runtime.xqueue['default_queuename'])]
	process_call = subprocess.check_output(command)
	
        self.count += 1        
	return {"count": self.count}
	

    @XBlock.json_handler
    def startingtime(self,data,suffix=''):
		newdict = self.time_dict
		newdict["start_time"] = time.time()
		self.time_dict = newdict
     
    @XBlock.json_handler
    def differenceoftimes(self,data,suffix=''):
                self.sum_time = (time.time() - self.time_dict["start_time"])		
		database.update_table(self.xmodule_runtime.user_id, self.xmodule_runtime.xqueue['default_queuename'], "web_count", self.sum_time)

   
    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}
 
    @XBlock.json_handler
    def web_screen_shot(self, data, suffix=''):
    	
    	image = base64.b64decode(data[22:])
    	
    	file_name = self.get_path_calling();
    	
    	with open(file_name, 'wb') as file_name:
    		file_name.write(image)
    
    # TO-DO: change this to create the scenarios you'd like to see in the
    # worbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
	
        """A canned scenario for display in the workbench."""
	
        return [
            ("EproctoringXBlock",
             """<eproctoring_xblock/>
             """),
            ("Multiple EproctoringXBlock",
             """<vertical_demo>
                <eproctoring_xblock/>
                <eproctoring_xblock/>
                <eproctoring_xblock/>
                </vertical_demo>
             """),
        ]
