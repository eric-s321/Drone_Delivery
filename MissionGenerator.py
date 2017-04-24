TOP_HEIGHT = 20 #meters above the coordinate
BOTTOM_HEIGHT = 3 #meters above the coordinate
COORD_FRAME = 3
VERSION = 110
WAYPOINT_COMMAND = 16
SERVO_COMMAND = 183
SERVO_NUMBER = 5
PWM = 1500

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

if __name__ == '__main__':
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
