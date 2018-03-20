# CTF

frozenkp's CTF Writeups & useful tools

## Writeups

| Year  | CTF               | Challenge                 | Category    | Keyword                           |
| ----- | ----------------- | ------------------------- | ----------- | --------------------------------- |
| 2014  | NoConName qual    | inBINcible                | reverse     | Golang, xor                       |
| 2015  | B-sides vancouver | delphi                    | reverse     | Golang, cmd injection             |
| 2017  | HITB CTF          | 2017, Dating in Singapore | misc        |                                   |
| 2017  | HITB CTF          | Flying High               | misc        | UBIfs                             |
| 2017  | HITB CTF          | Pasty                     | web         | Jwt                               |
| 2017  | Seccon CTF        | Qubic Rube                | programming | QRcode                            |
| 2017  | Seccon CTF        | putchar music             | programming |                                   |
| 2018  | BambooFox CTF     | infant-gogogo             | pwn         | Golang, buffer overflow           |
| 2018  | BambooFox CTF     | infant-gotoheaven         | pwn         | Golang, buffer overflow           |
| 2018  | BambooFox CTF     | water-impossible          | pwn         | buffer overflow                   |
| Other | pwnable.tw        | Start                     | pwn         | Buffer overflow, stack executable |
| Other | pwnable.tw        | hacknote                  | pwn         | Heap use after free               |
| Other | pwnable.tw        | dubblesort                | pwn         | Buffer overflow                   |

## Usefule Tools

### Dockerfile

Pwn environment in docker, inclusive of peda, pwngdb, one_gadget, readelf….

```bash
$ docker pull frozenkp/pwn
$ docker run -it {--name pwn_env} {-v /??/data:/root/data} --cap-add=SYS_PTRACE --security-opt seccomp=unconfined frozenkp/pwn /bin/bash
$ docker exec -it pwn_env /bin/bash
```

