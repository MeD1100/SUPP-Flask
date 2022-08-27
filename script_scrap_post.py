# -*- coding: utf-8 -*-
from genericpath import exists
import string
from turtle import pos
from click import style
import pymongo
import datetime
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from insert_posts_mongoDB import Post, insert_post
from selenium.webdriver.common.action_chains import ActionChains
import random
import os
import pyautogui
import sys
import re
import requests as r
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import wget
from PIL import Image 
import PIL 
import urllib


PATH = r"C:/Users/medrh/Dropbox/Mon PC/Downloads/Compressed/chromedriver.exe"

def _login(browser, email, password):

    #browser.maximize_window()
    browser.find_element_by_id("email").send_keys(email)
    time.sleep(random.randint(4,7))
    browser.find_element_by_name("pass").send_keys(password)
    time.sleep(random.randint(4,7))
    browser.find_element_by_name("login").click()
    time.sleep(random.randint(4,7))

def extract_url_post(browser):
    urls = browser.find_element_by_css_selector("div.h07fizzr.nuz1ool1.alzwoclg > span.rse6dlih > a.qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq.cxfqmxzd.pbevjfx6")

    return urls.get_attribute("href")


def extract_nbr_commantaire(post,browser):
    try:
        time.sleep(5)
        boutton_comments = browser.find_elements_by_css_selector("div.dkzmklf5 > span.f7rl1if4.adechonz.f6oz4yja.dahkl6ri.axrg9lpx.rufpak1n.qtovjlwq.qbmienfq.rfyhaz4c.rdmi1yqr.ohrdq8us.nswx41af.fawcizw8.l1aqi3e3.sdu1flz4 > div.qi72231t.o9w3sbdw.tav9wjvu.flwp5yud.tghlliq5.gkg15gwv.fsf7x5fv.tgm57n0e.jez8cy9q.s5oniofx.dnr7xe2t.aeinzg81.rn8ck1ys.s3jn8y49.o9erhkwx.dzqi5evh.hupbnkgi.hvb2xoa8.fxk3tzhb.jl2a5g8c.f14ij5to.icdlwmnq.qgrdou9d.nu7423ey.s9ok87oh.s9ljgwtm.lxqftegz.bf1zulr9.frfouenu.bonavkto.djs4p424.r7bn319e.bdao358l.jxuftiz4.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.om3e55n1.cr00lzj9.g4tp4svg.cxfqmxzd > span")
        shares = ""

        if boutton_comments[0] is not None:
            x = boutton_comments[0].text
            x = x.split(" ", 0)
            shares = x
            return shares[0]     
        else:
            return "0"
    except:
        return "None"

# extraire l'url de la post
def extract_reactions (post):
    react = ""
    
    nbreact = post.find("span",class_= "cxfqmxzd nnzkd6d7").text
    if nbreact:
        react += "nbr_de_react :" + nbreact + "\n"
        
    list_react = post.find_all("div", class_="qi72231t o9w3sbdw nu7423ey tav9wjvu flwp5yud tghlliq5 gkg15gwv s9ok87oh s9ljgwtm lxqftegz bf1zulr9 frfouenu bonavkto djs4p424 r7bn319e bdao358l fsf7x5fv tgm57n0e jez8cy9q s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk dnr7xe2t aeinzg81 srn514ro oxkhqvkx rl78xhln nch0832m om3e55n1 cr00lzj9 rn8ck1ys s3jn8y49 g4tp4svg o9erhkwx dzqi5evh hupbnkgi hvb2xoa8 fxk3tzhb jl2a5g8c f14ij5to l3ldwz01 icdlwmnq")
    
    if list_react[0]["aria-label"]:
        react += "most_react :" + list_react[0]["aria-label"] + "\n"
        
    if list_react[1]["aria-label"] and list_react[1]["aria-label"] != list_react[0]["aria-label"]:
        react += "second_react :" + list_react[1]["aria-label"] + "\n"
        if list_react[2]["aria-label"] and list_react[2]["aria-label"] != list_react[1]["aria-label"]:
            react += "third_react" + list_react[2]["aria-label"] + "\n"
    
    return react

# extraire le nombre de partages
def extract_nbr_partages(browser):
    try:
        time.sleep(5)
        boutton_partage = browser.find_elements_by_css_selector("div.dkzmklf5 > span.f7rl1if4.adechonz.f6oz4yja.dahkl6ri.axrg9lpx.rufpak1n.qtovjlwq.qbmienfq.rfyhaz4c.rdmi1yqr.ohrdq8us.nswx41af.fawcizw8.l1aqi3e3.sdu1flz4 > div.qi72231t.o9w3sbdw.tav9wjvu.flwp5yud.tghlliq5.gkg15gwv.fsf7x5fv.tgm57n0e.jez8cy9q.s5oniofx.dnr7xe2t.aeinzg81.rn8ck1ys.s3jn8y49.o9erhkwx.dzqi5evh.hupbnkgi.hvb2xoa8.fxk3tzhb.jl2a5g8c.f14ij5to.icdlwmnq.qgrdou9d.nu7423ey.s9ok87oh.s9ljgwtm.lxqftegz.bf1zulr9.frfouenu.bonavkto.djs4p424.r7bn319e.bdao358l.jxuftiz4.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.om3e55n1.cr00lzj9.g4tp4svg.cxfqmxzd > span")
        shares = ""

        if boutton_partage[1] is not None:
            x = boutton_partage[1].text
            x = x.split(" ", 1)
            shares = x
            return shares[0]     
        else:
            return "0"
    except:
        return "None"

