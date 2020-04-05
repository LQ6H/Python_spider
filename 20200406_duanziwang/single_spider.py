from lxml import etree
import requests
import json
import re
import pandas as pd
import time
import random

headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}

base_url="https://duanziwang.com/category/%E7%BB%8F%E5%85%B8%E6%AE%B5%E5%AD%90/{}/"

local_file=open("duanzi1.json","a",encoding="utf-8")

def parse_html(html):
    
    root=etree.HTML(html)
    
    # 1.标题
    title=root.xpath('//div[@class="post-head"]/h1/a/text()')
    title=[i.split("_")[0] for i in title]
    
    # 2.内容
    content=root.xpath('//div[@class="post-content"]/p/text()')
    
    # 3.热度
    hot=root.xpath('//div[@class="post-meta"]/time[2]/text()')
    hot=[i.replace("°C","") for i in hot]
    
    # 4.赞
    zan=root.xpath('//div[@class="post-meta"]/time[3]/a/span/text()')
    
    # 5.发布时间
    release_time=root.xpath('//div[@class="post-meta"]/time[1]/text()')
    
    for i in range(len(title)):
        try:
            items={}
            items["title"]=title[i]
            items["content"]=content[i]
            items["hot"]=hot[i]
            items["zan"]=zan[i]
            items["date"]=release_time[i]
            
            
            local_file.write(json.dumps(items,ensure_ascii=False)+"\n")
        except Exception as e:
            print(e)
            
    df=pd.DataFrame()
    df['title']=title
    df['content']=content
    df['hot']=hot
    df['zhan']=zan
    df['date']=release_time
    
    try:
        df.to_csv("duanzi1.csv", mode="a+", header=None, index=None, encoding="utf-8")
    except:
        pass
          
        
def main():
    
    start_url=base_url.format(1)
    response=requests.get(start_url,headers=headers)
    response.encoding="utf-8"
    html=response.text
    
    pattern=re.compile(r'共 \d+ 页')
    result=pattern.findall(html)
    pages=int(result[0].split(" ")[1])
    
    for i in range(1,pages+1):
        if i==20: break
        
        print("正在解析第{}页".format(i))
        
        url=base_url.format(i)
        
        response=requests.get(url,headers=headers)
        response.encoding="utf-8"
        html=response.text
        
        parse_html(html)
        
        time.sleep(random.randint(2,5))
        

if __name__=="__main__":
    
    main()
    
    local_file.close()
    
    print("解析完毕!")
