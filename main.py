#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 * Created by PyCharm.
 * User: Spkiddai
 * Date: 2021-3-10
"""

import argparse
from tool_run import tool_run

print("""
                __   .__    .___  .___      .__ 
  ____________ |  | _|__| __| _/__| _/____  |__|
 /  ___/\____ \|  |/ /  |/ __ |/ __ |\__  \ |  |
 \___ \ |  |_> >    <|  / /_/ / /_/ | / __ \|  |
/____  >|   __/|__|_ \__\____ \____ |(____  /__|
     \/ |__|        \/       \/    \/     \/    
""")

print("""
use: rad and xray batch scanning
author: Spkiddai
github: https://github.com/spkiddai
csdn: https://blog.csdn.net/u012994510
""")

run = tool_run()

def main():
    info = "个人制作，仅供学习使用，不可用于商业用途，切勿将代码内容用于任何违法行为, 违者后果自负。"
    sysparser = argparse.ArgumentParser(description='rad and xray batch scanning',epilog=info)
    sysparser.add_argument('-l', '--log', dest='log', type=str, help='BurpSutie Export File')
    sysparser.add_argument('-t', '--target', dest='target', type=str, help='Target Name')
    sysparser.add_argument('-f', '--file', dest='file', type=str, help='Target File')
    sysparser.add_argument('-k', '--kill', dest='kill', action='store_true', help='Kill Xray')
    args = sysparser.parse_args()
    if args.target:
        run.target_run(args.target)
    elif args.file:
        run.file_run(args.file)
    elif args.log:
        run.log_run(args.log)
    elif args.kill:
        run.kill_xray()
    else:
        sysparser.print_help()

if __name__ == '__main__':
    main()