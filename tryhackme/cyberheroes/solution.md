Machine:Cyber Heroes  
Link:https://tryhackme.com/room/cyberheroes  


It's a pretty straight forward ctf focuses on "credential" and "authentication"  

start by exporting the target ip  

```
export IP=targetip
```  

run a nmap scan on it  

<h3>nmap -sC -sV $IP</h3>  

```
Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-09 21:06 IST
Nmap scan report for 10.10.227.239
Host is up (0.16s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 fc:93:54:18:d4:f0:1e:9e:39:5e:18:5b:cc:a4:dd:93 (RSA)
|   256 1d:26:a0:fa:29:17:1a:2c:97:61:84:a3:2b:81:cb:9f (ECDSA)
|_  256 98:70:1b:57:10:fc:45:d8:ee:dc:ec:36:b3:bb:a5:56 (ED25519)
80/tcp open  http    Apache httpd 2.4.48 ((Ubuntu))
|_http-title: CyberHeros : Index
|_http-server-header: Apache/2.4.48 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.04 seconds

```  

we found 2 open ports(22,80)  

Open the site in the browser  

![Screenshot_2023-09-09_22-24-06](https://github.com/Debang5hu/ctf-writeups/assets/114200360/9f3dcf1e-1baa-4e97-9208-231a2a303654)

Head to the login page  

![login](https://github.com/Debang5hu/ctf-writeups/assets/114200360/2cb46026-67b1-4c09-a006-92fd5874f1b4)

View the page source  

![pagesource](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ddca9dfa-1ab7-42bf-98e0-21a5012a14d7)

from the "authenticate" function we get the username and password  

![credentials](https://github.com/Debang5hu/ctf-writeups/assets/114200360/bc76ad99-038c-4d1c-9f61-023c1046192d)

the "b" variable stores the password and it calls a function named "RevereString" which basically reverse the string,reverse "54321@terceSrepuS"  to get the password  

```
Python 3.11.4 (main, Jun  7 2023, 10:13:09) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> "54321@terceSrepuS"[::-1]
'SuperSecret@12345'
>>> 

```


user:"h3ck3rBoi"
password="SuperSecret@12345"


login with the credentials to get the flag!  

![flag](https://github.com/Debang5hu/ctf-writeups/assets/114200360/f5a7ecf3-d8ac-417d-ad1a-19b289336313)
