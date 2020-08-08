import os
import shutil
   
archive_types = {
    'year': 'years',  
    'tag': 'tags',
    'category': 'categories'
}

for type in archive_types.keys():
    folder_name = archive_types[type]
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
        print('Deleted files in the archive', folder_name + '.')