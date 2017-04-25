from tkinter import *
from tkinter import messagebox

TOP_HEIGHT = 20 #meters above the coordinate
BOTTOM_HEIGHT = 3 #meters above the coordinate
COORD_FRAME = 3
VERSION = 110
WAYPOINT_COMMAND = 16
SERVO_COMMAND = 183
SERVO_NUMBER = 5
PWM = 1500
MIN_ALTITUDE = 0
MAX_ALTITUDE = 100

class MissionGenerator:

    def __init__(self, numWaypoints, fileName, coords, homeCoord):
        self.numWaypoints = numWaypoints
        self.fileName = fileName
        self.coords = coords 
        self.homeCoord = homeCoord
        self.index = 0

    def createWaypointFile(self):
        self.file = open(fileName, 'w')
        self.file.write('QGC WPL {}\n'.format(VERSION)) #Leading line expected by parser
        homeStart = "{0}\t1\t0\t{1}\t0\t0\t0\t0\t{2}\t{3}\t{4}\t1\n".format(self.index, WAYPOINT_COMMAND, self.homeCoord.longitude,
                            self.homeCoord.latitude, self.homeCoord.altitude)
        self.file.write(homeStart)
        self.index += 1
        for coord in coords:
            self.writeCoord(coord, altitude + TOP_HEIGHT)
            self.writeCoord(coord, altitude + BOTTOM_HEIGHT)
            self.activateServo()
            self.writeCoord(coord, altitude + TOP_HEIGHT)

        homeEnd = "{0}\t0\t0\t{1}\t0\t0\t0\t0\t{2}\t{3}\t{4}\t1\n".format(self.index, WAYPOINT_COMMAND, self.homeCoord.longitude,
                            self.homeCoord.latitude, self.homeCoord.altitude)
        self.file.write(homeEnd)
        self.file.close()

    def writeCoord(self, coord, altitude):
        line = "{0}\t0\t{1}\t{2}\t0\t0\t0\t0\t{3}\t{4}\t{5}\t1\n".format(self.index, 
                            COORD_FRAME, WAYPOINT_COMMAND, coord.longitude, coord.latitude, altitude, 1)
        self.index += 1
        self.file.write(line)

    def activateServo(self):
        line = "{0}\t0\t{1}\t{2}\t{3}\t{4}\t0\t0\t0\t0\t0\t1\n".format(self.index,
                            COORD_FRAME, SERVO_COMMAND, SERVO_NUMBER, PWM)
        self.index += 1
        self.file.write(line)
        
class Coordinate:
    def __init__(self, longitude, latitude, altitude):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude

class MissionWindow:

    def __init__(self, root):
        self.root = root
        self.frame1 = Frame(self.root)
        self.mainFrame = Frame(self.root)
        self.frame1.pack()
        self.coords = []
        self.fields = []
        self.initialSetup()

    def initialSetup(self):
        Label(self.frame1, text="Number of Waypoints:").grid(row=0, column=0) 
        Label(self.frame1, text="File Name:").grid(row=1,column=0)
        self.fields.append(Entry(self.frame1))
        self.fields.append(Entry(self.frame1))
        self.fields[0].grid(row=0,column=1)
        self.fields[1].grid(row=1,column=1)
        Button(self.frame1, text="Continue", command=self.mainWindowTransition).grid(
                row=2, column=1)

    def mainWindowSetup(self):
        r = 0
        c = 0
        Label(self.mainFrame, text="Home Coordinates").grid(row=r, column=c)
        r += 1
        waypointNum = 1
        for i,field in enumerate(self.fields):
            #skip first 3 because they are for the home coordinates
            #if i < 3:
            #    continue
            if i % 3 == 0 and i != 0:
                r += 1
                c = 0
                Label(self.mainFrame, text="Waypoint {}".format(waypointNum)).grid(row=r, column=c)
                waypointNum += 1
                r += 1
            field.grid(row=r,column=c)
            c += 1
        r += 1
        c = 2
        Button(self.mainFrame, text="Create Waypoint File", command=self.createFile).grid(row=r,column=c)

    def createFile(self):
        validInput = self.validateInput()
        if validInput:
            for coord in self.coords:
                print(coord)


    #returns false if input is invalid, true if valid
    def validateInput(self):
        LAT_TYPE = 0
        LONG_TYPE = 1
        ALT_TYPE = 2
        fieldTypes = [LAT_TYPE, LONG_TYPE, ALT_TYPE]
        typeIndex = 0
        for i,field in enumerate(self.fields, start=1):
            fieldType = fieldTypes[typeIndex % 3]
            try:
                currentField = float(field.get())
                if fieldType == ALT_TYPE:
                    if currentField < MIN_ALTITUDE or currentField > MAX_ALTITUDE:
                        raise AltError
                elif fieldType == LONG_TYPE:
                    if currentField < 0 or currentField > 180:
                        raise LongError
                elif fieldType == LAT_TYPE:
                    if currentField < 0 or currentField > 90:
                        raise LatError
                self.coords.append(currentField)
                typeIndex += 1
            except AltError:
                messagebox.showinfo("Error", "Altitude must be between 0 and 100 inclusive")
                return False
            except LongError:
                messagebox.showinfo("Error", "Longitude must be between 0 and 180 inclusive")
                return False
            except LatError:
                messagebox.showinfo("Error", "Latitude must be between 0 and 90 inclusive")
                return False
            except ValueError:
                messagebox.showinfo("Error", "All fields must be a valid number")
                return False
        return True
                    
    def mainWindowTransition(self):
        validInput = True
        try:
            self.numWaypoints = int(self.fields[0].get())
            if self.numWaypoints < 1 or self.numWaypoints > 8:
                raise ValueError
        except ValueError:
            validInput = False
            messagebox.showinfo("Error", "Number of waypoints must be an integer between 1 and 8")

        if validInput:
            self.fileName = self.fields[1].get()

            #remove frame1 
            self.frame1.grid_forget()
            self.frame1.destroy()

            #clear fields list
            self.fields = []
            self.addTextFields(self.numWaypoints * 3 + 3)
            self.mainWindowSetup()

            self.mainFrame.pack()

    def addTextFields(self, n):
        for i in range(n):
            self.fields.append(Entry(self.mainFrame))

class AltError(Exception):
    pass

class LongError(Exception):
    pass

class LatError(Exception):
    pass


if __name__ == '__main__':

    root = Tk()
    root.minsize(width=500,height=500)
    root.title('Mission Generator')
    window = MissionWindow(root)
    root.mainloop()

    numWaypoints = int(input('How many waypoint?\n'))
    fileName = input('What do you want to call the waypoint file?\n')
    coords = []

    homeLong = float(input('Longitude of starting coordinates\n'))
    homeLat = float(input('Latitude of starting coordinates\n'))
    homeAlt = float(input('Altitude of starting Coordinate\n'))
    homeCoord = Coordinate(homeLong, homeLat, homeAlt)
    for i in range(numWaypoints):
        longitude = float(input('Longitude of waypoint {0}?\n'.format(i+1)))
        latitude = float(input('Latitude of waypoint {0}?\n'.format(i+1)))
        altitude = float(input('Altitude of waypoint {0}?\n'.format(i+1)))
        coord = Coordinate(longitude, latitude, altitude)
        coords.append(coord)

    missionGenerator = MissionGenerator(numWaypoints, fileName, coords, homeCoord)
    missionGenerator.createWaypointFile()
