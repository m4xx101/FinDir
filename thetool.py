
#!/usr/bin/python
import argparse
import os 
import sys
# import commands
import requests
import concurrent.futures

threads = []
words=[]
files = [".vscode","config.yaml",".gitignore",".svn/wc.db",".git/config", "phpmyadmin/", ".travis.yml",".DS_Store",".htaccess",".htpasswd","Makefile","Dockerfile","package.json","gulpfile.js","composer.json","web.config",".env",".idea","nbproject/","bower.json","package-lock.json",".gitlab-ci.yml","database.yml"]

def arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u','--url',dest = "url", help='Target URL')
	parser.add_argument('-w','--wordlist',dest = "wordlist", help='Path to Wordlist')
	parser.add_argument('-t','--thread',dest = "thread", help='Threads Counts', default=10)
	args = parser.parse_args()
	return args

args = arguments()
with open(args.wordlist, 'r',encoding="utf8") as file:
  a = file.readlines()
  for i in a:
      words.append(i.strip())
#   print(a)
#   for i in a:
#       words.append(i.strip())

def bot(message):
        token = '' ##Your Telegra token
        chat_id = '' ## Your Telegra chat_id where you want to send the message
        endpoint='"https://api.telegram.org/bot'+token+'/sendmessage?chat_id='+chat_id+'&text='+message+'"'
        print(endpoint)
        cmd = requests.get(endpoint)
        return cmd

# with open(args.wordlist, 'r',encoding="utf8") as file:
# 	a = file.readlines()
# 	for i in a:
# 		words.append(i.strip())
# for i in len(word_list):
#     words.append(word_list[i])

def scan(word):
    for i in words:
        url = args.url+'/'+words[i]
        response = requests.get(url)
        print(url)
        # if response.status_code == 200:
        bot(url)	
        # else:
        bot('working-at-least!')

if args.thread:
    thread_count = int(args.thread)
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(scan, words)  
else:
    print('Lol')


    

    
