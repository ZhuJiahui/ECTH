#coding:utf-8
'''
Created on 2013年7月17日

@author: ZhuJiahui
'''

import time

def time_convert(time):
    """
    将系统时间转化为小时
    :param time:
    :return:
    """
    date = int(time)
    hour = round((time - date) * 24)
    time = date + hour / 24
    return time

def CST_to_Unix(time_string):
    #CST format: Mon Oct 21 16:59:02 CST 2013
    month_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", \
                  "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    
    time_split = time_string.strip().split()
    year_str = time_split[-1]
    month_str = month_dict[time_split[1]]
    day_str = time_split[2]
    hms_str = time_split[3]
    org_str = year_str + "-" + month_str + "-" + day_str + " " + hms_str
    
    
    this_time = time.mktime(time.strptime(org_str, '%Y-%m-%d %H:%M:%S'))
    return this_time

def unCST_to_Unix(time_string):
    #Format 2012:11:08:15:31:01:4:+0000
    
    time_split = time_string.strip().split(":")
    year_str = time_split[0]
    month_str = time_split[1]
    day_str = time_split[2]
    h_str = time_split[3]
    m_str = time_split[4]
    s_str = time_split[5]
    org_str = year_str + "-" + month_str + "-" + day_str + " " + h_str + ":" + m_str + ":" + s_str
    
    this_time = time.mktime(time.strptime(org_str, '%Y-%m-%d %H:%M:%S'))
    return this_time
    

if __name__ == '__main__':
    aa = "Mon Oct 21 16:59:02 CST 2013"
    ns = CST_to_Unix(aa)
    print type(ns)
    print ns
    
    