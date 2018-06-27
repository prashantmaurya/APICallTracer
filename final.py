import os
import re
import sys
fname = sys.argv[1]
fname = fname+"/smali/com"
##all files based on extension from a directory and its subdirectories
global total_files
total_files=0
def dir_byfiletype(dir_name, *args):
	fileList = []
	for file in os.listdir(dir_name):
		dirfile = os.path.join(dir_name, file)
		if os.path.isfile(dirfile):
			if os.path.splitext(dirfile)[1][1:] in args:
				fileList.append(dirfile)
			pass
		if os.path.isdir(dirfile):
			fileList += dir_byfiletype(dirfile, *args)
  	return fileList

#list of smali files to search and edit
def get_package_name():
	pfile = open("package_name")
	package_name = pfile.read()
	package_name = package_name[:-1]
	package_name = "L"+package_name
	package_name = package_name.replace('.','/')
	pfile.close()
	return package_name
def get_pck():
	pfile = open("package_name")
	package_name = pfile.read()
	package_name = package_name[:-1]
	package_name = package_name.replace('.','/')
	pfile.close()
	return package_name
#pck = get_pck()
#fname = fname+"/smali/"+pck
#pck = "alarmy/smali/"+pck
fileList = dir_byfiletype(fname, 'smali')
#print fileList
skip_classes = ['\\com\\flurry', '\\org\\cocos2dx', '\\android\\support','Pro.smali']
# Search and edit in all smali files present in the list 'fileList'
default_api_file = 'config/default_api'

#increase the .locals by 2 and return the new value

def get_local_count(f, local_var_lineno):
	smali_file = open(f)
	lines = smali_file.readlines()
	l = lines[local_var_lineno-1]	
	count = l.split()[1]
	count = int(count)+ 2
	new_line = ".locals " + str(count)
	#print new_line
	lines[local_var_lineno-1] = new_line+"\n"
	with open(f, 'w') as file:
    		file.writelines( lines )
	file.close()
	smali_file.close()
	return count


def get_api_name(api_num):
	default_api = open(default_api_file)
	lines = default_api.readlines()
	lines = lines[api_num]
	default_api.close()
	return lines[:-1]    #remove next line character
#code to insert in smali file to log sensitive api called. Need to give correct path of Pro.smali and name of 
#method name corresponding to the api called present in default_list.
def edit_smali(f,apiCallLineno,api_num):
	package_name = get_package_name()
	methodName = "logCurrentAPI"+str(api_num) 
	monitor_code =  '''\n    invoke-static {{}}, {package_name}/Pro;->{methodName}()V\n'''.format(methodName=methodName,package_name=package_name)
	
	restart  = write_monitor_code(f,monitor_code,apiCallLineno)
	search(f,restart,key,api_num)

#search for the api call(key) in smali file(f)
def search(f,start,key,api_num):
	smali_file = open(f) 
	for smali_num,line in enumerate(smali_file, 1):
		if re.search(key,line) and smali_num>start:
			apiCallLineno = smali_num				#pos of apicall 
			#print key + " " + line + " "+str(smali_num)
			#print linecache.getline(f, local_var_lineno)
			#edit_smali(local_var_lineno,apiCallLineno,api_num)
			smali_file.close()
			print "Found: "+ key+" in " +f
			edit_smali(f,apiCallLineno,api_num)
			return

#insert the monitor code at appropriate place just below the sensitive api call
def write_monitor_code(f,monitor_code,apiCallLineno):
	f1 = open(f)
	found = 0
	for smali_num,line in enumerate(f1, 1):
			if re.search(".line",line) or (re.search("goto",line)) or (re.search("return",line)) :
				if smali_num>apiCallLineno:
					edit_lineno = smali_num    #line number of .line just below the api call to add monitor code
					found = 1       
					break
	if found==1:
		f1.close()
		f2 = open(f)
		contents = f2.readlines()
		contents.insert(edit_lineno-1, monitor_code)              
		f2.close()
		f3 = open(f,"w")
		contents = "".join(contents)
		f3.write(contents)
		f3.close()
		restart = edit_lineno+2
		#total_files_edited = total_files_edited+1
		#print restart
		return restart
	else:
		restart = apiCallLineno+1
		return restart
#for every file in fileList it opens default_api file and searches each api in dafault list against the smali file
for f in fileList:
	if any( badpath in f for badpath in skip_classes ):
		print "Skipping file: " + f
		continue
	total_files=total_files+1
	print "Searching file: " + f
	start = 1
	default_api = open(default_api_file)
	for api_num,key in enumerate(default_api,1):
		key = key[:-1]			#remove next line character
		#print key
		search(f,start,key,api_num)

	default_api.close()



print total_files