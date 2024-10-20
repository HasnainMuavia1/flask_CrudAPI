import os
import glob
__all__=[]
path=os.listdir("controller")
for i in path:
    __all__.append(os.path.splitext(i)[0])
