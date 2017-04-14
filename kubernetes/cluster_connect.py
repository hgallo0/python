#!/usr/local/bin/python

import os
import sys
import psutil
import subprocess

def usage():
  os.system("clear")
  print "Plese provide your project id"
  print "usage\n ./cluster_connect.py my-google-project-1234567\n\n"

# ensure project id has been passed 
if len(sys.argv) < 2:
  usage()
  sys.exit(1)
elif len(sys.argv) == 2:
  project_id = sys.argv[1]
  print "your project id is: ", project_id

# record kubectl proxy PID
result = subprocess.Popen(['pgrep -f "kubectl proxy" | grep -v grep'], stdout=subprocess.PIPE, shell=True)
PID = result.communicate()[0]

# kill any existing kubectl proxy service
if PID:
  print "killing existing process"
  # convert output to integer
  p = int(PID)

  # kill process 
  p = psutil.Process(p)
  p.terminate()

# get clusters
command = "gcloud container clusters list | grep -v NAME | awk '{print $1, \" --zone \" $2}'"
process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True).communicate()[0]

# change output to list
LIST = process.split("\n")

# menu list
print "select from the list below: "
for i in LIST:
  print LIST.index(i), " ",  (i)

# input selection
try:
  choice = int(input("selection: "))
except (RuntimeError, TypeError, NameError, ValueError):
  print("Please use an integer selection ")
  quit()

if choice > len(LIST):
  print "You have selected a number not listed in the options"
  quit()
else:
  print "connecting to " + LIST[choice]
  connect = "gcloud container clusters get-credentials " + LIST[choice] +  " --project " + project_id
  process = subprocess.Popen([connect], stdout=subprocess.PIPE, shell=True).communicate()[0]

  # open kubectl proxy as a background process 
  pid = os.fork()
  if pid == 0:
    # Child
    os.setsid()  # This creates a new session
    print "kubectl proxy In background:", os.getpid()
    subprocess.Popen(['kubectl proxy'], stdout=subprocess.PIPE, shell=True).communicate()[0]
