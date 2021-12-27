# asiayo

有docker 就先build image，docker run時設好port就能使用

沒有docker在venv裡安裝requirements.txt，之後執行start_api.py

API設計文件: api_info_swagger.json

API測試: 程式執行後前往http://127.0.0.1:8000/restful_swagger按下Try it out就可以進行測試

API輸入驗證: source: USD, target: JPY, amount: 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
source: USD, target: USD, amount: -99
source: TWD, target: JPY, amount: 9999999
source: TWD, target: TWD, amount: 888888
source: TWD, target: USD, amount: 1000000000
source: JPY, target: JPY, amount: 77777777
source: JPY, target: TWD, amount: 1000000000000
source: JPY, target: USD, amount: 10000000000000000
source: USD, target: JPY, amount: 66666666.66
source: USD, target: TWD, amount: 7777777.77
source: USD, target: USD, amount: 9999999999.99