#extraire la la date du poste
def extract_post_date(post):
    div = post.find_all(class_="a.qi72231t.nu7423ey.n3hqoq4p.r86q59rh.b3qcqh3k.fq87ekyn.bdao358l.fsf7x5fv.rse6dlih.s5oniofx.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.srn514ro.oxkhqvkx.rl78xhln.nch0832m.cr00lzj9.rn8ck1ys.s3jn8y49.icdlwmnq.cxfqmxzd.rtxb060y.gh55jysx > span")
    if div :
            paragraphs = div[0].find('span')
            
            return(paragraphs.text)


#focntion pour extraire et retourner le contenue du titre du post   
def extract_titre(post,browser):

        # urls = browser.find_element_by_css_selector("div.hv4rvrfc.dati1w0a.jb3vyjys.qt6c0cv9 > div.f530mmz5.b1v8xokw.o0t2es00.oo9gr5id > div.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql")
        te = []
        actualPosts = post.find_all(class_="m8h3af8h l7ghb35v kjdc1dyq kmwttqpk gh25dzvf n3t5jt4f")
        # return(urls.text)
        if actualPosts is not None:
            for i in actualPosts:
                x=i.find_all('div', style="text-align: start;")
                if x is not None:
                    for p in x:
                        te.append(p.text + '\n')
                        print("AAAAAAAAAAAAA")
            
                y=i.find_all('div', style="text-align:start")
                if y is not None:
                    for p in y:
                        te.append(p.text + '\n')
                        print("BBBBBBBBBBBBB")

            print("nrmlmnt join mchet")
            return('\n'.join(te))
        else:
            return "None"



def extract_contenu(post,browser):
    
    try:
        actualPosts = post.find_all(class_="l7ghb35v kjdc1dyq kmwttqpk gh25dzvf jikcssrz n3t5jt4f")
        text = []
        if actualPosts is not None:
            for p in actualPosts:
                x=p.find('div', style="text-align: start;").text + '\n'
                text.append(x)
            return('\n'.join(text))
    except:
        return "None"



def save_img(src_save):
    
    initial_count = 0
    dir = "C:/Users/medrh/Dropbox/Mon PC/Downloads/Compressed/Web Scraping/Scraping/scrap_fb/Flask-back/Dossier_pour_drive"
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1

    for e in src_save:
        urllib.request.urlretrieve(e,'C:/Users/medrh/Dropbox/Mon PC/Downloads/Compressed/Web Scraping/Scraping/scrap_fb/Flask-back/Dossier_pour_drive/Image'+str(initial_count)+'.png')
        initial_count+=1

def extract_img_post(post,browser,url_post):

    #IMAGES 
                                                        
            postPictures = post.find_all("img",class_="z6erz7xo on4d8346 pytsy3co s8sjc6am myo4itp8 ekq1a7f9 mfclru0v")
            browser.execute_script("window.scrollTo(0, 400)")
            exist5 = post.find(class_="mqmf5637 nsf2ypdj innypi6y hsphh064")
            src_img = ''
            src_img_supp = ''
            src_save = []
            time.sleep(3)
            
            if postPictures is not None:
                for postPicture in postPictures:
                    src_img += postPicture['src'] + '\n'
                    src_save.append(postPicture['src'])
            else:
                src_img = 'None'
                print("img extraction mamchetech")
            
            if exist5 is not None:
                url_img5 = browser.find_elements_by_css_selector("div.om3e55n1 > div.lq84ybu9.hf30pyar.s8sjc6am > a")
                test = browser.find_element_by_css_selector("a.qi72231t.o9w3sbdw.nu7423ey > div.i85zmo3j.kl0yapha.z6erz7xo.alzwoclg.on4d8346.cqf1kptm.jcxyg2ei.l10tt5db.s8sjc6am.myo4itp8.ekq1a7f9 > div.mqmf5637 nsf2ypdj innypi6y hsphh064").text
                if test:
                    browser.get(url_img5[3].get_attribute('href'))
                    time.sleep(3)
                    for _ in range(int(test) + 1):
                        postPic5 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".nuz1ool1.lq84ybu9.hf30pyar.om3e55n1")))
                        postPic5.click()
                        src_img_supp += postPic5.get_attribute('src') + '\n'
                        src_save.append(postPic5.get_attribute('src'))
                        pyautogui.press('right')
                        time.sleep(3)
                else:
                    src_img_supp = 'None'

            browser.get(url_post)


            save_img(src_save)

            return src_img, src_img_supp


def extract_img_unique_post(post,browser,url_post):

    postPictures = post.find_all("img",class_="z6erz7xo on4d8346 pytsy3co s8sjc6am myo4itp8 ekq1a7f9 mfclru0v p9wrh9lq")
    print("mchet?")
    src_save = []
    src_img = ''
    
    if postPictures is not None:
        print("ouii")
        for postPicture in postPictures:
            src_img += postPicture['src']
            src_save.append(postPicture['src'])
            print("ahiiii hna")
            save_img(src_save)
    else:
        src_img = 'None'
        print("img extraction mamchetech")

    return src_img


