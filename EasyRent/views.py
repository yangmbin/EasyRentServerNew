# -*- coding:utf-8 -*-
import json
import os
import urllib2
import uuid
from urllib import urlopen, quote

import time
from flask import render_template, redirect, request, session, url_for, flash, jsonify, json
from qiniu import Auth, put_file
from sqlalchemy import text, select

from EasyRent import app, DBSession, imageServer


@app.route('/manage')
def manage():
    return render_template('guipiao_manage_template/index.html')


# 贵漂公寓主页
@app.route('/')
def main_page():
    return render_template('/guipiao_web_template/index.html')


# 贵漂公寓关于
@app.route('/about')
def about():
    return render_template('/guipiao_web_template/about.html')


# 登录函数
@app.route('/manage/login', methods=['GET', 'POST'])
def manage_login():
    success_json = jsonify({'success': True, 'msg': '登录成功'})
    failure_json = jsonify({'success': False, 'msg': '用户名或密码不正确'})
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if username != 'admin' or password != 'admin':
            return failure_json
        else:
            session['is_login'] = True
            return success_json

    logged_json = jsonify({'success': False})
    not_logged_json = jsonify({'success': False})
    if request.method == 'GET':
        if 'is_login' in session and session['is_login']:
            return logged_json
        else:
            return not_logged_json


@app.route('/manage/index', methods=['GET', 'POST'])
def index():
    return render_template('/guipiao_manage_template/index.html')


# 登录函数（废弃）
# @app.route('/manage/login', methods=['GET', 'POST'])
# def login():
#     # 如果已经登录，则重定向到主页
#     if 'is_login' in session and session['is_login']:
#         return redirect(url_for('index'))
#
#     error = None
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         app.logger.error('username:' + username + ' password:' + password)
#         if username != 'admin' or password != 'admin':
#             error = '*用户名或密码不正确'
#             flash(error)
#             return redirect(url_for('login'))
#         else:
#             # 保存Cookie
#             response = make_response(redirect(url_for('index')))
#             if request.form.get('remember_me') is not None:
#                 response.set_cookie('username', username)
#                 response.set_cookie('password', password)
#             session['is_login'] = True
#             return response
#
#     return render_template('/guipiao_manage_template/login.html')



# 退出
@app.route('/logout')
def logout():
    session.pop("is_login", None)
    return redirect(url_for('login'))


# 添加租房信息
@app.route('/manage/add_house_info', methods=['GET', 'POST'])
def add_house_info():
    if request.method == 'POST':
        # name = request.form['name']
        # phone = request.form['phone']
        # DBSession.execute(text('insert into test(name, phone) values(:name, :phone)'), {'name':name, 'phone':phone})

        # 先根据输入的地址获取经纬度
        url = 'http://api.map.baidu.com/geocoder/v2/'
        output = 'json'
        ak = 'w92IN1iDP57Z5TH2G4I9I5kzpTnNj4NC'
        # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
        address = request.json.get('city') + request.json.get('region') + request.json.get('address')
        print address
        add = quote(str(address))
        uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
        req = urlopen(uri)
        res = req.read()
        temp = json.loads(res)

        # 非0状态都是地址解析失败
        if temp['status'] != 0:
            # flash('地址解析失败，请重新输入地址')
            print '地址解析失败，请重新输入地址'
            return jsonify({'success': False, 'msg': '地址解析失败，请重新输入地址'})
        else:
            lat = temp['result']['location']['lat']
            lng = temp['result']['location']['lng']
            print lng, lat

        params = request.json
        params['lat'] = lat
        params['lng'] = lng

        # 插入数据到数据库
        check_session_validation()
        DBSession.execute(text(
            'insert into house(city, region, images, address, minprice, maxprice, renttype, installation_wifi, installation_kitchen, installation_hoods, installation_water_heater, installation_washer, installation_toilet, pay_month, pay_season, pay_half, pay_year, longimage, lat, lng)' +
            'values(:city, :region, :images, :address, :minprice, :maxprice, :renttype, :installation_wifi, :installation_kitchen, :installation_hoods, :installation_water_heater, :installation_washer, :installation_toilet, :pay_month, :pay_season, :pay_half, :pay_year, :longimage, :lat, :lng)'),
            params)
        DBSession.commit()

        app.logger.error('添加成功')
        # flash('添加成功')
        # return redirect(url_for('add_house_info'))
        return jsonify({'success': True, 'msg': '添加成功'})
        # return render_template('/guipiao_manage_template/add_house_info.html')


