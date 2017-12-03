import subprocess

print("--------------Menu----------")

def list_containers():
	command = 'curl -s -X GET -H \'Accept: application/json\' http://localhost:8080/containers | python -mjson.tool'
	print subprocess.check_output(['curl', '-s', '-X', 'GET', '-H', '\'Accept:', 'application/json\'', 'hhtp://localhost:8080/containers'])

def menu():
    	print '1. List All containers\t2. List specific containers\n'

	input = raw_input('What do you want to do: ')


	if input == '1':
		list_containers()


menu()
