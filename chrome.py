import os
import sys

# Change the Default Encoding 
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

bookmark_json = os.path.join(path_name, 'Bookmarks')