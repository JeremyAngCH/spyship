from pathlib import Path
import gameconfig as gConf

SETTINGS_FILE = 'res/settings.dat'
RANKINGS_FILE = 'res/rankings.dat'

gRankings = []


def saveSettings():
    f = open(SETTINGS_FILE, "w+")
    f.write("%s\n" % str(gConf.MUSIC))
    f.write("%s\n" % str(gConf.SOUND))
    f.close()


def loadSettings():
    settings = [line.rstrip('\n') for line in open(SETTINGS_FILE)]
    gConf.MUSIC = True if settings[0].lower() == 'true' else False
    gConf.SOUND = True if settings[1].lower() == 'true' else False


def generateRankings():
    global gRankings

    gRankings.clear()
    for i in range(10):
        rankEntry = [(10 - i) * 500, 'ABC']
        gRankings.append(rankEntry)


def saveRankings():
    f = open(RANKINGS_FILE, "w+")
    for i in range(10):
        f.write("%s," % str((gRankings[i])[0]))
        f.write("%s\n" % (gRankings[i])[1])
    f.close()


def loadRankings():
    rankings = [line.rstrip('\n') for line in open(RANKINGS_FILE)]
    gRankings.clear()
    for i in range(10):
        dat = rankings[i].split(',')
        rankEntry = [int(dat[0]), dat[1]]
        gRankings.append(rankEntry)


def checkRankings(score):
    for i in range(10):
        if score > (gRankings[i])[0]:
            return i
    return -1


def insertRankings(score, name):
    startRank = checkRankings(score)
    if startRank < 0:
        return

    for i in range(9, startRank - 1, -1):
        if i < 9:
            (gRankings[i + 1])[0] = (gRankings[i])[0]
            (gRankings[i + 1])[1] = (gRankings[i])[1]
    (gRankings[startRank])[0] = score
    (gRankings[startRank])[1] = name


__settingsFile = Path(SETTINGS_FILE)
if not __settingsFile.is_file():
    saveSettings()
else:
    loadSettings()


__rankingsFile = Path(RANKINGS_FILE)
if not __rankingsFile.is_file():
    generateRankings()
    saveRankings()
else:
    loadRankings()
