#coding=utf-8


def get_json_string(str, start, end):
    new_str = str
    
    s_pos =  new_str.find(start) + len(start)
    s_len = len(new_str)
    new_str = new_str[s_pos:s_len]
    s_end=new_str.find(end)
    new_str = new_str[0:s_end]
    
    return new_str
    
    


