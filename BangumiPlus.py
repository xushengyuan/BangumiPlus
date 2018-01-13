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
    IdData=json.dumps(IdJson) 
    RequestUrl='https://bangumi.moe/api/tag/fetch'
    Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    Request=request.Request(url=RequestUrl,data=IdData.encode('utf-8'),headers=Headers)
    ResponseData=urllib.request.urlopen(Request).read().decode('utf-8')
    ResponseJson=json.loads(ResponseData)
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
                          'params':[[Magnet+'&tr=https%3A%2F%2Ftr.bangumi.moe%3A9696%2Fannounce&tr=http%3A%2F%2Ftr.bangumi.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftr.bangumi.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=http%3A%2F%2F208.67.16.113%3A8000%2Fannounce&tr=udp%3A%2F%2F208.67.16.113%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker.ktxp.com%3A6868%2Fannounce&tr=http%3A%2F%2Ftracker.ktxp.com%3A7070%2Fannounce&tr=http%3A%2F%2Ft2.popgo.org%3A7456%2Fannonce&tr=http%3A%2F%2Fbt.sc-ol.com%3A2710%2Fannounce&tr=http%3A%2F%2Fshare.camoe.cn%3A8080%2Fannounce&tr=http%3A%2F%2F61.154.116.205%3A8000%2Fannounce&tr=http%3A%2F%2Fbt.rghost.net%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.prq.to%2Fannounce&tr=http%3A%2F%2Fopen.nyaatorrents.info%3A6544%2Fannounce']]})
    urllib.request.urlopen(SettingsJson['download_settings']['aria2_server'], jsonreq.encode('utf-8'))
    print('Start download magnet: {}',Magnet,end=' ')
def isItemInLibraries(id):
    LibrariesFile=open(SettingsJson['libraries_settings']['libraries_json'])
    LibrariesJson=json.loads(LibrariesFile.read())
    LibrariesFile.close()
    for x in LibrariesJson['items']:
        if x['_id']==id:
            print("Item already download:",id,end=' ')
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
    BangumiIds=[{'_id':x['_id'],'magnet':x['magnet'],'name':x['title']} for x in ResponseJson['torrents']]
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
    print("Item added   from:",BangumiId," item:",Id," magnet:",Magnet)
def CheckBangumiUpdate(Tags):
    ItemList=GetBangumiListUseTags(Tags)
    for x in ItemList:
        if isItemInLibraries(x['_id'])==False:
            DownloadBangumi(x['magnet'])
            LibrariesAddItem(Tags[0],x['_id'],x['magnet'])
        print(x['name'])
def UpdateAll():
    for Element in SettingsJson['bangumis']:
        Name=GetTagName([Element['bangumi']])[0]
        print("Start process bangumi:",Element['bangumi']," ",Name)
        Tags=[Element['bangumi']];
        for x in Element['tags']:
            Tags.append(x)
        CheckBangumiUpdate(Tags)

UpdateAll()