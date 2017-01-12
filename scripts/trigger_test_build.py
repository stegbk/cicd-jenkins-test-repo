import jenkins
import wget
import sys

jenkins_url = 'http://jenkins-loop.internal.elasticbox.com:8080'
job_name = 'TestJenkinsBuild'
server = jenkins.Jenkins(jenkins_url, username='s@elasticbox.com', password='7d8e01a409b086ce29134fa1b3ed39ba')
next_build_number = server.get_job_info(job_name)['nextBuildNumber']
server.build_job(job_name)
print(next_build_number)
found = False
finished = False
iteration = 0


while finished == False and iteration < 100:
    iteration = iteration + 1
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
#url = jenkins_url+'/job/'+job_name+'/lastSuccessfulBuild/artifact/PrintCompileTimeNumber/dist/PrintCompileTimeNumber.jar'
#filename = wget.download(url)

