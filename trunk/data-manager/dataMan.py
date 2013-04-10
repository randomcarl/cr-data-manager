﻿'''
replaceData

plugin script for ComicRack to replace field content in the library
based on user-defined conditions
the rules are read from file replaceData.dat, located in the script directory

The CR Data Manager plugin is licensed under the Apache 2.0 software
license, available at: http://www.apache.org/licenses/LICENSE-2.0.html

v 0.1.15

by docdoom

images and icons used by permission of 600WPMPO and www.aha-soft.com

revision history

v 0.1.15
fixed - "do you want to see the log" dialogbox always appears behind the Comicrack Window
        (issue 34) (set ComicRack.Window  as parent window handle for all forms)
change - modular rewriting of forms
change - Contains compares now case insensitive
change - StartsWith compares now case insensitive
change - comparison for equality (==) is now case insensitive
change - comparison for less (<) is now case insensitive
change - comparison for lessEqual (<=) is now case insensitive
change - comparison for greater (>) is now case insensitive
change - comparison for greaterEq (>=) is now case insensitive
change - comparison for not equal (<>) is now case insensitive
fix - missing references to globalvars added
change - PageCount added to allowed keys
change - new modifier ContainsAnyOf (issue 28)
change - new modifier ContainsNot (may used as well as NotContains)
change - new modifier ContainsAllOf
change - if no value was modified by the DM, only "book xxx was touched" is written to logfile
change - new modifier NotContainsAnyOf
change - new modifier StartsWithAnyOf
change - new directive "#@ END_RULES"
change - new class "parser"
change - new class "ruleFile" (encapsulated reading and writing the DATFILE)
fix - exception when Null value was used in Range modifier
change - when error was raised by compiling code a MessageBox will show the error
...
r105
change - Configurator form re-written
change - basic Search functionality in Configurator
...
r106
change - first rudimentary GUI written (no functionality yet)
...
r109
change - ComicRack version check at start (min is 0.9.165)
change - basic GUI functionality


>> revision history for older releases is at http://code.google.com/p/cr-replace-data/wiki/RevisionLog

issues:
exclude duplicate lines from parsing
marker in books if handled by the dataman (tags or notes?)
todo: modifier Before
todo: modifier After
todo: use In as modifier in keys
     e.g. <<Number.In:1,3,8>>
todo: add RegExp as modifier
todo: simulation instead of actual replacing of data
------------------------------------------------------
'''

import clr
import sys
import re
import System
import System.Text
from System import String
from System.IO import File,  Directory, Path, FileInfo, FileStream
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

# this handles unicode encoding:
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

DEBUG__ = True

import globalvars
import utils
from utils import parser
from utils import comparer
from utils import nullToZero
from mainform import mainForm
from displayResultsForm import displayResultsForm
from aboutForm import aboutForm
from progressForm import progressForm
from configuratorForm import configuratorForm
from utils import ruleFile

sys.path.append(globalvars.FOLDER)

#allowedKeys = [
#	'Series',
#	'Volume',
#	'Imprint',
#	'Publisher',
#	'Number',
#	'FileDirectory',
#	'SeriesGroup',
#	'Month',
#	'Year',
#	'MainCharacterOrTeam',
#	'Format',
#	'AlternateSeries',
#	'Count',
#	'FilePath',
#	'FileName',
#	'Genre',
#	'Tags',
#	'PageCount'
#	]

#numericalKeys = [
#	'Volume',
#	'Month',
#	'Year',
#	'Count',
#	'PageCount'
#	]

#multiValueKeys = [
#	'Tags',
#	'Genre'
#	]
	
#allowedVals = [
#	'Series',
#	'Volume',
#	'Imprint',
#	'Publisher',
#	'Number',
#	'SeriesGroup',
#	'MainCharacterOrTeam',
#	'Format',
#	'AlternateSeries',
#	'Count',
#	'Genre',
#	'Tags'
#	]


def writeCode(s, level, linebreak):
	''' 
	writes code to dataMan.tmp
	parameters: 
	s - string to write (str)
	level - indentation level (int)
	linebreak - add linebreak? (bool)
	'''
	s = str(s)
	prefix = '\t' * level
	s = prefix + s
	if linebreak == True: s += '\n'
	try:
		File.AppendAllText(globalvars.TMPFILE, s)
		
	except Exception, err:
		print "Error in function writeCode: ", str(err)

