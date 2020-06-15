

import os.path
import json 

def readConfig():

    if os.path.exists('user_data/config.json'):
        with open('user_data/config.json') as json_file:
            return json.load(json_file)
    else:
        raise Exception("config.json file is not in user_data folder")