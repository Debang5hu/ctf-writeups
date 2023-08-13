Raven1  
---------  

link: https://www.vulnhub.com/entry/raven-1,256/  

download the machine and boot it in virtual box an configure it

Next step:  

then find the ip of target machine,you can use "arp-scan" or "netdiscover" to do so

I used "arp-scan --interface=wlan0 --localnet"  to get the ip of the machine  

After getting the it run a nmap scan "nmap -sC -sV ip"  

![enum](https://github.com/Debang5hu/ctf-writeups/assets/114200360/58cc9022-1e5b-44bf-8797-b60bbd1376d1)

since it have port 80 open,open it in a browser and navigate to "service page" and inspect its page source to get the first flag!  

![flag1](https://github.com/Debang5hu/ctf-writeups/assets/114200360/875cd155-086b-40e7-817f-739b89c34b5f)

then run a gobuster scan or any other directory fuzzing tool to get its hidden directories "gonuster dir -u {url} -w {wordlists}"  

![dir_fuzz](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ad0c5be2-890a-4931-ab7b-6aee3b4ca106)

we got an interesting directory i.e, "wordpress"  

![wordpress_raven](https://github.com/Debang5hu/ctf-writeups/assets/114200360/fbbc87ec-00bd-4a4d-9273-c0e59637e874)

since it is running on wordpress,just run a wordpress scan to see if we can enumerate the user/s or not "wpscan --url http://192.168.0.106/wordpress/ -e u"  

![wpscan](https://github.com/Debang5hu/ctf-writeups/assets/114200360/5e224b5f-1558-433c-b78d-df9655809639)

we were successful to get the users(michael,steven)  
since it have its ssh open we can bruteforce using hydra,i was successful to get michael's password "michael"  

![hydra_raven](https://github.com/Debang5hu/ctf-writeups/assets/114200360/bd2a5f76-c5ca-470e-9f84-5504de3b58f7)

then log in with the credentials "ssh  michael@ip"  

![ssh_raven](https://github.com/Debang5hu/ctf-writeups/assets/114200360/74badc0a-4e3d-40ca-a2da-4cb05a47eb46)

just get into /var/www directory to get the 2nd flag  

![flag2](https://github.com/Debang5hu/ctf-writeups/assets/114200360/4f68122c-4f02-481b-8ccd-4a31fdfcca6e)

then get into /var/www/html directory to explore the contents of the website  
get into the "wordpress" directory and access the "wp-config.php" file to get credentials of the mysql  

![mysql_raven](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ec41b4de-79f2-4bf0-82d1-bf4a4d2868db)

from "wp-users" we will get the hash of stevens password,we can crack it using "john the ripper" "john hash_file"  

![steven_pass](https://github.com/Debang5hu/ctf-writeups/assets/114200360/811bca59-e2b9-4f17-8b3e-6b0eb614ced7)

accress the "wp-posts" table to get the 3rd flag(we will even find the 4th flag there,it is due to some misconfiguration)  

![flag3](https://github.com/Debang5hu/ctf-writeups/assets/114200360/961382ad-cd6f-4f22-814b-52ed1b1f32a1)

then login in to steven's account,we see that python can be run with sudo permission,just exploit it to root the machine
"sudo python -c "import os;os.system('/bin/bash')"" and we are root  
"cat /root/flag4.*" to get the 4th flag   

![flag4](https://github.com/Debang5hu/ctf-writeups/assets/114200360/9bf6ae19-6a49-4772-8c2d-ab8c811f56c6)
