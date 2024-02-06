import flet as ft
import time
import pyshark
from packet_page import Packet, PacketRow
import pandas as pd
import random
from datetime import datetime, timedelta
from keras.models import model_from_json


class AdminInfo:
    def __init__(self, id, log_class, ts, success):
        self.id = id
        self.log_class = log_class
        self.ts = ts
        self.success = success

class AttackInfo:
    def __init__(self, id:int, attack_type:str, attack_time:str, threat_level:str, source:str, packets:list=[]):
        self.id = id
        self.attack_type = attack_type
        self.timestamp = attack_time
        self.threat_level = threat_level        
        self.source = source
        if packets == []:
            self.packets = self.generate_packets()
        else:
            self.packets = packets
    
    def generate_packets(self):
        packets = []
        for packet_id in range(1, random.randint(5, 10)):
            packet_time = datetime.strptime(self.timestamp, "%d.%m.%Y %H:%M:%S") + timedelta(seconds=random.randint(1, 60))
            packet = Packet(
                id=packet_id,
                time=packet_time.strftime("%d.%m.%Y %H:%M:%S"),
                source=self.source,
                destination=f"192.168.{random.randint(1, 10)}.{random.randint(1, 255)}",
                proto=random.choice(["TCP", "UDP"]),
                length=random.randint(64, 1500),
                raw_info=f"{random.choice(['TCP Connection Established', 'UDP Flood to port 80'])}",
                info=[{"header": f"Header {i}", "info": f"Info {i}"} for i in range(1, random.randint(2, 5))]
            )
            packets.append(packet)
        return packets   


class Attack:
    def __init__(self, master, id, attack_type, attack_time, source, threat_level, packet_group):
        self.master = master
        self.id = id
        self.attack_type = attack_type
        self.attack_time = attack_time
        self.source = source
        self.threat_level = threat_level
        self.packet_group = packet_group
        self.packets = []

    def get_packet(self, new_packet):
        return ft.Container(
            expand=True,      
            padding=0,                           
            #bgcolor=colors.GREY_400,
            border=ft.border.all(0.5, ft.colors.BLACK),
            alignment=ft.alignment.center,      
            content=PacketRow(new_packet, self.master.master)      
        ) 
    
    def attack(self):
        pass
class Notification(ft.UserControl):
    def __init__(self, attack: Attack):
        self.attack = attack
        self.have_seen = False
        self.report_btn = ft.Container(
            height=150,
            border_radius=10,
            expand=1,
            bgcolor=ft.colors.RED_400,            
            on_hover=self.btn_on_hover,
            content=ft.Text("Сформировать отчёт об атаке")
            )
        self.threat_color = ft.colors.RED_600
        #if self.attack.threat_level == "Высокий":
        #    self.threat_color = self.threat_color = ft.colors.RED_600
        #elif self.attack.threat_level == "Средний":
        #    self.threat_color = self.threat_color = ft.colors.YELLOW_600
        super().__init__()

    def form_report(self):
        pass

    def btn_on_hover(self, e):
        cur_color = e.control.bgcolor
        hover_color = None
        if cur_color == ft.colors.GREY_400 or cur_color == ft.colors.GREY_200:
            cur_color = ft.colors.GREY_400
            hover_color = ft.colors.GREY_200        
        if cur_color == ft.colors.GREEN_400 or cur_color == ft.colors.GREEN_200:
            cur_color = ft.colors.GREEN_400
            hover_color = ft.colors.GREEN_200
        if cur_color == ft.colors.RED_400 or cur_color == ft.colors.RED_200:
            cur_color = ft.colors.RED_400
            hover_color = ft.colors.RED_200
        e.control.bgcolor = hover_color if e.data == "true" else cur_color
        e.control.update()

    def build(self):
        return ft.Row(
            controls=[
                ft.Container(
                    #bgcolor=ft.colors.RED_600,
                    border=ft.border.all(5, self.threat_color),
                    expand=True,
                    height=170,
                    margin=10,
                    border_radius=20,
                    content=ft.Row(
                        spacing=0,
                        controls=[
                            ft.Container(
                                #bgcolor=ft.colors.RED_600,
                                #border=ft.border.all(0.5, ft.colors.RED_600),
                                expand=2,
                                content=ft.Icon(name=ft.icons.WARNING_OUTLINED, color=self.threat_color, size=85)                    
                            ),
                            ft.Container(
                                #bgcolor=ft.colors.RED_600,                                
                                padding=10,
                                #border=ft.border.all(0.5, ft.colors.RED_600),
                                expand=3,
                                content=ft.Row(
                                    alignment=ft.alignment.center,
                                    controls=[
                                        ft.Text(f"{self.attack.attack_type}", size=20, weight="bold",text_align="center"),                                        
                                    ]
                                )                 
                            ),
                            ft.Container(
                                #bgcolor=ft.colors.RED_600,                                
                                padding=10,
                                border=ft.border.all(0.5, ft.colors.RED_600),
                                expand=3,
                                content=ft.Column(
                                    alignment=ft.alignment.center,
                                    controls=[                                        
                                        ft.Text(f"Время атаки: {self.attack.attack_time}", size=17),                                        
                                        ft.Text(f"Источник: {self.attack.source}", size=17),
                                        #ft.Text(f"Уровень угрозы: {self.attack.threat_level}", size=17),
                                        ft.Text(f"Пакеты: {self.attack.packet_group}", size=17),
                                    ]
                                )                 
                            ),
                            ft.Container(                                
                                expand=2,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.IconButton(icon=ft.icons.BALLOT, icon_color="green", icon_size = 50, tooltip= "Сформировать отчёт"),
                                        ft.IconButton(icon=ft.icons.DELETE_FOREVER, icon_color="red", icon_size = 50, tooltip="Удалить уведомление"),
                                    ]
                                )                    
                            ),
                        ]
                    )
                )
            ]
        )


