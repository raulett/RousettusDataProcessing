import os
from datetime import datetime


def get_app_version(version_first=None):
    current_path = os.path.dirname(os.path.abspath(__file__)).split('\\')
    root_path = '\\'.join(current_path[0: len(current_path) - 1]) + "\\"
    metadata_file = open(os.path.join(root_path, 'metadata.txt'), 'r')
    lines = metadata_file.readlines()
    metadata_file.close()
    version_line_num = [index for index, string in enumerate(lines) if 'version=' in string][0]
    version = lines[version_line_num].strip().split('=')[1].split(' build ')
    version_first = version[0].split('.')
    version_date = datetime.strptime(version_first[len(version_first)-1], '%Y%m%d')
    if version_date.date() == datetime.now().date():
        build_num = int(version[1]) + 1
    else:
        version_first[2] = datetime.now().strftime('%Y%m%d')
        build_num = 0
    version_first = '.'.join(version_first)
    lines[version_line_num] = 'version=' + version_first + ' build ' + str(build_num) + '\n'
    metadata_file = open(os.path.join(root_path, 'metadata.txt'), 'w')
    for line in lines:
        metadata_file.write(line)
    metadata_file.close()
    print('metadata.txt updated')