def extract_vid_post(post,browser):
        #VIDEOS

        try:
            src = ''
            ancestor = browser.find_element(By.XPATH,"//a[@aria-label='Agrandir']")
            src += ancestor.get_attribute('href')
            url = ancestor.get_attribute('href')
            download_vid(url,browser,post)
                
            return src
            
        except:
            print("Vid script didn't start")
            pass


def download_vid(url,browser,post):
    browser.get("https://en.savefrom.net/9-how-to-download-facebook-video-96.html")
    time.sleep(3)

    browser.find_element(By.XPATH,"//input[@placeholder='Paste your video link here']").send_keys(url)
    time.sleep(1)
    browser.find_element_by_id("sf_submit").send_keys(Keys.ENTER)
    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".download-icon"))).click()
    time.sleep(15)
    #obtain parent window handle
    p= browser.window_handles[0]
    #obtain browser tab window
    c = browser.window_handles[1]
    #switch to tab browser
    browser.switch_to.window(c)
    browser.close()
    time.sleep(2)


# def who_share(browser,nb_de_scroll): ---------------------------------------------------------------------------------------
#     time.sleep(random.randint(1,4))
#     try:
#             person_share = browser.find_elements_by_class_name('oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.pq6dq46d.mg4g778l.btwxx1t3.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.gpro0wi8.dwo3fsh8.ow4ym5g4.auili1gw.gmql0nx0')
            
#             ActionChains(browser).move_to_element(person_share[1])
#             time.sleep(random.randint(1,4))
#             ActionChains(browser).click(person_share[1]).perform()
#             time.sleep(random.randint(1,4))
#             fBody  = browser.find_elements_by_xpath("//div[@role='dialog']//div[@class='q5bimw55 rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 eg9m0zos l9j0dhe7 du4w35lb ofs802cu pohlnb88 dkue75c7 mb9wzai9 d8ncny3e buofh1pr g5gj957u tgvbjcpo l56l04vs r57mb794 kh7kg01d c3g1iek1 k4xni2cv']")
#             scroll = 0
            
#             while scroll < nb_de_scroll: 
#                 height = random.randint(250,300)
#                 browser.execute_script(f'arguments[0].scrollTop = arguments[0].scrollTop + {height};', fBody[2])
#                 time.sleep(random.randint(4,7))
#                 scroll += 1 
                        
           
#     except:
#         # do nothing right heree
#             pass
    
#     time.sleep(random.randint(1,4))
#     X_button = browser.find_elements_by_class_name('oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.j83agx80.taijpn5t.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.tv7at329.thwo4zme.tdjehn4e')
            
#     ActionChains(browser).move_to_element(X_button[0])
#     time.sleep(random.randint(1,4))
#     ActionChains(browser).click(X_button[0]).perform()
#     time.sleep(random.randint(1,3))
#     return share_data



# def who_react(browser,nb_de_scroll):------------------------------------------------------------------------------------
    # try:
            
    #         element_who = browser.find_element_by_css_selector("span.gpro0wi8.cwj9ozl2.bzsjyuwj.ja2t1vim > span > span.pcp91wgn")
    #         browser.execute_script('arguments[0].click()', element_who)


    #         # person_react = browser.find_elements_by_class_name('ue3kfks5.pw54ja7n.uo3d90p7.l82x9zwi.a8c37x1j')
    #         # print(len(person_react))
            
    #         # ActionChains(browser).move_to_element(person_react[0])
    #         # time.sleep(random.randint(1,4))
    #         # print("t3amlet 1")
    #         # ActionChains(browser).click(person_react[0]).perform()
    #         # print("t3amlet 2")
    #         # time.sleep(random.randint(1,4))
    #         # fdy = browser.find("pwoa4pd7 mkhogb32 n7fi1qx3 datstx6m b5wmifdl pmk7jnqg kr520xx4 qgmjvhk0 art1omkt nw2je8n7 hhz5lgdu pyaxyem1")
    #         # fbody = WebDriverWait(browser, 20).until(EC.presence_of_element_located(By.CSS_SELECTOR,".pwoa4pd7.mkhogb32.n7fi1qx3.datstx6m.b5wmifdl.pmk7jnqg.kr520xx4.qgmjvhk0.art1omkt.nw2je8n7.hhz5lgdu.pyaxyem1"))

    #         time.sleep(7)

    #         # WebDriverWait(browser, 10).until(EC.element_to_be_clickable(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]')).click()
            
    #         browser.find_element(By.XPATH,"//div[@class='j83agx80 cbu4d94t buofh1pr l9j0dhe7']").click()
            
    #         # buttons = browser.find_elements_by_xpath("//div[@role='button']//div[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql abiwlrkh p8dawk7l lzcic4wl rq0escxv pq6dq46d cbu4d94t taijpn5t l9j0dhe7 k4urcfbm']")
    #         # for btn in buttons:
    #         #     #Use the Java script to click on follow because after the scroll down the buttons will be un clickeable unless you go to it's location
    #         #     browser.execute_script("arguments[0].click();", btn)
    #         #     time.sleep(3)

    #         # fBody  = browser.find_element(By.XPATH,"//div[@class='rq0escxv mkhogb32 n7fi1qx3 b5wmifdl jb3vyjys ph5uu5jm qt6c0cv9 b3onmgus hzruof5a pmk7jnqg kr520xx4 enuw37q7 dpja2al7 art1omkt nw2je8n7 hhz5lgdu']")

    #         time.sleep(2)
    #         i = 0                       

    #         while True:
                 
    #              try:
    #                 print("dakhlet fl try")
    #                 row = WebDriverWait(browser,10).until(EC.visibility_of_element_located(By.XPATH, f"(//div[@data-visualcompletion='ignore-dynamic'])[{i}]"))
    #                 time.sleep(0.5)
    #                 print("saret el row")

    #                 browser.execute_script("arguments[0].scrollIntoView(true);", row)
    #                 print("scrolla bl element bl element")
    #                 i = i + 1
    #              except:
    #                 print('Scrolled all the elements, and must have not found the index hence break from the loop')
    #                 break   
           
    # except:
    #         print("mchet lel exception")
            
    # source_data = browser.page_source
    # react_data = bs(source_data, 'html.parser')
    
    # time.sleep(random.randint(1,4))
    # X_button = browser.find_elements_by_class_name('oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.j83agx80.taijpn5t.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.tv7at329.thwo4zme.tdjehn4e')
            
    # ActionChains(browser).move_to_element(X_button[0])
    # time.sleep(random.randint(1,4))
    # ActionChains(browser).click(X_button[0]).perform()
    # time.sleep(random.randint(1,3))
    # return react_data

