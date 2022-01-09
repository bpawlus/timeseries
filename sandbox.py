
# creation of data
from ruptures.metrics import *

set1split = "0,20,150,huj".split(",")
set2split = "0,20,150".split(",")
try:
    set1 = list(map(int, set1split))
    set2 = list(map(int, set2split))

    if(len(set1) >= 3, len(set2) >= 3):
        hausdorff(set1, set2)
        randindex(set1, set2)
        p, r = precision_recall(set1, set2, margin=5)
    else:
        print('shit')
except:
    print('shit')