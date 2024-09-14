import json
def printC(*value):
    for el in value:
        if type(el) == list or type(el) == dict:
            print(json.dumps(el, indent=4))
        else:
            print(el)
            