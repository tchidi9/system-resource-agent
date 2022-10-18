from cgi import print_environ_usage
import re
import psutil
import platform
import os
import requests 
import subprocess

Machine = platform.uname()
client_info = {
    "operating_system" : Machine.system, 
    "version" : Machine.version,
    "client_name" : Machine.node,
    "client_processor" : Machine.processor,
    "client_machine" : Machine.machine}
client_os = str(client_info.get("operating_system"))
os_version = str(client_info.get("version"))
machine_name = str(client_info.get("client_name"))
machine_processor = str(client_info.get("client_processor"))
machine_type = str(client_info.get("client_machine"))

cpu = psutil.cpu_percent(interval=1)
cpu_usage = str(cpu) + "%"
ram = psutil.virtual_memory()
ram_size = str(round(ram.total/(1024**3),2))
ram_usage = str(ram.percent) + "%"
disk = psutil.disk_usage(os.getcwd())
disk_space = str(disk.percent) + "%"


def get_latency():
    link = '8.8.8.8'
    ping_result = subprocess.run(['ping', link],stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    latency = str(ping_result[len(ping_result)-2])
    avg_latency = re.findall("Average = [0-9][0-9]ms|Average = [0-9][0-9][0-9]ms",latency)
    if avg_latency: return avg_latency
    else: return "Error! Failed Latency Test, Check Internet Connection"


avg_latency = str(get_latency())
index = open("index.html").read().format(machine_name=machine_name,client_os=client_os,os_version=os_version,machine_processor=machine_processor,machine_type=machine_type,ram_size=ram_size,cpu_usage=cpu_usage,ram_usage=ram_usage,disk_space=disk_space,avg_latency=avg_latency)
                                          
apikey = '4A4850A9A927B8E859C9CE978F9F88814F084D618F1EFF0424985ECDA7D3FEE373A7A3F112A36E9679A69518242F1219'

def Send(apikey, subject, EEfrom, fromName, to, bodyHtml, isTransactional):
    API_ENDPOINT = "https://api.elasticemail.com/v2/email/send"
    payload = {
        'apikey': '4A4850A9A927B8E859C9CE978F9F88814F084D618F1EFF0424985ECDA7D3FEE373A7A3F112A36E9679A69518242F1219',
		'subject': subject,
		'from': EEfrom,
		'fromName': fromName,
		'to': to,
		'bodyHtml': bodyHtml,
		'isTransactional': isTransactional
    }
    r = requests.post(url = API_ENDPOINT, data = payload)
    print(r)
				

Send(apikey, "System Resource Alert", "info.bastionteklogics@gmail.com", "Bastion Tek Logics", "nwabukochidi@gmail.com;chidiebere.nwabuko@oolusolar.com", "<h1>Html Body</h1>", True)



