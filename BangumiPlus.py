import urllib
import json
import os
import libxmlrpc
SettingsPath='.\\settings.json'
SettingsFile=open(SettingsPath,"r+")
SettingsJson=json.loads(SettingsFile)
LibrariesPath=SettingsJson['libraries_settings']['libraries_path']

def GetTagName(id):
    from urllib import request,parse
    IdJson={'_ids':id}
    IdData=parse.urlencode(IdJson) 
    RequestUrl='https://bangumi.moe/api/tag/fetch'
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    Request=request.Request(url=RequestUrl,data=IdData.encode('utf-8'),headers=Headers)
    ResponseData=urllib.request.urlopen(Request).read().decode('utf-8')
    ResponseJson=json.load(ResponseData)
    TagNames=[y['locale'][SettingsJson['ui_settings']['language']] for x in id:for i in ResponseJson:if x==i['_id']:y=i]
def DownloadBanguni(id):
    
def GetItemNOTInLibraries(id):
    
def GetBangumiListUseTags(Tags):
    from urllib import request,parse
    IdJson={'tag_id':Tags}
    IdData=json.dumps(IdJson) 
    RequestUrl='https://bangumi.moe/api/torrent/search'
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    Request=request.Request(url=RequestUrl,data=IdData.encode('utf-8'),headers=Headers)
    ResponseData=urllib.request.urlopen(Request).read().decode('utf-8')
    ResponseJson=json.loads(ResponseData)
    BangumiIds=[x['_id'] for x in ResponseJson['torrents']]
    return BangumiIds
def LibrariesAddItem(BangumiId,ItemId):
