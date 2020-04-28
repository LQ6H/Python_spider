import requests
import json
import re
import os

session=requests.session()

path="F:\\桌面\\Files"

if not os.path.exists(path):
    os.mkdir(path)

def parse_txt1(code,doc_id):
    
    content_url='https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id='+doc_id

    content=session.get(content_url).content.decode(code)
    md5sum=re.findall('"md5sum":"(.*?)",',content)[0]
    rsign=re.findall('"rsign":"(.*?)"',content)[0]
    pn=re.findall('"totalPageNum":"(.*?)"',content)[0]
    
    content_url='https://wkretype.bdimg.com/retype/text/'+doc_id+'?rn='+pn+'&type=txt'+md5sum+'&rsign='+rsign
    content=json.loads(session.get(content_url).content.decode('gbk'))
    
    result=''

    for item in content:
        for i in item['parags']:
            result+=i['c']
            
    return result

def parse_txt2(content,code,doc_id):
    md5sum=re.findall('"md5sum":"(.*?)",',content)[0]
    rsign=re.findall('"rsign":"(.*?)"',content)[0]
    pn=re.findall('"show_page":"(.*?)"',content)[0]
    
    content_url='https://wkretype.bdimg.com/retype/text/'+doc_id+'?rn='+pn+'&type=txt'+md5sum+'&rsign='+rsign
    content=json.loads(session.get(content_url).content.decode('utf-8'))
    
    result=''

    for item in content:
        for i in item['parags']:
            result+=i['c']
            
    return result

def parse_doc(content):
    
    url_list=re.findall(r'(https.*?0.json.*?)\\x22}',content)
    url_list=[addr.replace("\\\\\\/","/") for addr in url_list]
    
    result=""

    for url in set(url_list):
        content=session.get(url).content.decode('gbk')

        y=0
        txtlists=re.findall(r'"c":"(.*?)".*?"y":(.*?),',content)
        for item in txtlists:
            # 当item[1]的值与前面不同时，代表要换行了
            if not y==item[1]:
                y=item[1]
                n='\n'
            else:
                n=''
            result+=n
            result+=item[0].encode('utf-8').decode('unicode_escape','ignore')
    
    return result

def parse_pdf(content):
    
    url_list=re.findall(r'(https.*?0.json.*?)\\x22}',content)
    url_list=[addr.replace("\\\\\\/","/") for addr in url_list]
    
    result=""

    for url in set(url_list):
        content=session.get(url).content.decode('gbk')

        y=0
        txtlists=re.findall(r'"c":"(.*?)".*?"y":(.*?),',content)
        for item in txtlists:
            # 当item[1]的值与前面不同时，代表要换行了
            if not y==item[1]:
                y=item[1]
                n='\n'
            else:
                n=''
            result+=n
            result+=item[0].encode('utf-8').decode('unicode_escape','ignore')
    
    return result


def parse_ppt(doc_id,title):
    
    content_url='https://wenku.baidu.com/browse/getbcsurl?doc_id='+doc_id+'&pn=1&rn=9999&type=ppt'
    content=session.get(content_url).content.decode('gbk')
    
    url_list=re.findall('{"zoom":"(.*?)","page"',content)
    url_list=[addr.replace('\\','') for addr in url_list]
    
    path="F:\\桌面\\Files"+"\\"+title

    if not os.path.exists(path):
        os.mkdir(path)
    
    for index,url in enumerate(url_list):
        content=session.get(url).content
        paths=os.path.join(path,str(index)+'.jpg')
    
        with open(paths,'wb') as f:
            f.write(content)
    print("图片保存在"+title+"文件夹")
    
    
def parse_xls(content):
    
    url_list=re.findall(r'(https.*?0.json.*?)\\x22}',content)
    url_list=[addr.replace("\\\\\\/","/") for addr in url_list]
    
    result=""

    for url in set(url_list):
        content=session.get(url).content.decode('gbk')

        y=0
        txtlists=re.findall(r'"c":"(.*?)".*?"y":(.*?),',content)
        for item in txtlists:
            # 当item[1]的值与前面不同时，代表要换行了
            if not y==item[1]:
                y=item[1]
                n='\n'
            else:
                n=''
            result+=n
            result+=item[0].encode('utf-8').decode('unicode_escape','ignore')
            
    result=result.replace("\udb80","").replace("\udc00","")
    
    return result
    
def save_file(title,filename,content):
    
    with open(filename,'w',encoding='utf-8') as f:
        f.write(content)
        print("文件"+title+"保存成功")
    f.close()
    

def main():
    
    print("欢迎来到百度文库文件下载：")
    print("-----------------------\r\n")
     
    
    while True:
        try:
            print("1.doc \n 2.txt \n 3.ppt \n 4.xls\n 5.ppt\n")
            types=input("请输入需要下载文件的格式(0退出)：")

            if types=="0":
                break

            if types not in ['txt','doc','pdf','ppt','xls']:
                print("抱歉文件格式错误，请重新输入!")
                continue


            url=input("请输入下载的文库URL地址：")

            # 网页内容
            response=session.get(url)

            code=re.findall('charset=(.*?)"',response.text)[0]

            if code.lower()!='utf-8':
                code='gbk'

            content=response.content.decode(code)

            # 文件id
            doc_id=re.findall('view/(.*?).html',url)[0]
            # 文件类型
            #types=re.findall(r"docType.*?:.*?'(.*?)'",content)[0]
            # 文件主题
            #title=re.findall(r"title.*?:.*?'(.*?)'",content)[0]

            if types=='txt':
                md5sum=re.findall('"md5sum":"(.*?)",',content)
                if md5sum!=[]:
                    result=parse_txt2(content,code,doc_id)
                    title=re.findall(r'<title>(.*?). ',content)[0]
                    #filename=os.getcwd()+"\\Files\\"+title+'.txt'
                    filename=path+"\\"+title+".txt"
                    save_file(title,filename,result)
                else: 
                    result=parse_txt1(code,doc_id)
                    title=re.findall(r"title.*?:.*?'(.*?)'",content)[0]
                    #filename=os.getcwd()+"\\Files\\"+title+'.txt'
                    filename=path+"\\"+title+".txt"
                    save_file(title,filename,result)
            elif types=='doc':
                title=re.findall(r"title.*?:.*?'(.*?)'",content)[0]
                result=parse_doc(content)
                filename=path+"\\"+title+".doc"
                save_file(title,filename,result)
            elif types=='pdf':
                title=re.findall(r"title.*?:.*?'(.*?)'",content)[0]
                result=parse_pdf(content)
                filename=path+"\\"+title+".txt"
                save_file(title,filename,result)
            elif types=='ppt':
                title=re.findall(r"title.*?:.*?'(.*?)'",content)[0]
                parse_ppt(doc_id,title)
            elif types=='xls':
                title=re.findall(r"title.*?:.*?'(.*?)'",content)[0]
                result=parse_xls(content)
                filename=path+"\\"+title+".txt"
                save_file(title,filename,result)
                
                
        except Exception as e:
            print(e)


if __name__=='__main__':
    main()