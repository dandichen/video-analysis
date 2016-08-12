import os
import shutil
import fnmatch


def copyData(src_path, dst_path, date):
    for dir_name, _, file_list in os.walk(src_path):
        for name in sorted(file_list):
            if name.split('_')[0][:-2] == date:
                if fnmatch.fnmatch(name, '*cam1*.mp4'):
                    print name
                    shutil.copyfile(os.path.join(dir_name, name), os.path.join(dst_path, date + '-2', 'binocular_camera/sync', name))

                if fnmatch.fnmatch(name, '*cam2*.mp4'):
                    print name
                    shutil.copyfile(os.path.join(dir_name, name), os.path.join(dst_path, date + '-2', 'binocular_camera/sync', name))

                if fnmatch.fnmatch(name, '*dms*.mp4'):
                    print name
                    shutil.copyfile(os.path.join(dir_name, name), os.path.join(dst_path, date + '-2', 'dms/sync', name))

def main():
    date = ['20160626', '20160627', '20160629']
    src_path = '/mnt/scratch/time_alignment'
    dst_path = '/mnt/scratch/sync_sd/car_record/demo/'

    for d in date:
        copyData(src_path, dst_path, d)


if __name__ == '__main__':
    main()