import requests
from lxml import etree
import random
import json

local_file=open("movie.json","a",encoding="utf-8")


headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

def GetIp():
    
    url="https://www.xicidaili.com/nt/"
    
    response=requests.get(url,headers=headers)
    response.encoding="utf-8"
    html=response.text
    root=etree.HTML(html)
    
    ip=root.xpath('//table[@id="ip_list"]//tr/td[2]/text()')
    port=root.xpath('//table[@id="ip_list"]//tr/td[3]/text()')
    protocol=root.xpath('//table[@id="ip_list"]//tr/td[6]/text()')
    protocol=[i.lower() for i in protocol]
    
    proxies=[]

    for i in range(len(ip)):
    
        proxies.append(protocol[i]+"://"+ip[i]+":"+port[i])
    
    for i in range(len(proxies)):
        
        ip=choice(proxies)
        
        try:
            
            p={ip.split(":")[0]:ip.split(":")[1]}
            
            response=requests.get("https://www.baidu.com",headers=headers,proxies=p,timeout=3)
            
            if response.status_code==200:
                
                return p
            
        except:
            pass
            
        

def getMovie():
    
    start_page=int(input("请输入起始页面："))
    end_page=int(input("请输入结束页面："))
    
    base_url="https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=movie&listpage=2&offset={}&pagesize=30&sort=18"
    
    
    for i in range(start_page,end_page,30):
        
        url=base_url.format(i)
        
        proies=GetIp()
        
        response=requests.get(url,headers=headers,proxies=proies,timeout=5)
        
        response.encoding="utf-8"
        
        root=etree.HTML(response.text)
    
        title=root.xpath('//div[@class="list_item"]/a/@title')
        actors=root.xpath('//div[@class="list_item"]/div/div/@title')
        hot=root.xpath('//div[@class="list_item"]/div[2]/text()')
        
        for i in range(len(title)):
            
            item={}
            item["title"]=title[i]
            item["actors"]=actors[i]
            item['hot']=hot[i]
            
            local_file.write(json.dumps(item,ensure_ascii=False)+"\n")


def main():
    
    getMovie()



if __name__=="__main__":
    
    main()
    
    local_file.close()