# 上传图片到七牛
@app.route('/uploadFileToQiniu')
def uploadFileToQiniu():
    # if request.method == 'POST':
    # 需要填写你的 Access Key 和 Secret Key
    access_key = '-hmIOQEIQgnx_3dolengCAqBFqYF-07ntqFvENxd'
    secret_key = '7N7h6SINhsDjzhVbyaVo5hECxYRDvNcJMYREojXL'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'guipiao-oos'
    # 上传到七牛后保存的文件名
    # key = 'image/guipiao_manage/' + str(uuid.uuid1()) + '.png'
    key = 'image/test/' + str(uuid.uuid1()) + '.png'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = request.values.get('path')
    basepath = os.path.dirname(__file__)
    localfile = os.path.join(basepath, 'static' + os.path.sep + 'uploads', 'temp.png')
    print(localfile)
    ret, info = put_file(token, key, localfile)
    print(ret)
    if info.status_code == 200:
        return jsonify({'success': True, 'msg': '上传图片成功', 'path': ret['key']})
    else:
        return jsonify({'success': False, 'msg': '上传图片失败'})


# 上传图片到服务器
@app.route('/uploadFileToServer', methods=['POST'])
def uploadFileToServer():
    if request.method == 'POST':
        basepath = os.path.dirname(__file__)
        file = request.files['file']
        file.save(os.path.join(basepath, 'static' + os.path.sep + 'uploads', 'temp.png'))
        # return redirect(url_for('uploadFileToQiniu'))
        return uploadFileToQiniu()


# 修改联系方式
@app.route('/manage/edit_contact', methods=['GET', 'POST'])
def edit_contact():
    if request.method == 'POST':
        check_session_validation()
        DBSession.execute(text('update contact set phone = :contact where id = 1'), request.json)
        DBSession.commit()
        success_json = jsonify({'success': True, 'msg': '修改成功'})
        return success_json
        # return render_template('edit_contact.html')


# 主页banner图列表
@app.route('/manage/banner_list', methods=['GET', 'POST'])
def banner_list():
    check_session_validation()
    res = DBSession.execute(text('select * from house, banner where house.id = banner.houseid'), {})
    rows = res.fetchall()
    jsonData = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return jsonData
    # res = json.loads(jsonData)
    # for item in res:
    #     item['image'] = imageServer + item['image']
    # return render_template('banner_list.html', bannerList=res)


# 添加banner
@app.route('/manage/add_banner', methods=['GET', 'POST'])
def add_banner():
    if request.method == 'POST':
        check_session_validation()
        DBSession.execute(text('insert into banner(image, houseid) values(:image, :houseid)'), request.json)
        DBSession.commit()
        # flash('添加成功')
        return jsonify({'success': True, 'msg': '添加成功'})
        # return render_template('add_banner.html')


# 获取所有租房信息
@app.route('/manage/get_all_house_info', methods=['GET', 'POST'])
def get_all_house_info():
    check_session_validation()
    res = DBSession.execute(text('select * from house order by id DESC'), {})
    rows = res.fetchall()
    jsonData = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return jsonData


# 推荐公寓添加
@app.route('/manage/add_recommend', methods=['GET', 'POST'])
def add_recommend():
    if request.method == 'POST':
        check_session_validation()
        DBSession.execute(text('insert into recommend(image, houseid) values(:image, :houseid)'), request.json)
        DBSession.commit()
        # flash('添加成功')
        return jsonify({'success': True, 'msg': '添加成功'})
        # return render_template('add_recommend.html')


# 主页推荐公寓列表
@app.route('/manage/recommend_list', methods=['GET', 'POST'])
def recommend_list():
    check_session_validation()
    res = DBSession.execute(text('select * from house, recommend where house.id = recommend.houseid'), {})
    rows = res.fetchall()
    jsonData = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return jsonData
    # res = json.loads(jsonData)
    # for item in res:
    #     item['image'] = imageServer + item['image']
    # return render_template('recommend_list.html', recommendList=res)


# 删除banner公寓条目
@app.route('/manage/delete_banner', methods=['GET', 'POST'])
def delete_banner():
    check_session_validation()
    DBSession.execute(text('delete from banner where id=:id'), request.json)
    DBSession.commit()
    return jsonify({'success': True, 'msg': '删除成功'})


# 删除推荐公寓条目
@app.route('/manage/delete_recommend', methods=['GET', 'POST'])
def delete_recommend():
    check_session_validation()
    DBSession.execute(text('delete from recommend where id=:id'), request.json)
    DBSession.commit()
    return jsonify({'success': True, 'msg': '删除成功'})


