import sys 
import json
import time
import io
import os

def checkCommandName():
    return sys.argv[1].lower() != 'start' and sys.argv[1].lower() != 'finish'

if len(sys.argv) == 1:
    print('you must pass 2 arguments')
    sys.exit()
elif len(sys.argv) == 2:
    if checkCommandName():
        sys.exit('it must be start or finish')
    else:
       sys.exit('it must have project name')
elif len(sys.argv) == 3:
    if checkCommandName():
        sys.exit('it must be start or finish')

print(sys.argv[1] + "ing ", sys.argv[2] + "...")

# checks if file exists
if os.path.isfile('C:/Users/Hyunjeong Choi/source/repos/time_tracker_python/data.json') and os.access('C:/Users/Hyunjeong Choi/source/repos/time_tracker_python/data.json', os.R_OK):
    print ("File exists and is readable")
    # read json
    with open('data.json') as json_file:
        data = json.load(json_file)

        for x in data["tasks"]:
            if x == sys.argv[2]:
                sys.exit('You already started this project')

        with open('data.json', 'w', encoding='utf-8') as f:
            dest = {
                sys.argv[2]: [
                    {
                        sys.argv[1] : time.time()
                    }
                ]
            }
            data["tasks"].update(dest)
            json.dump(data, f, ensure_ascii=False, indent=2)
    
else:
    print ("Either file is missing or is not readable, creating file...")
    # create a file
    with io.open(os.path.join('C:/Users/Hyunjeong Choi/source/repos/time_tracker_python', 'data.json'), 'w') as json_file:
        json_file.write(json.dumps({}))

    info = {
        "tasks":{
            sys.argv[2]: [
                {
                    sys.argv[1] : time.time()
                }
            ]
        }
    }

    with open('data.json', 'w') as json_file:
        json.dump(info, json_file)
