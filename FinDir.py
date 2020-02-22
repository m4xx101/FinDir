import argparse
import os 
import sys
import requests
import concurrent.futures
import requests
from pyfiglet import figlet

threads = []
words=[]
files = [".vscode","config.yaml",".gitignore",".svn/wc.db",".git/config", "phpmyadmin/", ".travis.yml",".DS_Store",".htaccess",".htpasswd","Makefile","Dockerfile","package.json","gulpfile.js","composer.json","web.config",".env",".idea","nbproject/","bower.json","package-lock.json",".gitlab-ci.yml","database.yml"]
info_status = {"Continue":100,"Switching Protocols":101,"Processing ":102,"Early Hints":103}
success_status = {"OK":200,"Created":201,"Accepted ":202,"Non-Authoritative Information":203,"No Content":204,"Reset Content":205,"Partial Content":206,"Multi-Status":207,"Already Reported":208,"IM Used":226}
redirection_status={"Multiple Choices":300,"Moved Permanently":301,"Found ":302,"See Other":303,"Not Modified":304,"Use Proxy":305,"Switch Proxy":306,"Temporary Redirect":307,"Permanent Redirect":308}
cerror_status={"Bad Request":400,"Unauthorized ":401,"Payment Required":402,"Forbidden":403,"Not Found":404,"Method Not Allowed":405,"Not Acceptable":406,"Proxy Authentication Required":407,"Request Timeout":408,"Conflict":409,"Gone":410,"Length Required":411,"Precondition Failed":412,"Payload Too Large":413,"URI Too Long":414,"Unsupported Media Type":415,"Range Not Satisfiable":416,"Expectation Failed":417,"Im a teapot":418,"Misdirected Request":421,"Unprocessable Entity":422,"Locked":423,"Failed Dependency":424,"Too Early":425,"Upgrade Required":426,"Precondition Required":428,"Too Many Requests":429,"Request Header Fields Too Large":431,"Unavailable For Legal Reasons":451}
serror_status={"Internal Server Error":500,"Not Implemented":501,"Bad Gateway":502,"Service Unavailable":503,"Gateway Timeout":504,"HTTP Version Not Supported":505,"Variant Also Negotiates":506,"Insufficient Storage":507,"Loop Detected":508,"Not Extended":510,"Network Authentication Required":511}
aws_ELB_status={"timeout":460,"X-Forwarded-For request header with more than 30 IP":463}
Cloudflare_status={"Web Server Returned an Unknown Error":520,"Web Server Is Down":521,"Connection Timed Out":522,"Origin Is Unreachable":523,"A Timeout Occurred":524,"SSL Handshake Failed":525,"Invalid SSL Certificate":526,"Railgun Error":527,"Error":530}
nginx_status={"No Response":444,"Request header too large":494," SSL Certificate Error":495,"SSL Certificate Required":496,"HTTP Request Sent to HTTPS Port":497,"Client Closed Request":499}
iis_status={"Login Time-out":440,"Retry With":449,"Redirect":451}
unofficial_status={"Checkpoint":103,"This is fine (Apache web server)":218,"Page Expired (Laravel Framework)":419,"Method Failure (Spring Framework)":420,"Request Header Fields Too Large (Shopify)":430,"Blocked by Windows Parental Controls (Microsoft)":450,"Invalid Token (Esri)":498,"Token Required (Esri)":499,"Bandwidth Limit Exceeded (Apache Web Server/cPanel)":509,"Invalid SSL Certificate":526,"Site is overloaded":529,"Site is frozen":530," (Informal convention) Network read timeout error":598}

custom_fig = Figlet(font='block')
print(custom_fig.renderText('FinDir'))
def arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u','--url',dest = "url", help='Target URL')
	parser.add_argument('-w','--wordlist',dest = "wordlist", help='Path to Wordlist')
	parser.add_argument('-t','--thread',dest = "thread", help='Threads Counts', default=10)
	args = parser.parse_args()
	return args

args = arguments()

def load_words(): 
       with open(args.wordlist, 'r',encoding="utf-8") as f:
            # fetch one line each time, include '\n'
            for line in f:
                # strip '\n', then append it to wordlist
                words.append(line.strip())
load_words()

def bot(message):
        token = '' ##Your Telegra token
        chat_id = '' ## Your Telegra chat_id where you want to send the message
        url = "https://api.telegram.org/bot{}/sendmessage?chat_id={}&text={}".format(token,chat_id,message)
        r = requests.get(url)
        return r
        
def scan(word):
    url = args.url+'/'+word   
    session = requests.session()
    r = session.get(url)
    print(url+" - "+str(r.status_code))
    if r.status_code in success_status.values() or r.status_code==403 or r.status_code in Cloudflare_status.values() or r.status_code in info_status.values() :
        bot("[{} ] ".format(r.status_code)+url+" | Content-length: {} ".format(len(r.content)))
    elif r.status_code == 200 or r.status_code == 403 or r.status_code == 401 or r.status_code == 405 or r.status_code in info_status.values():
        bot("[!] (You might wanna take a look at this) "+url+" | Content-length: {} ".format(len(r.content)))
       

if args.thread:
    thread_count = int(args.thread)
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(scan, words)  
else:
    print('Lol')
