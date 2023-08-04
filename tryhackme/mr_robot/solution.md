https://tryhackme.com/room/mrrobot  

connect to tryhackme vpn and spawn the machine  

[!] for the first part we dont need any answer  

--------------------------------------------------------------------------------------------------------------  

Now scan the target and list the open ports,since we got that it have its http port open we will see  
the website and start a directory fuzzing  

we got a lot of directories just head to the robots.txt  
we find 2 files are listed over there  

[*] What is key 1?  
 => visit "key-1-of-3.txt" for the first flag  
 
next download another file which is listed there  
 
from the directory fuzzing we got an very interesting page i.e the "wp-login.php"  
I just tried to login as user:test and password:test  
but it shows something interesting "Invalid username"  

![mr_robot_login](https://github.com/Debang5hu/ctf-writeups/assets/114200360/6db3babc-0de3-4532-8d64-80af9180e548)


without giving a second thought just use hydra and remember they gave us a wordlist! just use it for bruteforcing.  

But before bruteforce just use this command ["cat fsocity.dic | sort | uniq > newfsocity.dic"]  

this simply means that we are making a file where only unique words of the dic file is getting stored (sometimes in a wordlist there can be many repeated words  
just to remove them I am using the command!)   

command used to bruteforce the user [hydra -L fsocity.dic -p test http-post-form://10.10.13.123/wp-login.php:"log=^USER^&pwd=^PASS^&wp-submit=Log+In":"Invalid username" -V]  

![user_mr_robot](https://github.com/Debang5hu/ctf-writeups/assets/114200360/43a420fd-1ff8-4b00-82d1-7d9e98389a8a)


Now,we got "Elliot" as the username  
next,time to bruteforce the password  

command used [hydra -l Elliot -P newfsocity.dic http-post-form://10.10.13.123/wp-login.php:"log=^USER^&pwd=^PASS^&wp-submit=Log+In":"The password you entered for" -V]  

![mr_robot_pass](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ccdbe2dd-b4cb-4e27-aba7-f301e89d5be8)



then just log in to the website with the credentials  

just explore the account and we find something interesting i.e the editor option under appearance and we can edit it too  

just upload php reverse shell over there(in the 404 Template)  

![error](https://github.com/Debang5hu/ctf-writeups/assets/114200360/c1ae2b13-f9a7-4da0-a6f9-2004f4f30074)  


now open a terminal and use netcat to establish the reverse shell (nc -lnvp {port_you_choose})  

and generate an error in the website to get the reverse shell cause at that time the php script will get executed  

and BOOM we got the reverse shell,just check whether it have python in it or not if yes they use pty module to make an interective shell [python -c "import pty;pty.spawn('/bin/bash')"]   

the 2nd key can be find in "/home/robot" dir but we dont have the permission to read it  

but we find something interesting that is the "password.raw-md5" file  
just crack the md5 to get the password of "robot" user and get into it  

[*] What is key 2?  
 => and cat the key-2-of-3.txt to get the flag  
 
So,its the time to get root,do a SUID lookup  

I used this "find / -user root -perm /4000 2>/dev/null" for SUID lookup   
and got something interesting that is nmap got the SUID bit,and we can use it to get root privileges  

you can use GTFOBins to exploit it  


[*] What is key 3?  
 => now just read the key-3-of-3.txt to get the final flag  
 
 
 Thankyou

-----------------------------------------------------------------------------x-------------------------------------------------------------------------------------
