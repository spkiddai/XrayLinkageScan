#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 * Created by PyCharm.
 * User: Spkiddai
 * Date: 2021-3-10
"""

import os,yaml,urllib.parse,subprocess,requests,time
from yaml_write import *

def parse_log(filepath,sys_config):
    req_dict = {}
    with open(filepath,'r') as burp_log:
        req_list = burp_log.readlines()
    s = req_list[0].replace("\n","").replace("HTTP/1.1","").split(" ",1)
    req_dict.update({"Path":s[1].replace(" ","")})
    for i in req_list[1:]:
        s = i.replace("\n", "").split(":", 1)
        if s[0] in sys_config['parse']['header']:
            req_dict.update({s[0].replace(" ", ""): s[1].replace(" ", "")})
    return req_dict

def parse_target(arg,id):
    host = []
    target = []
    if id == 0:
        parse = urllib.parse.urlparse(arg)
        host.append(parse.netloc)
        target.append(arg)
    elif id == 1:
        with open(arg, 'r') as domain_file:
            domain_list = domain_file.readlines()
        for i in domain_list:
            parse = urllib.parse.urlparse(i.replace("\n",""))
            host.append(parse.netloc)
            target.append(i.replace("\n",""))
    return host,target

def rad_run(sys_config,target,datetime):
    if sys_config['system']['sys'] == 'win':
        radsh = [sys_config['rad']['name'],'-t',target,'-http-proxy',sys_config['xray']['proxy']]
    elif sys_config['system']['sys'] == 'linux' or sys_config['system']['sys'] == 'mac':
        radsh = ['./'+sys_config['rad']['name'], '-t', target, '-http-proxy', sys_config['xray']['proxy']]
    with open('./log/rad'+datetime+'.log', 'w') as radlog:
        radsp = subprocess.Popen(radsh, stdout=radlog, start_new_session=True)
        radsp.communicate()
    return

def xray_run(sys_config,datetime):
    if os.path.exists('ca.crt') and os.path.exists('ca.key'):
        if sys_config['system']['sys'] == 'win':
            if req_proxy(sys_config):
                killcmd = "taskkill /f /t /im {}".format(sys_config['xray']['name'])
                subprocess.Popen(killcmd, stdout=subprocess.PIPE, shell=True)
            xraysh = [sys_config['xray']['name'], 'webscan', '--listen', sys_config['xray']['proxy'], '--html-output',datetime + '.html']
        elif sys_config['system']['sys'] == 'linux' or sys_config['system']['sys'] == 'mac':
            if req_proxy(sys_config):
                pidsh = """ps -ef|grep """+sys_config['xray']['name']+"""|grep -v "grep"|awk '{print $2}'"""
                pid = subprocess.Popen(pidsh, stdout=subprocess.PIPE, shell=True)
                killsh = "kill -9 " + pid.stdout.readline().decode()
                subprocess.Popen(killsh, stdout=subprocess.PIPE, shell=True)
            xraysh = ['./'+sys_config['xray']['name'], 'webscan', '--listen', sys_config['xray']['proxy'], '--html-output',datetime + '.html']
        else:
            raise Exception('[-] ERROR:请检查配置文件，确认操作系统类型！')
        with open('./log/xray'+datetime+'.log', 'w') as xraylog:
            subprocess.Popen(xraysh, stdout=xraylog)
            return
    else:
        raise Exception('[-] ERROR: 证书文件不存在，请执行genca.py生成证书，并导入证书文件！')

def req_proxy(sys_config):
    proxies = {'http': sys_config['xray']['proxy']}
    try:
        response = requests.get('http://xray/', proxies=proxies)
        if response.status_code == 200:
            return True
    except:
        return False


with open('sys_config.yaml', 'r', encoding='utf-8') as config_yaml:
    sys_config = yaml.load(config_yaml, Loader=yaml.FullLoader)

yw = yaml_write(sys_config)

datetime = time.strftime("%Y%m%d%H%M%S", time.localtime())

def log_run(arg):
    xray_run(sys_config,datetime)
    time.sleep(5)
    req_dict = parse_log(arg, sys_config)
    yw.log_write(req_dict)
    target = req_dict['Host']+ req_dict['Path']
    rad_run(sys_config,target,datetime)

def target_run(arg,id):
    xray_run(sys_config,datetime)
    time.sleep(5)
    host,target = parse_target(arg,id)
    yw.target_write(host)
    for t in target:
        rad_run(sys_config, t, datetime)