class Worm(Attack):
    def __init__(self, master, id, attack_type, attack_time, source, threat_level):
        super().__init__(master, id, attack_type, attack_time, source, threat_level)
        self.__threat_color = ft.colors.YELLOW_400
        self.packets = [
            Packet(id, self.master.last_time, "192.168.0.10", "192.168.0.1", "ARP", 42, "ARP запрос: У кого есть 192.168.0.1? Скажите 192.168.0.10", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+1, self.master.last_time, "192.168.0.1", "192.168.0.10", "ARP", 42, "ARP Ответ: 192.168.0.1 у 00:1a:2b:3c:4d:5e", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+2, self.master.last_time, "192.168.0.10", "192.168.0.1", "TCP", 60, "TCP SYN в порт 445", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+3, self.master.last_time, "192.168.0.1", "192.168.0.10", "TCP", 60, "TCP SYN/ACK из порта 445", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+4, self.master.last_time, "192.168.0.10", "192.168.0.1", "TCP", 52, "TCP ACK в порт 445", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+5, self.master.last_time, "192.168.0.10", "192.168.0.1", "UDP", 48, "UDP в порт 53", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+6, self.master.last_time, "192.168.0.1", "192.168.0.10", "UDP", 48, "UDP из порта 53", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+7, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо Запрос на 192.168.0.1", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+8, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо Ответ от 192.168.0.1", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+9, self.master.last_time, "192.168.0.10", "192.168.0.1", "TCP", 60, "TCP SYN в порт 22", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+10, self.master.last_time, "192.168.0.1", "192.168.0.10", "TCP", 60, "TCP SYN/ACK из порта 22", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+11, self.master.last_time, "192.168.0.10", "192.168.0.1", "TCP", 52, "TCP ACK в порт 22", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+12, self.master.last_time, "192.168.0.10", "192.168.0.1", "UDP", 60, "UDP в порт 123", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+13, self.master.last_time, "192.168.0.1", "192.168.0.10", "UDP", 60, "UDP из порта 123", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+14, self.master.last_time, "192.168.0.10", "192.168.0.1", "TCP", 60, "TCP SYN в порт 80", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+15, self.master.last_time, "192.168.0.1", "192.168.0.10", "TCP", 60, "TCP SYN/ACK из порта 80", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+16, self.master.last_time, "192.168.0.10", "192.168.0.1", "TCP", 52, "TCP ACK в порт 80", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+17, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо Запрос на 192.168.0.1", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
            Packet(id+18, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо Ответ из 192.168.0.1", 
                                                        [{"header":"", "info":""},{"header":"", "info":""}, {"header":"", "info":""}]),
        ]       
    def attack(self):
        print('Worm!')
        for pkt in self.packets:
            pkt.threat_color = self.__threat_color
            self.master.master.packet_page.content.packet_list_row.controls[0].content.controls.append(self.get_packet(pkt))
        self.master.bias+= len(self.packets)
        self.master.master.packet_page.content.packet_list_row.update()
class DoS(Attack):
    def __init__(self, master, id, attack_type, attack_time, source, threat_level, packet_group):
        self.__threat_color = ft.colors.RED_400
        super().__init__(master, id, attack_type, attack_time, source, threat_level, packet_group)
        self.packets = [
            [Packet(id, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id, True, 1)),
            Packet(id+1, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+1, False, 1)),
            Packet(id+2, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+2, True, 2)),
            Packet(id+3, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+3, False, 2)),
            Packet(id+4, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+4, True, 1)),
            Packet(id+5, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+5, False, 1)),
            Packet(id+6, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+6, True, 2)),     
            Packet(id+7, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+7, False, 2)),
            Packet(id+8, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+8, True, 1)),
            Packet(id+9, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+9, False,1 ))],
            [Packet(id+10, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+10, True, 2)),
            Packet(id+11, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+11, False, 2)),
            Packet(id+12, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+12, True, 2)),                                                                                                                                                                                       
            Packet(id+13, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+13, False, 2)),
            Packet(id+14, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+14, True,1)),
            Packet(id+15, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+15, False,1)),
            Packet(id+16, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+16, True, 2)),
            Packet(id+17, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+17, False, 2)),     
            Packet(id+18, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+18, True, 1)),
            Packet(id+19, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+19, True, 1)),
            Packet(id+20, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+20, False, 2))],
            [Packet(id+21, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+21, True, 2)),
            Packet(id+22, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+22, False, 2)),                                                                                                                                                                                       
            Packet(id+23, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+23, True, 2)),
            Packet(id+24, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+24, False, 2)),
            Packet(id+25, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+25, True, 1)),
            Packet(id+26, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+26, False, 1)),
            Packet(id+27, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+27, True, 2)),     
            Packet(id+28, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+28, False, 2)),
            Packet(id+29, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+29, True, 2)),
            Packet(id+30, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+30, False, 2))],
            [Packet(id+31, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+31, True, 2)),
            Packet(id+32, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+32, False, 2)),                                                                                                                                                                                       
            Packet(id+33, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+33, True, 1)),
            Packet(id+34, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+34, False, 1)),
            Packet(id+35, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+35, True, 1)),
            Packet(id+36, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+36, False, 1)),
            Packet(id+37, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+37, True, 2))],     
            [Packet(id+38, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+38, False, 2)),
            Packet(id+39, self.master.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+39, True, 1)),
            Packet(id+40, self.master.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+40, False, 1)),
            Packet(id+41, self.master.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        self.get_request_info(id+41, True, 2)),
            Packet(id+42, self.master.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        self.get_request_info(id+42, False, 2))],                                                                                                                                                                                       
        
        ]

    def get_request_info(self, id, request:bool, ip:int):
        frame_layer = {}
        frame_layer['header'] = f"КАДР {id}"
        frame_len_info = f"ДЛИНА КАДРА: 74 байт ({74*8} бит)"
        iface_id_info = f"ID ИНТЕРФЕЙСА: 0 (\\Device\\NPF_Loopback)"
        time_info = f"ВРЕМЯ ЗАХВАТА: {self.master.last_time}"
        time_delta_info = f"ВРЕМЕННАЯ РАЗНИЦА С ПРЕДЫДУЩИМ КАДРОМ: {random.uniform(0.005, 0.03)}"
        time_relative_info = f"ВРЕМЯ ОТ НАЧАЛА ЗАХВАТА: {self.master.last_time}"
        proto_info = f"ПРОТОКОЛЫ: null:ipv6:icmpv6:data"
        # сбор информации 
        frame_layer['info'] = f"{frame_len_info}\n{iface_id_info}\n{time_info}\n{time_delta_info}\n"+\
                                                                                f"{time_relative_info}\n{proto_info}"
        ####################################
        # ИНФОРМАЦИЯ СЛОЯ ETHERNET
        ####################################
        ether_layer = {}
        ether_layer['header'] = 'ICMP СЛОЙ'
        if request:
            ether_layer['info'] = f"РАЗМЕР ДАННЫХ: 40\nСЛЕДУЮЩИЙ ЗАГОЛОВОК: IPV6 (58)\nЛИМИТ ПЕРЕХОДОВ: 128\nIPV6-АДРЕС ИСТОЧНИКА: 192.168.0.{ip}\nIPV6-АДРЕС НАЗНАЧЕНИЯ: 192.168.0.10"
        else:
            ether_layer['info'] = f"РАЗМЕР ДАННЫХ: 40\nСЛЕДУЮЩИЙ ЗАГОЛОВОК: IPV6 (58)\nЛИМИТ ПЕРЕХОДОВ: 128\nIPV6-АДРЕС ИСТОЧНИКА: 192.168.0.10\nIPV6-АДРЕС НАЗНАЧЕНИЯ: 192.168.0.{ip}"
        return [frame_layer, ether_layer]
    def attack(self):
        print('DoS!')
        time.sleep(random.uniform(1.5, 3))
        for pkt_group in self.packets:
            for pkt in pkt_group:
                pkt.threat_color = self.__threat_color
                self.master.master.packet_page.content.packet_list_row.controls[0].content.controls.append(self.get_packet(pkt))
            self.master.master.side_bar_column.content.controls[0].content.controls[3].content.controls[0].icon_color="red"
            self.master.master.side_bar_column.content.controls[0].content.controls[3].content.controls[0].update()
            self.master.master.side_bar_column.content.update_controls()
            self.master.master.packet_page.content.packet_list_row.controls[0].content.scroll_to(offset=-1)
            self.master.master.packet_page.content.packet_list_row.controls[0].content.update()
            time.sleep(random.uniform(1.5, 2.5))
            self.master.master.packet_page.content.packet_list_row.update()
        self.master.bias += len(self.packets)
        

