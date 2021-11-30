import numpy as np
import re

def delete_sub(s, ss):
    ind = s.find(ss) + len(ss)
    return s[ind:]

def either(s):
    s = delete_sub(s, 'ither ')
    ss = s.split(', ')
    ssub = ss[-1].split('or ')
    ss = ss[:-1]
    for i in ssub:
        if i != '':
            if i[-1] == ' ':
                i = i[:-1]
            ss.append(i)
    return ss

def one_of(s):
    s = delete_sub(s, 'ne of ')
    ss = s.split(', ')
    ssub = ss[-1].split('or ')
    ss = ss[:-1]
    for i in ssub:
        if i != '':
            if i[-1] == ' ':
                i = i[:-1]
            ss.append(i)
    return ss

def one_of_(s):
    s = delete_sub(s, 'ne of: ')
    ss = s.split(', ')
    return ss

def two_of(s):
    s = delete_sub(s, 'wo of ')
    ss = s.split(', ')
    ssub = ss[-1].split('or ')
    ss = ss[:-1]
    for i in ssub:
        if i != '':
            if i[-1] == ' ':
                i = i[:-1]
            ss.append(i)
    return ss

def or_(s):
    ss = s.split(' or ')
    return ss

def OR(s):
    ss = s.split(' OR ')
    return ss

def and_(s):
    ss = s.split(' and ')
    for i in range(len(ss)):
        if 'or' in ss[i]:
            ss[i] = or_(ss[i])

    return ss

def _and_(s):
    ss = s.split(', ')
    ss[-1] = ss[-1][4:]
    for i in range(len(ss)):
        if 'or' in ss[i]:
            ss[i] = or_(ss[i])
    return ss

def prerequisite(string):
    pre = []
    if string is np.NaN:
        return pre
    substrings = string.split('.')
    for substr in substrings:
        if 'Prerequisite: ' in substr:
            substr = delete_sub(substr, 'Prerequisite: ')
            if 'SE 261, SE 390 and; SE 311, IE 300, IE 310, and TAM 335; or IE 310, IE 311' in substr:
                return [['SE 261'], ['SE 311'], ['IE 300'], ['IE 310'], ['TAM 335', 'IE 310', 'IE 311']]
            subsub = substr.split('; ')

            for ss in subsub:
                x = re.findall("\d", ss)
                if len(x) < 3:
                    continue


                if 'Credit or registration in ' in ss:
                    ss = delete_sub(ss, 'Credit or registration in ')

                if 'credit for ' in ss:
                    ss = delete_sub(ss, 'credit for ')

                if 'credit in ' in ss:
                    ss = delete_sub(ss, 'credit in ')


                if 'or equivalent' in ss:
                    ind = ss.find(' or equivalent')
                    ss = ss[:ind]

                if 'or the equivalent' in ss:
                    ind = ss.find(' or the equivalent')
                    ss = ss[:ind]

                if 'and knowledge' in ss:
                    ind = ss.find(' and knowledge')
                    ss = ss[:ind]
                
                if ' with concurrent registration in the other' in ss:
                    ind = ss.find(' with concurrent registration in the other')
                    ss = ss[:ind]

                if ', and senior' in ss:
                    ind = ss.find(', and senior')
                    ss = ss[:ind]

                if ' and senior' in ss:
                    ind = ss.find(' and senior')
                    ss = ss[:ind]
                
                if ', and consent of instructor' in ss:
                    ind = ss.find(', and consent of instructor')
                    ss = ss[:ind]

                if ', or consent of instructor' in ss:
                    ind = ss.find(', or consent of instructor')
                    ss = ss[:ind]

                if ' or consent of instructor' in ss:
                    ind = ss.find(' or consent of instructor')
                    ss = ss[:ind]

                if ', or permission of instructor' in ss:
                    ind = ss.find(', or permission of instructor')
                    ss = ss[:ind]

                if ' or permission of instructor' in ss:
                    ind = ss.find(' or permission of instructor')
                    ss = ss[:ind]

                if ' permission of instructor' in ss:
                    ind = ss.find(' permission of instructor')
                    ss = ss[:ind]

                if ' or both' in ss:
                    ind = ss.find(' or both')
                    ss = ss[:ind]

                if '/STAT 361' in ss:
                    ind = ss.find('/STAT 361')
                    ss = ss[:ind]

                if ', and IE Technical Elective' in ss:
                    ind = ss.find(', and IE Technical Elective')
                    ss = ss[:ind]


                if 'Three years of high school mathematics or ' in ss or 'another' in ss or 'Familiarity' in ss or ' recommended' in ss:
                    continue


                if 'ither' in ss:
                    pre.append(either(ss))
                    
                elif 'ne of ' in ss:
                    pre.append(one_of(ss))

                elif 'ne of: ' in ss:
                    pre.append(one_of_(ss))

                elif 'wo of ' in ss:
                    pre.append(two_of(ss))

                elif 'oncurrent registration in ' in ss or 'oncurrent enrollment in ' in ss:
                    if ' is allowed' in ss:
                        ind = ss.find(' is allowed')
                        ss = ss[:ind]

                    if 'credit in ' in ss:
                        ss = delete_sub(ss, 'credit in ')

                    if 'oncurrent registration in ' in ss:
                        ss = delete_sub(ss, 'oncurrent registration in ')
                        
                    else:
                        ss = delete_sub(ss, 'oncurrent enrollment in ')
                    
                    if 'ne of ' in ss:
                        pre.append(one_of(ss))

                    elif 'ne of: ' in ss:
                        pre.append(one_of_(ss))

                    elif 'wo of ' in ss:
                        pre.append(two_of(ss))
                    
                    elif ', and ' in ss:
                        for i in _and_(ss):
                            pre.append([i])

                    elif ' and ' in ss:
                        for i in and_(ss):
                            pre.append([i])

                    elif ' or ' in ss:
                        pre.append(or_(ss))
                        
                    elif 'Recommended:' in ss:
                        continue

                    else:
                        pre.append([ss])

                elif ', and ' in ss:
                    for i in _and_(ss):
                        pre.append([i])

                elif ' and ' in ss:
                    for i in and_(ss):
                        pre.append([i])

                elif ' or ' in ss:
                    pre.append(or_(ss))

                elif ' OR ' in ss:
                    pre.append(OR(ss))
                    
                elif 'Recommended:' in ss:
                    continue

                elif ',' in ss:
                    sss = ss.split(', ')
                    for i in sss:
                        pre.append([i])
                else:
                    pre.append([ss])

    return pre