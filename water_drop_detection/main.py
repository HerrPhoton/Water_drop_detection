import sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from water_drop_detection.ui.GUI import main

if __name__ == "__main__":
    main() 