def extract_who_react(browser,post):
            
    nbreact = post.find("span",class_= "cxfqmxzd nnzkd6d7").text

    time.sleep(3)
    
    
    element_who = browser.find_element_by_css_selector("span.cxfqmxzd.k0kqjr44.o3hwc0lp.nws3uo2z > span > span.nnzkd6d7")
    browser.execute_script('arguments[0].click()', element_who)


    
    print("SARET")
    time.sleep(7)

    
    browser.find_element(By.XPATH,"//div[@class='r7ybg2qv qbc87b33 jk4gexc9 alzwoclg cqf1kptm lq84ybu9 g4tp4svg ly56v2vv h67akvdo ir1gxh3s sqler345 by1hb0a5 id4k59z1 jfw19y2w om3e55n1 b95sz57d mm05nxu8 izce65as kzemv7a0 q46jt4gp oxkhqvkx r5g9zsuq nch0832m']").click()
    
    print("saret el click !! --------")

    time.sleep(2)
    i = 2       


    persons_name = []
    react_list = {"like":[], "love":[], "haha":[], "wow":[], "sad":[], "angry":[], "help":[]}

    while i < 250:
        try:
            print("dakhlet fl loop")
            time.sleep(0.5)
            row = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, f"(//div[@class='alzwoclg cqf1kptm cgu29s5g om3e55n1']//div[@data-visualcompletion='ignore-dynamic'])[{i}]")))
            time.sleep(0.5)
                                                                                                                
            print("saret el row")

            browser.execute_script("arguments[0].scrollIntoView(true);", row)
            print("scrolla bl element bl element")
            print(i)

            i = i + 1
        except:
            break



    try:
        # persons_div = react_html.find_all(class_="q9uorilb")
        print("test1111")
        persons_div = browser.find_elements(By.XPATH,"//div[@class='aglvbi8b']//a[@role='link']")
        persons_react = browser.find_elements(By.XPATH,"//div[@class='s9ok87oh bf1zulr9 s9ljgwtm lxqftegz frfouenu r7bn319e bonavkto djs4p424 bdao358l alzwoclg cqf1kptm cgu29s5g i15ihif8 m8h3af8h l7ghb35v kjdc1dyq kmwttqpk dnr7xe2t aeinzg81 om3e55n1 g4tp4svg i85zmo3j qmqpeqxj e7u6y3za qwcclf47 nmlomj2f jcxyg2ei lq84ybu9 hf30pyar op9v4316 d1v569po p4n9ro91 onux6t7x t4os9e1m jttuzw70']//img[@class='gneimcpu p9wrh9lq']")
        print("hereee")                                                 
        for i in range(len(persons_div)):
            #persons names
            persons_text = persons_div[i].text
            print("HAW JAAA HNAA")
            if persons_text is not None:
                print(persons_text)
            else:
                print("Pas d'affichage de nom")
            persons_name.append(persons_text)

            #persons reactions
            p_react = persons_react[i].get_attribute("src")
                           
            if p_react == "https://scontent.ftun10-1.fna.fbcdn.net/m1/v/t6/An8TxrncfS4U_evP89c2GTGoBe2r0S9YacO1JWgXsSujyi44y6BPf9kkfnteC4B3wzEXsYS1dwFIG3UcC1c_CnQTTPxJ2zIXeAxTrhL8YV0Sp8quSZo.png?ccb=10-5&oh=00_AT84sU6eLR4ocft9EJindVRUyJAxL4efSEMxAwtUAmPUgw&oe=62F32E96&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An8TxrncfS4U_evP89c2GTGoBe2r0S9YacO1JWgXsSujyi44y6BPf9kkfnteC4B3wzEXsYS1dwFIG3UcC1c_CnQTTPxJ2zIXeAxTrhL8YV0Sp8quSZo.png?ccb=10-5&oh=00_AT_NO0m8TW6_OQN4SMdPRo1uK0dZrMQBjFQPmHPuv8c8pA&oe=62FD11D6&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An8TxrncfS4U_evP89c2GTGoBe2r0S9YacO1JWgXsSujyi44y6BPf9kkfnteC4B3wzEXsYS1dwFIG3UcC1c_CnQTTPxJ2zIXeAxTrhL8YV0Sp8quSZo.png?ccb=10-5&oh=00_AT8Qj3lUcthE8F7xAUFf_An7JTb4FNdjBpGprGnbpSvj-Q&oe=6304FAD6&_nc_sid=55e238":
                react_list["like"].append(persons_text)
            if p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An_gITNN0Ds6xnioTKduC3iqXXKmHcF0TaMvC1o32T--llsYDRmAjtiWFZ4R0stgYTwjHPojz-hShHPtB7jPz6xck8JN3Tg0UaA0OqYOiezH8xJvjrc.png?ccb=10-5&oh=00_AT_3EpBCydw05oElJbMT8UFGZLiWERXDsFVOsq74G5AGCA&oe=62F3878A&_nc_sid=55e238" or p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An_gITNN0Ds6xnioTKduC3iqXXKmHcF0TaMvC1o32T--llsYDRmAjtiWFZ4R0stgYTwjHPojz-hShHPtB7jPz6xck8JN3Tg0UaA0OqYOiezH8xJvjrc.png?ccb=10-5&oh=00_AT_cMn5AA12U_ZCegZ4uTr6maN6ceKEi3zHn_P6zm-epdQ&oe=62FD6ACA&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An_gITNN0Ds6xnioTKduC3iqXXKmHcF0TaMvC1o32T--llsYDRmAjtiWFZ4R0stgYTwjHPojz-hShHPtB7jPz6xck8JN3Tg0UaA0OqYOiezH8xJvjrc.png?ccb=10-5&oh=00_AT_s36gC_TtLur3WL8cPjV_pbPVGzIB31o88_Q6kWxyDUg&oe=630553CA&_nc_sid=55e238":
                react_list["love"].append(persons_text)
            if p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An8UT5zh0xj_ZBy831gcqoVKvjjaBF8jCucOr8PgCD5KlFQ-JaR1IyJrRavwOoHyP9H3HYdxmOZlVV9lBf8OPE_JF-bfAxKj5e1dyPTlBzKMTNoY2YlKLWo.png?ccb=10-5&oh=00_AT-AoXygyVLxN6K0-CwtZ7wQADG5wJBYnWWAe1qDNCgfZQ&oe=62F337D7&_nc_sid=55e238" or p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An8UT5zh0xj_ZBy831gcqoVKvjjaBF8jCucOr8PgCD5KlFQ-JaR1IyJrRavwOoHyP9H3HYdxmOZlVV9lBf8OPE_JF-bfAxKj5e1dyPTlBzKMTNoY2YlKLWo.png?ccb=10-5&oh=00_AT-aLxcNKyZvu5l3DwLMbwA7InGgrkRPJLnDn08P7CPP9A&oe=62FD1B17&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An8UT5zh0xj_ZBy831gcqoVKvjjaBF8jCucOr8PgCD5KlFQ-JaR1IyJrRavwOoHyP9H3HYdxmOZlVV9lBf8OPE_JF-bfAxKj5e1dyPTlBzKMTNoY2YlKLWo.png?ccb=10-5&oh=00_AT-k7prOxI89MIuMW5N9vVnZl_wnlthBbUVUUAaeHs-M9Q&oe=63050417&_nc_sid=55e238":
                react_list["help"].append(persons_text)
            if p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An-THWPVXq6iGcl9m0xpRXz841UFwm90bi1X84tlxOb8AG7h_2L7pTpESZnYZ-V90dtWcspSSm2WT0yqmOIxbs7Ms6rYoZGGCYDIVXAaSAA9l2YWfA.png?ccb=10-5&oh=00_AT_HRbNlwLrATvnbQxkkLR5Mw3PM9_ETu_uG4wBy4WoglQ&oe=62F2A6A9&_nc_sid=55e238" or p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An-THWPVXq6iGcl9m0xpRXz841UFwm90bi1X84tlxOb8AG7h_2L7pTpESZnYZ-V90dtWcspSSm2WT0yqmOIxbs7Ms6rYoZGGCYDIVXAaSAA9l2YWfA.png?ccb=10-5&oh=00_AT8tS2yKViAy7ZlIKbc-dISkXnPYy5DCi2akaae_P2ByKA&oe=62FC89E9&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An-THWPVXq6iGcl9m0xpRXz841UFwm90bi1X84tlxOb8AG7h_2L7pTpESZnYZ-V90dtWcspSSm2WT0yqmOIxbs7Ms6rYoZGGCYDIVXAaSAA9l2YWfA.png?ccb=10-5&oh=00_AT8VJa6JCs_JmaU43X9jEkQW0nJHDnWaUYgpQh0u0Veb5A&oe=630472E9&_nc_sid=55e238":
                react_list["haha"].append(persons_text)
            if p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An9wqz15qSJBbtkJMsumo0WeMIE_6_MbAVHA1LdiH0PgQ82pe50V_Ey2f1YPiEO4lxTLUrsjaXWUC1bTJ3NKmC9FEw2jDlT2KFDmX_N13xBOjzFU8ws.png?ccb=10-5&oh=00_AT8tLufCUwr2wbKJYMOTxmEE_UGSDRCZC_tvkmCNZHZJfg&oe=62F37F42&_nc_sid=55e238" or p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An9wqz15qSJBbtkJMsumo0WeMIE_6_MbAVHA1LdiH0PgQ82pe50V_Ey2f1YPiEO4lxTLUrsjaXWUC1bTJ3NKmC9FEw2jDlT2KFDmX_N13xBOjzFU8ws.png?ccb=10-5&oh=00_AT8jOEAER1Hq8lBS7NCZL55IeH6ymDsf355HgFRuR1WFDQ&oe=62FD6282&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An9wqz15qSJBbtkJMsumo0WeMIE_6_MbAVHA1LdiH0PgQ82pe50V_Ey2f1YPiEO4lxTLUrsjaXWUC1bTJ3NKmC9FEw2jDlT2KFDmX_N13xBOjzFU8ws.png?ccb=10-5&oh=00_AT-HFWvcx67EJ8u3RZ55lU15l0AjJjuEprXk__gyRFPguA&oe=63054B82&_nc_sid=55e238":
                react_list["wow"].append(persons_text)
            if p_react == "https://scontent.ftun10-1.fna.fbcdn.net/m1/v/t6/An8ph2gwH6WsvW6pxuYzGzrW8CdpQXACl5PKb5e3I8yS82dPyO-cHlpZDGDHuNFUBIPS8_rJmr6L5JKI6gpOd6GVgh3sLHS6qMD_fv-qg6FoJAzZC2k.png?ccb=10-5&oh=00_AT829-DhnsHHnkcC--97qg_g3NZP66r_VG0GFA99zkQHBQ&oe=62F3940C&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An8ph2gwH6WsvW6pxuYzGzrW8CdpQXACl5PKb5e3I8yS82dPyO-cHlpZDGDHuNFUBIPS8_rJmr6L5JKI6gpOd6GVgh3sLHS6qMD_fv-qg6FoJAzZC2k.png?ccb=10-5&oh=00_AT-wBY0FXQXLOZhGnxF6uJzGtsZCplTut5H5R4yEfMfIFg&oe=62FD774C&_nc_sid=55e238" or p_react == "https://scontent.ftun9-1.fna.fbcdn.net/m1/v/t6/An8ph2gwH6WsvW6pxuYzGzrW8CdpQXACl5PKb5e3I8yS82dPyO-cHlpZDGDHuNFUBIPS8_rJmr6L5JKI6gpOd6GVgh3sLHS6qMD_fv-qg6FoJAzZC2k.png?ccb=10-5&oh=00_AT_4JHSw-6tRzcQHtl2TVam1ziXZX9wFFGw-yPnFfkaZ-Q&oe=6305604C&_nc_sid=55e238":
                react_list["angry"].append(persons_text)
            if p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An8Y5LK0k-qkMes9nYNV5vHn0mALQUIvZXTKK-xekAdyqSbtBsDEcK0-FCVj5Mb7Ycj3xrItHd6q8iTSOi1VEki42ICqEi72j_mjN03-qgfUiGvWFfy1.png?ccb=10-5&oh=00_AT-i0MebIeS1Yd_KGcPsxDA8mlpXNxmwI_a7tSS1PYJLTQ&oe=62F2F865&_nc_sid=55e238" or p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An8Y5LK0k-qkMes9nYNV5vHn0mALQUIvZXTKK-xekAdyqSbtBsDEcK0-FCVj5Mb7Ycj3xrItHd6q8iTSOi1VEki42ICqEi72j_mjN03-qgfUiGvWFfy1.png?ccb=10-5&oh=00_AT9MnZpnU68Cx_d1sY2I0jCb-QFo-DA8YYvwppRXJ6Hurg&oe=62FCDBA5&_nc_sid=55e238" or p_react == "https://scontent.xx.fbcdn.net/m1/v/t6/An8Y5LK0k-qkMes9nYNV5vHn0mALQUIvZXTKK-xekAdyqSbtBsDEcK0-FCVj5Mb7Ycj3xrItHd6q8iTSOi1VEki42ICqEi72j_mjN03-qgfUiGvWFfy1.png?ccb=10-5&oh=00_AT9cPQkR9rBEZelI0uzpf-iVZklEBIhJ-rliAEKnnFmnyg&oe=6304C4A5&_nc_sid=55e238":
                react_list["sad"].append(persons_text)

        time.sleep(random.randint(1,3)) #A remplacer si on veut augmenter le temps de sleep dans a fenetre de likes.
        print('wselna hna')

        try:
            X_button = browser.find_element(By.XPATH,'//div[@class="qi72231t n3hqoq4p r86q59rh b3qcqh3k fq87ekyn fsf7x5fv s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk cr00lzj9 rn8ck1ys s3jn8y49 f14ij5to l3ldwz01 icdlwmnq i85zmo3j qmqpeqxj e7u6y3za qwcclf47 nmlomj2f frfouenu bonavkto djs4p424 r7bn319e bdao358l alzwoclg jcxyg2ei srn514ro oxkhqvkx rl78xhln nch0832m om3e55n1 jvc6uz2b g90fjkqk a5wdgl2o"]')
            
            ActionChains(browser).move_to_element(X_button)
            time.sleep(random.randint(1,4))
            ActionChains(browser).click(X_button).perform()
            time.sleep(random.randint(1,3))
            print("nrmlmnt taw saret el clique aal 9ars")
        except:
            print("mal9ash el X")
    
    except:
        print("nothing is working react")

    return persons_name, react_list["like"], react_list["love"], react_list["help"], react_list["haha"], react_list["wow"], react_list["angry"], react_list["sad"]
    