#def parsedCode():
#	try:
#		return File.ReadAllText(globalvars.TMPFILE)
#	except Exception, err:
#		print "Error in function parsedCode: ", str(err)
		
def parseString(s):
	# todo: this belongs in class ruleFile
	
	# read a line from replaceData.dat and generate python code from it
	
	myCrit = ''				# this will later contain the left part of the rule
	myNewVal = ''			# this will later contain the new value (right part of rule)
	myModifier = ''			# the modifier (like Contains, Range, Calc etc.)

	rules = utils.ruleFile()
	allowedKeys = rules.allowedKeys
	allowedVals = rules.allowedVals
	numericalKeys = rules.numericalKeys
	multiValueKeys = rules.multiValueKeys
	
	myParser = utils.parser()
	myParser.validate(s)
	if myParser.err:
		File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (%s)\nline: %s)" % (myParser.error, s))
		return 0
	
	a = String.split(s,"=>")
	i = len(a[0])
	a[0] = String.Trim(a[0])
	i = len(a[0])
	
	# split the string and retrieve the criteria (left part) and newValues (right part) 
	# store those in lists
	try:		
		criteria = a[0].split(">>")			
		newValues = String.split(a[1],">>")
	except Exception, err:
		print str(err)
	
	# iterate through each of the criteria
	for c in criteria:
		#i = len(c)
		if len(c) > 0:
			c = String.Trim(String.replace(c,"<<",""))
			myKey = ''  # only to reference it
			if String.find(c,':') > 0:
				tmp = String.split(c,":",1)
				tmp2 = String.split(tmp[0],".",1)
				myKey = tmp2[0]
				try:
					myModifier = tmp2[1]
				except Exception, err:
					myModifier = ""
			else:
				File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0

			if c <> "" and not (myKey in allowedKeys):
				File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0
			myOperator = "=="
			# handling if modifier is appended to field
			# like Volume.Range:1961, 1963
			try:
				if myModifier <> "":
					if str.lower(myModifier) == "range":
						myOperator = "in range"
					elif str.lower(myModifier) == 'is':
						myOperator = '=='
					elif str.lower(myModifier) == "not":
						myOperator = "<>"
					elif str.lower(myModifier) == "contains":
						myOperator = ""
					elif str.lower(myModifier) == "greater":
						myOperator = ">"
					elif str.lower(myModifier) == "greatereq":
						myOperator = ">="
					elif str.lower(myModifier) == "less":
						myOperator = "<"
					elif str.lower(myModifier) == "lesseq":
						myOperator = "<="
					elif str.lower(myModifier) == "startswith":
						myOperator = "startswith"
					elif str.lower(myModifier) == 'startswithanyof':
						myOperator = ''
					elif str.lower(myModifier) == "containsanyof":
						myOperator = ""
					elif str.lower(myModifier) == "notcontainsanyof":
						myOperator = ""
					elif str.lower(myModifier) == "containsnot" or str.lower(myModifier) == "notcontains":
						myModifier = "ContainsNot"
					elif str.lower(myModifier) == "containsallof":
						myOperator = ""
					else:
						File.AppendAllText(globalvars.ERRFILE,"Syntax not valid (invalid modifier %s)\nline: %s)" % (myModifier, s))
						return 0
											
			except Exception, err:
				MessageBox.Show("error at parseString: %s" % str(err))
				return

			myVal = tmp[1]
			myVal = String.replace(myVal,"\"","\\\"")
			
			if myOperator == "in range":
				tmp = String.Split(myVal,",")
				myVal = "%d, %d" % (float(tmp[0]), float(tmp[1]) + 1)
				if myKey in numericalKeys:
					myCrit = myCrit + ("book.%s %s (%s) and " % (myKey, myOperator, myVal))
				else:
					myCrit = myCrit + ("float(nullToZero(book.%s)) %s (%s) and " % (myKey, myOperator, myVal))

			# ---------------------------------------------------------------------------
			# now begins the interesting part for field Number which is stored as 
			# a string but treated as a numerical value
			elif myOperator in ('==', '>', '>=', '<', '<=') and myKey == 'Number':
				if str.Trim(myVal) == '':
					# fix issue 31
					myCrit = myCrit + ('str(book.Number) %s \'\' and ' % (myOperator))
				else:
					# if the current value of book.Number is Null it has to be converted to
					# 0 before it can be converted to float
					myCrit = myCrit + ('float(nullToZero(book.Number)) %s float(nullToZero(%s)) and ' % (myOperator, myVal))
			# end of extra handling of Number field
			# ----------------------------------------------------------------------------
			elif str.lower(myModifier) == "contains" and myKey not in numericalKeys:
				myCrit = myCrit + 'comp.contains(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				#MessageBox.Show(myCrit)
				#myCrit = myCrit + ("comp.contains
				# myCrit = myCrit + ("String.find(book.%s,\"%s\") >= 0 and " % (myKey,myVal)) 
			
			elif str.lower(myModifier) == "containsanyof": # and myKey not in numericalKeys:
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.containsAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "ContainsAnyOf modifier cannot be used in %s field" % (myKey))
					return 0
			elif str.lower(myModifier) == "notcontainsanyof":
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.notContainsAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "NotContainsAnyOf modifier cannot be used in %s field" % (myKey))
					return 0
				
			elif str.lower(myModifier) == "containsallof": # and myKey not in numericalKeys:
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.containsAllOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "ContainsAllOf modifier cannot be used in %s field" % (myKey))
					return 0

			elif str.lower(myModifier) == "containsnot":
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.containsNot(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "ContainsNot modifier cannot be used in %s field" % (myKey))
					return 0															
			elif myOperator == "startswith" and myKey not in numericalKeys:
				myCrit = myCrit + ("comp.startsWith(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey,myVal))
				#myCrit = myCrit + ("book.%s.startswith(\"%s\") and " % (myKey,myVal))
			elif str.lower(myModifier) == "startswithanyof": # and myKey not in numericalKeys:
				if myKey not in numericalKeys:
					myCrit = myCrit + 'comp.startsWithAnyOf(book.%s,\"%s\",COMPARE_CASE_INSENSITIVE) == True and ' % (myKey, myVal)
				else:
					File.AppendAllText(globalvars.ERRFILE, "Syntax not valid\nline: %s)\n" % (s))
					File.AppendAllText(globalvars.ERRFILE, "StartsWithAnyOf modifier cannot be used in %s field" % (myKey))
					return 0
			elif myOperator == '==' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.equals(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey,myVal)
			elif myOperator == '<' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.less(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '<=' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.lessEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '>' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.greater(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '>=' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.greaterEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			elif myOperator == '<>' and myKey not in numericalKeys:
				myCrit = myCrit + "comp.notEq(book.%s,\"%s\", COMPARE_CASE_INSENSITIVE) and " % (myKey, myVal)
			else:
				# numerical values in CR are -1 if Null
				if myKey in numericalKeys and str.Trim(myVal) == '':
					myVal = -1
				myCrit = myCrit + ("str(book.%s) %s \"%s\" and " % (myKey, myOperator, myVal))
				
			
	myCrit = "if " + String.rstrip(myCrit, " and") + ":"
	writeCode(myCrit,1,True)
	writeCode("f.write(book.Series.encode('utf-8') + ' v' + str(book.Volume) + ' #' + book.Number + ' was touched \\t(%s)\\n')" % a[0], 2, True)
	
	# iterate through each of the newValues
	for n in newValues:
		if len(n) > 0:
			n = String.Trim(String.replace(n,"<<",""))
			if String.find(n,':') > 0:
				tmp = String.split(n,":",1)
				tmp2 = tmp[0]
				myKey = tmp2
				myModifier = ''
				if String.find(tmp2,'.') > 0:
					tmp3 = String.split(tmp2,'.')
					myKey = tmp3[0]
					myModifier = tmp3[1]
			else:
				File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))			
				return 0
			if not (myKey in allowedVals):
				File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)" % (myKey, s))
				return 0
			# to do: handling if function is appended to field
				
			myVal = tmp[1]
			
			writeCode("myOldVal = str(book.%s)" % myKey, 2, True)

			if str.lower(myModifier) = 'setvalue':
				myModifier = ''
				
			if myModifier <> "":
				if str.lower(myModifier) == "calc":
					if myKey not in numericalKeys and myKey <> 'Number':
						myVal = String.replace(myVal,'{','str(book.')
					else:
						myVal = String.replace(myVal,'{','int(book.')
					myVal = String.replace(myVal,'}',')')
					if myKey == 'Number':
						writeCode("book.%s = str(%s)" % (myKey, myVal), 2, True)
					else:
						writeCode("book.%s = %s" % (myKey, myVal), 2, True)
				if str.lower(myModifier) == "add":
					if myKey in numericalKeys or myKey == 'Number':
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Add modifier cannot be used in %s field" % (myKey))
						return 0
					elif myKey in multiValueKeys:
						if len(String.Trim(myVal)) == 0:
							File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
							File.AppendAllText(globalvars.ERRFILE, "Remove modifier needs 1 argument")
							return 0
						else:
							writeCode('book.%s = multiValueAdd(book.%s,"%s")' % (myKey, myKey, myVal), 2, True)
				if str.lower(myModifier) == "replace":
					if myKey in numericalKeys or myKey == 'Number':
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Replace modifier cannot be used in %s field" % (myKey))
						return 0
					elif myKey in multiValueKeys:
						tmpVal = myVal.split(',')
						if len(tmpVal) > 1:
							writeCode ('book.%s = multiValueReplace(book.%s,"%s","%s")' % (myKey, myKey, tmpVal[0], tmpVal[1]), 2, True)
						else:
							File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
							File.AppendAllText(globalvars.ERRFILE, "Replace modifier needs 2 arguments")
							return 0
				if str.lower(myModifier) == "remove":
					if myKey in numericalKeys or myKey == 'Number':
						File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
						File.AppendAllText(globalvars.ERRFILE, "Remove modifier cannot be used in %s field" % (myKey))
						return 0
					elif myKey in multiValueKeys:
						if len(String.Trim(myVal)) == 0:
							File.AppendAllText(globalvars.ERRFILE, "Syntax not valid (invalid field %s)\nline: %s)\n" % (myKey, s))
							File.AppendAllText(globalvars.ERRFILE, "Remove modifier needs 1 argument")
							return 0
						else:
							writeCode('book.%s = multiValueRemove(book.%s,"%s\")' % (myKey, myKey, myVal), 2, True)

			else:

				if myKey in numericalKeys:
					if len(myVal) == 0:
						writeCode("book.%s = \'\'\n" % (myKey), 2, True)
					else:
						writeCode("book.%s = %s\n" % (myKey, myVal), 2, True)
				else:
					writeCode("book.%s = \"%s\"" % (myKey, myVal), 2, True)
				myNewVal = myNewVal + ("\t\tbook.%s = \"%s\"" % (myKey, myVal)) 

			writeCode("myNewVal = str(book.%s)" % myKey, 2, True)
			writeCode("if myNewVal <> myOldVal:", 2, True)	
			writeCode("f.write('\\tbook.%s - old value: ' + myOldVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode("f.write('\\tbook.%s - new value: ' + myNewVal.encode('utf-8') + '\\n')" % (myKey), 3, True)
			writeCode('book.Tags = multiValueAdd(book.Tags,"DMProc")', 3, True)
			writeCode("else:", 2, True)
			writeCode("pass",3,True)
			# writeCode("f.write('\\t%s - old value was same as new value\\n')" % (myKey), 3, True)
	return -1
	

def dmConfig():

	form = configuratorForm()
	form.setFile(globalvars.DATFILE)
	form.Text = 'Data Manager Configurator %s' % globalvars.VERSION
	form.ShowDialog(ComicRack.MainWindow)
	form.Dispose()

def crVersion():
	minVersion = '0.9.164'
	vMin = 0 + 9000 + 164
	myVersion = ComicRack.App.ProductVersion
	v = str.Split(myVersion,'.')
	vMyVersion = (int(v[0]) * 1000000) + (int(v[1]) * 1000) + int(v[2])
	if vMyVersion < vMin:
		MessageBox.Show(
		'You have only CR version %s installed.\nPlease install at least version %s of ComicRack first!' % (myVersion,minVersion),
		'Data Manger for ComicRack %s' % globalvars.VERSION)
		return False
	return True

#@Name	Data Manager
#@Image dataMan16.png
#@Hook	Books

def replaceData(books):

	ERROR_LEVEL = 0

	if not crVersion():
		return
	form = mainForm()
	form.ShowDialog(ComicRack.MainWindow)
	form.Dispose()

	if form.DialogResult == DialogResult.No:
		dmConfig()
		return
	elif form.DialogResult <> DialogResult.OK:
		return
	else:
		pass
	
	try:
		File.Delete(globalvars.TMPFILE)
		File.Delete(globalvars.ERRFILE)
	except Exception, err:
		pass
	
	# check if configuration exists
	if not File.Exists(globalvars.DATFILE):
		MessageBox.Show('Please use the Data Manager Configurator first!','Data Manager %s' % globalvars.VERSION)
		return

	# check if configuration has been saved once
	if not File.Exists(globalvars.CHKFILE):
		MessageBox.Show('Please save your configuration first!','Data Manager %s' % globalvars.VERSION)
		return

	writeCode('try:', 0, True)
	
	progBar = progressForm()
	progBar.Show()
	writeCode('import System',1,True)
	writeCode('from System.Windows.Forms import MessageBox',1,True)
	writeCode('from globalvars import *',1,True)
	writeCode('from utils import *',1,True)
	writeCode('comp = comparer()',1,True)
	
	try:
		s = File.ReadAllLines(globalvars.DATFILE)
#		print s
		i = 0
		s = [line for line in s if str.Trim(line) <> '']
		for line in s:
			i += 1
#			if String.find(line," => ") and line[0] <> "#":
			if not line.StartsWith('#'):

				if not parseString(line):
					error_message = File.ReadAllText(globalvars.ERRFILE)
					MessageBox.Show("Error in line %d!\n%s" % (i, str(error_message)),"CR Data Manager %s - Parse error" % globalvars.VERSION)
					ERROR_LEVEL = 1
					break
			if String.StartsWith(line,'#@ end rules'):
				break
			
	except Exception, err:
		print 'getCode: ', str(err)

	progBar.Dispose()

	writeCode('except Exception,err:', 0, True)
	writeCode('MessageBox.Show (\"Error in code generation: %s\" % str(err))', 1, True)
	
	if ERROR_LEVEL == 0:
		# theCode = parsedCode()	# read generated code from file
		theCode = File.ReadAllText(globalvars.TMPFILE)
		if DEBUG__:
			print "code generated by CR Data Manager: \n%s" % theCode   # remove in first stable release!
			
		progBar = progressForm()
		progBar.Show()
		progBar.setMax(books.Length)
		touched = 0
		f=open(globalvars.LOGFILE, "w")	# open logfile
		for book in books:
			touched += 1
			progBar.setValue(touched)
			try:
				exec (theCode)
				
			except Exception, err:
				MessageBox.Show('Error while executing the rules. \n%s\nPlease check your rules.' % str(err), 'Data Manager - Version %s' % globalvars.VERSION)
				ERROR_LEVEL = 1
		
		f.close()				# close logfile

		progBar.Dispose()
		
		if ERROR_LEVEL == 0:
			msg = "Finished. I've inspected %d books.\nDo you want to take look at the log file?" % (touched)
	
			form = displayResultsForm()
			form.configure(msg)
			form.ShowDialog(ComicRack.MainWindow)
			form.Dispose()

			if form.DialogResult == DialogResult.Yes:
	
				form = configuratorForm()
				form.setFile(globalvars.LOGFILE)
				form.Text = 'Data Manager Logfile %s' % globalvars.VERSION
				form.ShowDialog(ComicRack.MainWindow)
				form.Dispose()

	try:
		#File.Delete(TMPFILE)
		File.Delete(globalvars.ERRFILE)
	except Exception, err:
		pass
	

