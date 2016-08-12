import sys
sys.path.insert(0, '/mnt/scratch/third-party-packages/libopencv_3.1.0/lib/python')
sys.path.insert(1, '/mnt/scratch/third-party-packages/libopencv_3.1.0/lib')

import os
import cv2
import ConfigParser
import numpy as np

import file_operations
import img2video

def main():
    conf = ConfigParser.RawConfigParser()
    params_path = './config/data.cfg'
    if os.path.isfile(params_path):
        conf.read(params_path)
    else:
        raise ValueError('Please provide a correct path for config file')

    for i in range(15):
        if i == 7 or i == 14:   # 20160624/20160714
            continue
        else:
            print i
            human_time1, approx_time1, sec_arr1, epoch_time1, file_name1, frame_idx1 = file_operations.read_raw_data(conf, 'cam1', i)
            human_time2, approx_time2, sec_arr2, epoch_time2, file_name2, frame_idx2 = file_operations.read_raw_data(conf, 'cam2', i)
            human_time, approx_time, sec_arr, epoch_time, file_name, frame_idx = file_operations.read_raw_data(conf, 'dms', i)

            img2video.getSyncVideo(conf, human_time1, human_time2, human_time,
                                   approx_time1, approx_time2, approx_time,
                                   epoch_time1, epoch_time2, epoch_time,
                                   sec_arr1, sec_arr2, sec_arr,
                                   file_name1, file_name2, file_name,
                                   frame_idx1, frame_idx2, frame_idx, i)

if __name__ == '__main__':
    main()