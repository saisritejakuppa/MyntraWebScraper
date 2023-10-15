import os
from glob import glob

path = '/home/girish/teja/virtualtryon/data'

# all json files
json_files = glob(os.path.join(path, '*', 'meta.json'))

import json
data = []
all_names = []
for json_file in json_files:
    with open(json_file) as f:
        info_json = json.load(f)
        all_names.extend(info_json['name'].split(' '))
        
# get the unq names and counts of each
from collections import Counter
name_counts = Counter(all_names)
print(name_counts)
print(len(name_counts))


print(all_names[1])