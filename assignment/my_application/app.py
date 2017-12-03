from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return """
Available API endpoints:\n
GET /containers                     List all containers
GET /containers?state=running      List running containers (only)
GET /containers/<id>                Inspect a specific container
GET /containers/<id>/logs           Dump specific container logs
GET /images                         List all images
POST /images                        Create a new image
POST /containers                    Create a new container
PATCH /containers/<id>              Change a container's state
PATCH /images/<id>                  Change a specific image's attributes
DELETE /containers/<id>             Delete a specific container
DELETE /containers                  Delete all containers (including running)
DELETE /images/<id>                 Delete a specific image
DELETE /images                      Delete all images
"""

@app.route('/containers', methods=['GET'])
def containers_index():
    """
    List all containers

    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool
    """
    #Only display running containers
    if request.args.get('state') == 'running':
	output = docker('ps')
	resp = json.dumps(docker_ps_to_array(output))
    #Display all containers
    else:
	output = docker('ps', '-a')
	resp = json.dumps(docker_ps_to_array(output))


    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['GET'])
def images_index():
    """
    List all images
    """
    #Display images
    output = docker('images')
    resp = json.dumps(docker_images_to_array(output))

    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    """

    List container based on ID

    """
    #Inspect certain container
    output = docker('inspect', id)
    resp = output

    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>/logs', methods=['GET'])
def containers_log(id):
    """
    Dump specific container logs
    """
    #Display certain container's log
    output = docker('logs', id)
    resp = json.dumps(docker_logs_to_object(id, output))

    return Response(response=resp, mimetype="application/json")


@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
    """
    Delete a specific image

    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/images/<id> | python -mjson.tool
    """
    #Remove certain image based on id
    #Get all running containers and add to array of containers
    output = docker('ps')
    all = docker_ps_to_array(output)

    #Run through all containers in array
    for containers in all:
    	#If image is being used by running container then call 
	#function to stop and remove container
	#Then remove image based on id
	if id == containers["image"]:
    		containers_remove(containers["id"])
		docker('rmi', id)
    		resp = '{"id": "%s"}' % id
	else:
		resp = '{"id": "FAILED"}'

    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):
    """
    Delete a specific container - must be already stopped/killed
    """
    #Stop container if it is running
    #Remove container based on id
    docker ('stop', id)
    docker ('rm', id)
    resp = '{"id": "%s"}' % id

    return Response(response=resp, mimetype="application/json")

@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
    """
    Force remove all containers - dangrous!
    """
    #Get all containers and put them in array
    all = docker('ps', '-a')
    array = []
    array = docker_ps_to_array(all)

    #Go through container array
    #Stop and delete containers based on each id
    for containers in array:
	id = containers["id"]
	docker('stop', id)
	docker('rm', id)

    return 'All containers deleted'

@app.route('/images', methods=['DELETE'])
def images_remove_all():
    """
    Force remove all images - dangrous!
    """
    #Get all images and put them in array 
    all = docker('images', '-a')
    array = []
    array = docker_ps_to_array(all)

    #Go through image array
    #Delete images based on each id
    for images in array:
	id = images["id"]
	docker('rmi', id)

    return 'Deleted all images'


@app.route('/containers', methods=['POST'])
def containers_create():
    """
    Create container (from existing image using id or name)
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "my-app"}'
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e"}'
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e","publish":"8081:22"}'
    """

    body = request.get_json(force=True)
    image = body['image']
    args = ('run', '-d')
    id = docker(*(args + (image,)))[0:12]

    return Response(response='{"id": "%s"}\n' % id, mimetype="application/json")


@app.route('/images', methods=['POST'])
def images_create():
    """
    Create image (from uploaded Dockerfile)
    curl -H 'Accept: application/json' -F file=@Dockerfile http://localhost:8080/images
    """

    try:
	#Get docker file from path
	dockerfile = request.files['file']
	#Build image
    	docker("build", "-t", "testcreate:100", ".")
	resp = "Image created"

    except:
	resp = "Failed to create image\n"
	pass

    return Response(response=resp, mimetype="application/json")


@app.route('/containers/<id>', methods=['PATCH'])
def containers_update(id):
    """
    Update container attributes (support: state=running|stopped)
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "running"}'
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "stopped"}'
    """
    body = request.get_json(force=True)

    try:
        state = body['state']
        #Checks curl query state
	#If state is running restart container based on id
	if state == 'running':
            docker('restart', id)
	#If state is stopped stop container based on id
	elif state == 'stopped':
		docker('stop', id)
    except:
        pass

    #Return container who's state was changed
    resp = '{"id": "%s"}\n' % id
    return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
    """
    Update image attributes (support: name[:tag])  tag name should be lowercase only
    curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/7f2619ed1768 -d '{"tag": "test:1.0"}'
    """

    body = request.get_json(force=True)

    try:
	state = body['tag']
        #Get all images and put in image array
	output = docker('images')
	all = docker_images_to_array(output)
	#Check all images in image array until id matches
	for images in all:
		if id == images["id"]:
			#Add tag to specific image and remove old image tag
			docker('tag', id, state)
			oldstate = (images["name"] + ":" + images["tag"])
			docker('rmi', oldstate)
			resp = '{"new tag": "%s"}\n{"removed tag": "%s"}\n' %(state, oldstate)
    except:
	resp = 'Failed'
	pass

    return Response(response=resp, mimetype="application/json")

@app.route('/nodes', methods=['GET'])
def all_nodes():
    #Get all nodes
    output = docker('node', 'ls')
    resp = json.dumps(docker_ps_to_array(output))

    return Response(response=resp, mimetype="application/json")

@app.route('/service', methods=['GET'])
def all_services():
    #Get all services
    output = docker('service', 'ls')
    resp = json.dumps(docker_ps_to_array(output))

    return Response(response=resp, mimetype="application/json")

def docker(*args):
    cmd = ['docker']
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr.startswith('Error'):
        print 'Error: {0} -> {1}'.format(' '.join(cmd), stderr)
    return stderr + stdout

# 
# Docker output parsing helpers
#

#
# Parses the output of a Docker PS command to a python List
# 
def docker_ps_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['image'] = c[1]
        each['name'] = c[-1]
        each['ports'] = c[-2]
        all.append(each)
    return all

#
# Parses the output of a Docker logs command to a python Dictionary
# (Key Value Pair object)
def docker_logs_to_object(id, output):
    logs = {}
    logs['id'] = id
    all = []
    for line in output.splitlines():
        all.append(line)
    logs['logs'] = all
    return logs

#
# Parses the output of a Docker image command to a python List
# 
def docker_images_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[2]
        each['tag'] = c[1]
        each['name'] = c[0]
        all.append(each)
    return all

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)