class Flow:
    def __init__(self, src, dst, proto, flags=[]):
        self.src = src
        self.dst = dst
        self.proto = proto
        self.flags = flags        
        self.packets = []
        self.attack = False

class MyCheckBox(ft.UserControl):
    def __init__(self, master, id:int):
        self.master = master
        self.id = id        
        self.cb = ft.Checkbox(value=True, on_change=self.on_change)
        super().__init__()

    def on_change(self, e):
        if self.cb.value:            
            self.master.enabled_log_list.append(self.id)
            if len(self.master.enabled_log_list) == (len(self.master.attack_logs_data)):
                self.master.data_header.controls[0].content.value = True
                self.master.data_header.controls[0].content.update()
        else:
            self.master.data_header.controls[0].content.value = False
            self.master.data_header.controls[0].content.update()
            self.master.enabled_log_list.remove(self.id)
        print(self.master.enabled_log_list)

    def update_view(self):
        self.cb.update()

    def build(self):
        return self.cb

class PacketAnalyzer:
    def __init__(self, pcap, master):
        self.master = master
        self.packets=[]
        self.not_classified = []
        self.flows = {}                
        #with open("model_architecture.json", "r") as json_file:
        #    loaded_model_json = json_file.read()
        #    self.nnclf = model_from_json(loaded_model_json)
        #    self.nnclf.load_weights("model_weights.h5")
        self.t = time.time()
        self.capture = pcap
        self.attack_stats = {"DoS":1, "DDoS":4, "Сетевые черви":1, "Эксплойт":1, "Сканирование портов":1, "Shell-код":1, "Бэкдор":1}
        self.threat_stats = {"Высокий": 606, "Средний":345, "Низкий":148}
        self.recent_attacks = 0
        self.last_id = 0
        self.last_time = 0.0
        self.bias = 0
        self.time_bias = 0
        self.commands_dict = {
          "worm": self.init_worm_attack,
          "ddos": self.init_dos_attack,
          "Key.f1": self.do_nothing
        }
        """
        self.intrusion_counts = [
            (0, 273.60),
            (1, 279.00),
            (2, 348.20),
            (3, 363.70),
            (4, 438.40),
            (5, 518.90),
            (6, 638.00),
            (7, 833.75),
            (8, 874.75),
            (9, 1096.50),
            (10, 1226.75),
            (11, 1577.00),
            (12, 1668.75),
            (13, 1200.00),
            (14, 1184.75),
            (15, 1061.25),
            (16, 1151.00),
            (17, 1257.25),
            (18, 1301.50),
            (19, 1493.25),
            (20, 1906.25),
            (21, 1753.90),
            (22, 1980.40),
        ]
        """
        self.intrusion_counts = [(0,0)]
        self.attack_logs = [
            AttackInfo(1, "DoS", "17.12.2023 10:20:19", 2, "192.168.0.1", []),
            AttackInfo(2, "DDoS", "17.12.2023 10:22:16", 2, "192.168.0.1\n192.168.0.2", []),
            AttackInfo(3, "DDoS", "17.12.2023 16:32:28", 2, "192.168.0.1\n192.168.0.2", []),
            AttackInfo(4, "Shell-код", "17.12.2023 15:14:45", 1, "192.168.124.34", []),
            AttackInfo(5, "DDoS", "18.12.2023 14:16:18", 2, "192.168.0.1\n192.168.0.2", []),
            AttackInfo(6, "DDoS", "19.12.2023 11:20:21", 2, "192.168.0.1\n192.168.0.2", []),
            AttackInfo(7, "Червь", "19.12.2023 11:56:01", 1, "192.168.5.3", []),
            AttackInfo(8, "Эксплойт", "19.12.2023 19:02:01", 2, "192.168.6.4", []),
            AttackInfo(9, "Сканирование портов", "20.12.2023 09:20:16", 3, "192.168.7.3", []),
            AttackInfo(10, "Бэкдор", "20.12.2023 14:05:10", 1, "192.168.2.10", []),
        ]
        self.admin_logs = [
            AdminInfo(0, 'Вход в систему', '27.12.2023 09:35:47', 'Успешно'),
            AdminInfo(1, 'Формирование отчёта событий сети', '27.12.2023 09:38:09', 'Успешно'),
            AdminInfo(2, 'Формирование отчёта событий системы', '27.12.2023 09:38:56', 'Успешно'),
            AdminInfo(3, 'Выход из системы', '27.12.2023 09:40:23', 'Успешно'),
            AdminInfo(4, 'Вход в систему', '28.12.2023 11:14:35', 'Неуспешно'),
            AdminInfo(5, 'Вход в систему', '28.12.2023 11:14:49', 'Неуспешно'),
            AdminInfo(6, 'Вход в систему', '28.12.2023 11:15:28', 'Успешно'),
            AdminInfo(7, 'Выход из системы', '27.12.2023 09:40:23', 'Успешно'),
            AdminInfo(8, 'Вход в систему', '27.12.2023 09:35:47', 'Успешно'),
            AdminInfo(9, 'Формирование отчёта событий сети', '27.12.2023 09:38:09', 'Успешно'),
            AdminInfo(10, 'Формирование отчёта событий системы', '27.12.2023 09:38:56', 'Успешно'),
            AdminInfo(11, 'Выход из системы', '27.12.2023 09:40:23', 'Успешно'),
            AdminInfo(12, 'Вход в систему', '25.01.2024 22:06:34', 'Успешно'),
        ]
        self.layer3func = {
            'arp':self.__get_arp_info,
            'ip':self.__get_ip_info,
            'ipv6':self.__get_ipv6_info
        }
        self.layer4func = {
            'tcp':self.__get_tcp_info,
            'udp':self.__get_udp_info,
            'icmpv6':self.__get_icmpv6_info,
            'igmp':self.__get_igmp4_info,
            'ipv6.hopopts':self.__get_ipv6hopopts_info
        }
        self.layer5func = {
            'ssdp':self.__get_ssdp_info,
            'tls':self.__get_tls_info,
            'ssl':self.__get_ssl_info,
            'quic':self.__get_quic_info,
            'dns':self.__get_dns_info,
            'data':self.__get_data_info,
            'http':self.__get_http_info,
            'igmp':self.__get_igmp5_info,
            'icmpv6':self.__get_icmpv6l5_info
        }
        self.ethertype_dict = {
            '0x0800': 'IPv4',
            '0x0806': 'ARP',
            '0x0842': 'Wake-on-LAN',
            '0x22f0': 'Audio Video Transport Protocol',
            '0x6003': 'DECnet Phase IV, DNA Routing',
            '0x8035': 'Reverse Address Resolution Protocol (RARP)',
            '0x809b': 'EtherTalk',
            '0x80f3': 'AppleTalk Address Resolution Protocol (AARP)',
            '0x8100': 'VLAN-tagged (IEEE 802.1Q) frame',
            '0x8137': 'IPX',
            '0x8138': 'IPX',
            '0x86dd': 'IPv6',
            '0x876b': 'EtherNet/IP',
            '0x8847': 'MPLS unicast',
            '0x8848': 'MPLS multicast',
            '0x8863': 'PPPoE Discovery Stage',
            '0x8864': 'PPPoE Session Stage',
            '0x888e': 'EAP over LAN (802.1X)',
            '0x88a2': 'ATA over Ethernet (AoE)',
            '0x88a4': 'EtherCAT Protocol',
            '0x88b5': 'IEEE 802.1AE (MACsec)',
            '0x88b8': 'Ethernet Powerlink Standard',
            '0x88cc': 'Link Layer Discovery Protocol (LLDP)',
            '0x88cd': 'SERCOS III',
            '0x88e1': 'HomePlug AV MME',
            '0x88e3': 'Media Redundancy Protocol (MRP)',
            '0x88e5': 'MAC Layer Security Protocol (IEEE 802.1AE)',
            '0x88f7': 'Precision Time Protocol (PTP) over Ethernet (IEEE 1588)',
            '0x88f8': 'NC-SI',
            '0x88fb': 'Parallel Redundancy Protocol (PRP)',
            '0x8902': 'PROFINET Protocol',
            '0x8906': 'Fibre Channel over Ethernet (FCoE)',
            '0x8914': 'FCoE Initialization Protocol',
            '0x8915': 'RDMA over Converged Ethernet (RoCE)',
            '0x8922': 'High-Performance Parallel Interface (HiPPI)',
            '0x892f': 'High-Speed Transparent LAN Service (IEEE 802.10)',
            '0x9000': 'Ethernet Configuration Testing Protocol',
            '0x9100': 'VLAN-tagged (IEEE 802.1Q) frame',
            '0x9200': 'VLAN-tagged (IEEE 802.1Q) frame',
            '0xffff': 'Experimental'    
        }
        self.hardware_type_dict = {
            '1': 'Ethernet',
            '6': 'IEEE 802 Networks',
            '15': 'Frame Relay',
            '16': 'Asynchronous Transfer Mode (ATM)',
            '17': 'HDLC',
            '18': 'Fibre Channel',
            '19': 'Asynchronous Transfer Mode (ATM)',
            '20': 'Serial Line'
        }  
        self.arp_opcode_dict = {
            '1': 'ARP запрос',
            '2': 'ARP ответ',
            '3': 'RARP запрос',
            '4': 'RARP ответ'
        }
        self.transport_protocol_dict = {
            '0': 'HOPOPT',         # IPv6 Hop-by-Hop Option
            '1': 'ICMP',           # Internet Control Message Protocol
            "2": 'IGMP',           # Internet Group Management Protocol
            '3': 'GGP',            # Gateway-to-Gateway Protocol
            '4': 'IPv4',           # IPv4 encapsulation
            '5': 'ST',             # Stream Protocol
            '6': 'TCP',            # Transmission Control Protocol
            '7': 'CBT',            # CBT
            '8': 'EGP',            # Exterior Gateway Protocol
            '9': 'IGP',            # любой частный внешний шлюз (используется Cisco для их IGRP)
            '10': 'BBN-RCC-MON',    # BBN RCC Monitoring
            '11': 'NVP-II',         # Network Voice Protocol
            '12': 'PUP',            # Xerox PUP
            '13': 'ARGUS',          # ARGUS
            '14': 'EMCON',          # EMCON
            '15': 'XNET',           # Cross Net Debugger
            '16': 'CHAOS',          # Chaos
            '17': 'UDP',            # User Datagram Protocol
            '18': 'MUX',            # Multiplexing Protocol
            '19': 'DCN-MEAS',       # DCN Measurement Subsystems
            '20': 'HMP',            # Host Monitoring Protocol    
        }
        self.tcp_flags_dict = {
    '0x0000': '[No flags]',
    '0x0001': '[FIN]',
    '0x0002': '[ACK]',
    '0x0003': '[FIN,ACK]',
    '0x0010': '[SYN]',
    '0x0011': '[SYN,FIN]',
    '0x0012': '[SYN,ACK]',
    '0x0013': '[SYN,FIN,ACK]',
    '0x0014': '[RST]',
    '0x0018': '[PSH,ACK]',
    '0x0019': '[PSH,FIN,ACK]',
    '0x0100': '[RST]',
    '0x0101': '[RST,FIN]',
    '0x0102': '[RST,ACK]',
    '0x0103': '[RST,FIN,ACK]',
    '0x1000': '[PSH]',
    '0x1001': '[PSH,FIN]',
    '0x1002': '[PSH,ACK]',
    '0x1003': '[PSH,FIN,ACK]',
    '0x1100': '[PSH,RST]',
    '0x1101': '[PSH,RST,FIN]',
    '0x1102': '[PSH,RST,ACK]',
    '0x1103': '[PSH,RST,FIN,ACK]'
}   
    def __get_packet(self):
        id = len(self.packets)
        time = str(float(self.capture[id].frame_info.time_relative) + self.time_bias)+'000'
        l2_proto = self.capture[id].frame_info.protocols.split(':')[2]
        if  l2_proto == "ip":      
            source = self.capture[id][l2_proto].src
            destination = self.capture[id]['ip'].dst            
            length = self.capture[id]['ip'].len            
        elif l2_proto == 'ipv6':
            source = self.capture[id]['ipv6'].src
            destination = self.capture[id]['ipv6'].dst            
            length = "-"
        elif l2_proto == 'arp':
            source = self.capture[id][l2_proto].src_proto_ipv4
            destination = self.capture[id][l2_proto].dst_proto_ipv4            
            length = "-"
        proto = self.capture[id].highest_layer
        #raw_info = f"INFO ID {id+self.bias}"
        raw_info = self.__get_raw_info(id)
        info = self.get_packet_info(id)      
        new_packet = Packet(id+self.bias, time, source, destination, proto, length, raw_info, info)
        self.last_id = id+self.bias
        self.last_time = time
        self.packets.append(new_packet)
        self.not_classified.append(new_packet)      
        return new_packet

    def __get_raw_info(self, id):
        raw_info = "Информация о пакете"
        proto = self.capture[id].highest_layer
        if proto == 'TLS':
            raw_info = "Данные приложения"
        elif 'tcp' in self.capture[id].frame_info.protocols.split(':'):
            raw_info = f"{self.capture[id]['tcp'].srcport} -> {self.capture[id]['tcp'].dstport} {self.tcp_flags_dict[self.capture[id]['tcp'].flags]}"
        elif 'udp' in self.capture[id].frame_info.protocols.split(':'):
            raw_info = f"{self.capture[id]['udp'].srcport} -> {self.capture[id]['udp'].dstport}"
        return raw_info

    def do_nothing(self):
        pass

    def __update_groups(self):        
        #print([x.id for x in self.not_classified])        
        for i in range(len(self.not_classified)):            
            src = self.not_classified[i].source
            dst = self.not_classified[i].destination
            proto = self.not_classified[i].proto
            # нужно вытащить флаги и порты из tcp/upd пакетов
            srcport = ""
            dstport = ""
            flags = []
            flow_key = f"{src}:{srcport}->{dst}:{dstport}({proto}|{flags})"            
            if flow_key not in self.flows.keys():
                self.flows[flow_key] = Flow(src, dst, proto, flags) 
            self.flows[flow_key].packets.append(self.not_classified[i])
        self.not_classified.clear()
        for key in self.flows.keys():
            self.__classify_group(self.flows[key])

    def __classify_group(self, flow):           
        ######################################        
        for pkt in flow.packets:
            cur_proto_list = self.capture[pkt.id].frame_info.protocols.split(':')
            #prediction = self.nnclf.predict(cur_proto_list)
            #if prediction != 'benign':
            #   pkt.threat_color = ft.colors.GREEN_400
            #else:
            #   pkt.threat_color = ft.colors.RED_400
            if 'tcp' in cur_proto_list or 'udp' in cur_proto_list:                          
                pkt.threat_color = ft.colors.GREEN_400
        ######################################
        self.master.packet_page.content.packet_info.update()

    def get_packet_group(self):
        self.time = time.time()        
        packet_group = [self.__get_packet()]        
        while True:
            new_packet = self.__get_packet()
            if round(float(new_packet.time)) - round(float(packet_group[0].time)) < 1:
                packet_group.append(new_packet)                                
            else:
                time_to_sleep = round(round(float(packet_group[0].time))+self.t-self.time)   
                time.sleep(time_to_sleep if time_to_sleep >=0 else 0.5)
                self.packets.pop()
                self.not_classified.pop()             
                break
        self.__update_groups()
        return packet_group
    #########################################################################################################
    # 3-Й СЛОЙ
    def __get_arp_info(self, cur_frame):
        arp_info_header = "СЛОЙ ARP"
        opcode_info = f"ОПЕРАЦИЯ: {self.arp_opcode_dict[cur_frame['arp'].opcode]} ({cur_frame['arp'].opcode})"
        hw_type_info = f"ТИП ОБОРУДОВАНИЯ: {self.hardware_type_dict[cur_frame['arp'].hw_type]} ({cur_frame['arp'].hw_type})"
        src_ipv4_info = f"IPV4-АДРЕС ОТПРАВИТЕЛЯ: {cur_frame['arp'].src_proto_ipv4}"
        dst_ipv4_info = f"IPV4-АДРЕС ПОЛУЧАТЕЛЯ: {cur_frame['arp'].src_proto_ipv4}"
        arp_info_info = f"{opcode_info}\n{hw_type_info}\n{src_ipv4_info}\n{dst_ipv4_info}"
        
        return arp_info_header, arp_info_info

    def __get_ip_info(self, cur_frame):
        ip_info_header ="IP СЛОЙ"
        
        version_info = f"ВЕРСИЯ: {cur_frame['ip'].version}"
        hdr_len = f"ДЛИНА ЗАГОЛОВКА: {cur_frame['ip'].hdr_len}"
        total_len = f"ОБЩАЯ ДЛИНА: {cur_frame['ip'].len}"
        group_id = f"ID В ГРУППЕ: {cur_frame['ip'].id} ({int(cur_frame['ip'].id, 0)})"
        flags = f"ФЛАГИ: {cur_frame['ip'].flags}"
        flag_offset = f"СМЕЩЕНИЕ ФРАГМЕНТА: {cur_frame['ip'].frag_offset}"
        ttl_info = f"TTL: {cur_frame['ip'].ttl}"
        proto = f"ПРОТОКОЛ: {cur_frame['ip'].proto}"
        checksum = f"КОНТРОЛЬНАЯ СУММА ЗАГОЛОВКА: {cur_frame['ip'].checksum}"
        src = f"АДРЕС ИСТОЧНИКА: {cur_frame['ip'].src}"
        dst = f"АДРЕС НАЗНАЧЕНИЯ: {cur_frame['ip'].dst}"

        ip_info_info = f"{version_info}\n{hdr_len}\n{total_len}\n{group_id}\n{flags}\n{flag_offset}\n{ttl_info}\n{proto}"+\
            f"{checksum}\n{src}\n{dst}"

        return ip_info_header, ip_info_info

    def __get_ipv6_info(self, cur_frame):
        ipv6_info_header = "СЛОЙ IPV6"
        
        plen = f"РАЗМЕР ДАННЫХ: {cur_frame.ipv6.plen}"
        nxt = f"СЛЕДУЮЩИЙ ЗАГОЛОВОК: IPV6 ({cur_frame.ipv6.nxt})"
        hlim = f"ЛИМИТ ПЕРЕХОДОВ: {cur_frame.ipv6.hlim}"
        src = f"IPV6-АДРЕС ИСТОЧНИКА: {cur_frame.ipv6.src}"
        dst = f"IPV6-АДРЕС НАЗНАЧЕНИЯ: {cur_frame.ipv6.dst}"
        #src_slaac_mac = f"SLAAC MAC ИСТОЧНИКА: {cur_frame.ipv6.src_slaac_mac}"

        ipv6_info_info = f"{plen}\n{nxt}\n{hlim}\n{src}\n{dst}\n"
        return ipv6_info_header, ipv6_info_info
    ########################################################################################################
    # 4-Й СЛОЙ
    def __get_tcp_info(self, cur_frame):
        header = "СЛОЙ TCP"
        srcport = f"ПОРТ ИСТОЧНИКА: {cur_frame['tcp'].srcport}"
        dstport = f"ПОРТ НАЗНАЧЕНИЯ: {cur_frame['tcp'].dstport}"        
        checksum = f"КОНТРОЛЬНАЯ СУММА: {cur_frame['tcp'].checksum}"
        stream_id = f"ИНДЕКС ПОТОКА: {cur_frame['tcp'].stream}"
        #payload = f"ДАННЫЕ ПАКЕТА: \n{cur_frame['tcp'].payload}"

        info = f"{srcport}\n{dstport}\n{stream_id}\n{checksum}\n"
        return header, info  

    def __get_udp_info(self, cur_frame):
        header = "СЛОЙ UDP"
        srcport = f"ПОРТ ИСТОЧНИКА: {cur_frame['udp'].srcport}"
        dstport = f"ПОРТ НАЗНАЧЕНИЯ: {cur_frame['udp'].dstport}"
        length = f"ДЛИНА: {cur_frame['udp'].length}"
        checksum = f"КОНТРОЛЬНАЯ СУММА: {cur_frame['udp'].checksum}"
        stream_id = f"ИНДЕКС ПОТОКА: {cur_frame['udp'].stream}"
        payload = f"ДАННЫЕ ПАКЕТА: \n{cur_frame['udp'].payload}"

        info = f"{srcport}\n{dstport}\n{length}\n{stream_id}\n{checksum}\n{payload}"
        return header, info   

    def __get_icmpv6_info(self, cur_frame):
        header = "СЛОЙ ICMPv6"
        tclass = f"ТИП ТРАФИКА: {cur_frame['icmpv6'].type}"
        checksum = f"КОНТРОЛЬНАЯ СУММА: {cur_frame['icmpv6'].checksum}"
        checksum_status = f"СТАТУС КОНТРОЛЬНОЙ СУММЫ: {cur_frame['icmpv6'].checksum_status}"
        hop_limit = f"ТЕКУЩИЙ ПРЕДЕЛ ПЕРЕХОДОВ: {cur_frame['icmpv6'].nd_ra_cur_hop_limit}"
        flag = f"ФЛАГ: {cur_frame['icmpv6'].nd_ra_flag}"

        info = f"{tclass}\n{checksum}\n{checksum_status}\n{hop_limit}\n{flag}"

        return header, info
    
    def __get_igmp4_info(self, cur_frame):
        header = "СЛОЙ IGMP"
        version = f"ВЕРСИЯ: v{cur_frame.igmp.version}"
        ptype = f"ТИП: {cur_frame.igmp.type}"
        max_resp = f"МАКСИМАЛЬНОЕ ВРЕМЯ ОТВЕТА: {cur_frame.igmp.max_resp}"
        checksum = f"КОНТРОЛЬНАЯ СУММА: {cur_frame['igmp'].checksum}"
        checksum_status = f"СТАТУС КОНТРОЛЬНОЙ СУММЫ: {cur_frame['igmp'].checksum_status}"
        multicast_addr = f"ГРУППОВОЙ MAC-АДРЕСС: {cur_frame.igmp.maddr}"

        info = f"{version}\n{ptype}\n{max_resp}\n{checksum}\n{checksum_status}\n{multicast_addr}"
        
        return header, info

    def __get_ipv6hopopts_info(self, cur_frame):
        return "header", "info"
    ########################################################################################################
    # 5-Й СЛОЙ
    def __get_ssdp_info(self, cur_frame):
        return "header", "info"

    def __get_tls_info(self, cur_frame):
        return "header", "info"

    def __get_ssl_info(self, cur_frame):
        return "header", "info"

    def __get_quic_info(self, cur_frame):
        return "header", "info"

    def __get_dns_info(self, cur_frame):
        return "header", "info"
    
    def __get_data_info(self, cur_frame):
        return "header", "info"
    
    def __get_http_info(self, cur_frame):
        return "header", "info"
    
    def __get_igmp5_info(self, cur_frame):
        return "header", "info"
    
    def __get_icmpv6l5_info(self, cur_frame):
        return "header", "info"

