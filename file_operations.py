import os
import numpy as np

demo_path = '/mnt/scratch/sync_sd/car_record/demo/'

def genr_filelists(align_flag='/alignment/', data_type='/binocular_camera',
                   sync_flag='/sync/', sync_intrpl_flag='sync_interpolation',
                   conv_flag='/conv/'):
    for date_folder in sorted(os.listdir(demo_path)):
        if len(date_folder) == 10:  # yyyymmdd-X
            if align_flag == None:
                period_path = demo_path + date_folder + data_type
                if sync_flag == None and sync_intrpl_flag == None and conv_flag == None:
                    print period_path
                elif sync_flag != None and sync_intrpl_flag == None and conv_flag == None:
                    print period_path + sync_flag
                elif sync_flag == None and sync_intrpl_flag != None and conv_flag == None:
                    print period_path + sync_intrpl_flag
                elif sync_flag == None and sync_intrpl_flag == None and conv_flag != None:
                    print period_path + conv_flag
                else:
                    raise ValueError('Error params')
            else:
                print demo_path + date_folder + align_flag




def read_raw_data(conf, cam, line_idx):
    head_files = conf.get('raw_data', 'file_lists')
    with open(head_files) as line:
        for i, file_name in enumerate(line):
            if i == line_idx:
                f = open(file_name[0:-1]  + cam + '.txt', 'r')
                human_time = []
                approx_time = []
                sec = []
                epoch_time = []
                file_name = []
                frame_idx = []
                str = f.readline()
                while (str):
                    human_time.append(str[0:27])
                    approx_time.append(str[0:20])
                    sec.append(str[18:20])
                    epoch_time.append(str[30:47])
                    file_name.append(str[str.find('/mnt'):-1])
                    frame_idx.append(int(str[str.find('i') + 1:str.find('cam') - 1]))
                    str = f.readline()
                f.close()
                return human_time, approx_time, np.int0(sec), epoch_time, file_name, frame_idx


def read_sync_path(conf, line_idx):
    binocular_sync_files = conf.get('synchronizer', 'binocular_sync_files')
    dms_sync_files = conf.get('synchronizer', 'dms_sync_files')
    with open(binocular_sync_files) as line:
        for i, file_name in enumerate(line):
            if i == line_idx:
                cam1_path = file_name[0:-1] + file_name[37:47] + '-sync-cam1.avi'
                cam2_path = file_name[0:-1] + file_name[37:47] + '-sync-cam2.avi'

    with open(dms_sync_files) as line:
        for i, file_name in enumerate(line):
            if i == line_idx:
                dms_path = file_name[0:-1] + file_name[37:47] + '-sync-dms.avi'

    return cam1_path, cam2_path, dms_path
