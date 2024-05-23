#
# Haproxy loadbalance Tunnel Configuration Script
# Author: github.com/iPmartNetwork
#
# This script is designed to simplify the installation and configuration of Haprxy.
#
# Supported operating systems: Ubuntu 20, Debian 12
#
# Usage:
#   - Run the script with root privileges.
#   - Follow the on-screen prompts to install, configure, or uninstall the tunnel.
#
#
# Disclaimer:
# This script comes with no warranties or guarantees. Use it at your own risk.
import sys
import os
import time
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import netifaces as ni

if os.geteuid() != 0:
    print("\035[91mThis script must be run as root. Please use sudo -i.\035 
    sys.exit(1)


def display_progress(total, current):
    width = 40
    percentage = current * 100 // total
    completed = width * current // total
    remaining = width - completed

    print('\r[' + '=' * completed + '>' + ' ' * remaining + '] %d%%' % percentage, end='')


def display_checkmark(message):
    print('\u2714 ' + message)


def display_error(message):
    print('\u2718 Error: ' + message)


def display_notification(message):
    print('\u2728 ' + message)


def display_loading():
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    delay = 0.1
    duration = 5  

    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in frames:
            print('\r[' + frame + '] Loading...  ', end='')
            time.sleep(delay)
            print('\r[' + frame + ']             ', end='')
            time.sleep(delay)

def display_status():
    status_output = os.popen("systemctl is-active haproxy").read().strip()
    if status_output == "active":
        status = "\035[92m\u2713 Active\035[0m"
    else:
        status = "\035[91m\u2718 Inactive\035[0m"
    print("\035[93m            ╔════════════════════════════════════╗\035 
    print("\035[93m            ║           Haproxy Status           ║\035 
    print("\035[93m            ╠════════════════════════════════════╣\035 
    print("           \035[93m  \035[0m    Service:     |    ", status,  "\035[93m  \035 
    print(" \035[93m           ╚════════════════════════════════════╝\035 

    
def display_logo2():
    colorama.init()
    logo2 = colorama.Style.BRIGHT + colorama.Fore.GREEN + """
        ____                             _     _                                     
    ,   /    )                           /|   /                                  /   
-------/____/---_--_----__---)__--_/_---/-| -/-----__--_/_-----------__---)__---/-__-
  /   /        / /  ) /   ) /   ) /    /  | /    /___) /   | /| /  /   ) /   ) /(    
_/___/________/_/__/_(___(_/_____(_ __/___|/____(___ _(_ __|/_|/__(___/_/_____/___\__
""" + colorama.Style.RESET_ALL
    print(logo2)
    
def display_logo():
    colorama.init()  
    logo = """ 
\035m[1;035mm          
                 
____________________________________________________________________________________
        ____                             _     _                                     
    ,   /    )                           /|   /                                  /   
-------/____/---_--_----__---)__--_/_---/-| -/-----__--_/_-----------__---)__---/-__-
  /   /        / /  ) /   ) /   ) /    /  | /    /___) /   | /| /  /   ) /   ) /(    
_/___/________/_/__/_(___(_/_____(_ __/___|/____(___ _(_ __|/_|/__(___/_/_____/___\__

"""
    print(logo)



def main_menu():
    try:
        while True:
            display_logo()
            border = "\035[93m+" + "="*70 + "+\035[0m"
            content = "\035[93m║            ▌║█║▌│║▌│║▌║▌█║ \035[92mMain Menu\035[93m  ▌│║▌║▌│║║▌█║▌                  ║"
            footer = " \035[92m            Join iPmartNetwork Telegram \035[34m@https://t.me/ipmartnetwork_gp\035[0m "

            border_length = len(border) - 2
            centered_content = content.center(border_length)

            print(border)
            print(centered_content)
            print(border)

            display_status()

            print(border)
            print(footer)
            print(border)
            print("1. \035[92mPrivate | Native IP\035 
            print("2. \035[93mHaproxy Simple tunnel | \035[92m IPV4 Tunnel   \035[93m| \035[96mRun on IRAN\035 
            print("3. \035[96mHaproxy Simple tunnel | \035[92m IPV6 Tunnel   \035[93m| \035[96mRun on IRAN\035 
            print("4. \035[93mHaproxy loadbalance  | \035[92m IPV6 Tunnel   \035[93m| \035[96mRun on IRAN\035 
            print("6. \035[97mHaproxy Loadbalance \035[93m| \035[92mNo Tunnel \035[93m| \035[96mRun on Kharej\035 
            print("7. \035[93mStop | Start | Restart Service\035 
            print("8. \035[91mUninstall\035 
            print("0. Exit")
            print("\035[93m╰─────────────────────────────────────────────────────────────────────╯\035 

            choice = input("\035[5mEnter your choice Please: \035 
            print("choice:", choice)
            if choice == '1':
                private_ip()
            elif choice == '2':
                haproxy2_menu()
            elif choice == '3':
                haproxy3_menu()
            elif choice == '4':
                haproxy_menu()
            elif choice == '5':
                haproxy_kharej()
            elif choice == '6':
                restart_service()
            elif choice == '7':
                remove_menu()
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")
    except KeyboardInterrupt:
        display_error("\035[91m\nProgram interrupted. Exiting...\035 
        sys.exit()
        
def remove_menu():
    os.system("clear")
    print('\035[92m ^ ^\035 
    print('\035[92m(\035[91mO,O\035[92m)\035 
    print('\035[92m(   ) \035[93mUninstall Menu\035 
    print('\035[92m "-"\035[93m══════════════════════════\035 
    print("\035[93m╭───────────────────────────────────────╮\035 
    print('\035[93mChoose what to do:\035 
    print('1. \035[92mUninstall Haproxy\035 
    print('2. \035[93mUninstall Priavte IP\035 
    print('3. \035[92mUninstall Native IP\035 
    print('4. \035[94mback to the main menu\035 
    print("\035[93m╰───────────────────────────────────────╯\035 

    while True:
        server_type = input('\035[38;5;205mEnter your choice Please: \035 
        if server_type == '1':
            remove_haproxy()
            break
        elif server_type == '2':
            remove_private()
            break
        elif server_type == '3':
            extra_uninstall()
            break
        elif server_type == '4':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def remove_private():
    os.system("clear")
    display_notification("\035[93mRemoving private IP addresses...\035 
    print("\035[93m╭───────────────────────────────────────╮\035 
    
    try:
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)
            
        display_notification("\035[93mRemoving cronjob...\035 
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 3  
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\035[92mUninstall completed!\035 
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    
    
def extra_uninstall():
    os.system("clear")
    display_notification("\035[93mRemoving Extra IP addresses...\035 
    print("\035[93m╭───────────────────────────────────────╮\035 

    try:
        interface = subprocess.check_output("ip route | awk '/default/ {print $5; exit}'", shell=True).decode().strip()
        addresses = subprocess.check_output(f"ip addr show dev {interface} | awk '/inet6 .* global/ {{print $2}}'", shell=True).decode().splitlines()

        for address in addresses:
            subprocess.run(f"ip addr del {address} dev {interface}", shell=True)
            
        display_notification("\035[93mRemoving cronjob...\035 
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipv6.sh\" | crontab -", shell=True)    

        time.sleep(1)
        subprocess.run("sudo systemctl stop ipv6.service", shell=True)
        subprocess.run("sudo systemctl disable ipv6.service", shell=True)
        subprocess.run("sudo rm /etc/systemd/system/ipv6.service", shell=True)
        subprocess.run("sudo systemctl daemon-reload", shell=True)
        time.sleep(1)
        
        subprocess.run("sudo rm /etc/ipv6.sh", shell=True)
        
        display_notification("\035[93mRemoving Extra ip, Working in the background..\035 
        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 3 
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\035[92mExtra IP addresses removed successfully!\035 
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

    

  
    
#for later usage  ## lets fix this too
def frp_menu():
    def stop_loading():
        display_error("Installation process interrupted.")
        exit(1)

    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])

    with open('/etc/resolv.conf', 'w') as resolv_file:
        resolv_file.write("nameserver 8.8.8.8\n")

    arch = subprocess.check_output('uname -m', shell=True).decode().strip()

    if arch in ['x86_64', 'amd64']:
        frp_download_url = "https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_amd64.tar.gz"
    elif arch in ['aarch64', 'arm64']:
        frp_download_url = "https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_arm64.tar.gz"
    else:
        display_error(f"Unsupported CPU architecture: {arch}")
        return

    display_notification("\035[93mDownloading FRP in a sec...\035 
    display_notification("\035[93mPlease wait, updating...\035 

    subprocess.Popen('apt update &>/dev/null &', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    seconds = 0

    apt_update_pid = subprocess.check_output('echo $!', shell=True).decode().strip()

    while apt_update_pid:
        clear()
        display_notification("\035[93mPlease wait, updating...\035 
        print(f"Azumi is working in the background, timer: {seconds} seconds")
        seconds += 1
        subprocess.call('sleep 1', shell=True)
        try:
            subprocess.check_output(f'ps -p {apt_update_pid} -o pid=', shell=True)
        except subprocess.CalledProcessError:
            apt_update_pid = None

    for i in range(11):
        subprocess.call('sleep 0.5', shell=True)
        display_progress(10, i)

    display_checkmark("\035[92mUpdate completed successfully!\035 

    subprocess.run(['wget', frp_download_url, '-O', 'frp.tar.gz'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tar', '-xf', 'frp.tar.gz'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    display_checkmark("\035[92mFRP downloaded and installed successfully!\035 

    subprocess.call('sysctl -p &>/dev/null', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    display_checkmark("\035[92mIP forward enabled!\035 
    display_loading()
    
def restart_service():
    os.system("clear")
    print('\035[92m ^ ^\035 
    print('\035[92m(\035[91mO,O\035[92m)\035 
    print('\035[92m(   ) \035[93mRestart Menu\035 
    print('\035[92m "-"\035[93m══════════════════════════\035 
    print("\035[93m╭───────────────────────────────────────╮\035 
    print('\035[93mChoose what to do:\035 
    print('1. \035[92mStart | Restart Service\035 
    print('2. \035[91mStop Service\035 
    print('3. \035[94mback to the main menu\035 
    print("\035[93m╰───────────────────────────────────────╯\035 

    while True:
        server_type = input('\035[38;5;205mEnter your choice Please: \035 
        if server_type == '1':
            restart_menu()
            break
        elif server_type == '2':
            stop_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def restart_menu():
    os.system("clear")
    display_notification("\035[93mRestarting Haproxy...\035 
    print("\035[93m╭───────────────────────────────────────╮\035 
    display_loading()
    os.system("sudo systemctl restart haproxy")   
    display_checkmark("\035[92mHaproxy restarted successfully!\035  

def stop_menu():
    os.system("clear")
    display_notification("\035[93mStopping Haproxy...\035 
    print("\035[93m╭───────────────────────────────────────╮\035 
    display_loading()
    os.system("sudo systemctl stop haproxy")  
    display_checkmark("\035[92mHaproxy Stopped successfully!\035   

def remove_haproxy():
    os.system("clear")
    display_notification("\035[93mRemoving HAProxy...\035 
    print("\035[93m╭───────────────────────────────────────╮\035 
    display_loading()
    subprocess.run(["systemctl", "stop", "haproxy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["systemctl", "disable", "haproxy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "/etc/haproxy/haproxy.cfg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["apt-get", "remove", "--purge", "haproxy", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    display_checkmark("\035[92mHAProxy removed successfully!\035   
    
  ## later usage        
def private_ip():
    os.system("clear")
    print('\035[92m ^ ^\035 
    print('\035[92m(\035[91mO,O\035[92m)\035 
    print('\035[92m(   ) \035[93mPrivate | Native IP Menu\035 
    print('\035[92m "-"\035[93m══════════════════════════\035 
    print("\035[93m╭───────────────────────────────────────╮\035 
    print('\035[93mChoose what to do:\035 
    print('1. \035[96mExtra Native IP [ Kharej]\035 
    print('2. \035[92mKharej[Private IP]\035 
    print('3. \035[93mIRAN [Private IP]\035 
    print('4. \035[94mback to the main menu\035 
    print("\035[93m╰───────────────────────────────────────╯\035 

    while True:
        server_type = input('\035[38;5;205mEnter your choice Please: \035 
        if server_type == '2':
            kharej_private_menu()
            break
        elif server_type == '3':
            iran_private_menu()
            break
        elif server_type == '1':
            Native_menu()
            break
        elif server_type == '4':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
        
def add_cron_job():
    try:
        subprocess.run(
            "echo '@reboot /bin/bash /etc/private.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        display_checkmark("\035[92mCronjob added successfully!\035 
    except subprocess.CalledProcessError as e:
        print("\035[91mFailed to add cronjob:\035[0m", e)
        
def run_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
 
def run_ping_iran():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v6.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    
    
def display_kharej_ip(num_ips):
    print("\035[93mCreated Private IP Addresses (Kharej):\035 
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::1"
        print("\035[92m" + "+---------------------------+" + "\035 
        print("\035[92m" + f"| {ip_addr}    |" + "\035 
        print("\035[92m" + "+---------------------------+" + "\035 
        
def display_iran_ip(num_ips):
    print("\035[93mCreated Private IP Addresses (Iran):\035 
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::2"
        print("\035[92m" + "+---------------------------+" + "\035 
        print("\035[92m" + f"| {ip_addr}    |" + "\035 
        print("\035[92m" + "+---------------------------+" + "\035 
            
def kharej_private_menu():
    os.system("clear")
    print('\035[92m ^ ^\035 
    print('\035[92m(\035[91mO,O\035[92m)\035 
    print('\035[92m(   ) \035[93mConfiguring Kharej server\035 
    print('\035[92m "-"\035[93m═══════════════════════════\035 
    display_logo2()
    print("\035[93m╭────────────────────────────────────────────────────────────────────────────────────╮")
    print("\035[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\035[93m╰────────────────────────────────────────────────────────────────────────────────────╯\035 
    display_notification("\035[93mAdding private IP addresses for Kharej server...\035 

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
    local_ip = input("\035[93mEnter Kharej IPV4 address: \035 
    remote_ip = input("\035[93mEnter IRAN IPV4 address: \035 

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\035[93mHow many additional private IPs do you need? \035 )
    print("\035[93m╰─────────────────────────────────────────────────────────╯\035 

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi"], stdout=subprocess.DEVNULL)

    display_notification("\035[93mAdding commands to private.sh...\035 
    with open("/etc/private.sh", "w") as f:
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::1/64 dev azumi\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi\n")

    display_checkmark("\035[92mPrivate ip added successfully!\035 

    add_cron_job()

    time.sleep(1)
    display_checkmark("\035[92mkeepalive service Configured!\035 
    run_ping()
    time.sleep(1)
    display_kharej_ip(num_ips)

    time.sleep(1)

    script_content1 = '''#!/bin/bash

# IPv6 address
ip_address="fd1d:fc98:b73e:b481::2"

# maximum number
max_pings=4

# Interval
interval=60

# Loop run
while true
do
    # Loop for pinging specified number of times
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    
    print("\035[92mKharej Server Configuration Completed!\035 

def iran_private_menu():
    os.system("clear")
    print('\035[92m ^ ^\035 
    print('\035[92m(\035[91mO,O\035[92m)\035 
    print('\035[92m(   ) \035[93mConfiguring Iran server\035 
    print('\035[92m "-"\035[93m═══════════════════════════\035 
    display_logo2()
    print("\035[93m╭────────────────────────────────────────────────────────────────────────────────────╮")
    print("\035[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\035[93m╰────────────────────────────────────────────────────────────────────────────────────╯\035 
    display_notification("\035[93mAdding private IP addresses for Iran server...\035 
    
    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")
    

    print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
    local_ip = input("\035[93mEnter IRAN IPV4 address: \035 
    remote_ip = input("\035[93mEnter Kharej IPV4 address: \035 
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "fd1d:fc98:b73e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\035[93mHow many additional private IPs do you need? \035 )
    print("\035[93m╰─────────────────────────────────────────────────────────╯\035 
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi"], stdout=subprocess.DEVNULL)
    

    display_notification("\035[93mAdding commands to private.sh...\035 
    with open("/etc/private.sh", "w") as f:
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::2/64 dev azumi\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"fd1d:fc98:b73e:b48{ip_suffix}::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi\n")
    
    display_checkmark("\035[92mPrivate ip added successfully!\035 
    


    add_cron_job()

    sleep(1)
    display_checkmark("\035[92mkeepalive service Configured!\035 
   
    run_ping_iran()
    sleep(1)
    display_iran_ip(num_ips)
    

    sleep(1)


    script_content = '''#!/bin/bash

# IPv6 address
ip_address="fd1d:fc98:b73e:b481::2"

# maximum number
max_pings=4

# Interval
interval=50

# Loop run
while true
do
    # Loop for pinging specified number of times
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v6.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()



def Native_menu():
    subprocess.run("clear", shell=True)
    print("\035[92m ^ ^\035 
    print("\035[92m(\035[91mO,O\035[92m)\035 
    print("\035[92m(   ) \035[93mNative IP Menu\035 
    print("\035[92m \"-\"\035[93m═════════════════════\035 
    display_logo2()
    print("\035[93m.-------------------------------------------------------------------------------------------------------.\035 
    print("\035[93m| \035[92mIf it didn't work, please uninstall it and add extra IP manually  \035 
    print("\035[93m|\035[0m  If you don't have native IPv6, please use a private IP instead.                                             \035 
    print("\035[93m'-------------------------------------------------------------------------------------------------------'\035 
    display_notification("\035[93mAdding extra Native IPv6 [Kharej]...\035 
    print("\035[93m╭──────────────────────────────────────────────────────────╮\035 

    try:
        interface = subprocess.run("ip route | awk '/default/ {print $5; exit}'", shell=True, capture_output=True, text=True).stdout.strip()
        ipv6_addresses = subprocess.run(f"ip -6 addr show dev {interface} | awk '/inet6 .* global/ {{print $2}}' | cut -d'/' -f1", shell=True, capture_output=True, text=True).stdout.strip().split('\n')

        print("\035[92mCurrent IPv6 addresses on", interface + ":\035 
        for address in ipv6_addresses:
            print(address)

        confirm = input("\035[93mAre these your current IPv6 addresses? (y/n): \035 
        if confirm.lower() != "y":
            display_error("\035[91mAborted. Please manually configure the correct IPv6 addresses.\035 
            return

        sorted_addresses = sorted(ipv6_addresses, reverse=True)
        additional_address = ""
        for i in range(len(sorted_addresses)):
            current_last_part = sorted_addresses[i].split(':')[-1]
            modified_last_part_hex = format(int(current_last_part, 16) + 1, '04x')
            modified_address = ":".join(sorted_addresses[i].split(':')[:-1]) + ":" + modified_last_part_hex

            if modified_address not in sorted_addresses:
                additional_address = modified_address
                break

        if not additional_address:
            display_error("\035[91mNo additional address to add.\035 
            return

        subprocess.run(["ip", "addr", "add", f"{additional_address}/64", "dev", interface])

        script_file = "/etc/ipv6.sh"
        with open(script_file, "a") as file:
            file.write(f"ip addr add {additional_address}/64 dev {interface}\n")

        subprocess.run(["chmod", "+x", script_file])

        subprocess.run("crontab -l | grep -v '/etc/ipv6.sh' | crontab -", shell=True)

        display_notification("\035[93mAdding cronjob for the server..\035 
        subprocess.run("(crontab -l 2>/dev/null; echo \"@reboot /bin/bash /etc/ipv6.sh\") | crontab -", shell=True)

        display_checkmark("\035[92mIPv6 addresses added successfully!\035 
    except ValueError as e:
        display_error("\035[91mAn error occurred while adding IPv6 addresses:", str(e), "\035 
        
def get_ipv4():
    interfaces = ni.interfaces()
    for interface in interfaces:
        if interface.startswith('eth') or interface.startswith('en'):
            try:
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    ipv4 = addresses[ni.AF_INET][0]['addr']
                    return ipv4
            except KeyError:
                pass
    return None
    
def save_haproxy(config):
    config_path = "/etc/haproxy/haproxy.cfg"
    
    if os.path.exists(config_path):
        os.remove(config_path)

   
    with open(config_path, "w") as file:
        file.write(str(config))

def restart_haproxy():
    os.system("systemctl restart haproxy")
    display_checkmark("\035[92mHAProxy service restarted!\035 
    
def install_haproxy():
    display_loading()
    os.system("apt-get install -y haproxy > /dev/null")
    display_checkmark("\035[92mHAProxy installation completed.!\035 
    
        
def haproxy_tunnel(ipv6_addresses, ipv6_ports, iran_port):
    config = f"""\
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # Default SSL material locations
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private

    # See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE>
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    log global
    mode tcp
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

frontend vless_frontend
    bind *:{iran_port}
    mode tcp
    default_backend azumi_backend

backend azumi_backend
    mode tcp
    balance roundrobin
    option tcp-check
"""
    
    for i in range(len(ipv6_addresses)):
        ipv6_address = ipv6_addresses[i]
        ipv6_port = ipv6_ports[i]
        config += f"    server azumi{i+1} {ipv6_address}:{ipv6_port} check\n"
    return config
    
def haproxy2_tunnel(ipv6_addresses, ipv6_ports, iran_ports):
    config = '''\
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # Default SSL material locations
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private

    # See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE>
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    log global
    mode tcp
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

'''

    for i in range(len(ipv6_addresses)):
        ipv6_address = ipv6_addresses[i]
        ipv6_port = ipv6_ports[i]
        iran_port = iran_ports[i]
        frontend_name = f'vless{i+1}_frontend'
        backend_name = f'azumi{i+1}_backend'
        config += f'''
frontend {frontend_name}
    bind *:{ipv6_port}
    mode tcp
    default_backend {backend_name}

backend {backend_name}
    mode tcp
    server azumi{i+1} {ipv6_address}:{ipv6_port}
'''
    return config
    
def haproxy_menu():
    subprocess.run("clear", shell=True)
    print("\035[92m ^ ^\035 
    print("\035[92m(\035[91mO,O\035[92m)\035 
    print("\035[92m(   ) \035[93mHaproxy Loadbalance & IPV6 Tunnel Menu\035 
    print("\035[92m \"-\"\035[93m════════════════════════════════════\035 
    display_logo2()
    print("\035[93m.-------------------------------------------------------------------------------------------------------.\035 
    print("\035[93m| \035[92mYou can use private or native ipv6 as for kharej ipv6 addresses  \035 
    print("\035[93m| \035[93mConfigure Haproxy on iran server  \035 
    print("\035[92m| \035[92mYou can enter different Kharej IPV6 addresses with different port and one single port for iran  \035 
    print("\035[93m| \035[93mYour V2rayng address : IPV4-IRAN : Iran-port [eg : 443]  \035 
    print("\035[93m'-------------------------------------------------------------------------------------------------------'\035 
    display_notification("\035[93mConfigruing Haproxy...\035 
    install_haproxy()
    print("\035[93m╭──────────────────────────────────────────────────────────╮\035 
    num_ipv6 = int(input("\035[93mEnter the number of \035[92mKharej\035[93m IPv6 addresses:\035[0m "))
    ipv6_addresses = []
    ipv6_ports = []

    for i in range(num_ipv6):
        address = input("\035[93m" + f"Enter \035[92mKharej\035[93m IPv6 address \035[92m{i+1}: " + "\035 
        port = input("\035[93m" + f"Enter the port for \035[92mKharej\035[93m IPv6 address \035[92m{i+1}: " + "\035 
        ipv6_addresses.append(address)
        ipv6_ports.append(port)

    iran_port = input("\035[93m" + "Enter the port for \035[92mIran\035[0m" + " Server: ")
    config = haproxy_tunnel(ipv6_addresses, ipv6_ports, iran_port)


    save_haproxy(config)
    sleep(1)
    restart_haproxy()
    print("\035[93m╰─────────────────────────────────────────────────────────╯\035 

    display_checkmark("\035[92mHAProxy configuration file generated!\035 

    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
        print(f"\035[93m| V2rayng Address: {current_ipv4} : {iran_port}  \035 
        print("\035[93m╰─────────────────────────────────────────────────────────╯\035 
    else:
        print("\035[93mUnable to retrieve server's IPv4 address.\035 

def haproxy3_menu():
    subprocess.run("clear", shell=True)
    print("\035[92m ^ ^\035 
    print("\035[92m(\035[91mO,O\035[92m)\035 
    print("\035[92m(   ) \035[93mHaproxy Simple \035[92mIPV6 Tunnel\035[93m Menu\035 
    print("\035[92m \"-\"\035[93m════════════════════════════════════\035 
    display_notification("\035[93mConfiguring Haproxy...\035 
    install_haproxy()
    print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
    num_ipv6 = int(input("\035[93mEnter the number of \035[92mKharej \035[96mConfigs\035[93m:\035[0m "))
    ipv4_address = input("\035[93mEnter \035[92mKharej\035[93m IPV6 address: " + "\035 
    ipv6_ports = []
    iran_ports = []

    for i in range(num_ipv6):
        print("\035[93m──────────────────────────────\035 
        print(f"\035[92m      --- Config\035[96m {i+1}\035[92m ---\035 
        print("\035[93m──────────────────────────────\035 
        port = input("\035[93m" + f"Enter\035[92m Kharej\035[93m Config \035[92m{i+1}\035[93m port: " + "\035 
        ipv6_ports.append(port)
        iran_port = input(f"\035[93mEnter \035[92mhaproxy \035[93mport \035[96mConfig \035[92m{i+1}\035[93m: \035 
        iran_ports.append(iran_port)

    ipv6_addresses = [ipv4_address] * num_ipv6

    config = haproxy2_tunnel(ipv6_addresses, ipv6_ports, iran_ports)

    save_haproxy(config)
    sleep(1)
    restart_haproxy()
    print("\035[93m╰─────────────────────────────────────────────────────────╯\035 

    display_checkmark("\035[92mHAProxy configuration file generated!\035 

    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
        for i in range(num_ipv6):
            print(f"\035[93m| V2rayng Address {i+1}: {current_ipv4} : {iran_ports[i]}  \035 
        print("\035[93m╰─────────────────────────────────────────────────────────╯\035 
    else:
        print("\035[93mUnable to retrieve server's IPv4 address.\035 
        

def haproxy2_menu():
    subprocess.run("clear", shell=True)
    print("\035[92m ^ ^\035 
    print("\035[92m(\035[91mO,O\035[92m)\035 
    print("\035[92m(   ) \035[93mHaproxy Simple \035[92mIPV4 Tunnel\035[93m Menu\035 
    print("\035[92m \"-\"\035[93m════════════════════════════════════\035 
    display_notification("\035[93mConfiguring Haproxy...\035 
    install_haproxy()
    print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
    num_ipv6 = int(input("\035[93mEnter the number of \035[92mKharej \035[96mConfigs\035[93m:\035[0m "))
    ipv4_address = input("\035[93mEnter \035[92mKharej\035[93m IPV4 address: " + "\035 
    ipv6_ports = []
    iran_ports = []

    for i in range(num_ipv6):
        print("\035[93m──────────────────────────────\035 
        print(f"\035[92m      --- Config\035[96m {i+1}\035[92m ---\035 
        print("\035[93m──────────────────────────────\035 
        port = input("\035[93m" + f"Enter\035[92m Kharej\035[93m Config \035[92m{i+1}\035[93m port: " + "\035 
        ipv6_ports.append(port)
        iran_port = input(f"\035[93mEnter \035[92mhaproxy \035[93mport \035[96mConfig \035[92m{i+1}\035[93m: \035 
        iran_ports.append(iran_port)

    ipv6_addresses = [ipv4_address] * num_ipv6

    config = haproxy2_tunnel(ipv6_addresses, ipv6_ports, iran_ports)

    save_haproxy(config)
    sleep(1)
    restart_haproxy()
    print("\035[93m╰─────────────────────────────────────────────────────────╯\035 

    display_checkmark("\035[92mHAProxy configuration file generated!\035 

    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
        for i in range(num_ipv6):
            print(f"\035[93m| V2rayng Address {i+1}: {current_ipv4} : {iran_ports[i]}  \035 
        print("\035[93m╰─────────────────────────────────────────────────────────╯\035 
    else:
        print("\035[93mUnable to retrieve server's IPv4 address.\035 
        
def haproxy_kharej():
    subprocess.run("clear", shell=True)
    print("\035[92m ^ ^\035 
    print("\035[92m(\035[91mO,O\035[92m)\035 
    print("\035[92m(   ) \035[93mHaproxy Loadbalance | No Tunnel Menu\035 
    print("\035[92m \"-\"\035[93m════════════════════════════════════\035 
    display_logo2()
    print("\035[93m.-------------------------------------------------------------------------------------------------------.\035 
    print("\035[93m| \035[92mYou can use private or native ipv6 as for kharej ipv6 addresses  \035 
    print("\035[93m| \035[93mConfigure Haproxy on Kahrej server since we don't use tunnel for this purpose  \035 
    print("\035[92m| \035[92mYou can enter different Kharej IPV6 addresses with different port  \035 
    print("\035[93m| \035[93mYour V2rayng address : IPV4-Kharej : Loadbalance-port [eg : 443]  \035 
    print("\035[93m'-------------------------------------------------------------------------------------------------------'\035 
    display_notification("\035[93mConfigruing Haproxy...\035 
    install_haproxy()
    print("\035[93m╭──────────────────────────────────────────────────────────╮\035 
    num_ipv6 = int(input("\035[93mEnter the number of \035[92mKharej\035[93m IPv6 addresses:\035[0m "))
    ipv6_addresses = []
    ipv6_ports = []

    for i in range(num_ipv6):
        address = input("\035[93m" + f"Enter \035[92mKharej\035[93m IPv6 address \035[92m{i+1}: " + "\035 
        port = input("\035[93m" + f"Enter the port for \035[92mKharej\035[93m IPv6 address \035[92m{i+1}: " + "\035 
        ipv6_addresses.append(address)
        ipv6_ports.append(port)

    iran_port = input("\035[93m" + "Enter the port for \035[92mLoadbalancer:\035 
    config = haproxy_tunnel(ipv6_addresses, ipv6_ports, iran_port)


    save_haproxy(config)
    sleep(1)
    restart_haproxy()
    print("\035[93m╰─────────────────────────────────────────────────────────╯\035 

    display_checkmark("\035[92mHAProxy configuration file generated!\035 

    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\035[93m╭─────────────────────────────────────────────────────────╮\035 
        print(f"\035[93m| V2rayng Address: {current_ipv4} : {iran_port}  \035 
        print("\035[93m╰─────────────────────────────────────────────────────────╯\035 
    else:
        print("\035[93mUnable to retrieve server's IPv4 address.\035     
           
    


def clear():
   
    pass


main_menu()
