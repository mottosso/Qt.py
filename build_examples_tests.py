import os
import glob
import shutil


for filepath in glob.glob('examples/*.py'):
    filename = os.path.basename(filepath)
    shutil.copyfile(filepath, 'test_'+filename)
