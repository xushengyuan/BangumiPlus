import urllib
import json
import os
import xmlrpc.client
SettingsPath='.\\settings.json'
SettingsFile=open(SettingsPath,"r")
SettingsJson=json.loads(SettingsFile.read())
SettingsFile.close()

def GetTagName(id):
    from urllib import request,parse
    IdJson={'_ids':id} 
    IdData=parse.urlencode(IdJson) 
    RequestUrl='https://bangumi.moe/api/tag/fetch'
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    Request=request.Request(url=RequestUrl,data=IdData.encode('utf-8'),headers=Headers)
    ResponseData=urllib.request.urlopen(Request).read().decode('utf-8')
    ResponseJson=json.load(ResponseData)
    ReturnNames=[]
    for i in id:
        for Element in ResponseJson:
            if i==Element['_id']:
                ReturnNames.append(Element['locale'][SettingsJson['ui_settings']['language']])
                break
    return ReturnNames
def DownloadBangumi(Magnet):
    from urllib import request,parse
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',\
                          'method':'aria2.addUri',\
                          'params':[[Magnet]]})
    urllib.request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
def isItemInLibraries(id):
    LibrariesFile=open(SettingsJson['libraries_settings']['libraries_json'])
    LibrariesJson=json.loads(LibrariesFile.read())
    LibrariesFile.close()
    for x in LibrariesJson:
        if x['_id']==id:
            return True
    return False;
def GetBangumiListUseTags(Tags):
    from urllib import request,parse
    IdJson={'tag_id':Tags}
    IdData=json.dumps(IdJson) 
    RequestUrl='https://bangumi.moe/api/torrent/search'
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    Request=request.Request(url=RequestUrl,data=IdData.encode('utf-8'),headers=Headers)
    ResponseData=urllib.request.urlopen(Request).read().decode('utf-8')
    ResponseJson=json.loads(ResponseData)
    BangumiIds=[{'_id':x['_id'],'magnet':x['magnet']} for x in ResponseJson['torrents']]
    return BangumiIds
def LibrariesAddItem(BangumiId,Id,Magnet):
    LibrariesFile=open(SettingsJson['libraries_settings']['libraries_json'])
    LibrariesJson=json.loads(LibrariesFile.read())
    LibrariesFile.close()
    JsonElement={'_id':Id,'bangumi':BangumiId,'Magnet':Magnet}
    LibrariesJson['items'].append(JsonElement)
    LibrariesFile=open(SettingsJson['libraries_settings']['libraries_json'],mode='w')
    LibrariesFile.write(json.dumps(LibrariesJson))
    LibrariesFile.close()
def CheckBangumiUpdate(Tags):
    ItemList=GetBangumiListUseTags(Tags)
    for x in ItemList:
        if !isItemInLibraries(x['id']):
            DownloadBangumi(x['magnet'])
def main():
    
main()
