#coding=utf-8
import hashlib



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
    
    
def get_center_part_string2(str, start, end):
    new_str = str
    
    len_start = len(start)
    
    s_pos =  new_str.find(start)
    s_len = len(new_str) 
    new_str = new_str[s_pos+1:s_len]
    s_end = new_str.find(end)
    new_str = new_str[len_start-1:s_end]
    
    return new_str


def get_first_num_pos(str):
    for i in range(0, len(str)):
        s = str[i]
        if(s.isdigit()):
            pos = i
            break
            
    return pos

def get_md5_value(src):
    md5_value = hashlib.md5()
    md5_value.update(src)
    md5_value_Digest = md5_value.hexdigest()
    return md5_value_Digest

'''
str = "中关村在线2017年04月10日 10:00"
pos = get_first_num_pos(str)
print str[0:pos]
print str[pos:len(str)]
'''
