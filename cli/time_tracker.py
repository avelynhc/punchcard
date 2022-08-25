import sys
import json
import os
import argparse
from datetime import datetime

from lib.task_manager import TaskManager

parser = argparse.ArgumentParser()
parser.add_argument('x', type=str, help='Action')
parser.add_argument('y', type=str, help='Name of task')
parser.add_argument('--From', type=str)
parser.add_argument('--To', type=str)
args = parser.parse_args()
if args.From and args.To:
    print("You want to display data from", args.From, 'to', args.To)
if args.x.lower() == 'get':
    if args.From is not None and args.To is not None:
        Fromtimestamp = datetime.strptime(args.From, "%Y/%m/%d").replace(hour=12,minute=0).timestamp()
        Totimestamp = datetime.strptime(args.To, "%Y/%m/%d").replace(hour=23,minute=59,second=59).timestamp()
        print("Fromtimestamp:", Fromtimestamp)
        print("Totimestamp:", Totimestamp)
    else:
        sys.exit("You need to enter '--From YYYY/MM/DD --To YYYY/MM/DD'")


def check_command_name():
    return args.x.lower() != 'start' and args.x.lower() != 'finish' and args.x.lower() != 'cancel' and args.x.lower() != 'get'

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
data = {}
if os.path.isfile(filePath) and os.access(filePath, os.R_OK):
    with open(filePath) as json_file:
        data = json.load(json_file)

task_manager = TaskManager()
task_manager.parse_data(data)
if args.x == 'start':
    msg = task_manager.start_task(args.y)
elif args.x == 'finish':
    msg = task_manager.finish_task(args.y)
elif args.x == 'cancel':
    msg = task_manager.cancel_task(args.y)
elif args.x == 'get':
    msg = task_manager.get_task(args.y, int(Fromtimestamp), int(Totimestamp))

print(msg)
with open(filePath, 'w', encoding='utf-8') as f:
    data = task_manager.to_json()
    json.dump(data, f, ensure_ascii=False, indent=2)
