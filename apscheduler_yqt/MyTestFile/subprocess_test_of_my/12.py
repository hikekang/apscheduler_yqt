# -*- coding: utf-8 -*-
"""
   File Name：     12
   Description :
   Author :       hike
   time：          2021/4/21 13:44
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys

completed = subprocess.run(['ls',sys.argv[0],'-l'])
print('运行结果',completed.returncode)