def extract_who_share(browser):
    
    nbpartages = extract_nbr_partages(browser)
    print(nbpartages)

    if extract_nbr_partages(browser) == "None":
        return "None"
    else:
        
        time.sleep(2)
        

        element_who = browser.find_elements(By.XPATH,"//div[@class='i85zmo3j alzwoclg jez8cy9q epnzikpj']//span[@class='gvxzyvdx aeinzg81 t7p7dqev gh25dzvf exr7barw b6ax4al1 gem102v4 ncib64c9 mrvwc6qr sx8pxkcf f597kf1v cpcgwwas m2nijcs8 hxfwr5lz k1z55t6l oog5qr5w tes86rjd rtxb060y']")
        test = False
        i=0
        while (test == False):
            if ((element_who[i].text.split(" ")[1] == "partage") or (element_who[i].text.split(" ")[1] == "partages")):   
                browser.execute_script('arguments[0].click()', element_who[i])
                test = True
            i+=1
            if i > len(element_who):
                break


        print("SARET HNA")
        time.sleep(7)

        browser.find_element(By.XPATH,"//div[@class='r7ybg2qv qbc87b33 jk4gexc9 alzwoclg cqf1kptm lq84ybu9 g4tp4svg ly56v2vv h67akvdo ir1gxh3s sqler345 by1hb0a5 thmcm15y cgu29s5g i15ihif8 dnr7xe2t id4k59z1 jfw19y2w b95sz57d mm05nxu8 izce65as om3e55n1 qbfhvn0q']").click()
        
        print("saret el click !!! --------")

        time.sleep(2)
        i = 1              

        while i < int(nbpartages):
            print("dakhlet fl loop")
    
            try:
                WebDriverWait(browser, 20).until(EC.visibility_of_element_located(By.XPATH, "//div[@class='ehs4c0rc h4ejlli7']"))
                break
            except:
                pass

            try:
                time.sleep(1)                                                                                                                                           
                # row = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, f"(//div[@class='sjgh65i0']//div[@class='j83agx80 l9j0dhe7 k4urcfbm'])[{i}]")))
                row = browser.find_element(By.XPATH, f"(//div[@class='bdao358l om3e55n1 g4tp4svg nu7423ey c26d6ho5 sygo2mea qxuwncqo hxf2uw4e s9ok87oh s9ljgwtm lxqftegz bf1zulr9 r4jidfu8 ahb38r9s scpwgmsl opot3u1k g6da2mms yn3a2qjl b52o6v01 a96hb305 mfclru0v lq84ybu9 hf30pyar b3dzj11p'])[{i}]")  #  "//h3[@id='jsc_c_1f']//span[@class='nc684nl6']//span")
                time.sleep(1)
                
                print("saret el row")

                browser.execute_script("arguments[0].scrollIntoView(true);", row)
                print("scrolla bl element bl element")
                print(i)

                i = i + 1
            except:
                break

    persons_name = []

    try:
        # persons_div = react_html.find_all(class_="q9uorilb")
        print("test1111")
        persons_div = browser.find_elements_by_css_selector("span.rse6dlih > a > strong > span")
        print("aaa")
        for p in persons_div:
            persons_text = p.text + '\n'
            print("HAW JAAA HNAA")
            if persons_text is not None:
                print(persons_text)
            else:
                print("Pas d'affichage de nom")
            persons_name.append(persons_text)
        #persons = post.find_all(class_="qzhwtbm6 knvmm38d")

        time.sleep(random.randint(10,20))

        try:
            X_button = browser.find_element(By.XPATH,'//div[@class="h28iztb5 s8sjc6am facqkgn9 b0ur3jhr"]')
            
            ActionChains(browser).move_to_element(X_button)
            time.sleep(random.randint(1,4))
            ActionChains(browser).click(X_button).perform()
            time.sleep(random.randint(1,3))
            print("nrmlmnt taw saret el clique aal 9ars")
        except:
            print("mal9ash el X")

    except:
        print("nothing is working share")
        persons_name.append("None")

    return persons_name
    
