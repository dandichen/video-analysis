import os
import fnmatch
import subprocess as sp

width = 1024
height = 768
ratio = 1.6

def compress(src_video_path, dst_video_path, height, width):
    d = dict(os.environ)
    d['PATH'] = '/mnt/scratch/third-party-packages/libffmpeg/bin:$PATH'
    d['LD_LIBRARY_PATH'] = '/mnt/scratch/third-party-packages/libffmpeg/lib/'

    cmd = "ffmpeg -i " + src_video_path + " -vf scale=" + str(width) + ":" + str(height) + " " + dst_video_path

    print 'excuting: ' + cmd
    pipe = sp.Popen(cmd, shell=True, stdout=sp.PIPE, env=d)
    pipe.wait()

def main():
    date = ['20160617-1', '20160621-1', '20160621-2', '20160622-1', '20160623-1', '20160623-2', '20160624-1', '20160626-1', '20160627-1', '20160629-1', '20160714-1']
    for d in date:
        print d
        src_video_path = '/'.join(['/mnt/scratch/sync_sd/car_record/demo/', d, '/binocular_camera', d + '-cam1.avi'])
        dst_video_path = '/mnt/scratch/hcomp_data/hcomp_raw_data/20160809_hcomp_video/raw/' + d +  '-cam1_' + \
                         str(int(width / float(ratio))) + '*' + str(int(height / float(ratio))) + '.avi'

        compress(src_video_path, dst_video_path, int(height / float(ratio)), int(width / float(ratio)))



if __name__ == "__main__":
    main()
