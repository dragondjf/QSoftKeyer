# -*- coding: utf-8 -*-
#
# Copyright © 2013 dragondjf
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
guidata.disthelper

How to create an executable with py2exe or cx_Freeze with less efforts than
writing a complete setup script.

"""

import os
import shutil
import zipfile
from distribution import Distribution
import subprocess
import time
import json
# import matplotlib

def change_package_fromLib(package_name):
    library_zippath = os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip'])
    library_path = os.getcwd() + os.sep + os.sep.join(['dist', 'library'])
    with zipfile.ZipFile(library_zippath, 'r') as zip_file:
        zip_file.extractall(path=library_path)
    shutil.rmtree(library_path + os.sep + package_name)
    for item in [package_name]:
        package = __import__(item)
        package_path = os.path.dirname(package.__file__)
        shutil.copytree(package_path, library_path + os.sep + package_name)

    os.remove(os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip']))
    addFolderToZip(library_path, 'dist\library.zip')
    shutil.rmtree(library_path)

def change_package_fromLocal(package_name):
    library_zippath = os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip'])
    library_path = os.getcwd() + os.sep + os.sep.join(['dist', 'library'])
    with zipfile.ZipFile(library_zippath, 'r') as zip_file:
        zip_file.extractall(path=library_path)
    shutil.rmtree(library_path + os.sep + package_name)
    for item in [package_name]:
        package_path = os.getcwd() + os.sep + item
        shutil.copytree(package_path, library_path + os.sep + package_name)

    os.remove(os.getcwd() + os.sep + os.sep.join(['dist', 'library.zip']))
    addFolderToZip(library_path, 'dist\library.zip')
    shutil.rmtree(library_path)

def addFolderToZip(folder, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        def addhandle(folder, zip_file):
            for f in os.listdir(folder):
                full_path = os.path.join(folder, f)
                if os.path.isfile(full_path):
                    print 'Add file: %s' % full_path
                    zip_file.write(full_path, full_path.split('library\\')[1])
                elif os.path.isdir(full_path):
                    print 'add folder: %s' % full_path
                    addhandle(full_path, zip_file)
        addhandle(folder, zip_file)


def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass


def get_py2exe_datafiles(datapath, relativehead):
    head, tail = os.path.split(datapath)
    d = {}
    for root, dirs, files in os.walk(datapath):
        files = [os.path.join(root, filename) for filename in files]
        root = root.replace(tail, relativehead)
        root = root[root.index(relativehead):]
        d[root] = files
    return d.items()

def write_file(filename, instr):
    fd = open(filename, "w")
    fd.write(instr)
    fd.close()


def backiss(full_name):
    iss1 = '''
[Setup]
AppId={{A88315E7-BAE0-49F5-B004-F89E4E5F072D}
AppName=QSoftkeyer
AppVerName=QSoftkeyer1.0
AppPublisher=ov-orange
AppPublisherURL=http://www.ov-orange.com/
AppSupportURL=http://www.ov-orange.com/
AppUpdatesURL=http://www.ov-orange.com/
DefaultDirName={pf}\QSoftkeyer
DefaultGroupName=QSoftkeyer
OutputDir= Output
OutputBaseFilename='''
    iss2 = '''
Compression=lzma
SolidCompression=yes
SetupIconFile=dist\skin\images\logo3.ico

[Languages]
Name: "chinese"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\QSoftKeyer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\QSoftkeyer"; Filename: "{app}\QSoftKeyer.exe"
Name: "{commondesktop}\QSoftkeyer"; Filename: "{app}\QSoftKeyer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\QSoftKeyer.exe"; Description: "{cm:LaunchProgram,QSoftkeyer}"; Flags: nowait postinstall skipifsilent

'''
    return iss1 + full_name + iss2


def cleanall():
    delete_file_folder('svn_co')
    delete_file_folder('dist')
    delete_file_folder('build')
    delete_file_folder('QSoftKeyer-setup-v2.iss')
    # os.system("rm svn_co -rf")
    # os.system("rm dist -rf")
    # os.system("rm build -rf")
    # os.system("rm QSoftKeyer-setup-v2.iss -rf")
    # os.system("rm js/ver.json -rf")

if __name__ == '__main__':
    
    local_name = "QSoftKeyer"
    version_name = "v1.0"
    time_str = ""
    svn_version = ""
    json_str = ""
    cleanall()
    os.system("svn co http://192.168.10.200/svn/SW/trunk/QSoftKeyer svn_co")
    p = subprocess.Popen(
        ['cd','svn_co','&&','svn','info'], 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell = True,
        )
    (child_stdin, child_stdout) = (p.stdin, p.stdout)
    svn_version = 'r' + (''.join(child_stdout.readlines())).split("\n")[6].split(":")[1].strip()
    time_str = 'b' + time.strftime("%Y%m%d", time.localtime(int(time.time()))).decode('UTF8')
    json_str = json.dumps({"local_name": local_name, "version_name": version_name, "svn_version": svn_version, "time_str": time_str}, indent=3)
    full_name = "-".join([local_name, version_name, svn_version, time_str])
    write_file("js/ver.json", json_str)
    issstr = backiss(full_name)
    write_file("QSoftKeyer-setup-v2.iss", issstr)
    if os.name == "nt":
        dist = Distribution()
        dist.vs2008 = None
        dist.setup(name=u"QSoftKeyer", version='1.0.0',
                   description=u"Application based on PyQt4",
                   script="svn_co/QSoftKeyer.py", target_name="QSoftKeyer",
                   icon=os.sep.join([os.getcwd(), 'skin', 'images', 'logo3.ico']))

        dist.add_modules('PyQt4')
        dist.bin_excludes += ["libzmq.dll"]
        dist.includes += []
        # dist.data_files += matplotlibdata_files
        dist.data_files += get_py2exe_datafiles(os.sep.join([os.getcwd(), 'utildialog', 'utildialogskin']), 'utildialogskin')
        dist.data_files += [('phonon_backend', [
                'C:\Python27\Lib\site-packages\PyQt4\plugins\phonon_backend\phonon_ds94.dll'
                ]),
            ('imageplugins', [
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qgif4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qjpeg4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qsvg4.dll',
            'c:\Python27\lib\site-packages\PyQt4\plugins\imageformats\qico4.dll',
            ])]

        dist.excludes += [
                  '_gtkagg',
                  '_tkagg',
                  '_agg2',
                  '_cairo',
                  '_cocoaagg',
                  '_fltkagg',
                  '_gtk',
                  '_gtkcairo', ]

        dist.build('py2exe')

        '''
            拷贝响应的图片皮肤和与项目有关的资源文件到打包目录
        '''

    for item in ['skin', 'docs', 'Bootstrap Metro UI CSS', 'js']:
        shutil.copytree(os.getcwd() + os.sep + item, os.getcwd() + os.sep + os.sep.join(['dist', item]))

    for item in ['log', 'options']:
        os.mkdir(os.getcwd() + os.sep + os.sep.join(['dist', item]))

    for key in ['build']:
        path = os.getcwd() + os.sep + key
        delete_file_folder(path)

    change_package_fromLocal('Cheetah')
    os.system("iscc QSoftKeyer-setup-v2.iss")
    cleanall()
