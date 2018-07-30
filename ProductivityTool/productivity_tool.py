import time
from datetime import datetime as dt
#instead of typing datetime.datetime we write dt.(...)

hosts_temp='hosts'

# 'r' before the string allows to the programm to ignore the 'ESC' and read the full path as it should
hosts_path=r'C:\Windows\System32\drivers\etc\hosts'
redirect='127.0.0.1' #dead page
sites_to_block= ['www.facebook.com', 'www.gmail.com', 'facebook.com']

print('\n')
print(dt.now())

