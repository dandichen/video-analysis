import os
import cv2
import numpy as np
import subprocess as sp
from datetime import datetime

import file_operations

def _getSecIdx(conf, epoch_time, sec_arr, camFlag, flag):
    binocular_fps = conf.getint('meta_data', 'binocular_fps')
    dms_fps = conf.getint('meta_data', 'dms_fps')
    if flag == 'start':
        arr = range(len(epoch_time))
    else:
        arr = reversed(range(len(epoch_time)))

    if camFlag == 'binocular':
        for i in arr:
            if abs(np.sum(sec_arr[i:i + binocular_fps]) / float(binocular_fps) - sec_arr[i]) < 0.000001:
                return i
    else:  # camFlag == 'dms'
        for i in arr:
            if abs(np.sum(sec_arr[i:i + dms_fps]) / float(dms_fps) - sec_arr[i]) < 0.000001:
                return i


def getSyncIdx(conf, human_time1, human_time2, human_time,
               approx_time1, approx_time2, approx_time,
               epoch_time1, epoch_time2, epoch_time,
               sec_arr1, sec_arr2, sec_arr, flag):

    if flag == 'start':
        idx1 = _getSecIdx(conf, epoch_time1, sec_arr1, 'binocular', 'start')
        idx2 = _getSecIdx(conf, epoch_time2, sec_arr2, 'binocular', 'start')
        idx = _getSecIdx(conf, epoch_time, sec_arr, 'dms', 'start')
    else:
        idx1 = _getSecIdx(conf, epoch_time1, sec_arr1, 'binocular', 'end')
        idx2 = _getSecIdx(conf, epoch_time2, sec_arr2, 'binocular', 'end')
        idx = _getSecIdx(conf, epoch_time, sec_arr, 'dms', 'end')

    t1 = datetime.strptime(human_time1[idx1], "%d %b %Y %H:%M:%S.%f")
    t2 = datetime.strptime(human_time2[idx2], "%d %b %Y %H:%M:%S.%f")
    t = datetime.strptime(human_time[idx], "%d %b %Y %H:%M:%S.%f")

    if flag == 'start':
        ref = max(t1, t2, t)
    else:
        ref = min(t1, t2, t)

    if ref == t1:     # reference: cam1
        cam1_ref = idx1
        cam2_ref = approx_time2.index(approx_time1[idx1])
        dms_ref = approx_time.index(approx_time1[idx1])
    elif ref == t2:   # reference: cam2
        cam1_ref = approx_time1.index(approx_time2[idx2])
        cam2_ref = idx2
        dms_ref = approx_time.index(approx_time2[idx2])
    else:             # reference: dms
        cam1_ref = approx_time1.index(approx_time[idx])
        cam2_ref = approx_time2.index(approx_time[idx])
        dms_ref = idx
    return cam1_ref, cam2_ref, dms_ref


def img2video(file_name, frame_idx, fps, width, height, flag, out_path):
    frame_idx_diff = np.diff(np.array(frame_idx))
    loss_idx = np.argwhere(frame_idx_diff != 1)
    loss_num = (frame_idx_diff - 1)[(frame_idx_diff - 1).nonzero()]

    # ans = []
    # for i in range(len(loss_idx)):
    #     for j in range(loss_num[i]):
    #         ans.append(loss_idx[i]+j)

    codec = cv2.VideoWriter_fourcc(*'XVID')
    cap = cv2.VideoWriter(out_path, codec, fps, (width, height))

    k = 0
    count = 0
    file_list = np.chararray(len(frame_idx) + np.sum(loss_num), itemsize=140)
    file_len = len(file_list)
    for i in range(file_len):
        count += 1
        if i in loss_idx:
            for j in range(len(loss_idx)):     # len(loss_idx1) == len(loss_num1)
                file_list[i:i + loss_num[j] + 1] = 'None'
        else:
            file_list[i] = file_name[k]
            k += 1
            if (k == len(file_name)):
                break

    for m in range(file_len):
        print 'frame num = ', m
        if file_list[m] == 'None' and flag == 'black':
            cap.write(np.zeros((height, width, 3), dtype=np.uint8))
        elif file_list[m] == 'None' and flag == 'same':
            cap.write(cv2.imread(file_list[m-1]))
        else:
            cap.write(cv2.imread(file_list[m]))
    print 'done'

    cap.release()
    cv2.destroyAllWindows()
    return file_list, loss_idx, loss_num


def getSyncVideo(conf, human_time1, human_time2, human_time,
                 approx_time1, approx_time2, approx_time,
                 epoch_time1, epoch_time2, epoch_time,
                 sec_arr1, sec_arr2, sec_arr,
                 file_name1, file_name2, file_name,
                 frame_idx1, frame_idx2, frame_idx, i):
    binocular_fps = conf.getint('meta_data', 'binocular_fps')
    binocular_width = conf.getint('meta_data', 'binocular_width')
    binocular_height = conf.getint('meta_data', 'binocular_height')
    dms_fps = conf.getint('meta_data', 'dms_fps')
    dms_width = conf.getint('meta_data', 'dms_width')
    dms_height = conf.getint('meta_data', 'dms_height')

    cam1_start, cam2_start, cam_start = getSyncIdx(conf, human_time1, human_time2, human_time,
                                                   approx_time1, approx_time2, approx_time,
                                                   epoch_time1, epoch_time2, epoch_time,
                                                   sec_arr1, sec_arr2, sec_arr, 'start')
    cam1_end, cam2_end, cam_end = getSyncIdx(conf, human_time1, human_time2, human_time,
                                             approx_time1, approx_time2, approx_time,
                                             epoch_time1, epoch_time2, epoch_time,
                                             sec_arr1, sec_arr2, sec_arr, 'end')
    cam1_end -= 1
    cam2_end -= 1
    cam_end -= 1

    print human_time1[cam1_end], human_time2[cam2_end], human_time[cam_end]
    file_name1 = file_name1[cam1_start:cam1_end]
    file_name2 = file_name2[cam2_start:cam2_end]
    file_name = file_name[cam_start:cam1_end]

    frame_idx1 = frame_idx1[cam1_start:cam1_end]
    frame_idx2 = frame_idx2[cam2_start:cam2_end]
    frame_idx = frame_idx[cam_start:cam_end]

    cam1_path, cam2_path, dms_path = file_operations.read_sync_path(conf, i)

    # sync
    file_list1, loss_idx1, loss_num1 = img2video(file_name1, frame_idx1,
                                                 binocular_fps, binocular_width,
                                                 binocular_height, 'black', cam1_path)

    file_list2, loss_idx2, loss_num2 = img2video(file_name2, frame_idx2,
                                                 binocular_fps, binocular_width,
                                                 binocular_height, 'black', cam2_path)

    file_list, loss_idx, loss_num = img2video(file_name, frame_idx,
                                              dms_fps, dms_width,
                                              dms_height, 'black', dms_path)

start_time = '00:00:03'
align_duration = '00:22:12'
def getClips(src_video_path, dst_video_path):
    d = dict(os.environ)
    d['PATH'] = '/mnt/scratch/third-party-packages/libffmpeg/bin:$PATH'
    d['LD_LIBRARY_PATH'] = '/mnt/scratch/third-party-packages/libffmpeg/lib/'

    cmd = "ffmpeg -i " + src_video_path + " -ss " + start_time + " -t " + align_duration + " -c copy " + dst_video_path
    print 'excuting: ' + cmd
    pipe = sp.Popen(cmd, shell=True, stdout=sp.PIPE, env=d)
    pipe.wait()





