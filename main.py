import re
import subprocess

from pathlib import Path
from tqdm import tqdm


# 将日志输出的时间类型转换成秒
def get_seconds(time):
    h = int(time[0:2])
    # print("时：" + str(h))
    m = int(time[3:5])
    # print("分：" + str(m))
    s = int(time[6:8])
    # print("秒：" + str(s))
    ms = int(time[9:12])
    # print("毫秒：" + str(ms))
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts


def exec_ffmpeg(old_file, new_file):
    cmd = [
        "D:\\ffmpeg\\ffmpeg.exe", "-i", old_file, "-c:v", "hevc_nvenc", "-q:a", "0", new_file
    ]

    pi = subprocess.Popen(cmd, shell=True, bufsize=0, encoding="utf-8", universal_newlines=True,
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    duration = None
    while pi.poll() is None:
        line = pi.stderr.readline().strip()

        if line:
            duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)
            result = re.search(r'time=(?P<time>\S+)', line)
            speeds = re.search(r'speed=(?P<speed>\S+)', line)
            if result is not None and duration is not None and speeds is not None:
                elapsed_time = result.groupdict()['time']
                speed = speeds.groupdict()['speed']
                currentTime = get_seconds(elapsed_time)
                allTime = get_seconds(duration)
                speedx = {'speed': None}
                with tqdm(total=allTime, desc="FFmpeg") as pbar:
                    speedx['speed'] = speed
                    pbar.set_postfix(speedx)
                    pbar.update(currentTime)

    pi.communicate()
    if pi.wait() != 0:
        print("异常退出！！")


def filter_file(path):
    directory = Path(path)
    files = directory.rglob('*')
    file_dir = {}
    for file in files:
        ffile = Path(file)

        if ffile.suffix in [".flv"]:
            new = str(ffile.with_name(ffile.stem + "-h")) + ".mp4"
            old = str(ffile.with_stem(ffile.stem))
            file_dir[old] = new

    return file_dir


if __name__ == '__main__':
    aa = filter_file('E:\\live')
    for bb in aa.keys():
        print("start transcoding:", bb, aa[bb])
        exec_ffmpeg(bb, aa[bb])
