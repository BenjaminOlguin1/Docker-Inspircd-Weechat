from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())
    
    if scapy_packet.haslayer(Raw):
        try:
            payload = scapy_packet[Raw].load.decode('utf-8')
            modified = False
            
            #Mod1: Cambiar delimitador (':' por 'x')
            if "PRIVMSG" in payload and ":" in payload:
                payload = payload.replace(":", "x", 1)
                modified = True
                
            #Mod2: Cambiar Comando ('PING' por 'GNIP')
            elif "PING" in payload:
                payload = payload.replace("PING", "GNIP")
                modified = True
                
            #Mod3: Cambiar respuesta numérica (353 a 401
            elif " 353 " in payload:
                payload = payload.replace(" 353 ", " 401 ")
                modified = True

            if modified:
                scapy_packet[Raw].load = payload.encode('utf-8')
                del scapy_packet[IP].len
                del scapy_packet[IP].chksum
                del scapy_packet[TCP].chksum
                packet.set_payload(bytes(scapy_packet))
                print(f"[+] Paquete modificado: {payload.strip()}")
                
        except UnicodeDecodeError:
            pass
            
    packet.accept()

print("Escuchando tráfico IRC en la cola 1...")
nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)
try:
    nfqueue.run()
except KeyboardInterrupt:
    nfqueue.unbind()
    print("Detenido.")