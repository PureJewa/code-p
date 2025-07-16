import os
import socket
import select
import sys
import threading
import time
#from thread import *

def clientthread(conn):
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    while True:
        #Receiving from client
        data = conn.recv(1024)
        print ("data socket actief")
        print ("SOCKET IN: "+data)
        reply = 'OK...' + data
        if not data: 
            break
        conn.sendall(reply)
    conn.close()

class WebCommunicator:
    def __init__(self):
        self.CONNECTION_LIST = []    # list of socket clients
        self.RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
        self.PORT = 4000
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("", self.PORT))
            self.CONNECTION_LIST.append(self.server_socket)
            
            self.thread = threading.Thread(target=self._monitor)
            self.thread.daemon = True
            self.thread.start()
        except socket.error as msg:
            print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            
    def parseData(self,data):
        try:
            print("data :"+str(data))
            if "sendGCode" in data:
                cmd = data.split(":")[1]
                globals.app.api.printer.sendCommand(cmd)
                            
            elif data == "getStatus":
                statusString = globals.app.api.getStatusString()
                hasWebcam = 0
                webcamOn= 0
                if globals.app.api.hasWebcam ==True:
                    hasWebcam = 1
                    if globals.app.api.runWebcam("checkRunning") == True:
                        webcamOn = 1
                        #print("webcam on")c
                    else: 
                        webcamOn = 0
                        #print("webcam off")
                else:
                    hasWebcam = 0
                printerTypeString= globals.app.api.getPrinterType()
                printerSerialString= globals.app.api.getSerialNumber()
                nozzleCurrent = globals.app.api.temp_nozzle.actual
                nozzleTarget = globals.app.api.temp_nozzle.target
                bedCurrent = globals.app.api.temp_bed.actual
                bedTarget = globals.app.api.temp_bed.target
                
                return ("{\"status\":\"" + statusString + 
                        "\",\"printerType\":\"" + printerTypeString +
                        "\",\"printerSerial\":\"" + printerSerialString+
                        "\",\"nozzleCurrent\":\"" + str(nozzleCurrent) + 
                        "\",\"nozzleTarget\":\"" + str(nozzleTarget) + 
                        "\",\"bedCurrent\":\"" + str(bedCurrent) + 
                        "\",\"bedTarget\":\"" + str(bedTarget) + 
                        "\",\"hasWebCam\":\"" + str(hasWebcam) + 
                        "\",\"webCamOn\":" + str(webcamOn) + "}")
                               
            elif "getPrintStatus" in data:
                fileName = globals.app.api.printFileName
                if fileName is None:
                    fileName = "-"
                
                progressNormal = globals.app.api.progress
                def getHourString(seconds):
                    hours = int(int(seconds) / 3600)
                    minutes = int((int(seconds)-(hours*3600)) / 60)
                    return (u'{00:02d}').format(hours)+':'+(u'{00:02d}').format(minutes)
                
                textPrintTime = ''
                printTime = globals.app.api.getPrintTime()
                if printTime is not None:
                    textPrintTime = getHourString(printTime)
                
                textPrintTimeLeft = 'ETA -'
                printTimeLeft = globals.app.api.getPrintTimeRemainingEstimate()
                if printTimeLeft is not None:
                    textPrintTimeLeft = 'ETA '+getHourString(printTimeLeft)
                eta = textPrintTime# + textPrintTimeLeft
                self.fileNameTmp = fileName.decode('utf-8')
                return ("{\"fileName\":\"" +self.fileNameTmp + 
                        "\",\"eta\":\"" + eta + 
                        "\",\"progress\":" + str(progressNormal) + "}")
            elif "printFile:" in data:
                if globals.app.api.canPrint():
                    #if Marlin doesn't know its position, start with homing, otherwise skip
                    if globals.app.api.startHome:
                        globals.app.api.printer.sendCommand('G28 X0 Y0 Z0')
                    filename = data.split(":")[1].decode('utf-8')
                    file_uri = "/home/debian/OctoPiPanel/printfiles/" + filename
                    file_uri =file_uri.encode('utf-8') 
                    globals.app.api.printFile(filename,file_uri,"sd")
                    return "file started"
                else:
                    return "Trial time over!"
            elif "cancelPrint" in data:
                globals.app.api.cancelPrint()
            elif "pausePrint" in data:                
                if globals.app.api.printPaused:
                    if not globals.app.api.powerFail and globals.app.api.door and globals.app.api.filament:
                        globals.app.api.pausePrint(False)
                else:
                    globals.app.api.pausePrint(True)
            elif "cameraOn" in data:
                globals.app.api.runWebcam("runOnTime")
            elif "movePrinter" in data:
                globals.app.api.idleTimer = time.time()
                globals.app.api.browserMoveCommand(data)
            elif "sendCommand" in data:
                globals.app.api.idleTimer = time.time()
                data = data.replace('sendCommand: ', "")
                globals.app.api.printer.sendCommand(data, priority=True)
                
        except Exception as e:
            print("error in ParseData")
            print(str(e))
        return ""
        
    def _monitor(self):
        self.server_socket.listen(11)
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST,[],[])
            for sock in read_sockets:
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.CONNECTION_LIST.append(sockfd)
                else:
                    data = sock.recv(self.RECV_BUFFER)
                    if not data:
                        break
                    print("my_string: ")    
                    my_string = 'Ontvangen' + self.parseData(data) + '\n'
                    my_string = my_string.encode('utf-8')
                    sock.send(my_string)
                    sock.close()
                    self.CONNECTION_LIST.remove(sock)

        self.server_socket.close()