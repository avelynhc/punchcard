import sys
import json
import time
import os
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('x', type=str, help='Action')
parser.add_argument('y', type=str, help='Name of task')
parser.add_argument('--From', type=str)
parser.add_argument('--To', type=str)
args = parser.parse_args()
if args.From and args.To:
    print('You want to display data from', args.From, 'to', args.To)
Fromtimestamp = datetime.datetime.strptime(args.From, "%Y/%m/%d").timestamp()
Totimestamp = datetime.datetime.strptime(args.To, "%Y/%m/%d").timestamp()
print(Fromtimestamp)
print(Totimestamp)


def check_command_name():
    return args.x.lower() != 'start' and args.x.lower() != 'finish' and args.x.lower() != 'cancel' and args.x.lower() != 'get'


def has_duplicate_task(tasks, task_name):
    for task in tasks:
        if task == task_name:
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

# check arguments
if len(sys.argv) == 1:
    print('you must pass 2 arguments')
    sys.exit()
elif len(sys.argv) == 2:
    if check_command_name():
        sys.exit('it must be start,finish or get')
    else:
        sys.exit('it must have project name')
elif len(sys.argv) == 3:
    if check_command_name():
        sys.exit('it must be start,finish or get')

print(args.x + "ing",args.y + "...")

# checks if file exists
filePath = os.path.join(sys.path[0], 'data.json')
if os.path.isfile(filePath) and os.access(filePath, os.R_OK):
    print("File exists and is readable")
    # read json
    with open(filePath) as json_file:
        data = json.load(json_file)
    if args.x == 'start':
        if has_duplicate_task(data["tasks"], args.y):
            if has_finish(data["tasks"][args.y],args.x):
                with open(filePath, 'w', encoding='utf-8') as f:
                    data["tasks"][args.y].append({args.x: time.time()})
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
            else:
                sys.exit('You already started this project')

        else:
            with open(filePath, 'w', encoding='utf-8') as f:
                dest = {
                    args.y: [
                        {
                            args.x: time.time()
                        }
                    ]
                }
                data["tasks"].update(dest)
                json.dump(data, f, ensure_ascii=False, indent=2)

    elif args.x == 'finish':
        if has_duplicate_task(data["tasks"], args.y):
            if has_finish(data["tasks"][args.y],args.x):
                sys.exit("You do not have unfinished project named " + args.y)
            else:
                print("adding finishing time")
                with open(filePath, 'w', encoding='utf-8') as f:
                    last_index = len(data["tasks"][args.y]) - 1
                    data["tasks"][args.y][last_index][args.x] = time.time()
                    json.dump(data, f, ensure_ascii=False, indent=2)

        else:
            sys.exit("You do not have unfinished project named " + args.y)

    elif args.x == 'cancel':
        if has_finish(data["tasks"][args.y],"finish") == False:
            cancel_task(data["tasks"],args.y)
            sys.exit("Project Not Found")
        else:
            sys.exit("Not Authorized")

    elif args.x == 'get':
        if has_finish(data["tasks"][args.y],"finish"):  
            timeDiff = 0
            for task in data["tasks"][args.y]:
                if task["start"] >= Fromtimestamp and Totimestamp >= task["finish"]:
                    startTime = task["start"]*1000
                    finishTime = task["finish"]*1000
                    timeDiff += finishTime - startTime
            if timeDiff > 0:
                sec, min, hr = convertTime(int(timeDiff))
                print("{} hr {} min {} sec".format(hr, min, sec))
            else:
                sys.exit("You have no data available between two values")

        else:
            sys.exit("You have not finished project named " + args.y)


else:
    print("Either file is missing or is not readable, creating file...")
    info = {
        "tasks": {
            args.y: [
                {
                    args.x: time.time()
                }
            ]
        }
    }

    with open(filePath, 'w') as json_file:
        json.dump(info, json_file, ensure_ascii=False, indent=2)