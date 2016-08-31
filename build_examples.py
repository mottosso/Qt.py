import os
import glob
import shutil

# Copy example files into current working directory
for filepath in glob.glob('examples/*/*'):
    filename = os.path.basename(filepath)
    if filepath.endswith('.py'):
        shutil.copyfile(filepath, 'test_'+filename)  # Prepend 'test' to *.py
    else:
        shutil.copyfile(filepath, filename)
