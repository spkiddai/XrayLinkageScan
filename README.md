rad_xray_auto Release
===========================
***
# 环境依赖
> 
* Python3
* requirements.txt
***
# 运行方式
> 
* usage: main.py

* optional arguments:
  - -h, --help            show this help message and exit
  - -l LOG, --log LOG     BurpSutie Export File
  - -t TARGET, --target TARGET    Target Name
  - -f FILE, --file FILE  Target File
***
# 配置文件介绍
> 
* system:                                       #系统配置
  - sys: mac                                    #操作系统[win、mac、linux]
* xray:                                         #xray配置信息
  - name: xray_darwin_amd64                     #xray程序名称 注:win操作系统需要exe后缀名
  - proxy: 127.0.0.1:8888                       #代理端口配置
* rad:                                          #rad配置信息
  - name: rad_darwin_amd64                      #rad程序名称 注:win操作系统需要exe后缀名
  - chrome:                                     #chrome浏览器路径 注：rad报错时可配置
* parse:                                        #默认解析配置
  - header:                                     #需要解析的header请求，可按照格式新增其他header
    + Host
    + Cookie
    + User-Agent
***
# 目录结构描述
> 
* ├──Readme.md                   #help
* ├──main.py                     #执行函数
    - ├──run.py                  #rad和xray运行函数
    - ├──yaml_write.py           #rad配置文件读写函数
    - ├──sys_config.yaml         #配置文件
* ├──rad_config.yaml.example     #rad配置文件示例
* ├──xray_config.yaml.example    #xray配置文件示例
* ├──config.yaml                 #xray配置文件
* ├──rad_config.yml              #rad配置文件
* └──requirements.txt            #Python3依赖
***
# V2.1 版本内容更新
> 
1. 新增-k参数，用于kill xray进程
2. 优化http、https检测函数
3. 解决存在的某些BUG
