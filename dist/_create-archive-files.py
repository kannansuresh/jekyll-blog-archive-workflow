import re
import os
import json
import pathlib
import requests

archive_data_url = 'https://aneejian.com/archives/archivedata'
json_data = json.loads(requests.get(archive_data_url).content)

archive_types = {
    'year': 'years',
    'tag': 'tags',
    'category': 'categories'
}


def createfrontmatter(archive_s_form, archive_p_form, archive_item_value, archive_value_escaped):
    front_matter_template = f'''
---
title: {archive_item_value}
{archive_s_form}: "{archive_item_value}"
layout: archive-{archive_p_form}
permalink: "{archive_s_form}/{archive_value_escaped}"
---
'''
    return front_matter_template

added_files = []
removed_files = []
for type in archive_types.keys():
    file_list = []
    archive_type = archive_types[type]
    for archive_value in list(set(json_data[archive_type])):
        value_escaped = re.sub(r'\s|\.', '-', archive_value)
        value_escaped = re.sub(r'#', 'sharp', value_escaped)
        value_escaped = re.sub(r'[^a-z0-9A-Z_]', '-', value_escaped)
        value_escaped = value_escaped.lower()
        frontmatter = createfrontmatter(
            type, archive_type, archive_value, value_escaped)
        file_name = value_escaped + '.md'
        file_list.append(file_name)
        file_path = archive_type + '/' + file_name
        if not os.path.exists(file_path):            
            pathlib.Path(archive_type).mkdir(
                parents=True, exist_ok=True)
            with open(file_path, 'w') as archivefile:
                archivefile.writelines(frontmatter)
            added_files.append(archive_type + ': ' + file_name)
    all_files = os.listdir(archive_type)
    for archive_file in all_files:
        if archive_file not in file_list:            
            os.remove(archive_type + '/' + archive_file)
            removed_files.append(archive_type + ": " + archive_file)

if len(added_files) > 0:
    print('Added files:')
    for file_info in added_files:
        print(file_info)

if len(removed_files) > 0:
    print('Removed files:')
    for file_info in removed_files:
        print(file_info)