import flet as ft
import time
from random import randint

class Packet:
    def __init__(self, id, time, source, destination, proto, length, raw_info, info):
        self.id = id
        self.time = time
        self.source = source
        self.destination = destination
        self.proto = proto
        self.length = length
        self.raw_info = raw_info
        self.info = info
        self.threat_color = ft.colors.GREY_400        

class PacketRow(ft.UserControl):
    def __init__(self, packet: Packet, master):
        self.master = master
        self.id = packet.id
        self.time = packet.time
        self.source = packet.source
        self.destination = packet.destination
        self.proto = packet.proto
        self.length = packet.length
        self.raw_info = packet.raw_info
        self.info = packet.info
        self.threat_color = packet.threat_color           
        super().__init__()

    def update_packet_info(self, e):
        self.master.packet_page.content.scroll_flag = False
        self.master.packet_page.content.packet_info.clean()
        #print(self.info)
        for i in range(len(self.info)):
            print(self.info[i])
            self.master.packet_page.content.packet_info.controls.append(ft.Container(PacketInfoRow(self.info[i]['header'], 
                                                                                            self.info[i]['info'])))
        self.master.packet_page.content.packet_info.update()
    
    def update_color(self):
        self.controls[0].bgcolor = self.threat_color
        self.update()

    def on_hover(self, e):
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
        if cur_color == ft.colors.YELLOW_400 or cur_color == ft.colors.YELLOW_200:
            cur_color = ft.colors.YELLOW_400
            hover_color = ft.colors.YELLOW_200
        e.control.bgcolor = hover_color if e.data == "true" else cur_color
        e.control.update()          

    def build(self):
        return ft.Row(
            controls=[
                ft.Container(
                    bgcolor=self.threat_color,
                    expand=True,
                    on_click=self.update_packet_info,
                    on_hover=self.on_hover,                    
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                expand=10,                  
                                alignment=ft.alignment.center,
                                border=ft.border.all(0.5, ft.colors.BLACK),                    
                                content=ft.Text(f"{self.id}", color="black", text_align="center")
                            ),
                            ft.Container(
                                expand=25,                  
                                alignment=ft.alignment.center,
                                border=ft.border.all(0.5, ft.colors.BLACK),                    
                                content=ft.Text(f"{self.time}", color="black", text_align="center")
                            ),
                            ft.Container(
                                expand=45,                  
                                alignment=ft.alignment.center,
                                border=ft.border.all(0.5, ft.colors.BLACK),
                                content=ft.Text(f"{self.source}", color="black", text_align="center"),
                            ),
                            ft.Container(
                                expand=35,                  
                                alignment=ft.alignment.center,
                                border=ft.border.all(0.5, ft.colors.BLACK),
                                content=ft.Text(f"{self.destination}", color="black", text_align="center"),
                            ),
                            ft.Container(
                                expand=20,                  
                                alignment=ft.alignment.center,
                                border=ft.border.all(0.5, ft.colors.BLACK),
                                content=ft.Text(f"{self.proto}", color="black", text_align="center"),
                            ),
                            ft.Container(
                                expand=15,                  
                                alignment=ft.alignment.center,
                                border=ft.border.all(0.5, ft.colors.BLACK),
                                content=ft.Text(f"{self.length}", color="black", text_align="center"),
                            ),
                            ft.Container(
                                expand=80,                  
                                alignment=ft.alignment.center,
                                border=ft.border.all(0.5, ft.colors.BLACK),
                                content=ft.Text(f"{self.raw_info}",color="black", text_align="center"),
                            ),
                        ],
                        spacing=0
                    ) 
                )                     
            ],
            alignment=ft.alignment.center,
            spacing=0
        )
        

class PacketInfoRow(ft.UserControl):
    def __init__(self, main_packet_text, expand_info):
        self.expand_btn = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_RIGHT,
            selected_icon=ft.icons.KEYBOARD_ARROW_DOWN,
            on_click=self.__expand_unexpand,
        )
        self.main_packet_text = ft.Text(value=main_packet_text)
        self.expand_info = ft.Container(content=ft.Text(value=expand_info))
        self.expand_info.visible = False
        super().__init__()

    def __expand_unexpand(self, e):
        e.control.selected = not e.control.selected
        e.control.update()
        self.expand_info.visible = e.control.selected
        self.update()

    def build(self):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.expand_btn,
                        self.main_packet_text
                    ]
                ),
                self.expand_info
            ]
        )

