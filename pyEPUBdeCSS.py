import os
import os.path
from os.path import basename
import zipfile
import shutil
from bs4 import BeautifulSoup


def epub_zip(start): #解壓縮
    files = os.listdir(start+'\\.')#讀取目錄檔案
    for filename in files:
        portion = os.path.splitext(filename)#檔案名稱和副檔名拆開
        if portion[1] == ".epub": #EUPB改成ZIP
            newname = portion[0] + ".zip" 
            os.rename(start+'\\'+filename,start+'\\'+newname) #重新命名
            with zipfile.ZipFile('epub\\'+newname,mode='r')as z:
                z.extractall('zip\\'+newname) #解壓縮至名稱資料夾
            z.close()
            os.remove(start+'\\'+newname) #刪除檔案
        elif portion[1] == ".zip": #ZIP直接解壓縮
            newname = portion[0] +portion[1] 
            with zipfile.ZipFile('epub\\'+newname,mode='r')as z:
                z.extractall('zip\\'+portion[0])
            z.close()
            os.remove(start+'\\'+newname) #刪除檔案

def find_css(filepath,all_file): #取得CSS檔位置
    for root, dirs,files in os.walk(filepath): #遍歷目錄
        for f in files:
            fullpath = os.path.join(root, f) #儲存目錄底下所有檔案的個別路徑
            if '.css' in fullpath:
                all_file.append(fullpath) #儲存CSS檔位置
    #print(all_file)
    return all_file

def de_css(path): #刪除CSS檔
    for file in path :
        os.remove(file)

def replace_css(old):
    for file in old :
        shutil.copyfile("D:\\CODE\\epubcss\\main.css",file)

def zip_epub(path):
    files = os.listdir(path+'\\.')#讀取目錄檔案
    for filename in files:
        with zipfile.ZipFile('new\\'+filename,'a') as z:
            for root, dirs,files in os.walk(path+'\\'+filename+'\\'): #遍歷目錄
                for f in files:
                    if '\EPUB' in root:
                        if '.css' in  root:
                            z.write(os.path.join(root,f),'EPUB\\css\\'+f) 
                        else:
                            z.write(os.path.join(root,f),'EPUB\\'+f) 
                    elif '\META-INF' in root:
                        z.write(os.path.join(root,f),'META-INF\\'+f) 
        z.close()

    files = os.listdir('new\\.')#讀取目錄檔案
    for filename in files:
        portion = os.path.splitext(filename)#檔案名稱和副檔名拆開
        if portion[1] == ".zip": #zip改成epub
            newname = portion[0] + ".epub" 
            os.rename('new\\'+filename,'new\\'+newname) #重新命名
    shutil.rmtree('zip\\')
    os.mkdir('zip\\')

def find_html(filepath,all_file): #取得文本位置
    for root, dirs,files in os.walk(filepath): #遍歷目錄
        for f in files:
            fullpath = os.path.join(root, f) #儲存目錄底下所有檔案的個別路徑
            if '.html' in fullpath or '.xhtml' in fullpath:
                all_file.append(fullpath) #儲存文本位置
    return all_file

def modify_html(path):
    for file in path:
        text=open(file,'r+', encoding='utf-8')
        tmp=text.read()
        soup=BeautifulSoup(tmp,"lxml")
        # print(soup)
        check=soup.find("p",class_="linegroup calibre1") #確認有沒有文本
        # print(check)
        if check != None: 
            savedata=soup.find_all("p",class_="linegroup calibre1") #儲存過濾文本
            a=soup.article.extract() #清空article
            #print(soup)
            #print(a)
            original_tag = soup.section
            new_tag = soup.new_tag("article")
            original_tag.append(new_tag) #重新新增article標籤
            #print(save)
            for sentence in savedata :
                soup.article.append(sentence) #將過濾過的文本重新寫入
            #print(soup.article)
            newtext=soup.prettify() #輸出
            #print(newtext)
            text.seek(0) #read後指針會移到最下面，將指針歸零
            text.truncate() #清空檔案
            text.write(newtext) #寫入編輯好的檔案
        text.close()

html_file=[]
css_file=[]
epub='epub'
zip='zip' 
epub_zip(epub)
find_css(zip,css_file)
# replace_css(css_file)
de_css(css_file)
find_html(zip,html_file)
modify_html(html_file)
zip_epub(zip)