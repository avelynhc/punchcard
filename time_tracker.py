import sys
import json
import time

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

with open('data.json') as json_file:
    data = json.load(json_file)

    dest = {
        sys.argv[2]: [
            {
                sys.argv[1] : time.time()
            }
        ]
    }
    data['tasks'].update(dest)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