# 租房列表（所有）
@app.route('/manage/house_list', methods=['GET', 'POST'])
def house_list():
    check_session_validation()
    res = DBSession.execute(text('select * from house'), {})
    rows = res.fetchall()
    jsonData = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    res = json.loads(jsonData)
    for item in res:
        images = item['images'].split(',')
        item['image'] = imageServer + images[0]
    return render_template('/guipiao_manage_template/house_list.html', houseList=res)


# 删除公寓
@app.route('/manage/delete_house', methods=['GET', 'POST'])
def delete_house():
    check_session_validation()
    try:
        DBSession.execute(text('delete from house where id=:id'), request.json)
        DBSession.execute(text('delete from banner where houseid=:id'), request.json)
        DBSession.execute(text('delete from recommend where houseid=:id'), request.json)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '删除失败，请重试'})
    return jsonify({'success': True, 'msg': '删除成功'})


# ====================================================================客户端相关接口====================================================================
# 每次请求完毕后，移除数据库session
@app.teardown_appcontext
def shutdown_session(exception=None):
    DBSession.remove()


# 每次数据库请求前，检查session是否可用
def check_session_validation():
    try:
        DBSession.scalar(select([1]))
    except:
        DBSession.rollback()
        DBSession.scalar(select([1]))


@app.route('/get_house_info/<int:size>/<int:page>', methods=['POST'])
def get_house_info(size, page):
    # res叫做ResultProxy      rows[0]叫做RowProxy

    if request.method == 'POST':
        # 获取传递过来的参数
        cityIndex = request.values.get('cityIndex')
        regionIndex = request.values.get('regionIndex')
        priceIndex = request.values.get('priceIndex')
        # print cityIndex
        # print regionIndex
        # print priceIndex

        # 城市目前只有贵阳，只判断区域和价格范围即可
        regionSql = ''
        priceSql = ''
        if regionIndex == '0':
            regionSql = ' where 1=1'
        elif regionIndex == '1':
            regionSql = ' where region=' + '"观山湖区"'
        elif regionIndex == '2':
            regionSql = ' where region=' + '"南明区"'
        elif regionIndex == '3':
            regionSql = ' where region=' + '"云岩区"'
        elif regionIndex == '4':
            regionSql = ' where region=' + '"花溪区"'

        if priceIndex == '0':
            priceSql = ' and 1=1 '
        elif priceIndex == '1':
            priceSql = ' and minprice<1000 '
        elif priceIndex == '2':
            priceSql = ' and ((minprice>=1000 and minprice<=1500) or (maxprice>=1000 and maxprice<=1500)) '
        elif priceIndex == '3':
            priceSql = ' and ((minprice>=1500 and minprice<=2000) or (maxprice>=1500 and maxprice<=2000)) '
        elif priceIndex == '4':
            priceSql = ' and ((minprice>=2000 and minprice<=2500) or (maxprice>=2000 and maxprice<=2500)) '
        elif priceIndex == '5':
            priceSql = ' and maxprice>2500 '

        offset = (page - 1) * size
        check_session_validation()
        res = DBSession.execute(
            text('select * from house' + regionSql + priceSql + 'order by id DESC limit :offset, :size'),
            {'offset': offset, 'size': size})
        rows = res.fetchall()
        # print rows[0].id

        # dictData = dict(rows[0].items())
        jsonData = json.dumps([(dict(row.items())) for row in rows])
        DBSession.commit()

        print jsonData
        return jsonData


# 获取联系方式
@app.route('/get_contact')
def get_contact():
    check_session_validation()
    res = DBSession.execute(text('select * from contact'))
    row = res.fetchone()
    jsonData = json.dumps(dict(row.items()))
    DBSession.commit()

    print jsonData
    return jsonData


# 获取banner公寓列表
@app.route('/get_banner_house_list')
def get_banner_house_list():
    check_session_validation()
    res = DBSession.execute(text('select * from house, banner where house.id = banner.houseid'), {})
    rows = res.fetchall()
    jsonData = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return jsonData


# 获取推荐公寓列表
@app.route('/get_recommend_house_list')
def get_recommend_house_list():
    check_session_validation()
    res = DBSession.execute(text('select * from house, recommend where house.id = recommend.houseid'), {})
    rows = res.fetchall()
    jsonData = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return jsonData


