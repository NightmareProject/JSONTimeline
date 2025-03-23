## imports json module to work with json
## import subprocess to run subprocess
## import csv for csv
## import io for io
## import pyperclip for clipboard
import json
import subprocess
import csv
import pyperclip
import io

##opens file to read
# opens file to read
with open('PathtoFile', 'r') as f:
    # Use json.load(f) to deserialize and store in json_data, if using a string use json.loads()
    json_data = json.load(f)

    # Create an in-memory string buffer to store the tab-delimited output
    tsv_buffer = io.StringIO()

    # Create a csv writer with tab delimiter
    tsv_writer = csv.writer(tsv_buffer, delimiter='\t')

    ## use data.get to pull the remote IP field
    for entry in json_data:
     remote_ip = entry.get('ipaddress')
     Hostname = entry.get('url')
     UserName = entry.get('username')
     UserAgent = entry.get('user_agent')
     TimeStamp = entry.get('timestamp')
     ip_lookup = f"curl https://ipinfo.io/{remote_ip}/json"
     ip_result = subprocess.run(ip_lookup, capture_output=True, text=True, shell=True)
     if ip_result.returncode == 0:
         response = json.loads(ip_result.stdout)
         asn = response.get('org')  # asn info is under org in response
         Location_City = response.get('city')  # gets city
         Location_Region = response.get('region')  # gets region
         # Create IOCs
         IOCS = remote_ip + ' | ' + UserAgent + ' | ' + Location_City + ' ' + Location_Region
         #Create Activity Column
         Activity = Timestamp + ' , 'UserName + " Logged In From " + remote_ip + " to " + Hostname
         #Create Timestamp Type Column
         TimestampType = "Sign-In-Logs"

         # Write row output to tsv_writer
         tsv_writer.writerow([Hostname,TimeStamp,UserName,Activity,IOCS,TimeStampType])
# get tsv data as a string
tsv_output = tsv_buffer.getvalue()
# Write row output to tsv_writer
tsv_writer.writerow([Hostname, UserName, Activity, IOCS])
# copy with pyperclip.copy
pyperclip.copy(tsv_output)

#print tsv string
print(tsv_output)
print("Copied to Clipboard! :)")




