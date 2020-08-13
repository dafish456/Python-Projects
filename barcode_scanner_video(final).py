# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
from datetime import datetime
import imutils
import time
import cv2
from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import sys
from pprint import pprint
from googleapiclient import discovery
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#GPIO Setup Code
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
        help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "w")
found = set()

################### SHEETS STUFF ###############################################

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds  = ServiceAccountCredentials.from_json_keyfile_name("creds(imp).json", scope)

client = gspread.authorize(creds)

sheet = client.open("BSP: Names, ID#'s, Attendance").sheet1

AllIDs = sheet.row_values(3)

################################################################################

def escape():
    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        sys.exit()

def ledFlash(ledColor, flashNums, blinkTime):
    portNum = 0
    if(ledColor == 'green'):
        portNum = 13
    elif(ledColor == 'red'):
        portNum = 26
    GPIO.output(portNum, GPIO.HIGH)
    sleep(1)
    GPIO.output(portNum, GPIO.LOW)
    sleep(1)
    for i in range(0, flashNums):
        GPIO.output(portNum, GPIO.HIGH)
        sleep(blinkTime)
        GPIO.output(portNum, GPIO.LOW)
        sleep(blinkTime)
def getCurrentDatePos():
    currentDate = datetime.today().strftime("%m/%d/%y")
    dateCol = sheet.col_values(1)
    for i in range(5, 1000):
        if currentDate == sheet.cell(i, 1).value: #investigate non constant iterators
            return i
        
def parser(studentID, scanNumber):
    #ID validation
    if studentID < 0 | len(str(studentID)) != 7:
        ledFlash('red', 4, 0.5)
        print('The item you are scanning isn\'t a student ID')
        
    #Sheets API
    idList = []
    idRow = 3
    idColStart = 2
    studentIDCol = 0
    #create array/list of id values from column
    for i in range(0, len(AllIDs) - 1):
        nextVal = int(sheet.cell(idRow, idColStart + i).value)
        idList.append(nextVal)
        #if studentID is in column, find its position
        if nextVal == studentID:
            studentIDCol = i + idColStart
   
    if studentIDCol == 0: #equivalent to 'if studentID not in idList'
        ledFlash('red', 4, 0.25)
        print('HALT! Stay under the speed limit')
    else:
        userName = str(sheet.cell(idRow - 1, studentIDCol).value)
        #find position of current date in spreasheet so time can be stamped in correct spot
        #write the time at intersection of correct student and day cells
        ledFlash('green', 4, 0.25)
        if scanNumber == 1:
            sheet.update_cell(getCurrentDatePos(), studentIDCol, datetime.now().strftime("%H:%M:%S"))
            print('Welcome ' + userName + '. Your hours are now being tracked')
        elif scanNumber == 2:
            sheet.update_cell(getCurrentDatePos() + 1, studentIDCol, datetime.now().strftime("%H:%M:%S"))
            print('Goodbye ' + userName + '. Your hours have been logged')

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)
    
    escape()

    numOfScans = 0
    # loop over the detected barcodes
    for barcode in barcodes:
        escape()
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        if barcodeData not in found:
            csv.write("{},{}\n".format(datetime.now(), barcodeData))
            csv.flush()
            found.add(barcodeData)
            numOfScans = 1
            parser(int(barcodeData), numOfScans)

        if barcodeData in found:
            numOfScans+=1
            if numOfScans > 2:
                print('You cannot scan more than 2 times in a day')
            else:
                csv.write("{},{}\n".format(datetime.now(), barcodeData))
                csv.flush()
                found.add(barcodeData)
                parser(int(barcodeData), 2)
                        
    # show the output frame
    cv2.imshow("Barcode Scanner", frame)
    escape()
    
#close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()   
