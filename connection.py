#Simple test for redis failures
#input - none
#output - UUID to stdout and written to DB for troubleshooting
#   timestamp to indicate start
#   one line per second (loop iteration) showing:
#       timestamp and successful write or failure with loop iteration
#   timestamp to indication stop
#   number of seconds redis was up (iterations)
#   number of seconds redis was down (iterations)
#Display every second that Redis master is working properly 
#In case of a failure, show the time in seconds Redis was not available

# Import libraries
import time
from datetime import datetime
import uuid
import redis

redisHost ='redis-oss.local'
redisPort = 6379
redisPassword = 'redispassword'
#counters for seconds up/down and number of loop iterations
upseconds = 0
downseconds = 0
n = 60

#Attempt to create initial connection to redis
#set a key with a unique id to "iniitial" (for troubleshooting)
try:
    r = redis.Redis(host=redisHost, port=redisPort, password=redisPassword)
    r.ping()
    thisinstance = str(uuid.uuid4())
    r.set(thisinstance, "initial", ex=3600)
    print(thisinstance, "Initial connection successful")
except:
    print("Can't make initial connection")

#print start time
print(format(datetime.now(), '%H:%M:%S'), "start")

#loop n times, each iteration, attempt to write to the key
#redis-alive with the iteration count
#print one line of output for each success/failure with iteration count
#update upseconds and downsecond for each iteration based
#on success/failure of write
for i in range (0, n):
    try:
        time.sleep(1)
        currenttime = datetime.now()
        r.set("redis-alive", str(currenttime))
        print(format(currenttime, '%H:%M:%S'), "successful write to database", i)
        upseconds = upseconds + 1
    except:
        print(format(currenttime, '%H:%M:%S'), "write error", i)
        downseconds = downseconds + 1

#print end time and up/down counters
print(format(datetime.now(), '%H:%M:%S'), "end")
print("redis up for", str(upseconds), "seconds")
print("redis down for", str(downseconds), "seconds")
