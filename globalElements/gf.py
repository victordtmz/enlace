#!/usr/bin/python3
from setup import load
load()
import re
import winsound

def insertNewRecord(record):
    ''' 
    record is passed as a tuple with id, this function will remove the id and
    make the tuple a string of text to be inserted into database
    '''
    record1 = list(record)
    record1.pop(0)
    record1 = str(record1)
    record1 = record1[1:-1]
    return record1

def create_regEx(regEx):
    if regEx:
        regEx = regEx.lower()
        regEx_updated = ''
        for i in regEx:
            match i:
                case 'a':
                    i = '[aá]'
                case 'á':
                    i = '[aá]'
                case 'e':
                    i = '[eé]'
                case 'é':
                    i = '[eé]'
                case 'i':
                    i = '[ií]'
                case 'í':
                    i = '[ií]'
                case 'o':
                    i = '[oó]'
                case 'ó':
                    i = '[oó]'
                case 'u':
                    i = '[uú]'
                case 'ú':
                    i = '[uú]'
            regEx_updated = regEx_updated+i
        return(regEx_updated)

def formatPhoneNo(currentNo):
    currentNo = re.findall(r"\d+",currentNo)[0] 
    try:
        if len(currentNo) > 10:
            formatNo = formatNo[0:10]
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        else: formatNo = currentNo
        match len(formatNo):
            case 10:
                PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}',str(formatNo)))
            case 9:
                PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{3}',str(formatNo)))
            case 8:
                PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{3}|\d{2}',str(formatNo)))
            case 7:
                PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{3}|\d',str(formatNo)))
            case 6:
                PhoneNo = '(%s) %s' % tuple(re.findall(r'\d{3}',str(formatNo)))
            case 5:
                PhoneNo = '(%s) %s' % tuple(re.findall(r'\d{3}|\d{2}',str(formatNo)))
            case 4:
                PhoneNo = '(%s) %s' % tuple(re.findall(r'\d{3}|\d',str(formatNo)))
        return PhoneNo
    except:
        return currentNo
        
        