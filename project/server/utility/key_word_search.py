import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
def key_word_search(result, key_word):
    '''
    input:
    df: pandas dataframe, contain all courses infomation
    key_word: string

    return: 
    df_out: pandas dataframe, contain all courses info relate to key word
    '''

    labels = result['labels']
    values = result['values']
    new_values = None
    df = pd.DataFrame(values, columns=labels)
    if key_word.isalpha():
        # subject search
        if len(key_word) >=2 and len(key_word) <= 4:
            sub = key_word.upper()
            df_sub = df[df['Subject'] == sub]
            if len(df_sub) > 0:
                df_out = df_sub
                records = df_out.to_records(index=False)
                new_values = list(records)
                if len(new_values) > 10:
                    new_values = new_values[:10]
                new_values.sort(key=lambda course: course[5])
                return new_values
                
    else:
        ints = re.findall("\d", key_word)
        alphas = re.findall('[A-Za-z]', key_word)
        if len(ints) == 3 and len(alphas) > 0:
            num = int(ints[0] + ints[1] + ints[2])
            df_num = df[df['Number'] == num]
            if len(df_num) == 0:
                pass
            else: 
                if len(alphas) <=4 and len(alphas) >= 2:
                    sub = ''.join(alphas)
                    sub = sub.upper()
                    df_sub_num = df_num[df_num['Subject'] == sub]
                    if len(df_sub_num) == 0:
                        pass
                    else:
                        df_out = df_sub_num
                        records = df_out.to_records(index=False)
                        new_values = list(records)
                        if len(new_values) > 10:
                            new_values = new_values[:10]
                        new_values.sort(key=lambda course: course[5])
                        return new_values


        elif len(ints) == 1 and len(alphas) > 0:
            num = int(ints[0])
            df_num = df[df['Number'] // 100 == num]
            if len(df_num) == 0:
                pass
            else: 
                if len(alphas) <=4 and len(alphas) >= 2:
                    sub = ''.join(alphas)
                    sub = sub.upper()
                    df_sub_num = df_num[df_num['Subject'] == sub]
                    if len(df_sub_num) == 0:
                        pass
                    else:
                        df_out = df_sub_num
                        records = df_out.to_records(index=False)
                        new_values = list(records)
                        if len(new_values) > 10:
                            new_values = new_values[:10]
                        new_values.sort(key=lambda course: course[5])
                        return new_values
        
        elif len(ints) == 3 and len(alphas) == 0:
            num = int(ints[0] + ints[1] + ints[2])
            df_num = df[df['Number'] == num]
            if len(df_num) == 0:
                pass
            else:
                df_out = df_num
                records = df_out.to_records(index=False)
                new_values = list(records)
                if len(new_values) > 10:
                    new_values = new_values[:10]
                new_values.sort(key=lambda course: course[5])
                return new_values
        else:
            pass

    df_apply = df.apply(
        lambda row: fuzz.partial_ratio(row['Name'], key_word), axis=1
    )
    df_out = df[df_apply > 70]
    records = df_out.to_records(index=False)
    new_values = list(records)
    
    if len(new_values) > 10:
        new_values = new_values[:10]

    return new_values