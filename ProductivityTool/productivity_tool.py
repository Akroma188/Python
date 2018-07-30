#You need to open cmd with admin permission or it wont run

import time
from datetime import datetime as dt
#instead of typing datetime.datetime we write dt.(...)



# 'r' before the string allows to the programm to ignore the 'ESC' and read the full path as it should
hosts_path=r'C:\Windows\System32\drivers\etc\hosts'
redirect='127.0.0.1' #dead page
sites_to_block= ['www.facebook.com', 'www.gmail.com', 'facebook.com']

print('\n')
print(dt.now())

while True:

    #if we are within the working hours
    if dt(dt.now().year, dt.now().month, dt.now().day, 9) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day,17):
        print('Working Hours: ')

        with open(hosts_path, 'r+') as file: # r+ equals read or write R/W
            content = file.read() #loads file
            for site in sites_to_block:
                if site in content:
                    pass
                else:
                    file.write(redirect + ' ' + site + '\n')

    else:
        with open(hosts_path, 'r+') as file:
            content = file.readlines()
            #seek puts the pointer in the beginning of the list
            #we do this becouse readlines leaves the pointer at the very last position
            file.seek(0)
            for line in content:
                if not any(site in line for site in sites_to_block):
                    file.write(line)

            file.truncate()
            print('Time to play')

    time.sleep(5)
            

