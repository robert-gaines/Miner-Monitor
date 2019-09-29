#!/usr/bin/env python

from requests.auth import HTTPDigestAuth
#from MinerGraph import *
import requests
import time
import json
import sys

def GetStats(host,port,user,password):
    #
    # var - response contains the HTTP Digest
    #
    response = requests.get('http://{host}:{port}/cgi-bin/get_miner_status.cgi'.format(host=host, port=port),auth=HTTPDigestAuth(user, password))
    #
    # Intake contains converted HTTP Request in JSON format
    #
    intake = response.json()
    #
    # Values contains the 'devs' dictionary in the parent object variable
    #
    values = intake['devs']
    #
    # sub_values contains the relevant performance data in index 0 of values
    #
    sub_values = values[0]
    #
    dev = sub_values['freq']
    #
    dev = str(dev)
    #
    asic_freq = int(dev[0:3])
    #
    fan_one_value = SearchString(dev,'fan1',',')
    #
    fan_two_value = SearchString(dev,'fan2',',')
    #
    tc1_val = SearchString(dev,'temp2_1',',')
    #
    tc2_val = SearchString(dev,'temp2_2',',')
    #
    tc3_val = SearchString(dev,'temp2_3',',')
    #
    tc4_val = SearchString(dev,'temp2_4',',')
    #
    hv_one = SearchString(dev,'chain_rate1',',')
    #
    hv_two = SearchString(dev,'chain_rate2',',')
    #
    hv_three = SearchString(dev,'chain_rate3',',')
    #
    hv_four = SearchString(dev,'chain_rate4',',')
    #
    try:
        #
        CheckFans(fan_one_value, fan_two_value, host)
        #
    except:
        #
        print("[!] Check Fans Sub-Routine Failed ")
        #
    try:
        #
        CheckHash(hv_one, hv_two,hv_three,hv_four, host)
        #
    except:
        #
        print("[!] Check Hash Sub-Routine Failed ")
        #
    try:
        #
        CheckTemps(tc1_val, tc2_val, tc3_val, tc4_val, host)
        #
    except:
        #
        print("[!] Check Temperature Sub-Routine Failed ")
        #
    try:
        #
        CheckFrequency(asic_freq, host)
        #
    except:
        #
        print("[!] Check Frequency Sub-Routine Failed ")
        #
    print('\n')
    #
    print("[*] -------------------------- [*]")
    #
    print("[*] Miner Stats for %s [*]" % host)
    #
    print("[*] -------------------------- [*]")
    #
    print('\n')
    #
    time.sleep(1)
    #
    print("  <--ASIC Processing Frequency-->  ")
    #
    print('\n')
    #
    print("[*] Frequency (MHz) --> %i " % asic_freq)
    #
    print('\n')
    #
    print("  <--Fan Speeds-->  ")
    #
    print('\n')
    #
    print("[*] Fan 1 (r/s): %.2f " % fan_one_value)
    #
    print("[*] Fan 2 (r/s): %.2f " % fan_two_value)
    #
    print('\n')
    #
    print("  <--Chip Temperatures-->  ")
    #
    print('\n')
    #
    print("[*] Chip 1 (c): %.2f " % tc1_val)
    #
    print("[*] Chip 2 (c): %.2f " % tc2_val)
    #
    print("[*] Chip 3 (c): %.2f " % tc3_val)
    #
    print("[*] Chip 4 (c): %.2f " % tc4_val)
    #
    print('\n')
    #
    print("    <--Hash Rates-->    ")
    #
    print('\n')
    #
    print("[*] Hash Rate -> Chip 1 (MH/s): %.2f " % hv_one)
    #
    print("[*] Hash Rate -> Chip 2 (MH/s): %.2f " % hv_two)
    #
    print("[*] Hash Rate -> Chip 3 (MH/s): %.2f " % hv_three)
    #
    print("[*] Hash Rate -> Chip 4 (MH/s): %.2f " % hv_four)
    #
    print('\n')