class PacketPageClass(ft.UserControl):
    def __init__(self):
        self.scroll_flag = True
        self.packet_header = ft.Container(content=ft.Row(
            controls=[
                ft.Container(
                    expand=10,                  
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.RED_600),                    
                    content=ft.Text("ID", text_align="center")
                ),
                ft.Container(
                    expand=25,                  
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.RED_600),                    
                    content=ft.Text("Время", text_align="center")
                ),
             ft.Container(
                    expand=45,                  
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.RED_600),
                    content=ft.Text("Источник", text_align="center"),
                ),
             ft.Container(
                    expand=35,                  
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.RED_600),
                    content=ft.Text("Назначение", text_align="center"),
                ),
             ft.Container(
                    expand=20,                  
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.RED_600),
                    content=ft.Text("Протокол", text_align="center"),
                ),
            ft.Container(
                    expand=15,                  
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.RED_600),
                    content=ft.Text("Длина", text_align="center"),
                ), 
                ft.Container(
                    expand=80,                  
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.RED_600),
                    content=ft.Text("Информация", text_align="center"),
                ),             
            ],
            alignment=ft.alignment.center,
            spacing=0            
            #expand=True
        ),
        margin = ft.margin.symmetric(horizontal=15)
        )
        self.packet_info = ft.ListView(expand=1)
        self.packet_info.controls.append(ft.Container(PacketInfoRow("Главная информация пакета 1", "Разв. инф. пакета 1")))
        self.packet_info.controls.append(ft.Container(PacketInfoRow("Главная информация пакета 2", "Разв. инф. пакета 2"))) 
        self.packet_info.controls.append(ft.Container(PacketInfoRow("Главная информация пакета 3", "Разв. инф. пакета 3"))) 
        self.packet_info.controls.append(ft.Container(PacketInfoRow("Главная информация пакета 4", "Разв. инф. пакета 4")))          
        self.packet_list_row = self.PacketListRow()                
        super().__init__()

    def PacketListRow(self):
        packet_list_row = ft.Row(   # Верхняя строка (для пакетного анализатора)
                    expand=True,                 
                    controls=[                        
                        ft.Container(
                            margin=ft.margin.symmetric(horizontal=15),
                            #padding=10                            
                            expand=True, 
                            #bgcolor=ft.colors.RED_300,
                            border=ft.border.all(1, ft.colors.RED_600),
                            alignment=ft.alignment.center,
                            border_radius=10,
                            content=ft.ListView(expand=1, auto_scroll=False)                     
                        )
                    ]
                )
        return packet_list_row   

    def build(self):
        return ft.Column(                                  
            controls=[
                    # Верхняя строка
                    self.packet_header,
                    self.packet_list_row, 
                    # Нижняя строка              
                    ft.Row(
                    expand=1,                 
                    controls=[                        
                            ft.Container(                            
                            margin=15,
                            padding=5, 
                            expand=1,                            
                            alignment=ft.alignment.center,
                            border_radius=10,
                            content=
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                        expand=1,                                
                                        controls=[
                                        ft.Column(
                                            expand=2,
                                            controls=[                                                    
                                                    ft.Container(                                                        
                                                        padding=5, 
                                                        expand=1,                                                        
                                                        border=ft.border.all(1, ft.colors.RED_600),
                                                        alignment=ft.alignment.center,
                                                        border_radius=10,
                                                        content=self.packet_info
                                                    )
                                                    ]
                                                ),                                                                                    
                                        ]
                                    ),
                                ]
                            )                            
                                    )
                                ] 
                            )
                ]
            )

def BuildPacketPage(animation_style): 
    page1 = ft.Container(
        alignment=ft.alignment.center,
        offset=ft.transform.Offset(0,0),
        animate_offset=animation_style,
        bgcolor="#1f2128",
        #bgcolor="white",
        content= PacketPageClass()
        )   
    return page1



