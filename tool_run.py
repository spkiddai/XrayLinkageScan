#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 * Created by PyCharm.
 * User: Spkiddai
 * Date: 2021-3-10
"""

import os
import time
import yaml
import requests
import subprocess
import urllib.parse
from yaml_write import yaml_write

class tool_run:

    def __init__(self):
        self.sys_config = self.read_sys()
        self.yw = yaml_write(self.sys_config)

    def read_sys(self):
        with open('sys_config.yml', 'r', encoding='utf-8') as config_yaml:
            sys_config = yaml.load(config_yaml, Loader=yaml.FullLoader)
        return sys_config

    def kill_xray(self):
        sys_proxy = self.sys_config['xray']['proxy'].split(':')
        if self.sys_config['system']['sys'] == 'mac':
            checksh = "lsof -i :" + sys_proxy[1] + "|awk 'NR==2 {print $1,$2}'"
            checksp = subprocess.run(checksh, shell=True, stdout=subprocess.PIPE)
            if checksp.stdout:
                killsh = 'kill -9 '+checksp.stdout.decode().split()[1]
                subprocess.run(killsh, shell=True, stdout=subprocess.PIPE)
                print('[+] INFO:xray进程结束')
            else:
                raise Exception('[-] ERROR:进程不存在')
        elif self.sys_config['system']['sys'] == 'linux':
            checksh = "netstat -auntp|grep ':" + sys_proxy[1] + "'|awk 'NR==2 {print $7}'"
            checksp = subprocess.run(checksh, shell=True, stdout=subprocess.PIPE)
            if checksp.stdout:
                killsh = 'kill -9 '+checksp.stdout.decode().split('/')[0]
                subprocess.run(killsh, shell=True, stdout=subprocess.PIPE)
                print('[+] INFO:xray进程结束')
            else:
                raise Exception('[-] ERROR:进程不存在')
        elif self.sys_config['system']['sys'] == 'win':
            check_sh = "netstat -ano|findstr "+sys_proxy
            checksp = subprocess.run(check_sh, shell=True, stdout=subprocess.PIPE)
            if checksp.stdout:
                killsh = "taskkill /f /im" + self.sys_config['xray']['name']
                subprocess.run(killsh, shell=True, stdout=subprocess.PIPE)
                print('[+] INFO:xray进程结束')
            else:
                raise Exception('[-] ERROR:进程不存在')
        else:
            raise Exception('[-] ERROR:请检查配置文件，确认操作系统类型！')

    def check_prot(self):
        sys_proxy = self.sys_config['xray']['proxy'].split(':')
        if self.sys_config['system']['sys'] == 'mac':
            checksh = "lsof -i :" + sys_proxy[1] + "|awk 'NR==2 {print $1,$2}'"
            checksp = subprocess.run(checksh, shell=True, stdout=subprocess.PIPE)
            if checksp.stdout:
                raise Exception('[-] ERROR:{}端口占用'.format(sys_proxy[1]))
            else:
                print('[+] INFO:端口未占用,xray正常启动')
        elif self.sys_config['system']['sys'] == 'linux':
            checksh = "netstat -auntp|grep ':" + sys_proxy[1] + "'|awk 'NR==2 {print $7}'"
            checksp = subprocess.run(checksh, shell=True, stdout=subprocess.PIPE)
            if checksp.stdout:
                raise Exception('[-] ERROR:{}端口占用'.format(sys_proxy[1]))
            else:
                print('[+] INFO:端口未占用,xray正常启动')
        elif self.sys_config['system']['sys'] == 'win':
            check_sh = "netstat -ano|findstr 8888"
            checksp = subprocess.run(check_sh, shell=True, stdout=subprocess.PIPE)
            if checksp.stdout:
                raise Exception('[-] ERROR:{}端口占用'.format(sys_proxy[1]))
            else:
                print('[+] INFO:端口未占用,xray正常启动')
        else:
            raise Exception('[-] ERROR:请检查配置文件，确认操作系统类型！')

    def check_sys(self,sh):
        if self.sys_config['system']['sys'] == 'mac' or 'linux':
            sh[0] = './' + sh[0]
            return sh
        elif self.sys_config['system']['sys'] == 'win':
            return sh
        else:
            raise Exception('[-] ERROR:请检查配置文件，确认操作系统类型！')

    def check_ca(self):
        if os.path.exists('ca.crt') and os.path.exists('ca.key'):
            print('[+] INFO:CA文件存在,无需新建')
            return
        else:
            os.unlink('ca.crt')
            os.unlink('ca.key')
            sh = [self.sys_config['xray']['name'], 'genca']
            gencash = self.check_sys(sh)
            subprocess.run(gencash)
            print('[+] INFO:CA文件创建成功')
            return

    def check_protocol(self,host):
        if 'http://' in host or 'https://' in host:
            return host
        else:
            try:
                target = 'https://' + host
                requests.get(target, timeout=5)
            except:
                target = 'http://' + host
            return target


    def rad_run(self, target, output,date):
        sh = [self.sys_config['rad']['name'], '-t', target, '-http-proxy', self.sys_config['xray']['proxy']]
        radsh = self.check_sys(sh)
        with open('log/rad_'+output+'_'+date+'.log', 'w') as radlog:
            sp = subprocess.Popen(radsh, stdout=radlog, start_new_session=True)
            sp.communicate()
            print('[+] INFO:爬取完成，log文件位置 log/rad_'+output+'_'+date+'.log')
        return

    def xray_run(self,output,date):
        self.check_ca()
        self.check_prot()
        sh = [self.sys_config['xray']['name'], 'webscan', '--listen', self.sys_config['xray']['proxy'], '--html-output',output+'_'+date+'.html']
        xraysh = self.check_sys(sh)
        with open('log/xray_'+output+'_'+date+'.log', 'w') as xraylog:
            subprocess.Popen(xraysh, stdout=xraylog)
            time.sleep(5)
            print('[+] INFO:xray已经启动，log文件位置 log/xray_'+output+'_'+date+'.log')
            return

    def parse_log(self,logpath):
        req_dict = {}
        with open(logpath, 'r') as burp_log:
            req_list = burp_log.readlines()
        s = req_list[0].replace("\n", "").replace("HTTP/1.1", "").split(" ", 1)
        req_dict.update({"Path": s[1].replace(" ", "")})
        for i in req_list[1:]:
            s = i.replace("\n", "").split(":", 1)
            if s[0] in self.sys_config['parse']['header']:
                req_dict.update({s[0].replace(" ", ""): s[1].replace(" ", "")})
        return req_dict

    def parse_file(self,file):
        hosts = []
        targets = []
        with open(file, 'r') as domain_file:
            for i in domain_file.readlines():
                i = self.check_protocol(i.replace("\n", ""))
                targets.append(i)
                parse = urllib.parse.urlparse(i)
                hosts.append(parse.netloc)
        return hosts,targets

    def target_run(self,argv):
        date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        target = self.check_protocol(argv)
        parse = urllib.parse.urlparse(target)
        host = parse.netloc
        self.yw.target_write(host)
        self.xray_run(host,date)
        print('[+] INFO:爬取开始，目标地址为{}'.format(target))
        self.rad_run(target,host,date)

    def file_run(self,argv):
        date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        hosts,targets = self.parse_file(argv)
        self.yw.target_write(hosts)
        file = os.path.basename(argv)
        self.xray_run(file,date)
        for t,h in zip(targets,hosts):
            print('[+] INFO:爬取开始，目标地址为{}'.format(t))
            self.rad_run(t, h, date)

    def log_run(self,argv):
        date = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        req_dict = self.parse_log(argv)
        self.yw.log_write(req_dict)
        self.xray_run(req_dict['Host'],date)
        target = self.check_protocol(req_dict['Host'] + req_dict['Path'])
        print('[+] INFO:爬取开始，目标地址为{}'.format(target))
        self.rad_run(target, req_dict['Host'], date)