#!/usr/bin/env python
# coding: utf-8
import sys,pysrt
import urllib2,urllib,json
import re
from urlparse import urlparse
import os
from mtranslate import translate
from argparse import ArgumentParser
reload(sys)  
sys.setdefaultencoding('utf8')

#----------------------------------------------------------------------------------------------------------------------------------
def cleanhtml(raw_html):
  '''
  TODO: refactor this to make it as generic as possible
  '''
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.replace('[vacilación]','...')
  cleantext = cleantext.replace('&nbsp;',' ')
  cleantext = urlparse(cleantext).path  
  return cleantext

#----------------------------------------------------------------------------------------------------------------------------------
def generateSub(args,_subtitle,_filename):   
    subs = pysrt.from_string(str(_subtitle).decode('utf-8'))     
    output = args.OUTPUT + _filename
    #file = pysrt.SubRipFile()    
    text = ''        
    for index in range(len(subs)):    
        if subs[index].text != '':           
            if args.VERBOSE:
                print "Translating line:" + cleanhtml(subs[index].text)                                                
            subs[index].text = translate(cleanhtml(subs[index].text).encode('utf-8'),args.LANG_TO,args.LANG_FROM)        
    subs.save(output)

#----------------------------------------------------------------------------------------------------------------------------------
def generateSubMedia(args):
    subLangURL= 'https://media.upv.es/rest/plugins/admin-plugin-translectures/langs/'
    subUrl = 'https://media.upv.es/rest/plugins/admin-plugin-translectures/srt/'     
    langlist =json.loads(urllib2.urlopen(subLangURL + args.SOURCE).read())          
    for lang in langlist:        
        if lang['lang']==args.LANG_FROM:             
            sub = urllib2.urlopen(subUrl + args.SOURCE +'/' + args.LANG_FROM).read()                                       
            generateSub(args,sub,args.SOURCE+'_' + args.LANG_TO.lower() + '.srt')            
            return 0

#----------------------------------------------------------------------------------------------------------------------------------
def generateSubFile(args,_filename=None):  
    if _filename is None:
        _source = args.SOURCE
    else:
        _source = _filename
    if _source[-4:]=='.srt': 
        substring = open(_source,'r').read() 
        generateSub(args,substring,_source.replace('.srt','_' + args.LANG_TO + '.srt'))   
    else:
        print "Incorrect file format"
        return -1

#----------------------------------------------------------------------------------------------------------------------------------
def generateSubFolder(args):  
    _source = args.SOURCE if args.SOURCE[-1:]=='/' else args.SOURCE + '/'
    if os.path.isdir(args.SOURCE):
        for root, dirs, files in os.walk(args.SOURCE):                        
            for f in files:                
                if f[-4:]=='.srt':
                    substring = open(root + f if root[-1:]=='/' else root + '/' + f,'r').read()     
                    generateSub(args,substring,f.replace('.srt','_' + args.LANG_TO + '.srt'))   
    else:
        print "Incorrect file format"
        return -1

#----------------------------------------------------------------------------------------------------------------------------------
def main():
    parser = ArgumentParser(description='Translate subtitle from media id, file or folder', parents=[])    
    parser.add_argument('-v', '--verbose', action='store_true', dest='VERBOSE', default=False, help='Verbose')        
    parser.add_argument('-t', '--sourceType', type=str, dest='SOURCE_TYPE', help='source type, pick between media|file|folder')
    parser.add_argument('-s', '--source', type=str, dest='SOURCE', help='source of the subtitle/s')
    parser.add_argument('-langf', '--langFrom', type=str, dest='LANG_FROM', default='es', help='Language that we want to translate')
    parser.add_argument('-langt', '--langTo', type=str, dest='LANG_TO', default='en', help='Language of the output subtitle')    
    parser.add_argument('-o', '--output', type=str, dest='OUTPUT', default='./', help='Output folder to store the result')    
    args = parser.parse_args()          
    
    
    if (args.SOURCE_TYPE.lower()=='file'):
        try:    
            generateSubFile(args)
        except:
            return -1     
    elif (args.SOURCE_TYPE.lower()=='folder'):
        try:
            generateSubFolder(args)
        except:
            return -1
    elif (args.SOURCE_TYPE.lower()=='media'):
        try:            
            generateSubMedia(args)
        except:       
            return -1
    else:
        print "Choose a valid source type"        

    return 0
     
#----------------------------------------------------------------------------------------------------------------------------------        
if (__name__ == '__main__'):
    main()    

