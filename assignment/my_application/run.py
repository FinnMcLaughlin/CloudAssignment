import os

#1 List all containers
def list_containers():
	os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')
	print '\n\n'
	menu()

#2 List running containers
def list_run_containers():
	os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers?state=running | python -mjson.tool')
	print '\n\n'
	menu()

#3 List specific containers
def list_specific_container():
	print 'List of all containers to choose from:\n'

	os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')
	id = raw_input('Enter container id: ')
	os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers/' + id + ' | python -mjson.tool')
	print '\n\n'
	menu()

#4 List container logs
def list_container_logs():
	print '--Container Logs'
        print 'List of all containers to choose from:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')

        id = raw_input('Enter container id: ')
	os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers/11d1c9947029/logs | python -mjson.tool')
	print '\n\n'
	menu()

#5 Delete specific container
def delete_container():
	print '--Delete Container'
        print 'List of all containers to choose from:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')

	id = raw_input('Enter container id: ')
        os.system('curl -s -X DELETE -H \'Accept: application/json\' http://localhost:8080/containers/' + id + ' | python -mjson.tool')

        print 'Update list of containers:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')

        print '\n\n'
        menu()

#6 Delete all containers
def delete_all_containers():
        print '--Delete All Containers'
        os.system('curl -s -X DELETE -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')

        print 'Update list of containers:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')

	print '\n\n'
        menu()

#7 List all images
def list_images():
        print '---All Images'
	os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/images | python -mjson.tool')
        print '\n\n'
        menu()

#8. Delete specific image
def delete_image():
        print '--Delete Image'
        print 'List of all images to choose from:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/images | python -mjson.tool')

	id = raw_input('Enter image id: ')
        os.system('curl -s -X DELETE -H \'Accept: application/json\' http://localhost:8080/images/' + id + ' | python -mjson.tool')

        print 'Update list of images:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/images | python -mjson.tool')
        print '\n\n'
        menu()

#9 Delete all images
def delete_all_images():
        print '--Delete All Images'
        os.system('curl -s -X DELETE -H \'Accept: application/json\' http://localhost:8080/images | python -mjson.tool')

        print 'Update list of images:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/images | python -mjson.tool')
        print '\n\n'
        menu()

#10 Create container
def create_container():
        print '--Create Container'
        print 'List of all images to choose from:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/images | python -mjson.tool')
        id = raw_input('Enter images id: ')
    	os.system('curl -X POST -H \'Content-Type: application/json\' http://localhost:8080/containers -d \'{\"image\": \"' + id + '\"}\'')
        print '\n\n'
        menu()

#11 Create Image
def create_image():
        print '--Create Image'
        #Not implemented correctly yet
	print 'Coming soon'
        print '\n\n'
        menu()

#12 Update container status
def update_container():
	print '--Update Container Status'
        print 'List of all containers to choose from:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool')
        state = raw_input('Do you want to 1.start or 2.stop a container: ')
	if state == '1':
		id = raw_input('Enter container id: ')
		os.system('curl -X PATCH -H \'Content-Type: application/json\' http://localhost:8080/containers/' + id + ' -d \'{"state": "running"}\'')
	elif state == '2':
                id = raw_input('Enter container id: ')
                os.system('curl -X PATCH -H \'Content-Type: application/json\' http://localhost:8080/containers/' + id + ' -d \'{"state": "stopped"}\'')

        print '\n\n'
        menu()


#13 Update image tag
def update_image():
        print '--Update Image Tag'
        print 'List of all images to choose from:\n'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/images | python -mjson.tool')

        id = raw_input('Enter image id: ')
        name = raw_input('Enter new image name: ')
	tag = raw_input('Enter new image  tag: ')
	os.system('curl -s -X PATCH -H \'Content-Type: application/json\' http://localhost:8080/images/' + id + ' -d \'{\"tag\": \"' + name + ':' + tag + '\"}\'')
	print '\n\n'
        menu()

#14 List all nodes
def list_nodes():
	print '--List All Nodes'
	os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/nodes | python -mjson.tool')
        print '\n\n'
        menu()

#15 List services
def list_services():
        print '--List All Services'
        os.system('curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/service | python -mjson.tool')
        print '\n\n'
        menu()

def menu():
    	print("----------------Menu----------------")
	print '1. List all containers\t\t2. List all running containers\t\t3. List specific containers'
	print '4. List container logs\t\t5. Delete specific container\t\t6. Delete all containers (Dangerous)'
	print '7. List all images\t\t8. Delete specific image\t\t9. Delete all image (Dangerous)'
	print '10. Create container\t\t11. Create image\t\t\t12. Update container status'
	print '13. Update image tag\t\t14. List all nodes\t\t\t15. List all services'
	input = raw_input('What do you want to do: ')


	if input == '1':
		list_containers()
	elif input == '2':
		list_run_containers()
	elif input == '3':
		list_specific_container()
	elif input == '4':
		list_container_logs()
	elif input == '5':
		delete_container()
	elif input == '6':
		delete_all_containers()
	elif input == '7':
		list_images()
	elif input == '8':
		delete_image()
	elif input == '9':
		delete_all_images()
	elif input == '10':
		create_container()
	elif input == '11':
		create_image()
	elif input == '12':
		update_container()
	elif input == '13':
		update_image()
	elif input == '14':
		list_nodes()
	elif input == '15':
		list_services()
	elif input == '0':
		exit()


menu()
