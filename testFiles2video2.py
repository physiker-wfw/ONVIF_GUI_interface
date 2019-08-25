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
parser.add_argument('--version', action='version', version='%(prog)s 1.0 2019-02-03')
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

file = vi.files2video2(myFiles)
# if args.force:
#     vi.removeFiles(myFiles)
  