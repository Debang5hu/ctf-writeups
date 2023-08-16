Machine: Anonforce  
Link: https://tryhackme.com/room/bsidesgtanonforce  

This is a very simple machine  


Start with a nmap scan "nmap -sC -sV {target_ip}"  
we find that port 21 and 22 are open and "anonymous" login is allowed  

![anonforce_nscan](https://github.com/Debang5hu/ctf-writeups/assets/114200360/495fe0ad-f36a-45e0-b109-4a6a47b672a7)

Get into its ftp server,we find that we can change our directory also found one interesting directory "notread",so get into home directory "cd /home/melodias"  
get the user.txt  

![ftp_anonforce](https://github.com/Debang5hu/ctf-writeups/assets/114200360/33098601-de9e-4e90-aed6-c80379a44d51)

![anon_user](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ab13fa98-afb3-4ed2-a425-2ec5db0d8c07)

![catuser_anonforce](https://github.com/Debang5hu/ctf-writeups/assets/114200360/5b29cf68-c50f-4710-bf91-a61a9aa12068)

now get into the notread directory,we find two files ‘backup.pgp’ and ‘private.asc’ get it into your machine (mget *).  

The "backup.pgp" file can be decypted using "private.asc" file

First crack the password of "private.asc" ("gpg2john private.asc > pass.txt")  
then ("john pass.txt --wordlist=/usr/share/wordlist/rockyou.txt")  
after getting the pass use it to open the "backup.pgp" file  

"gpg --import private.asc"  
"gpg backup.pgp"  

![dcrypt_anonforce](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ba1f0efb-9abc-444e-9a95-e309cb16a6aa)

we got a file named "backup"  
cat it to see its contains (it is a shadow file)  


Now,we need the contents of both the shadow file(which we got) and passwd file(which we can get using ftp) and combine them before cracking the hash using "unshadow" tool  

Get into the ftp session to get the "/etc/passwd" file  

"unshadow {passwd_file} {shadow_file} > root_pass.txt"  

then use john to crack the password  

"john root_pass.txt" --wordlist=/usr/share/wordlist/rockyou.txt"  

after getting the root password "hikari" log into its root account using ssh  

"ssh root@{ip}"

![root_anonforce](https://github.com/Debang5hu/ctf-writeups/assets/114200360/4d46d333-3daa-4886-8447-f5fda9f6452d)

and get the root flag(/root/root.txt)  

![rootflag_anonforce](https://github.com/Debang5hu/ctf-writeups/assets/114200360/78fe18ca-ebe1-4ac0-bc53-29f56b165ca1)
