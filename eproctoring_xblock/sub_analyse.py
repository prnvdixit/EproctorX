import numpy
import logging
import sys
import subprocess

def sub_process(path, student_name, course_name, block_id) :
	
	"""
	Calls Image-Analysing python file as a sub-process.
	"""
	
	command = ['python', '../lib/python2.7/site-packages/eyeGaze.py', path, student_name, course_name, block_id]
	process_call = subprocess.call(command)