# 获取共享公寓列表（获取全部、获取某个人的）
@app.route('/get_share_house_list/<int:page>')
@app.route('/get_share_house_list/<int:page>/<openid>')
def get_share_house_list(page, openid=None):
    size = 10  # 固定分页条数为10条
    offset = (page - 1) * size
    condition_sql = ''
    if openid is not None:
        condition_sql = " and user_id = '" + openid + "'"
    check_session_validation()
    res = DBSession.execute(
        text(
            "select date_format(due_time, '%Y年%m月%d日') as due_time, house_img, address, house_type, rental, region, id from share_house where is_delete = 0" + condition_sql + " limit :offset, :size"),
        {'offset': offset, 'size': size})
    rows = res.fetchall()
    json_data = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return json_data


# 小程序登录（获取openid）
@app.route('/mini_login', methods=['POST'])
def mini_login():
    js_code = request.form['js_code']
    avatar = request.form['avatar']
    nickname = request.form['nickname']

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx4dab771ae44ce9b2&secret=1eab4ec4f8b87935ea3080bb638ec9d0&grant_type=authorization_code&js_code=' + js_code
    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req)
    res = res.read()
    res_obj = json.loads(res)
    openid = res_obj['openid']
    print(openid)

    # 获取到openid后保存在数据库（有则更新，无则插入）
    check_session_validation()
    try:
        DBSession.execute(
            text('insert ignore into mini_user(openid, avatar, nickname) values(:openid, :avatar, :nickname)'),
            {'openid': openid, 'avatar': avatar, 'nickname': nickname})
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '登录失败'})
    return jsonify({'success': True, 'openid': openid, 'msg': '登录成功'})


# 插入公寓分享信息
@app.route('/add_share_house', methods=['POST'])
def add_share_house():
    check_session_validation()
    try:
        DBSession.execute(
            text(
                'insert into share_house(user_id, house_img, city, region, address, house_type, rental, pay_type, installation, due_time, contact, gender, phone, agreement, ownership) values(:user_id, :house_img, :city, :region, :address, :house_type, :rental, :pay_type, :installation, :due_time, :contact, :gender, :phone, :agreement, :ownership)'),
            request.form)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '提交失败，请重试'})
    return jsonify({'success': True, 'msg': '提交成功'})


# 获取公寓分享信息详情
@app.route('/get_share_house_detail/<int:house_id>/<openid>')
def get_share_house_detail(house_id, openid):
    check_session_validation()

    # 共享公寓的相关信息（得到字典）
    house_res = DBSession.execute(text('select * from share_house where share_house.id = :house_id'),
                                  {'house_id': house_id})
    house_row = house_res.fetchone()
    house_row_dict = dict(house_row.items())

    # 查询是否收藏
    like_res = DBSession.execute(text('select * from share_house_like where user_id = :openid and house_id = :house_id'), {'openid': openid, 'house_id': house_id})
    rowcount = like_res.rowcount
    house_row_dict['like'] = rowcount

    # 查询共享公寓的评论列表
    comment_res = DBSession.execute(text(
        'select *, date_format(share_house_comment.time, "%Y/%m/%d %H:%i:%s") as format_time from share_house_comment, mini_user where share_house_comment.share_house_id = :house_id and share_house_comment.user_id = mini_user.openid order by share_house_comment.id desc'),
        {'house_id': house_id})
    comment_rows = comment_res.fetchall()
    comment_dict_list = [(dict(comment_row.items())) for comment_row in comment_rows]
    # 查询共享公寓每个评论对应的回复
    for comment_item in comment_dict_list:
        comment_id = comment_item['id']
        reply_res = DBSession.execute(text(
            'select *, date_format(share_house_reply.time, "%Y/%m/%d %H:%i:%s") as format_time from share_house_reply, mini_user where share_house_reply.share_house_comment_id = :comment_id and share_house_reply.user_id = mini_user.openid order by share_house_reply.id desc'),
            {'comment_id': comment_id})
        reply_rows = reply_res.fetchall()
        reply_dict_list = [(dict(reply_row.items())) for reply_row in reply_rows]
        # 每个回复，添加被回复人的信息
        for item in reply_dict_list:
            reply_user_id = item['reply_user_id']
            reply_user_res = DBSession.execute(text('select * from mini_user where openid = :reply_user_id'),
                                               {'reply_user_id': reply_user_id})
            reply_user_row = reply_user_res.fetchone()
            reply_user_dict = dict(reply_user_row.items())
            item['reply_avatar'] = reply_user_dict['avatar']
            item['reply_nickname'] = reply_user_dict['nickname']
        comment_item['reply'] = reply_dict_list  # 添加回复信息
    house_row_dict['comment'] = comment_dict_list  # 添加评论信息

    json_data = json.dumps(house_row_dict)
    DBSession.commit()
    return json_data


