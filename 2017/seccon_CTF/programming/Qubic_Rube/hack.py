from PIL import Image
import zbarlight
import urllib
import time

yellow = (255, 213, 0)
red = (196, 30, 58)
orange = (255, 88, 0)
white = (255, 255, 255)
blue = (0, 81, 186)
green = (0, 158, 96)
color = [yellow, red, orange, white, blue, green]
colorNow = yellow

photo = ''

def photoInit():
    global photo
    photo = Image.open('1.png')
    pix = photo.load()
    for i in range(0, photo.size[0]):
        for j in range(0, photo.size[1]):
            pix[i, j] = (0, 0, 0)

mayPiece = ''

def init():
    global mayPiece
    photoInit()
    mayPiece = [[],[],[],[],[],[],[],[],[],[]]

def rotatePiece(piece):
    return zip(*piece[::-1])

def pieceDebug(piece, name):
    global photo
    photoInit()
    pix = photo.load()
    for i in range(0, 82):
        for j in range(0, 82):
            pix[i,j] = piece[i][j]
    photo.save(name+'.png')

def getIndex(x, y):
    if x<82:
        if y<82:
            return 1
        elif y>=82 and y<164:
            return 2
        else:
            return 3
    elif x>=82 and x<164:
        if y<82:
            return 4
        elif y>=82 and y<164:
            return 5
        else:
            return 6
    else:
        if y<82:
            return 7
        elif y>=82 and y<164:
            return 8
        else:
            return 9

def splitPiece(arr, x, y):
    global photo
    out = []
    for i in range(0, 10):
        tmp = []
        for j in range(0, 82):
            tmp.append([])
        out.append(tmp)
    for i in range(0, y):
        for j in range(0, x):
            out[getIndex(j,i)][i%82].append(arr[i,j])
    return out

def getPiece(name):
    global colorNow
    global mayPiece
    im = Image.open(name)
    pix = im.load()
    piece = splitPiece(pix, im.size[0], im.size[1])
    for i in range(1, len(piece)):
        valid = False
        for j in piece[i]:
            if colorNow in j:
                valid = True
                break
        if valid:
            target = []
            if i == 1:
                target = [7,9,3,1]
            elif i == 2:
                target = [4,8,6,2]
            elif i == 3:
                target = [1,7,9,3]
            elif i == 4:
                target = [8,6,2,4]
            elif i == 6:
                target = [2,4,8,6]
            elif i == 7:
                target = [9,3,1,7]
            elif i == 8:
                target = [6,2,4,8]
            elif i == 9:
                target = [3,1,7,9]
            else:
                target = [5,5,5,5]

            for j in target:
                piece[i] = rotatePiece(piece[i])
                mayPiece[j].append(piece[i])
        
                

def buildPhoto():
    global mayPiece
    global photo
    pix = photo.load()
    for a in range(0, len(mayPiece[1])):
        for b in range(0, len(mayPiece[2])):
            for c in range(0, len(mayPiece[3])):
                if c == a:
                    continue
                for d in range(0, len(mayPiece[4])):
                    if d == b:
                        continue
                    for e in range(0, len(mayPiece[5])):
                        for f in range(0, len(mayPiece[6])):
                            if f in [b,d]:
                                continue
                            for g in range(0, len(mayPiece[7])):
                                if g in [a,c]:
                                    continue
                                for h in range(0, len(mayPiece[8])):
                                    if h in [b,f,d]:
                                        continue
                                    for i in range(0, len(mayPiece[9])):
                                        if i in [a,c,g]:
                                            continue
                                        index = [0,a,b,c,d,e,f,g,h,i]
                                        for x in range(0, photo.size[0]):
                                            for y in range(0, photo.size[1]):
                                                tmp = getIndex(x,y)
                                                pix[y,x] = mayPiece[tmp][index[tmp]][y%82][x%82]
                                        #photo.save(str(a)+str(b)+str(c)+str(d)+str(e)+str(f)+str(g)+str(h)+str(i)+'.png')
                                        #time.sleep(3)
                                        code = zbarlight.scan_codes('qrcode', photo)
                                        if code is not None:
                                            print code[0]
                                            if 'http' in code[0]:
                                                return code[0].split('/')[-1]
                                            else:
                                                return ''
    return ''

def getPhoto(link):
    testfile = urllib.URLopener()
    testfile.retrieve(link, "tmp.png")

link = 'http://qubicrube.pwn.seccon.jp:33654/images/'
token = ['11ed5b705e72e9fa2e57']
note = 11
index = ['_R.png', '_L.png', '_U.png', '_D.png', '_F.png', '_B.png',]

j = 0
while j < len(token):
    print '******************' + token[j] + '******************'
    for k in color:
        print note, ':', k
        colorNow = k
        init()
        for i in index:
            getPhoto(link + token[j] + i)
            getPiece('tmp.png')
        m = {}
    
        tmp = buildPhoto()
        if tmp != '':
            token.append(tmp)
            print 'find at color', k
            break
    j += 1
    note += 1
    
