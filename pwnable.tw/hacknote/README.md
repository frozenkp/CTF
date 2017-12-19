# hacknote

> Challenge Link: [hacknote](https://pwnable.tw/challenge/#5)
>
> Category: pwn

A good Hacker should always take good notes!

`nc chall.pwnable.tw 10102`

[hacknote](https://pwnable.tw/static/chall/hacknote)

[libc.so](https://pwnable.tw/static/libc/libc_32.so.6)

## Observation

This challenge is a Hacknote. There are 4 features (actually 3) - **Add, Delete, and Print**.

```
----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :1
Note size :20
Content :abcd 
Success !
----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :3
Index :0
abcd

----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :2
Index :0
Success
----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :4
```

I wrote another challenge in `csie.ctf.tw` also called "hacknote" before, and both of these look similar.

In hacknote (csie), this program `malloc` when add and `free` when delete. However, **it didn't set the pointer to `NULL` **. Therefore, we can use add to write something, and use print to run.

What do I mean ? Let's try !

### Experiment

#### Add two notes

I add two notes with size 32 and contents are "aaaa" and "bbbb".

Here is the value on the heap.

```
0x804b000:	0x00000000	0x00000011	  0x0804862b	0x0804b018
0x804b010:	0x00000000	0x00000029	  0x61616161	0x0000000a 	<======= note "aaaa"
0x804b020:	0x00000000	0x00000000	  0x00000000	0x00000000
						-----------------------------
0x804b030:	0x00000000	0x00000000	| 0x00000000	0x00000011
            -------------------------------------
0x804b040:	0x0804862b	0x0804b050	  0x00000000	0x00000029
0x804b050:	0x62626262	0x0000000a	  0x00000000	0x00000000 	<======= note "bbbb"
0x804b060:	0x00000000	0x00000000	  0x00000000	0x00000000
```

Let's focus on note "aaaa".

```
           ------------------------------------------------------
0x804b000: | 0x00000000	0x00000011	0x0804862b  0x0804b018  | <======= struct note
   	   ---------------------------------------------|--------
   		   					|
   		   			    -------------
   		   			    |
           ---------------------------------v--------------------
0x804b010: | 0x00000000	0x00000029	0x61616161  0x0000000a 	|
0x804b020: | 0x00000000	0x00000000	0x00000000  0x00000000	| <======= content
0x804b030: | 0x00000000	0x00000000				|
   	   ------------------------------------------------------
```

The first 8 bytes of each blocks are headers of  heap.

- struct note is 0x10

- `0x0804862b`is print function

  ```
   804862b:       55                      push   ebp
   804862c:       89 e5                   mov    ebp,esp
   804862e:       83 ec 08                sub    esp,0x8
   8048631:       8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
   8048634:       8b 40 04                mov    eax,DWORD PTR [eax+0x4]
   8048637:       83 ec 0c                sub    esp,0xc
   804863a:       50                      push   eax
   804863b:       e8 90 fe ff ff          call   80484d0 <puts@plt>
   8048640:       83 c4 10                add    esp,0x10
   8048643:       90                      nop
   8048644:       c9                      leave  
   8048645:       c3                      ret
  ```

#### Delete

I delete note "aaaa" (index 0) first, then I delete note "bbbb" (index 1).

Here is the fastbin in heap.

```
(0x10)     fastbin[0]: 0x804b038 --> 0x804b000 --> 0x0
(0x18)     fastbin[1]: 0x0
(0x20)     fastbin[2]: 0x0
(0x28)     fastbin[3]: 0x804b048 --> 0x804b010 --> 0x0
(0x30)     fastbin[4]: 0x0
(0x38)     fastbin[5]: 0x0
(0x40)     fastbin[6]: 0x0
                  top: 0x804b070 (size : 0x20f90) 
       last_remainder: 0x0 (size : 0x0) 
            unsortbin: 0x0
```

#### Reallocate

I add a new note with size **0x8** (0x8 + header = 0x10). Note 2 is allocated to 0x804b038, and it's content is 0x804b000 (original note 0).

```
	      ---------------------------------------------------------------
0x804b000:    | 0x00000000      0x00000011      0x61616161      0x0804b00a  | <== content
 	      ---------------------------------------------------------------
0x804b010:      0x00000000      0x00000029      0x00000000      0x0000000a
0x804b020:      0x00000000      0x00000000      0x00000000      0x00000000
					     --------------------------------
0x804b030:      0x00000000      0x00000000   |  0x00000000      0x00000011  |
	      -------------------------------- 				    | <== header
0x804b040:    | 0x0804862b      0x0804b008 				    |
	      ---------------------------------------------------------------
```

## Solution

Accroding to the experiment above, we can exploit it by reusing note.

### Leak libc

First, we should leak the base of libc in order to using system().

I choose `puts_got = 0x804a024`to leak.

Because of the size of struct is 0x10, we can only use only 0x8 as content size (0x8 + header = 0x10). Thus, I put `printNote function` and `puts_got`in content to leak base.

After adding note 2, note 0 is like this:

```c
struct note {
	printNote(); 		// 0x0804862b
  	puts_got; 		// 0x804a024
}
```

When we print note 0, it will call printNote() then print puts_got.

### System()

Before printing note, this program send address of note as parameter to function.

![](https://i.imgur.com/dYKZzfa.png)

```
					    -----------------
0x804b000:      0x00000000      0x00000011  |   0x0804862b  |    0x0804b018
					    -----------------
0x804b010:      0x00000000      0x00000029      0x61616161      0x0000000a
```

What if this function is system() ?? Value from `0x804b008`would be considered as string.

Therefore, we can put something like `;sh` in content. Because string before `;` can not be executed, we have to add a `;` to split it. 

After printing (system), a shell will prompt !!
