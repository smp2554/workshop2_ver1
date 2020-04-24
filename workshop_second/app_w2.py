import json
import re
import requests
import random
from bs4 import BeautifulSoup
from datetime import date, timedelta
from flask import Flask, render_template, request
from selenium import webdriver

app = Flask(__name__, template_folder="template", static_folder="static")  
app.config['ENV'] = 'development'
app.config['DEBUG'] = True


# 첫 페이지 완성
@app.route("/")

def index():
    
    return "★ Welcome!! SHOPPING DAY!!!★ "


# main2 page 접속(NEW/OLD/쇼핑몰별 실시간 순위 링크 있음)

@app.route('/main2')
def main2():
    if 'user' in session:
        title = '★ Welcome!! ' + session['user']['id']+ '★'
    else:
        title = 'Welcome'
        
    menu=get_menu()
    return render_template('main2.html',
                           title=title,
                           menu=menu)



#wusinsa 홈페이지 호출
@app.route('/wusinsa')
def wusinsa():
    import requests
    res = requests.get('https://wusinsa.musinsa.com')
    return res.text


#쇼핑몰 별 실시간 순위 PAGE
# @app.route('/shop_ranking')
# def get_ranking():
    
    




#우신사 실시간 순위 
@app.route('/shop_ranking/wusinsa')
def get_ranking_wusinsa():
    
    res = requests.get("https://wusinsa.musinsa.com/app/contents/bestranking?u_cat_cd=")
    soup= BeautifulSoup(res.content, 'html.parser')
    product_rank=[]

    for num in soup.select("list-box.box"):
        rank_num = tag.select(".n-label")[0].get_text()
    
    for tag in soup.select(".article_info"):
        brand = tag.select(".item_title > a")[0].get_text()
        name = tag.select(".list_info > a")[0].get_text().strip()
        price = tag.select(".price")[0].get_text()
        if len(tag.select(".txt_cnt_like")) > 0:
            like_num= tag.select(".txt_cnt_like")[0].get_text().strip()
        else:
            like_num=0
        regex = re.compile("(\d+,\d+원)")
        real_price = re.findall(regex, price)[0]
        product_rank.append({'브랜드명': brand,
                 '이름': name,
                 '가격': real_price,
                 '좋아요 수': like_num})

        #print(price.replace('\t', '').strip())
#     print("*" * 30)   
#     print("실시간 랭킹 순위 ")
#     print("*" * 30)   

#     for i, rank in enumerate(product_rank):
#         print(i+1,"위", rank)
        
    
    return render_template('shoppingmall.html', 
                           title = "우신사", 
                           action='get_ranking_wusinsa',
                           products=product_rank)
        
        
app.run(port = 8009) #파이썬파일 실행 가능 (포트번호 지정)

#encoding="utf-8"