# 分享公寓（评论）
@app.route('/share_house_comment', methods=['POST'])
def share_house_comment():
    params = {}
    params['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for key in request.form.iterkeys():
        params[key] = request.form[key]
    print params

    check_session_validation()
    try:
        DBSession.execute(
            text(
                'insert into share_house_comment(user_id, share_house_id, content, time) values(:user_id, :share_house_id, :content, :time)'),
            params)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '提交失败，请重试'})
    return jsonify({'success': True, 'msg': '提交成功'})


# 分享公寓（回复）
@app.route('/share_house_reply', methods=['POST'])
def share_house_reply():
    params = {}
    params['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for key in request.form.iterkeys():
        params[key] = request.form[key]
    print params

    check_session_validation()
    try:
        DBSession.execute(
            text(
                'insert into share_house_reply(user_id, reply_user_id, share_house_comment_id, content, time) values(:user_id, :reply_user_id, :share_house_comment_id, :content, :time)'),
            params)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '提交失败，请重试'})
    return jsonify({'success': True, 'msg': '提交成功'})


# 删除分享公寓信息
@app.route('/delete_share_house', methods=['POST'])
def delete_share_house():
    check_session_validation()
    try:
        DBSession.execute(text('update share_house set is_delete = 1 where id = :id'), request.form)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '删除失败，请重试'})
    return jsonify({'success': True, 'msg': '已删除'})


# 小程序消息推送接口
@app.route('/message_push', methods=['GET', 'POST'])
def message_push():
    echostr = request.args.to_dict().get('echostr', "")
    return echostr


# 分享公寓添加收藏
@app.route('/share_house_like', methods=['POST'])
def share_house_like():
    check_session_validation()
    try:
        DBSession.execute(text('insert into share_house_like(user_id, house_id) values(:user_id, :house_id)'), request.form)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '添加收藏失败'})
    return jsonify({'success': True, 'msg': '已收藏', 'like': 1})


# 分享公寓取消收藏
@app.route('/share_house_dislike', methods=['POST'])
def share_house_dislike():
    check_session_validation()
    try:
        DBSession.execute(text('delete from share_house_like where user_id = :user_id and house_id = :house_id'), request.form)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '取消收藏失败'})
    return jsonify({'success': True, 'msg': '已取消', 'like': 0})


# 我的收藏列表
@app.route('/share_house_like_list/<int:page>/<openid>')
def share_house_like_list(page, openid):
    size = 10  # 固定分页条数为10条
    offset = (page - 1) * size
    check_session_validation()
    res = DBSession.execute(
        text(
            "select date_format(sh.due_time, '%Y年%m月%d日') as due_time, sh.house_img, sh.address, sh.house_type, sh.rental, sh.region, sh.id from share_house as sh, share_house_like as shl where sh.is_delete = 0 and shl.user_id = :openid and sh.id = shl.house_id limit :offset, :size"),
        {'offset': offset, 'size': size, 'openid': openid})
    rows = res.fetchall()
    json_data = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return json_data


# 我的留言列表
@app.route('/my_share_house_comment_list/<int:page>/<openid>')
def my_share_house_comment_list(page, openid):
    size = 10  # 固定分页条数为10条
    offset = (page - 1) * size
    check_session_validation()
    res = DBSession.execute(
        text(
            "select a.content, DATE_FORMAT(a.time,'%Y/%m/%d %H:%i:%s') as time, c.avatar, c.nickname, b.address, b.house_type, a.share_house_id as house_id, a.id as comment_id from share_house_comment as a, share_house as b, mini_user as c where a.share_house_id = b.id and b.user_id = :openid and a.user_id = c.openid and b.is_delete = 0 order by a.time desc limit :offset, :size"),
        {'offset': offset, 'size': size, 'openid': openid})
    rows = res.fetchall()
    json_data = json.dumps([(dict(row.items())) for row in rows])
    DBSession.commit()
    return json_data


# 删除评论（对应的二级回复也全部删除）
@app.route('/delete_share_house_comment', methods=['POST'])
def delete_share_house_comment():
    check_session_validation()
    try:
        DBSession.execute(text('delete from share_house_comment where id = :comment_id'), request.form)
        DBSession.execute(text('delete from share_house_reply where share_house_comment_id = :comment_id'), request.form)
        DBSession.commit()
    except:
        DBSession.rollback()
        return jsonify({'success': False, 'msg': '删除失败'})
    return jsonify({'success': True, 'msg': '已删除'})
