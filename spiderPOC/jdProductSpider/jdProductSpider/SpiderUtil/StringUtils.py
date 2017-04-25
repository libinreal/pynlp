#coding=utf-8


def find_last_post(strAll, strFind):
    last_position=-1
    while True:
        position=strAll.find(strFind,last_position+1)
        if position==-1:
            return last_position
        last_position=position
        
    return last_position

def get_center_part_string(str, start, end):
    new_str = str
    
    s_pos =  new_str.find(start)
    s_len = len(new_str) 
    new_str = new_str[s_pos+1:s_len]
    s_end = find_last_post(new_str, end)
    new_str = new_str[0:s_end]
    
    return new_str
    
    


