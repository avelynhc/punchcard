import sys
import json
import time
import os


def check_command_name():
    return sys.argv[1].lower() != 'start' and sys.argv[1].lower() != 'finish' and sys.argv[1].lower() != 'cancel' and sys.argv[1].lower() != 'get'


def has_duplicate_task(task, task_name):
    for x in task:
        if x == task_name:
            return True
    return False


def has_finish(task, finish):
    for x in task:
        if finish not in x: 
            return False
    return True


def cancel_task(task,cancel_item):
    for x in list(task):
        if cancel_item in x:
            task[cancel_item].pop()
            json.dump(data, open(filePath,'w'),indent=2)
            sys.exit("Found")


def convertTime(time):
    sec = (time/1000)%60
    min = (time/(1000*60))%60
    hr = (time/(1000*60*60))%24
    return int(sec),int(min),int(hr)


if len(sys.argv) == 1:
    print('you must pass 2 arguments')
    sys.exit()
elif len(sys.argv) == 2:
    if check_command_name():
        sys.exit('it must be start or finish')
    else:
        sys.exit('it must have project name')
elif len(sys.argv) == 3:
    if check_command_name():
        sys.exit('it must be start or finish')

print(sys.argv[1] + "ing ", sys.argv[2] + "...")

# checks if file exists
filePath = os.path.join(sys.path[0], 'data.json')
if os.path.isfile(filePath) and os.access(filePath, os.R_OK):
    print("File exists and is readable")
    # read json
    with open(filePath) as json_file:
        data = json.load(json_file)
    if sys.argv[1] == 'start':
        if has_duplicate_task(data["tasks"], sys.argv[2]):
            if has_finish(data["tasks"][sys.argv[2]],sys.argv[1]):
                with open(filePath, 'w', encoding='utf-8') as f:
                    data["tasks"][sys.argv[2]].append({sys.argv[1]: time.time()})
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
            else:
                sys.exit('You already started this project')

        else:
            with open(filePath, 'w', encoding='utf-8') as f:
                dest = {
                    sys.argv[2]: [
                        {
                            sys.argv[1]: time.time()
                        }
                    ]
                }
                data["tasks"].update(dest)
                json.dump(data, f, ensure_ascii=False, indent=2)

    elif sys.argv[1] == 'finish':
        if has_duplicate_task(data["tasks"], sys.argv[2]):
            if has_finish(data["tasks"][sys.argv[2]],sys.argv[1]):
                sys.exit("You do not have unfinished project named " + sys.argv[2])
            else:
                print("adding finishing time")
                with open(filePath, 'w', encoding='utf-8') as f:
                    last_index = len(data["tasks"][sys.argv[2]]) - 1
                    data["tasks"][sys.argv[2]][last_index][sys.argv[1]] = time.time()
                    json.dump(data, f, ensure_ascii=False, indent=2)

        else:
            sys.exit("You do not have unfinished project named " + sys.argv[2])

    elif sys.argv[1] == 'cancel':
        if has_finish(data["tasks"][sys.argv[2]],"finish") == False:
            cancel_task(data["tasks"],sys.argv[2])
            sys.exit("Project Not Found")
        else:
            sys.exit("Not Authorized")

    elif sys.argv[1] == 'get':
        if has_finish(data["tasks"][sys.argv[2]],"finish"):  
            timeDiff = 0
            for x in data["tasks"][sys.argv[2]]:
                startTime = x["start"]*1000
                finishTime = x["finish"]*1000
                timeDiff += finishTime - startTime
            sec, min, hr = convertTime(int(timeDiff))
            print("{} hr {} min {} sec".format(hr, min, sec))

        else:
            sys.exit("You have not finished project named " + sys.argv[2])


else:
    print("Either file is missing or is not readable, creating file...")
    info = {
        "tasks": {
            sys.argv[2]: [
                {
                    sys.argv[1]: time.time()
                }
            ]
        }
    }

    with open(filePath, 'w') as json_file:
        json.dump(info, json_file, ensure_ascii=False, indent=2)