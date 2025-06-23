timeb0mb | CTF Challenge Writeup  

    - Category: Reverse Engineering
    - Score: 50  

Challenge: [Download](https://github.com/Debang5hu/ctf-writeups/blob/main/challenges/timeb0mb)  

We begin by identifying the binary type using the file command:  

`file ./timeb0mb`  

[![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*9p1iF7xpu54dMeiiduf68w.png)]  


```sh
# Make the binary executable and run it:  
chmod +x timeb0mb

./timeb0mb  
```  

Upon execution, the binary starts printing characters of the flag one by one but at irregular intervals. It quickly becomes apparent that it would take a very long time to print the entire flag.  

Now, let's use a disassembler to reverse the binary  

We load the binary into a disassembler (like Ghidra or IDA Pro) to recover the logic behind it.  

[![](https://miro.medium.com/v2/resize:fit:526/format:webp/1*PNAb-3nG0xyc7kAIfrxd4g.png)]

We discover that the main function calls flag(), which contains the actual flag, stored in little-endian format across four variables: <i>local_38</i>, <i>local_30</i>, <i>local_28</i>, and <i>local_20</i>.  

Here's a decompiled version of the flag() function:

```c
void flag(void)

{
  int iVar1;
  long in_FS_OFFSET;
  int i;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_38 = 0x7665725f65646f63;
  local_30 = 0x6c6c615f736c6165;
  local_28 = 0x737465726365735f;
  local_20 = 0x21;
  for (i = 0; *(char *)((long)&local_38 + (long)i) != '\0'; i = i + 1) {
    if (i < 2) {
      sleep(3);
      putchar((int)*(char *)((long)&local_38 + (long)i));
      fflush(stdout);
    }
    else {
      iVar1 = jitter();
      putchar((int)*(char *)((long)&local_38 + (long)i));
      fflush(stdout);
      sleep(iVar1 + 3);
    }
  }
  
  return;
}
```  

Digging into the `jitter()` function reveals the source of the massive delay:

```c
int jitter(void)

{
  int iVar1;
  iVar1 = rand();
  return iVar1 % 0x321 + 0x4b0;
}
```  

The function returns a random number between 0x4b0 (1200) and 0x7d0 (2000), which is used to sleep before printing each character. That's up to 30 minutes of sleep per  
character! Although the flag is hardcoded, the binary deliberately slows down the output.  

Instead of waiting for ages, we can extract and decode the flag manually using the values in the variables.  

python script to get the flag.

```python
#! /usr/bin/python3
# _*_ coding: utf-8 _*_

flag = ''

# Little Endian
local_38 = 0x7665725f65646f63
local_30 = 0x6c6c615f736c6165
local_28 = 0x737465726365735f
local_20 = 0x21

for i in [local_38,local_30,local_28,local_20]:
 byte_array = i.to_bytes(8, byteorder='little')
 for x in byte_array:
  flag += chr(x)
print(f'flag: {flag}')
```  

Run it to get the flag!!!