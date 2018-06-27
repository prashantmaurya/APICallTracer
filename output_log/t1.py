import re
def search(key):
	f = "localweather.log"
	smali_file = open(f) 
	for smali_num,line in enumerate(smali_file, 1):
		if re.search(key,line):
			apiCallLineno = smali_num				#pos of apicall 
			print key
			smali_file.close()
			return
	return
	


#logfile = "SOURCE.txt"
logfile = "default_api"
default_api = open(logfile)
for api_num,key in enumerate(default_api,1):
	key = key[:-1]
	search(key)
	
