import os
import re
import cv2
from datetime import datetime  
from datetime import timedelta 
from jpg2videoClass import jpg2video

def validDate(string):
    date = datetime.strptime(string, "%Y-%m-%d_%H:%M")
    return date


import argparse
parser = argparse.ArgumentParser(description='This program converts a sequence of jpg files to a mp4 video.')
# parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],help="increase output verbosity")
parser.add_argument("-s", "--start", help="Start date and time (2018-01-01_08:00)", default='2018-01-01_00:00', type=validDate)
parser.add_argument("-e", "--end", help="End date and time (2018-01-01_08:00)", type=validDate, required=True)
parser.add_argument("-p", "--path", help="Path to jpg files", default="\\\\nas\\Camera\\snapshots\\")
parser.add_argument("-f", "--force", help="Force the jpg deletion after conversion", action='store_true')
parser.add_argument("-fa", "--factor", help="Reduction factor (size) between jpg and mp4 frame", default=1.0, type=float)
parser.add_argument('--version', action='version', version='%(prog)s 1.1 2019-08-25')
args = parser.parse_args()

print('This programm will convert the jpg files in ', args.path, ' to mp4 video')
start_date = args.start
end_date = args.end

vi = jpg2video(datapath=args.path)
allFiles, n = vi.getFileList()
print("Number of all saved frames:", n)
print("First frame:", str(vi.getFirstDate(allFiles)))
myFiles, n = vi.filterDate(allFiles, start_date, end_date)
print("Number of frames to convert:", n)
print("Size reduction:", args.factor)

file = vi.files2video2(myFiles, fac=args.factor)
if args.force:
    vi.removeFiles(myFiles)
  