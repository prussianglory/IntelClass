import flet as ft
from packet_analyzer import Attack

class AttackInfo:
    def __init__(self, id, attack_type, attack_time, source, threat_level, packet_group):       
        self.id = id
        self.attack_type = attack_type
        self.attack_time = attack_time
        self.source = source
        self.threat_level = threat_level
        self.packet_group = packet_group

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

class NotificationPageClass(ft.UserControl):
    def __init__(self):                
        self.notification_list = ft.ListView(expand=1, padding=10, auto_scroll=True)
        #DDoS = AttackInfo(len(self.notification_list.controls), 'DDoS', '12.02.2023:05:16:37', '236.124.75.48', 'Средний', '[137-167]')
        #self.notification_list.controls = [Notification(DDoS)] + self.notification_list.controls
        #intrusion = AttackInfo(len(self.notification_list.controls), 'Сетевой червь', '12.02.2023:06:14:37', '236.125.74.137', 'Высокий', '[64-72]')
        #self.notification_list.controls = [Notification(intrusion)] + self.notification_list.controls
        super().__init__()

    def build(self):
        return ft.Column(
            controls=[                
                ft.Container(
                    height=30,
                    padding=5,                    
                    alignment=ft.alignment.center,
                    margin=0,
                    content=ft.Text(value=f"У вас {len(self.notification_list.controls)} непросмотренных уведомлений")
                ),
                ft.Container(
                    expand=True,
                    border_radius=10,
                    margin=15,
                    alignment=ft.alignment.center,                   
                    #bgcolor=ft.colors.GREY,
                    border=ft.border.all(1, ft.colors.RED_600),
                    content=self.notification_list
                )
            ]
        )

def BuildNotificationPage(animation_style, counter=0):          
    return ft.Container(
        alignment=ft.alignment.center,
        offset=ft.transform.Offset(0,0),
        animate_offset=animation_style,
        bgcolor="#1f2128",
        #bgcolor="white",
        content=NotificationPageClass()
    )