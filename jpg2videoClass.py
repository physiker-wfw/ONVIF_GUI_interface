import os
import re
import cv2
from datetime import datetime  
from datetime import timedelta  
import time



class jpg2video:
    inputPath = "\\\\nas\\Camera\\snapshots\\"
    def __init__(self,datapath=inputPath):
        self.datapath = datapath
        self.outputPath = "\\\\nas\\VideoIPcam\\"
        self.outputLocal = "./"

    def getFileList(self):
        data_ext = ['jpg', 'JPG','jpeg']
        jpgFiles = [fn for fn in os.listdir(self.datapath)
                    if any(fn.endswith(ext) for ext in data_ext)]
        jpgFiles.sort()
        return jpgFiles, len(jpgFiles)

    def filterDate(self, filelist, startdate, enddate=datetime.now()):
        maxFrame = 4096*40
        counter = 0
        myFiles = []
        for filename in filelist:
            node, date, xtime,_ ,_,=re.split('\_',filename)
            fdate = datetime.strptime(date+xtime, "%Y-%m-%d%H-%M-%S")
            if startdate < fdate < enddate:
                # print(date, xtime)
                myFiles.append(filename)
                counter += 1
                if counter > maxFrame:
                    print("MAXIMUM NUMBER OF FRAMES DETECTED!!")
                    break
        return myFiles, counter

    def getFileNumber(self, fileList, selectDate):
        counter = 0
        _, date, xtime,_ ,_,=re.split('\_',fileList[-1])
        lastDate = datetime.strptime(date+xtime, "%Y-%m-%d%H-%M-%S")
        if selectDate > lastDate:
            return len(fileList)-1
        for filename in fileList:
            _, date, xtime,_ ,_,=re.split('\_',filename)
            fdate = datetime.strptime(date+xtime, "%Y-%m-%d%H-%M-%S")
            if selectDate > fdate:
                counter += 1
            else:
                break
        return counter


    def getFirstDate(self,filelist):
        _, date, xtime,_ ,_,=re.split('\_',filelist[0])
        return date, xtime

    def files2video(self, filelist, output=0, codec='mp42'):
        if not filelist:
            print("Nothing to convert (empty filelist).")
            return
        # Define the codec and create VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        fourcc = cv2.VideoWriter_fourcc(*'MP42')
        fac = 0.75
        fps = 15.0
        frame = cv2.imread(self.datapath+filelist[0])
        height, width, channels = frame.shape
        # print("height, width, channels",height, width, channels)
        newSize = (int(width*fac), int(height*fac))
        # if not output:
        node, date, xtime,_ ,_,=re.split('\_',filelist[0])
        output = self.outputPath+"vid_"+date+"_"+xtime+".avi"
        out = cv2.VideoWriter(output, fourcc, fps, newSize)
        print("Converting jpg to video:")
        for filename in filelist:
            try:
                frame = cv2.imread(self.datapath+filename)
                resized = cv2.resize(frame, newSize, interpolation = cv2.INTER_AREA)
                print(filename, end='\r', flush=True)
                out.write(resized)
            except:
                print("\n      ###  Error in reading, resizing or writing:", filename)
        out.release()
        print("\nConversion finished.")
        cv2.destroyAllWindows()
        print('Video saved in',output, '     with size: %3.1f MB' %(os.path.getsize(output)/(1024*1024.0)))
        return output

    def removeFiles(self, fileList):
        i = 0
        for filename in fileList:
            try:
                os.remove(self.datapath+filename)
                i += 1
            except:
                print("Error removing: ", self.datapath+filename)
        print(i, 'files removed from', len(fileList), 'in total.\n')
        return

    def files2video2(self, filelist, output=0, codec='mp42',fac=1.0):
        if not filelist:
            print("Nothing to convert (empty filelist).")
            return
        # Define the codec and create VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        fourcc = cv2.VideoWriter_fourcc(*'MP42')
        # fac = 0.75
        fps = 3
        frame = cv2.imread(self.datapath+filelist[0])
        height, width, channels = frame.shape
        # print("height, width, channels",height, width, channels)
        newSize = (int(width*fac), int(height*fac))
        # if not output:
        _, date, xtime,_ ,_,=re.split('\_',filelist[0])
        output = self.outputLocal+"vid_"+date+"_"+xtime+".avi"
        frameList = self.outputLocal+"vid_"+date+"_"+xtime+".dat"
        out = cv2.VideoWriter(output, fourcc, int(fps), newSize)
        print('Estimated time (min): ', len(filelist)*0.156/60.)
        print("Converting jpg to video:")
        convStart = time.time()
        iFrame =1
        with open(frameList, 'w') as fl:
            for filename in filelist:
                try:
                    frame = cv2.imread(self.datapath+filename)
                    if fac < 0.8:
                        resized = cv2.resize(frame, newSize, interpolation = cv2.INTER_AREA)
                        print(filename, end='\r', flush=True)
                        out.write(resized)
                    else:
                        out.write(frame)
                    node, xdate, xtime,_ ,_,=re.split('\_',filename)
                    print(iFrame, xdate , xtime, file=fl)
                    iFrame += 1
                except:
                    print("\n      ###  Error in reading, resizing or writing:", filename)
        out.release()
        print("\nConversion finished.")
        convEnd = time.time()
        cv2.destroyAllWindows()
        print('Video saved in',output, '     with size: %3.1f MB' %(os.path.getsize(output)/(1024*1024.0)))
        print('Time needed (min):', (convEnd-convStart)/60., ';  time/frame (sec): ', (convEnd-convStart)/(iFrame-1))
        return output




if __name__ == '__main__':
    print('This programm will convert the jpg files in \\nas\Camera\ to a mp4 video:')
    s1,s2 = input('Start time and duration (%Y-%m-%d_%H:%M number_of_hours):').split(' ')
    start_date = datetime.strptime(s1, "%Y-%m-%d_%H:%M")
    end_date = start_date + timedelta(seconds=3600*int(s2))

    vi = jpg2video()
    allFiles, n = vi.getFileList()
    print("Number of all saved frames:", n)
    print("First frame:", str(vi.getFirstDate(allFiles)))
    myFiles, n = vi.filterDate(allFiles, start_date, end_date)
    print("Number of frames to convert:", n)
    print("If you wish to delete ALL saved jpg files afterwards, answer exactly with 'yes all'")
    s1 = input('Delete all converted jpg files afterwards (y/n)?')
    file = vi.files2video(myFiles)
    if s1 in ['yes', 'Yes', 'y', 'Ja', 'j', '1']:
        vi.removeFiles(myFiles)
    elif s1 in ['yes all', 'Yes all', 'yes, all']:
        vi.removeFiles(allFiles)
    else:
        print('No files removed.')