##################################################################################################
# 6-й СЛОЙ
##################################################################################################


##################################################################################################   
    def get_packet_info(self, id) -> list:
        cur_frame = self.capture[id]
        layers = cur_frame.frame_info.protocols.split(':')
        packet_info = []
        for layer in layers:
            packet_info.append({})        
        ####################################
        # ИНФОРМАЦИЯ О КАДРЕ 
        ####################################
        packet_info[0]['header'] = f"КАДР {id}"
        frame_len_info = f"ДЛИНА КАДРА: {cur_frame.frame_info.cap_len} байт ({int(cur_frame.frame_info.cap_len)*8} бит)"
        iface_id_info = f"ID ИНТЕРФЕЙСА: {cur_frame.frame_info.interface_id} ({cur_frame.frame_info.interface_name})"
        time_info = f"ВРЕМЯ ЗАХВАТА: {cur_frame.frame_info.time}"
        time_epoch_info = f"ВРЕМЯ ЭПОХИ: {cur_frame.frame_info.time_epoch}"
        time_delta_info = f"ВРЕМЕННАЯ РАЗНИЦА С ПРЕДЫДУЩИМ КАДРОМ: {cur_frame.frame_info.time_delta}"
        time_relative_info = f"ВРЕМЯ ОТ НАЧАЛА ЗАХВАТА: {cur_frame.frame_info.time_relative}"
        proto_info = f"ПРОТОКОЛЫ: {cur_frame.frame_info.protocols}"
        # сбор информации 
        packet_info[0]['info'] = f"{frame_len_info}\n{iface_id_info}\n{time_info}\n{time_epoch_info}\n{time_delta_info}\n"+\
                                                                                f"{time_relative_info}\n{proto_info}"
        ####################################
        # ИНФОРМАЦИЯ СЛОЯ ETHERNET
        ####################################

        packet_info[1]['header'] = "СЛОЙ ETHERNET"
        mac_src_info = f"MAC-АДРЕС ИСТОЧНИКА: {cur_frame.eth.src}"
        mac_dst_info = f"MAC-АДРЕС НАЗНАЧЕНИЯ: {cur_frame.eth.dst}"
        eth_type_info = f"ТИП: {self.ethertype_dict[cur_frame.eth.type]} ({cur_frame.eth.type})"
        # сбор информации
        packet_info[1]['info'] = f"{mac_src_info}\n{mac_dst_info}\n{eth_type_info}"

        ####################################
        # ИНФОРМАЦИЯ 3-ГО СЛОЯ (ПРОТОКОЛ МОЖЕТ БЫТЬ РАЗНЫМ), 4-ГО И 5 СЛОЁВ (ЕСЛИ ЕСТЬ)
        ####################################
        packet_info[2]['header'], packet_info[2]['info'] = self.layer3func[layers[2]](cur_frame)
        if len(layers) >= 4:      
            packet_info[3]['header'], packet_info[3]['info'] = self.layer4func[layers[3]](cur_frame)
        if len(layers) >= 5:      
            packet_info[4]['header'], packet_info[4]['info'] = self.layer5func[layers[4]](cur_frame)
        
        return packet_info

    def init_worm_attack(self):
        worm = Worm(self, self.last_id, "Червь", "10.01.2012:01:45:34", "192.168.1.10", "Высокий")
        worm.attack()   

    def init_dos_attack(self):
        dos = DoS(self, self.last_id, "DDoS", "25.01.2024 22:08:12", "192.168.0.1, 192.168.0.2", "Высокий", f"[{self.last_id}-{self.last_id+42}]")
        self.master.notification_page.content.notification_list.controls.append(Notification(dos))
        self.master.notification_page.content.controls[0].controls[0].content.value = "У вас 1 новое уведомление"
        self.master.notification_page.content.controls[0].update()
        self.master.log_page.content.logs_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(MyCheckBox(self.master.log_page.content, 11)),
                        ft.DataCell(ft.Text(11)),
                        ft.DataCell(ft.Text("DDoS")),
                        ft.DataCell(ft.Text("25.01.2024 22:08:24")),
                        ft.DataCell(ft.Text("192.168.0.1\n192.168.0.2"))
                    ]
                )                
            )
        self.master.log_page.content.enabled_log_list.append(11)
        self.master.log_page.content.update()
        ddos_packets = [
            Packet(dos.id, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id, True, 1)),
            Packet(dos.id+1, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+1, False, 1)),
            Packet(dos.id+2, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+2, True, 2)),
            Packet(dos.id+3, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+3, False, 2)),
            Packet(dos.id+4, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+4, True, 1)),
            Packet(dos.id+5, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+5, False, 1)),
            Packet(dos.id+6, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+6, True, 2)),     
            Packet(dos.id+7, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+7, False, 2)),
            Packet(dos.id+8, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+8, True, 1)),
            Packet(dos.id+9, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+9, False,1 )),
            Packet(dos.id+10, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+10, True, 2)),
            Packet(dos.id+11, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+11, False, 2)),
            Packet(dos.id+12, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+12, True, 2)),                                                                                                                                                                                       
            Packet(dos.id+13, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+13, False, 2)),
            Packet(dos.id+14, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+14, True,1)),
            Packet(dos.id+15, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+15, False,1)),
            Packet(dos.id+16, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+16, True, 2)),
            Packet(dos.id+17, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+17, False, 2)),     
            Packet(dos.id+18, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+18, True, 1)),
            Packet(dos.id+19, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+19, True, 1)),
            Packet(dos.id+20, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+20, False, 2)),
            Packet(dos.id+21, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+21, True, 2)),
            Packet(dos.id+22, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+22, False, 2)),                                                                                                                                                                                       
            Packet(dos.id+23, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+23, True, 2)),
            Packet(dos.id+24, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+24, False, 2)),
            Packet(dos.id+25, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+25, True, 1)),
            Packet(dos.id+26, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+26, False, 1)),
            Packet(dos.id+27, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+27, True, 2)),     
            Packet(dos.id+28, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+28, False, 2)),
            Packet(dos.id+29, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+29, True, 2)),
            Packet(dos.id+30, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+30, False, 2)),
            Packet(dos.id+31, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+31, True, 2)),
            Packet(dos.id+32, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+32, False, 2)),                                                                                                                                                                                       
            Packet(dos.id+33, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+33, True, 1)),
            Packet(dos.id+34, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+34, False, 1)),
            Packet(dos.id+35, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+35, True, 1)),
            Packet(dos.id+36, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+36, False, 1)),
            Packet(dos.id+37, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+37, True, 2)),     
            Packet(dos.id+38, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+38, False, 2)),
            Packet(dos.id+39, self.last_time, "192.168.0.1", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+39, True, 1)),
            Packet(dos.id+40, self.last_time, "192.168.0.10", "192.168.0.1", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+40, False, 1)),
            Packet(dos.id+41, self.last_time, "192.168.0.2", "192.168.0.10", "ICMP", 74, "ICMP Эхо-запрос", 
                                                        dos.get_request_info(dos.id+41, True, 2)),
            Packet(dos.id+42, self.last_time, "192.168.0.10", "192.168.0.2", "ICMP", 74, "ICMP Эхо-ответ", 
                                                        dos.get_request_info(dos.id+42, False, 2))]
        self.master.log_page.content.attack_logs_data.append(AttackInfo(11, "DDoS", "25.01.2024 22:08:24", 1, "192.168.0.1\n192.168.0.2", ddos_packets))
        #print(self.master.side_bar_column.content.controls[0].content.controls[3])
        
        
        dos.attack()     







