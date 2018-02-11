## Compare2Set_test - Dakota Madden-Fong

from urllib import request as urlreq
import numpy as np
import cv2
from matplotlib import pyplot as plt
from mtg_cards import card_set_json as setjson
import math
import os

# User Provided Info
#--------------------------------------------------------------------
camimg = cv2.imread('Set2_c/bgl_c_cropped.jpg')

files = os.listdir('./Set2')
set_images = [];
for name in files:
    set_images.append(cv2.imread('Set2/'+name))
#--------------------------------------------------------------------

camimg2g = cv2.cvtColor(camimg, cv2.COLOR_BGR2GRAY)

surf = cv2.xfeatures2d.SURF_create()
surf.setHessianThreshold(100)
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

(kpr, desr) = surf.detectAndCompute(camimg2g,None)

printsimages = []
printsimages2g = []
printskp = []
printsdes = []
printsmatches = []
printsmatcheslen = []
## Fetch Card Images and Match Features
for img in set_images:
    printsimages.append(img)

    img2g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    printsimages2g.append(img2g)

    (kp, des) = surf.detectAndCompute(img2g,None)
    printskp.append(kp)
    printsdes.append(des)

    matches = bf.match(desr,des)
    matches = sorted(matches, key = lambda x:x.distance)
    printsmatches.append(matches)
    printsmatcheslen.append(len(matches))

## Find Three Best Matches and Display
print(printsmatcheslen)
for x in range(3):
    bestmatch = np.argmax(printsmatcheslen)
    print("Match",(x+1),':', bestmatch,'with',printsmatcheslen[bestmatch])
    test = camimg2g
    test = cv2.drawMatches(camimg2g,kpr,printsimages2g[bestmatch],printskp[bestmatch],printsmatches[bestmatch][:30],test,flags=2)
    cv2.namedWindow(("Match "+str(x+1)));
    cv2.imshow(("Match "+str(x+1)), test );
    cv2.waitKey()
#    plt.imshow(test),plt.show()
    printsmatcheslen[bestmatch] = -math.inf

cv2.destroyAllWindows()