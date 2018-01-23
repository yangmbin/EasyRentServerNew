# -*- coding:utf-8 -*-
import json
import os
import urllib2
import uuid
from urllib import urlopen, quote, urlencode

import time
from flask import render_template, redirect, request, session, url_for, flash, jsonify, json
from qiniu import Auth, put_file
from sqlalchemy import text, select

from EasyRent import app, DBSession, imageServer

import cgi, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

# 私钥文件
priKey = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCyW8fQpU+Qb078IFmeQAeqtRCNtPzvZLIFVJav2VDMP8BS3LoY33UDGTzqVPAJ7L01n/zmb4MNpxb3X2IsSo/SAWGEfgkFfpMuDfMH9v62X8KgsCBOSsEHK6K57NHKbC+gVonOM9yDGm3YFLP9b/YBFZ54lNkxQFHqetp31UWxawIDAQABAoGAS1eB3J04MucSEmcH9FVP58h8qZ+eiPGcUawdy0KdYuo7L8WVxxP9tcVfeg1PKKIcex6OEjlgvs+qX+ym59bHUVY+Htyo9u59QXNShTDFR3/pnhOxbgtkZZmyLE/qvA6s4H1efaLDj5NHlARMx7BD4QK9EDiw4JETo8oUzQXIZiECQQDZUR7wSjhDJv3zdcN/hU1w87IUTLyN1Fl2jchvOBIjYS434hdccatPiaxhCk8qmd+ybf6uE4Ro31U/SVttAwt3AkEA0htfRuBRQB5TrnHxsTDowWArQiILKjQ+KqJxtjPHXOH7zv2TGT8Zt6o3NNuKtwfbo6RMRyevHejUD5TkYdkerQJBAMuZTLsjTgLcDSCDPF3ErgEcz8JlAmJ+iDKiMx7AEX5EFeEVWX2qoS0rduyTlAf9ka7BjtHYRz1Zv6xDNfyz1ZECQETjlKm4gutzBhz8XzKpxqcg0Q4t+1srJfb0rDQBZiyeK+ICYmi0t8nwlYlPMnwwp2NQS3JJILG91UoGl5s9hUECQQDY+Xgorm7P5Q3WXMw+C3jPYpUsJPwi5ybbcipIXPqbD0bfgT9n+6FbNSzXiWlILxNwvRXjPrS+NwxLRIKH2paD
-----END RSA PRIVATE KEY-----'''

'''
* RSA签名
* data待签名数据
* 签名用商户私钥，必须是没有经过pkcs8转换的私钥
* 最后的签名，需要用base64编码
* return Sign签名
'''


def sign(data):
    key = RSA.importKey(priKey)
    h = SHA.new(data)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return base64.b64encode(signature)


'''
* 生成http请求的url字符串
* 参数顺序按照ASCII编码从小到大排列
* 最后生成的url的参数值需要做urlencode
'''


def generate_url():
    name = '杨明斌'
    cert_no = '522321199308256110'

    app_id = '2018010401588749'
    # biz_content = '{"transaction_id":' + time.strftime('%Y%m%d', time.localtime(
    #     time.time())) + ',"product_code":"w1010100000000002733","cert_type":"IDENTITY_CARD","cert_no":' + cert_no + ',"name":' + name + ',"admittance_score":650}'

    biz_content = '{admittance_score:650,cert_no:' + cert_no + ',cert_type:IDENTITY_CARD,product_code:w1010100000000002733,transaction_id:' + time.strftime('%Y%m%d', time.localtime(
        time.time())) + '}'
    charset = 'utf-8'
    format = 'JSON'
    method = 'zhima.credit.score.brief.get'
    sign_type = 'RSA'
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    version = '1.0'

    # 需要签名的参数（已排序）
    need_sign_params = 'app_id=' + app_id + '&' + \
                       'biz_content=' + biz_content + '&' + \
                       'charset=' + charset + '&' + \
                       'format=' + format + '&' + \
                       'method=' + method + '&' + \
                       'sign_type=' + sign_type + '&' + \
                       'timestamp=' + timestamp + '&' + \
                       'version=' + version

    # 生成签名
    sign_str = sign(need_sign_params)

    # urlencode字符串（针对参数值urlencode）
    urlencode_str = 'https://openapi.alipay.com/gateway.do?' + \
                    'app_id=' + quote(app_id) + '&' + \
                    'biz_content=' + quote(biz_content) + '&' + \
                    'charset=' + quote(charset) + '&' + \
                    'format=' + quote(format) + '&' + \
                    'method=' + quote(method) + '&' + \
                    'sign_type=' + quote(sign_type) + '&' + \
                    'timestamp=' + quote(timestamp) + '&' + \
                    'version=' + quote(version) + '&' + \
                    'sign=' + quote(sign_str)

    return urlencode_str


url = generate_url()
req = urllib2.Request(url)
res = urllib2.urlopen(req)
res = res.read()
print(res)
