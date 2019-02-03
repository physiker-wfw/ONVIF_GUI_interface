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
parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],help="increase output verbosity")
parser.add_argument("-s", "--start", help="Start date and time (2018-01-01_08:00)", default='2018-01-01_00:00', type=validDate)
parser.add_argument("-e", "--end", help="End date and time (2018-01-01_08:00)", type=validDate, required=True)
parser.add_argument("-p", "--path", help="Path to jpg files", default="\\\\nas\\Camera\\snapshots\\")
parser.add_argument("-f", "--force", help="Force the deletion; do not ask again", action='store_true')
args = parser.parse_args()

print('This programm will delete the jpg files in ', args.path)
start_date = args.start
end_date = args.end

vi = jpg2video(datapath=args.path)
allFiles, n = vi.getFileList()
print("Number of all saved frames:", n)
print("First frame:", str(vi.getFirstDate(allFiles)))
myFiles, n = vi.filterDate(allFiles, start_date, end_date)
print("Number of frames to delete:", n)

if not args.force:
    s1 = input('Delete all these jpg files (y/n)?')
    if s1 in ['yes', 'Yes', 'y', 'Ja', 'j', '1']:
        vi.removeFiles(myFiles)
    else:
        print('No files removed.')
else:
    vi.removeFiles(myFiles)

