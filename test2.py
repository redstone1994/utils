import re

import subprocess

#https://www.codeleading.com/article/20792721743/
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


# size=   25189kB time=00:04:28.67 bitrate= 768.0kbits/s speed= 748x
# video:0kB audio:25189kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.000302%
cmd = ['ffmpeg.exe', '-i', 'D:\\test.mp3', '-ar', '48000', '-ac',
       '1', '-acodec', 'pcm_s16le', '-hide_banner', 'D:\\out.wav']
process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8",
                           text=True)
for line in process.stdout:
    # print(line)

    duration_res = re.search(r'\sDuration: (?P<duration>\S+)', line)
    if duration_res is not None:
        duration = duration_res.groupdict()['duration']
        duration = re.sub(r',', '', duration)

    result = re.search(r'\stime=(?P<time>\S+)', line)
    if result is not None:
        elapsed_time = result.groupdict()['time']
        # 此处可能会出现进度超过100%，未对数值进行纠正
        progress = (get_seconds(elapsed_time) / get_seconds(duration)) * 100
        print(elapsed_time)
        print(progress)
        print("进度:%3.2f" % progress + "%")
process.wait()
if process.poll() == 0:
    print("success:", process)
else:
    print("error:", process)

