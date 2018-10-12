# be-quick-or-be-dead-3
Running either `strace` or `ltrace` shows that the binary uses `alarm`. We can instead run it in `gdb` using `ha SIGALRM i`. The program still runs for a long time, so we dissassemble the file in objdump using `objdump -M intel -d be-quick-or-be-dead-3`
The important sections are
```asm
00000000004008a6 <main>:
  4008a6:       55                      push   rbp
  4008a7:       48 89 e5                mov    rbp,rsp
  4008aa:       48 83 ec 10             sub    rsp,0x10
  4008ae:       89 7d fc                mov    DWORD PTR [rbp-0x4],edi
  4008b1:       48 89 75 f0             mov    QWORD PTR [rbp-0x10],rsi
  4008b5:       b8 00 00 00 00          mov    eax,0x0
  4008ba:       e8 a9 ff ff ff          call   400868 <header>
  4008bf:       b8 00 00 00 00          mov    eax,0x0
  4008c4:       e8 f8 fe ff ff          call   4007c1 <set_timer>
  4008c9:       b8 00 00 00 00          mov    eax,0x0
  4008ce:       e8 42 ff ff ff          call   400815 <get_key>
  4008d3:       b8 00 00 00 00          mov    eax,0x0
  4008d8:       e8 63 ff ff ff          call   400840 <print_flag>
  4008dd:       b8 00 00 00 00          mov    eax,0x0
  4008e2:       c9                      leave
  4008e3:       c3                      ret
  4008e4:       66 2e 0f 1f 84 00 00    nop    WORD PTR cs:[rax+rax*1+0x0]
  4008eb:       00 00 00
  4008ee:       66 90                   xchg   ax,ax

0000000000400815 <get_key>:
  400815:       55                      push   rbp
  400816:       48 89 e5                mov    rbp,rsp
  400819:       bf 08 0a 40 00          mov    edi,0x400a08
  40081e:       e8 0d fd ff ff          call   400530 <puts@plt>
  400823:       b8 00 00 00 00          mov    eax,0x0
  400828:       e8 65 ff ff ff          call   400792 <calculate_key>
  40082d:       89 05 7d 08 20 00       mov    DWORD PTR [rip+0x20087d],eax        # 6010b0 <__TMC_END__>
  400833:       bf 1b 0a 40 00          mov    edi,0x400a1b
  400838:       e8 f3 fc ff ff          call   400530 <puts@plt>
  40083d:       90                      nop
  40083e:       5d                      pop    rbp
  40083f:       c3                      ret

0000000000400792 <calculate_key>:
  400792:       55                      push   rbp
  400793:       48 89 e5                mov    rbp,rsp
  400796:       bf 65 99 01 00          mov    edi,0x19965
  40079b:       e8 66 ff ff ff          call   400706 <calc>
  4007a0:       5d                      pop    rbp
  4007a1:       c3                      ret

0000000000400706 <calc>:
  400706:       55                      push   rbp
  400707:       48 89 e5                mov    rbp,rsp
  40070a:       41 54                   push   r12
  40070c:       53                      push   rbx
  40070d:       48 83 ec 20             sub    rsp,0x20
  400711:       89 7d dc                mov    DWORD PTR [rbp-0x24],edi
  400714:       83 7d dc 04             cmp    DWORD PTR [rbp-0x24],0x4
  400718:       77 11                   ja     40072b <calc+0x25>
  40071a:       8b 45 dc                mov    eax,DWORD PTR [rbp-0x24]
  40071d:       0f af 45 dc             imul   eax,DWORD PTR [rbp-0x24]
  400721:       05 45 23 00 00          add    eax,0x2345
  400726:       89 45 ec                mov    DWORD PTR [rbp-0x14],eax
  400729:       eb 5b                   jmp    400786 <calc+0x80>
  40072b:       8b 45 dc                mov    eax,DWORD PTR [rbp-0x24]
  40072e:       83 e8 01                sub    eax,0x1
  400731:       89 c7                   mov    edi,eax
  400733:       e8 ce ff ff ff          call   400706 <calc>
  400738:       89 c3                   mov    ebx,eax
  40073a:       8b 45 dc                mov    eax,DWORD PTR [rbp-0x24]
  40073d:       83 e8 02                sub    eax,0x2
  400740:       89 c7                   mov    edi,eax
  400742:       e8 bf ff ff ff          call   400706 <calc>
  400747:       29 c3                   sub    ebx,eax
  400749:       8b 45 dc                mov    eax,DWORD PTR [rbp-0x24]
  40074c:       83 e8 03                sub    eax,0x3
  40074f:       89 c7                   mov    edi,eax
  400751:       e8 b0 ff ff ff          call   400706 <calc>
  400756:       41 89 c4                mov    r12d,eax
  400759:       8b 45 dc                mov    eax,DWORD PTR [rbp-0x24]
  40075c:       83 e8 04                sub    eax,0x4
  40075f:       89 c7                   mov    edi,eax
  400761:       e8 a0 ff ff ff          call   400706 <calc>
  400766:       41 29 c4                sub    r12d,eax
  400769:       44 89 e0                mov    eax,r12d
  40076c:       01 c3                   add    ebx,eax
  40076e:       8b 45 dc                mov    eax,DWORD PTR [rbp-0x24]
  400771:       83 e8 05                sub    eax,0x5
  400774:       89 c7                   mov    edi,eax
  400776:       e8 8b ff ff ff          call   400706 <calc>
  40077b:       69 c0 34 12 00 00       imul   eax,eax,0x1234
  400781:       01 d8                   add    eax,ebx
  400783:       89 45 ec                mov    DWORD PTR [rbp-0x14],eax
  400786:       8b 45 ec                mov    eax,DWORD PTR [rbp-0x14]
  400789:       48 83 c4 20             add    rsp,0x20
  40078d:       5b                      pop    rbx
  40078e:       41 5c                   pop    r12
  400790:       5d                      pop    rbp
  400791:       c3                      ret
```

Essentially, `main` calls `get_key()`, which calls `calculate_key()`, which calls `calc(0x19965)`. Looking at `calc`, it is essentially the same as
```python3
def calc(n):
    if n > 4:
        return calc(n - 1) - calc(n - 2) + calc(n - 3) - calc(n - 4) + calc(n - 5) * 0x1234
    return n * n + 0x2345
```
To speed up this calculation, we can convert the recursion into a loop. Also, `calc` returns a 32-bit integer (eax), so we have to remember to wrap values accordingly.
```python3
def calc(n):
    r = [i * i + 0x2345 for i in range(5)]
    for i in range(n):
        r = *r[1:], (r[4] - r[3] + r[2] - r[1] + r[0] * 0x1234) % (1 << 32)
    return r[0]
```

Calling `calc(0x19965)` yields `2653079950`. Now in `gdb`, we `ha SIGALRM i` as before, but we also `b calc` and `r`. When we hit the breakpoint, we can type `return (int)2653079950`, type `y` to confirm, and then `c` to continue. The flag is then printed.
