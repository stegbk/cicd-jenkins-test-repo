import jenkins
import sys
import time

jenkins_url = 'http://jenkins-loop.internal.elasticbox.com:8080'
job_name = 'TestJenkinsBuild'
server = jenkins.Jenkins(jenkins_url, username='s@elasticbox.com', password='7d8e01a409b086ce29134fa1b3ed39ba')
next_build_number = server.get_job_info(job_name)['nextBuildNumber']
print(next_build_number)

# Wait for an empty queue
#  These really need to get refactored since
#  we have three basically identical
#  waiting loops here.
empty = False
iteration = 0
while empty == False and iteration < 1000:
    time.sleep(1)
    qi = server.get_queue_info()    
    if len(server.get_queue_info()) == 0:
        empty=True
    iteration = iteration + 1

if empty == False:
    print("Waited for 1000 seconds and the queue didn't empty")
    print("failing the test")
    sys.exit(1)
    
# Kick off the build
server.build_job(job_name)
# This build always takes at least 10 seconds,  wait 5 to make
# sure it's been placed in the queue/is running or jenkins
# won't return in either list
time.sleep(5)

queued = True
iteration = 0
while queued == True and iteration < 1000:
    time.sleep(1)
    queued_jobs = server.get_queue_info()
    if len(queued_jobs) == 0:
        queued = False
    iteration = iteration + 1
    
if queued == True:
    print("Waited 1000 seconds for the build to be unqueued,  didn't happen")
    print("Failing test")
    sys.exit(1)

# The build has left the queue.  Wait for the build to complete
found = False
finished = False
iteration = 0

while finished == False and iteration < 100:
    iteration = iteration + 1
    time.sleep(0.5)
    builds = server.get_running_builds()
    if found == True and len(builds) == 0:
        finished = True
    for bld in range(0, len(builds)):
        if builds[bld]['name'] == job_name and builds[bld]['number'] == next_build_number:
            found = True
        elif found == True and finished == False:
            finished = True

if finished != True:
    sys.exit(1)
else:
    sys.exit(0)




