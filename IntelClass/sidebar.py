import flet as ft
from functools import partial

# Класс боковой панели
class IDSNavBar(ft.UserControl):
    def __init__(self, func):
        self.switch_page = func
        self.is_attacked = False
        super().__init__()

    def HighLight(self, e):
        if e.data == 'true':
            e.control.bgcolor = 'white10'
            e.control.update()
            e.control.content.controls[0].icon_color = 'white'
            e.control.content.controls[1].color = 'white'
            e.control.content.update()
        else:
            e.control.bgcolor = None
            e.control.update()
            e.control.content.controls[0].icon_color = 'white54'
            e.control.content.controls[1].color = 'white54'
            e.control.content.update() 

    def UserData(self, initials:str, name:str, description:str):
        # Первая строчка - информация о пользователе
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=42,
                        height=42,
                        bgcolor='bluegrey900',
                        alignment=ft.alignment.center,
                        border_radius=8,
                        content=ft.Text(
                            value=initials,
                            size=20,
                            weight='bold'
                            )
                    ),
                    ft.Column(
                        spacing=1,
                        alignment='center',
                        controls=[
                            ft.Text(
                                value=name,
                                size=11,
                                weight='bold',
                                # Детали анимации

                                opacity=1, #Непрозрачность 0-1
                                animate_opacity=200, #Скорость анимации
                            ),
                            ft.Text(
                                value=description,
                                size=9,
                                weight='w400',
                                color="white54",
                                # Детали анимации

                                opacity=1, #Непрозрачность 0-1
                                animate_opacity=200, #Скорость анимации
                            )
                        ]
                    )
                ]
            )
        )
    
    def update_controls(self):
        self.update()
            
            
    
    def ContainedIcon(self, icon_name:str, text:str, page_to_switch:str, color="white"):
        return ft.Container(
            width=180,
            height=45,
            border_radius=10,
            on_hover=lambda e: self.HighLight(e),
            #on_click=lambda e: self.switch_page(e,'page1'),
            on_click=lambda e: self.switch_page(e,page_to_switch),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=icon_name,
                        icon_size=18,
                        icon_color="white54",
                        style=ft.ButtonStyle(
                            shape={
                                "": ft.RoundedRectangleBorder(radius=7),
                            },
                            overlay_color={
                                "": 'transparent'
                            }
                        )
                    ),
                    ft.Text(
                        value=text,
                        color="white54",
                        size=11,
                        opacity=1,
                        animate_opacity=200
                    )
                ]
            ),
        )
        
    def build(self):
        return ft.Container(
            # Определяем измерения и характеристики контейнера
            width=200,
            height=580,
            padding=ft.padding.only(top=10),
            alignment=ft.alignment.center,
            content=ft.Column(
                #alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment='center',
                controls=[
                    # Здесь добавляются иконка для боковой панели
                    self.UserData("VS", "Вадим Сабуров", "Сетевой администратор"),
                    
                    ft.Divider(height=5, color='red'),
                    self.ContainedIcon(ft.icons.SEARCH, "Мониторинг трафика", "page1"),
                    self.ContainedIcon(ft.icons.NOTIFICATIONS, "Уведомления", "page2"),
                    self.ContainedIcon(ft.icons.PIE_CHART_ROUNDED, "Статистика", "page3"),
                    self.ContainedIcon(ft.icons.TABLE_CHART, "Журнал событий", "page4"),
                    self.ContainedIcon(ft.icons.TABLE_CHART, "Журнал безопасности", "page5"),
                    ft.Divider(height=5, color="white54"),
                    self.ContainedIcon(ft.icons.LOGOUT_ROUNDED, "Выход", "page3"),
                ]
            )
            )

def BlackSidebar(switch_page):
    sidebar = ft.Container(
            width=200,
            height=580,
            bgcolor='black',
            border_radius=10,
            animate=ft.animation.Animation(500, 'decelerate'),
            alignment=ft.alignment.center,
            padding=10,
            content=IDSNavBar(switch_page)
        )
    return sidebar


