import os
import re
import shutil
import compile_script
import datetime
import get_app_version

plugin_folder_name = "RousettusDataProcessing"

compile_script.compile_files()
qgis_plugins_path = os.environ["QGIS_PLUGINPATH"]

print("QGIS plugin path is: {}".format(qgis_plugins_path))

current_path = os.path.dirname(os.path.abspath(__file__)).split(os.sep)
deploy_path = os.path.dirname(os.path.abspath(__file__)).split(os.sep)
deploy_path = os.path.join(os.sep.join(deploy_path[0:len(deploy_path) - 2]), 'deploy')

root_path = os.sep.join(current_path[0: len(current_path) - 1])

files_to_copy_pattern = r'\.py$|README.MD$|.*\.png$|.*\.qml$|metadata.txt$'
ignore_pattern = r'deploy_scripts|.git|.idea|TestScripts'  # |*\.Dockerfile$


# files_to_copy_pattern = re.compile('(?!deploy_scripts).*\.py$|README.MD$|.*\.png$|metadata.txt$|(?!\.git)|(?!.idea)|')


# get list of files to copy
def get_files_to_copy(dir_name):
    files_to_copy_list = []
    for root, dirs, files in os.walk(dir_name):
        files_to_copy_list += [os.path.join(root, name) for name in files if
                               (bool(re.search(files_to_copy_pattern, os.path.join(root, name))) and
                                not bool(re.search(ignore_pattern, os.path.join(root, name))))]
    print(files_to_copy_list)
    return files_to_copy_list


files_to_copy = get_files_to_copy(root_path)

for root, dirs, files in os.walk(os.path.join(qgis_plugins_path, plugin_folder_name), topdown=False):
    for file in files:
        curpath = os.path.join(root, file)
        os.remove(curpath)

    for d in dirs:
        curpath = os.path.join(root, d)
        if not os.listdir(curpath):
            os.rmdir(curpath)

for file in files_to_copy:
    target_path = file.replace(root_path, qgis_plugins_path + os.sep + plugin_folder_name)
    if not os.path.exists(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path))
    shutil.copy(file, target_path)

for root, dirs, files in os.walk(os.path.join(deploy_path, os.sep, plugin_folder_name), topdown=False):
    for file in files:
        curpath = os.path.join(root, file)
        os.remove(curpath)

    for d in dirs:
        curpath = os.path.join(root, d)
        if not os.listdir(curpath):
            os.rmdir(curpath)

for file in files_to_copy:
    target_path = file.replace(root_path, deploy_path + os.sep + plugin_folder_name + os.sep)
    if not os.path.exists(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path))
    shutil.copy(file, target_path)

result_file = open("counter.txt", 'a')
counter = 0
for file in files_to_copy:
    curr_file = open(file, 'rb')
    data = curr_file.read()
    counter += len(data)
    curr_file.close()

result_file.write('{}\t{}\n'.format(datetime.datetime.now().strftime("%d.%m.%YT%H:%M:%S"), counter))
result_file.close()

get_app_version.get_app_version()
