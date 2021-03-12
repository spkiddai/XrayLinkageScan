#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 * Created by PyCharm.
 * User: Spkiddai
 * Date: 2021-3-10
"""

import yaml

class yaml_write:

    def __init__(self,sys_config):
        self.rad_example = 'rad_config.yaml.example'
        self.xray_example = 'xray_config.yaml.example'
        self.sys_config = sys_config
        self.rad_config,self.xray_config = self.__read()

    def __read(self):
        with open(self.rad_example, 'r', encoding='utf-8') as rad_yaml:
            rad_config = yaml.load(rad_yaml, Loader=yaml.FullLoader)
        with open(self.xray_example, 'r', encoding='utf-8') as xray_yaml:
            xray_config = yaml.load(xray_yaml, Loader=yaml.FullLoader)
        return rad_config,xray_config

    def __write(self,rad_config,xray_config):
        if self.sys_config['rad']['chrome'] is not None:
            rad_config['exec-path'] = self.sys_config['rad']['chrome']
        else:
            pass
        with open('rad_config.yml', 'w', encoding='utf-8') as rad_yaml:
            yaml.dump(rad_config, rad_yaml)
        with open('config.yaml', 'w', encoding='utf-8') as xray_yaml:
            yaml.dump(xray_config, xray_yaml)
        return

    def log_write(self,req_dict):
        for key in req_dict.keys():
            if 'Host' in key:
                #self.xray_config['mitm']['restriction']['hostname_allowed'] = ['%s' % (req_dict['Host'])]
                self.rad_config['restrictions-on-urls']['allowed-domains'] = ['%s' % (req_dict['Host'])]
            elif 'User-Agent' in key:
                #self.xray_config['http']['headers']['User-Agent'] = req_dict['User-Agent']
                self.rad_config['request-config']['user-agent'] = req_dict['User-Agent']
            elif 'Cookie' in key:
                #self.xray_config['http']['headers']['Cookie'] = req_dict['Cookie']
                self.rad_config['request-config']['cookies'].pop(0)
                cookie_list = req_dict['Cookie'].split(";")
                for i in cookie_list:
                    s = i.split("=", 1)
                    self.rad_config['request-config']['cookies'].append({'name': s[0], 'value': s[1]})
            elif 'Path' not in key:
                #self.xray_config['http']['headers'][key] = req_dict[key]
                self.rad_config['request-config']['headers'].pop(0)
                self.rad_config['request-config']['headers'].append({'name': key, 'value': req_dict[key]})
        self.__write(self.rad_config,self.xray_config)
        return

    def target_write(self,target):
        #self.xray_config['mitm']['restriction']['hostname_allowed'] = target
        self.rad_config['restrictions-on-urls']['allowed-domains'] = target
        self.__write(self.rad_config,self.xray_config)
        return