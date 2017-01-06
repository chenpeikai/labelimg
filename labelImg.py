#!/usr/bin/env python
# -*- coding: utf8 -*-
#!/usr/bin/env python
# -*- coding: utf8 -*-
import _init_path
import sys
from ui import *
from ui import __appname__
import resources
### Utility functions and classes.

def main(argv):
    """Standard boilerplate Qt application code."""
    app = QApplication(argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("app"))
    win = MainWindow(argv[1] if len(argv) == 2 else None)
    win.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
