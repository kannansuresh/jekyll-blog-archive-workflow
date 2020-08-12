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


def create_front_matter(archive_s_form, archive_p_form, archive_item_value, archive_value_escaped):
    front_matter_template = f'''---
title: {archive_item_value}
{archive_s_form}: "{archive_item_value}"
layout: archive-{archive_p_form}
permalink: "{archive_s_form}/{archive_value_escaped}"
---
'''
    return front_matter_template


def delete_folder(folder_path, out_message):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(out_message, folder_path + '.')
        return True
    else:
        print('Cannot find the folder', folder_path + '.')
        return False


if __name__ == '__main__':
    from sys import argv, stderr

    if len(argv) < 2:
        print("Usage: {} archive_url archive_folder_path".format(argv[0]), file=stderr)
        exit(1)

    archive_data_url = argv[1]
    archive_folder_path = argv[2]

    if archive_data_url in input_options:
        delete_folder_error = False
        for arch_type in archive_types.keys():
            if archive_data_url == input_options[1]:
                folder_name = archive_folder_path
                msg = 'Deleted the folder'
                deleted = delete_folder(folder_name, msg)
                delete_folder_error = not deleted
                break
            else:
                folder_name = archive_folder_path + '/' + archive_types[arch_type]
                msg = 'Deleted files in the folder'
                deleted = delete_folder(folder_name, msg)
                delete_folder_error = not deleted or delete_folder_error
        if delete_folder_error:
            exit(1)

    else:
        json_data = json.loads('{}')
        try:
            json_data = json.loads(requests.get(archive_data_url).content)
        except requests.RequestException as request_exception:
            print('Request error. Check input archive_url. Passed variable:', archive_data_url + '.', request_exception)
            exit(1)
        except ValueError as value_error:
            print('JSON Error. Check input variable archive_url. Passed variable', archive_data_url + '.', value_error)
            exit(1)

        added_files = []
        removed_files = []
        for arch_type in archive_types.keys():
            file_list = []
            archive_type = archive_types[arch_type]
            for archive_value in list(set(json_data[archive_type])):
                value_escaped = re.sub(r'\s|\.', '-', archive_value)
                value_escaped = re.sub(r'#', 'sharp', value_escaped)
                value_escaped = re.sub(r'[^a-z0-9A-Z_]', '-', value_escaped)
                value_escaped = value_escaped.lower()
                front_matter = create_front_matter(
                    arch_type, archive_type, archive_value, value_escaped)
                file_name = value_escaped + '.md'
                file_list.append(file_name)
                file_path = archive_folder_path + '/' + archive_type + '/' + file_name
                if not os.path.exists(file_path):
                    pathlib.Path(archive_folder_path + '/' + archive_type).mkdir(parents=True, exist_ok=True)
                    with open(file_path, 'w') as archive_md_file:
                        archive_md_file.writelines(front_matter)
                    added_files.append(archive_type + ': ' + file_name)
            all_files = os.listdir(archive_folder_path + '/' + archive_type)
            for archive_file in all_files:
                if archive_file not in file_list:
                    os.remove(archive_folder_path + '/' + archive_type + '/' + archive_file)
                    removed_files.append(archive_type + ": " + archive_file)

        if len(added_files) > 0:
            print('Added archive files:')
            for file_info in added_files:
                print(file_info)
        else:
            print('No archive files to add.')


        if len(removed_files) > 0:
            print('Removed archive files:')
            for file_info in removed_files:
                print(file_info)
        else:
            print('No archive files to remove.')