def img_text_extraction(browser):
    try:
        Text1 = browser.find_elements_by_css_selector("div.i85zmo3j.alzwoclg.cqf1kptm.pytsy3co.jcxyg2ei.s8sjc6am.myo4itp8.ekq1a7f9.mfclru0v > div.hhxaweo1.j5g1pja0.mt1396w6.bf78fbga.denrs251 > div.m8h3af8h.l7ghb35v.kjdc1dyq.kmwttqpk.gh25dzvf")
        Text2 = browser.find_elements_by_css_selector("div.i85zmo3j.alzwoclg.cqf1kptm.pytsy3co.jcxyg2ei.s8sjc6am.myo4itp8.ekq1a7f9.mfclru0v > div.hhxaweo1.j5g1pja0.mt1396w6.bf78fbga.denrs251 > div.l7ghb35v.kjdc1dyq.kmwttqpk.gh25dzvf.jikcssrz")
        t = []
        for x in Text1:
            m = x.text + '\n'
            t.append(m)
            result = '\n'.join(t)
        for y in Text2:
            n = y.text + '\n'
            t.append(n)
            result = '\n'.join(t)
        return result
    except:
        return "None"


def verif_url(browser): # Pour le boutton des groupes inconnues.
    try:
        browser.implicitly_wait(5) # seconds
        aa = browser.find_elements_by_css_selector("span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh > span")
        for x in aa:
            if x.text == "Rejoindre le groupe":
              time.sleep(2)
              print("AAAAAAAAAa")
              x.click()
        bb = browser.find_elements_by_css_selector("span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.a8c37x1j.fe6kdd0r.mau55g9w.c8b282yb.keod5gw0.nxhoafnm.aigsh9s9.d3f4x2em.iv3no6db.a5q79mjw.g1cxx5fr.lrazzd5p.bwm1u5wc > span.a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7.ltmttdrg.g0qnabr5.ojkyduve")
        for y in bb:
            if y.text == "Accéder au fil d’actualité":
                time.sleep(2)
                print("BBBBBBB")
                y.click()
                browser.close()
                time.sleep(2)
        
        
    except:
        print("--------ERROR----------")   #this is not a private group button, then.. procceed normally, no exceptions required.   



