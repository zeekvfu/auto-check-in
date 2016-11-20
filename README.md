auto-check-in
=======
### 用途
多家网站（eg. 淘宝、V2EX）的自动登录、签到。支持多用户。
### 运行环境
Linux/Windows + Python 3.x

# 淘宝
### 用途
登录[淘宝](https://www.taobao.com/)，领取淘金币。
### 软件包依赖
Selenium, Chrome/Firefox, lxml
### 运行方法
在 GUI 下，  
```
cd auto-check-in/src
PYTHONPATH=$(pwd) python3 taobao_taojinbi.py
```

# V2EX
### 用途
登录 [V2EX](https://www.v2ex.com/)，领取铜币。
### 软件包依赖
requests, lxml
### 运行方法
```
cd auto-check-in/src
PYTHONPATH=$(pwd) python3 v2ex_copper_coin.py
```


