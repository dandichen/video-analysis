import os
import fnmatch
import subprocess as sp


def converter(src_video_path, dst_video_path):
    d = dict(os.environ)
    d['PATH'] = '/mnt/scratch/third-party-packages/libffmpeg/bin:$PATH'
    d['LD_LIBRARY_PATH'] = '/mnt/scratch/third-party-packages/libffmpeg/lib/'
    cmd = "ffmpeg -i " + src_video_path + " -c copy " + dst_video_path
    print 'excuting: ' + cmd
    pipe = sp.Popen(cmd, shell=True, stdout=sp.PIPE, env=d)
    pipe.wait()

def main():
    video_path = '/mnt/scratch/time_alignment/'
    for dir_name, _, file_list in sorted(os.walk(video_path)):
        for name in file_list:
            if fnmatch.fnmatch(name, '*.avi'):
                converter(os.path.join(dir_name, name), os.path.join(dir_name, ''.join([name.split('.')[-2], '.mp4'])))


if __name__ == "__main__":
    main()
