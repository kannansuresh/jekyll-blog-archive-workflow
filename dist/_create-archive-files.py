import re
import os
import json
import shutil
import pathlib
import requests

archive_types = {
    'year': 'years',
    'tag': 'tags',
    'category': 'categories'
}

input_options = ['delete_archives', 'delete_archives_folder']

def createfrontmatter(archive_s_form, archive_p_form, archive_item_value, archive_value_escaped):
    front_matter_template = f'''---
title: {archive_item_value}
{archive_s_form}: "{archive_item_value}"
layout: archive-{archive_p_form}
permalink: "{archive_s_form}/{archive_value_escaped}"
---
'''
    return front_matter_template

if __name__ == '__main__':
    from sys import argv, stderr
    if len(argv) < 2:
        print("Usage: {} archive_url archive_folder_path".format(argv[0]), file=stderr)        
        exit(1)

    archive_data_url = argv[1]
    archive_folder_path = argv[2]

    if archive_data_url in input_options :
        for type in archive_types.keys():
            if archive_data_url == 'delete_archives_folder':
                folder_name = archive_folder_path
            else:
                folder_name = archive_folder_path + '/' + archive_types[type]
            if os.path.exists(folder_name):
                shutil.rmtree(folder_name)
                print('Deleted files in the archive', folder_name + '.')
    else:
        
        try:
            json_data = json.loads(requests.get(archive_data_url).content)
        except ConnectionError as identifier:
            print('Connection error.')
            exit(1)
        except:
            print('Failed to fetch information.')
            exit(1)

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
                file_path = archive_folder_path + '/' + archive_type + '/' + file_name
                if not os.path.exists(file_path):            
                    pathlib.Path(archive_folder_path + '/' + archive_type).mkdir(
                        parents=True, exist_ok=True)
                    with open(file_path, 'w') as archivefile:
                        archivefile.writelines(frontmatter)
                    added_files.append(archive_type + ': ' + file_name)
            all_files = os.listdir(archive_folder_path + '/' +archive_type)
            for archive_file in all_files:
                if archive_file not in file_list:            
                    os.remove(archive_folder_path + '/' +archive_type + '/' + archive_file)
                    removed_files.append(archive_type + ": " + archive_file)

        if len(added_files) > 0:
            print('Added files:')
            for file_info in added_files:
                print(file_info)

        if len(removed_files) > 0:
            print('Removed files:')
            for file_info in removed_files:
                print(file_info)