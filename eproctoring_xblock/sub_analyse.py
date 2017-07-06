import numpy
import logging
import sys
import subprocess

#def sub_process(path, student_name, course_name, block_id) :
def sub_process(path, student_name, course_name, block_id) :
	log = logging.getLogger(__name__)
	#subprocess.call(["Python", script1, 'arg1', 'arg2'])
	#command = ['sudo', 'python', '/edx/app/edxapp/venvs/proctor/lib/python2.7/site-packages/suspicious_images/eyeGaze.py', image_data]
	#command = ['sudo', 'python', '/edx/app/edxapp/venvs/proctor/lib/python2.7/site-packages/suspicious_images/eyeGaze.py', path, student_name, course_name, block_id, image_string]
	log.info(path)
	log.info(student_name)
	log.info(course_name)
	log.info(block_id)
	command = ['python', '../lib/python2.7/site-packages/eyeGaze.py', path, student_name, course_name, block_id]
	log.info("YYYYYYYYYYYY")
	process_call = subprocess.call(command)
