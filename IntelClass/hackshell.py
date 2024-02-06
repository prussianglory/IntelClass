from colorama import init, Fore
import sys
import random
import time
init(autoreset=True)

class Packet:
    def __init__(self, id, source, destination, proto, length, raw_info, info):
        self.id = id
        self.source = source
        self.destination = destination
        self.proto = proto
        self.length = length
        self.raw_info = raw_info
        self.info = info        


class HackerShell:
    def __init__(self):
        self.prompt = "hacker@host"
    
    def work(self):
        while True:
            print(Fore.RED + f"{self.prompt}>", end="")
            command = input()
            if command == "exit":
                sys.exit()
            elif command == "worm":
                print("Запуск атаки червя...")
            elif command == "ddos":
                print("Запуск DDoS атаки...")
                time.sleep(2)
                id=0
                self.packets = [
            Packet(id, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+1, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+2, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+3, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+4, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+5, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+6, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),     
            Packet(id+7, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+8, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+9, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+10, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+11, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+12, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),                                                                                                                                                                                       
            Packet(id+13, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+14, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+15, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+16, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+17, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),     
            Packet(id+18, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+19, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+20, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+21, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+22, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),                                                                                                                                                                                       
            Packet(id+23, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+24, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+25, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+26, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+27, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),     
            Packet(id+28, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+29, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+30, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+31, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+32, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),                                                                                                                                                                                       
            Packet(id+33, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+34, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+35, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+36, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+37, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),     
            Packet(id+38, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+39, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+40, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+41, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+42, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),                                                                                                                                                                                       
        
                ]
                for packet in self.packets:
                    print(f"{packet.raw_info}: {packet.source} -> {packet.destination} | {packet.length} байт")
                    time.sleep(random.uniform(0.03, 0.2))
            else:
                print(f"Команда {command} не найдена")

def main():
    hsh = HackerShell()
    hsh.work()

if __name__ == "__main__":
    main()