def main():
    #
    user = 'root'
    #
    password = 'root'
    #
    port = 80
    #
    miners = []
    #
    sentinel = ''
    #
    while(sentinel is not 'N' and sentinel is not 'n'):
        #
        miner_tmp = raw_input("[~] Add Miner IP-> ")
        #
        miners.append(miner_tmp)
        #
        print("[+] Miner %s added to miner list " % miner_tmp)
        #
        sentinel = raw_input("Continue adding miners-> ? (y/n) ")
        #
    while(True):
        #
        for m in miners:
            #
            try:
                #
                GetStats(m,port,user,password)
                #
            except:
                #
                print("[!] Connection Failure on: %s " % m)


def CheckHash(h1, h2, h3, h4, host):
    #
    hash_baseline = 100.00
    #
    hash_rates = [h1,h2,h3,h4]
    #
    for hr in hash_rates:
        #
        if(hr < hash_baseline):
            #
            print("[!] ------------------------------------- [!]")
            #
            print("[!] Deficient Hash Rate on Miner: %s " % host)
            #
            print("[!] ------------------------------------- [!]")
            #
            time.sleep(2)
            #
            return
            #
        else:
            #
            return

def CheckFans(f1,f2, host):
    #
    fan_baseline = 1000
    #
    fan_limit = 5000
    #
    if(f1 > fan_limit or f2 > fan_limit):
        #
        print("[!] ------------------------------------- [!]")
        #
        print("[!] Aberrant Fan Behavior Detected on Miner: %s " % host)
        #
        print("[!] ------------------------------------- [!]")
        #
        time.sleep(2)
        #
    elif(f1 < fan_baseline or f2 < fan_baseline):
        #
        print("[!] ------------------------------------- [!]")
        #
        print("[!] Aberrant Fan Behavior Detected on Miner: %s " % host)
        #
        print("[!] ------------------------------------- [!]")
        #
        time.sleep(2)
        #
    else:
        #
        return

def CheckTemps(t1,t2,t3,t4,host):
    #
    temp_limit = 70
    #
    temps =[t1,t2,t3,t4]
    #
    for t in temps:
        #
        if(t > temp_limit):
            #
            print("[!] ------------------------------------- [!]")
            #
            print("[!] Overheating Detected on Miner: %s " % host)
            #
            print("[!] ------------------------------------- [!]")
            #
            time.sleep(2)
            #
        else:
            #
            return

def CheckFrequency(frequency, host):
    #
    freq_baseline = 100
    #
    fan_limit = 1000
    #
    if(frequency > fan_limit):
        #
        print("[!] ------------------------------------- [!]")
        #
        print("[!] Aberrant ASIC Behavior Detected on Miner: %s " % host)
        #
        print("[!] ------------------------------------- [!]")
        #
        time.sleep(2)
        #
    elif(frequency < freq_baseline):
        #
        print("[!] ------------------------------------- [!]")
        #
        print("[!] Aberrant ASIC Behavior Detected on Miner: %s " % host)
        #
        print("[!] ------------------------------------- [!]")
        #
        time.sleep(2)
        #
    else:
        #
        return

def SearchString(intake_string, target_string, delimiter):
    #
    index = intake_string.find(target_string,0,len(intake_string))
    #
    cursor = 0
    #
    ret_value = ''
    #
    try:
        #
        if(index != -1):
            #
            cursor = index
            #
            while(intake_string[cursor] is not '='):
                #
                cursor += 1
                #
            cursor += 1
            #
            while(intake_string[cursor] is not delimiter):
                #
                ret_value = ret_value + intake_string[cursor]
                #
                cursor = cursor+1
                #
    except:
        #
        print("[!] String Parsing Error ")
        #
        return
        #
    return float(ret_value)



if(__name__ == '__main__'):
    #
    main()
