"""
Desired features:
  height, width, thickness, display_size, resolution, pixel_density
  camera_resolution / no camera,
  talk_time, stand_by_time,
  data_speed
"""

from sys import argv
from os.path import basename
import re
import glob
import pandas as pd


pd.set_option('display.expand_frame_repr', False)


class Capture(object):
    def __init__(self, regexp, names):
        self.regexp = regexp
        self.names = names
        self.seen = False

    def parse(self, line, data):
        if not self.seen:
            match = self.regexp.match(line)
            if match:
                attrs = {k: match.group(i+1) for k, i in zip(self.names, range(len(self.names)))}
                data.update(attrs)

    def reset(self):
        self.seen = False


class PhoneFeaturesExtractor(object):
    def __init__(self):
        self.captures = [
            Capture(
                re.compile('.*Dimensions:.*[\d.]+ x [\d.]+ x [\d.]+ inches +\(([\d.]+) x ([\d.]+) x ([\d.]+) mm\).*'),
                ['height', 'width', 'thickness']
            ),
            Capture(re.compile('.*Weight:.*[\d.]+ oz  \(([\d.]+) g\).*'), ['weight']),
            Capture(re.compile('.*Physical size:.*([\d.]+) inches.*'), ['display_size']),
            Capture(re.compile('.*Resolution:.*>(\d+) x  (\d+) pixels.*'), ['display_width', 'display_height']),
            Capture(re.compile('.*>(\d+) +ppi.*'), ['display_density']),
            Capture(re.compile('.*s_cpu_rating_s(\d).*'), ['cpu_rating']),
            Capture(re.compile('.*([\d.]+) GB RAM.*'), ['memory']),
            Capture(re.compile('.*Talk time:.*>([\d.]+) hours.*'), ['talk_time']),
            Capture(re.compile('.*Stand-by time:.*>[\d.]+ days \((\d+) hours\).*'), ['standby_time']),
        ]

    def parse(self, path):
        data = {}
        map(Capture.reset, self.captures)
        with open(path) as f:
            for line in f.readlines():
                for capture in self.captures:
                    capture.parse(line, data)
        return data

    def scan(self, paths):
        data = {}
        for path in paths:
            key = basename(path).split('.')[0]
            data[key] = self.parse(path)
            print(key)
        return pd.DataFrame(data.values(), index=data.keys())

if __name__ == '__main__':
    pfe = PhoneFeaturesExtractor()
    root = argv[1]
    paths = glob.glob(root + '/*.html')
    paths = sorted(paths)
    df = pfe.scan(paths)
    df.to_csv(argv[2])