# def verif_connection(browser):
#     try:
#         time.sleep(3)
#         approvation_de_connection = browser.find_element_by_css_selector("div._2s5p > button._42ft._4jy0._a1-c._4jy4._4jy1.selected._51sy")
#         time.sleep(3)
#         approvation_de_connection.click()

#     except:
#         pass

def Scrap_post(post_url,nb_scroll_react,nb_scroll_share):
    with open(r"C:/Users/medrh/Dropbox/Mon PC/Downloads/Compressed/Web Scraping/Scraping/scrap_fb/Flask-back/Configurations_fb.txt") as file:
        EMAIL = file.readline().split('"')[1]
        PASSWORD = file.readline().split('"')[1] 

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
        
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)

    option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1,
    "download.default_directory" : r"C:\Users\medrh\Dropbox\Mon PC\Downloads\Compressed\Web Scraping\Scraping\scrap_fb\Flask-back\Dossier_pour_drive",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
    }) 

    browser = webdriver.Chrome(PATH, options=option)
    browser.get("https://www.facebook.com/")
    url_post = post_url 
    
    _login(browser, EMAIL, PASSWORD)
    time.sleep(random.randint(8,12))
    # verif_connection(browser)
    browser.get(url_post)
    verif_url(browser)
    # share_data = who_share(browser,nb_scroll_share) # contient une parametre !!!!!!!!!!!!!!
    # react_data = who_react(browser,nb_scroll_react) # contient une parametre !!!!!!!!!!!!!!
    time.sleep(random.randint(1,3))

    # with open('./react.html',"w", encoding="utf-8") as file:
    #     file.write(str(react_data.prettify()))
    # react_html = react_data.find(class_="j83agx80 cbu4d94t buofh1pr l9j0dhe7")
    

    # with open('./share.html',"w", encoding="utf-8") as file:
    #         file.write(str(share_data.prettify()))
    # share_html = share_data.find(class_="dati1w0a hv4rvrfc f0kvp8a6 j83agx80")



    source_data = browser.page_source
    post_data = bs(source_data, 'html.parser')
    with open('./post.html',"w", encoding="utf-8") as file:
        file.write(str(post_data.prettify()))
    list_html = post_data.find(class_="g4tp4svg mfclru0v om3e55n1 p8bdhjjv")

    #To split date and time in scraping_date.
    date = datetime.datetime.now()
    string_date = str(date)
    found_index_T = string_date.find(' ')

    
    #insertion dans un dictionnaire
    data=dict()
    data['post_url']=url_post
    print("1")
    data['scraping_date'] = string_date[:found_index_T]
    print("2")
    data['scraping_time'] = string_date[(found_index_T + 1):]
    print("3")
    data["page_url"] =extract_url_post(browser)
    print("4")
    data["image_text_publication"] = img_text_extraction(browser)
    print("5")
    data["titre_publication"]=extract_titre(list_html,browser)
    print("6")
    data["contenu_publication"]=extract_contenu(list_html,browser)
    print("7")
    data["reactions"]=extract_reactions(list_html)
    print("8")
    data["nbr_de_partage"]= extract_nbr_partages(browser)
    print("9")
    data["post_date"]=extract_post_date(list_html)
    print("10")
    data["nbr_de_comments"]=extract_nbr_commantaire(list_html,browser)
    print("11")
    data["general_react_names"], data["react_type_like"], data["react_type_love"], data["react_type_help"],data["react_type_haha"], data["react_type_wow"], data["react_type_angry"], data["react_type_sad"] =extract_who_react(browser,list_html)
    print("12")
    data["who_share"] =extract_who_share(browser)
    print("13")
    data["src_img"], data["src_img_supp"] = extract_img_post(list_html,browser,url_post)
    print("14")
    data["post_img_unique"]=extract_img_unique_post(list_html,browser,url_post)
    print("15")
    data["post_vid"]=extract_vid_post(list_html,browser)
    print("16")
    return (data)

    
