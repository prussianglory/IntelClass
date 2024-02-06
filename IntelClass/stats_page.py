import flet as ft
import time

base_chart_style: dict = {
    "expand": True,
    "tooltip_bgcolor": ft.colors.with_opacity(0.8, ft.colors.WHITE),
    "left_axis": ft.ChartAxis(labels_size=50),
    "bottom_axis": ft.ChartAxis(labels_interval=1, labels_size=40),
    "horizontal_grid_lines": ft.ChartGridLines(
        interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
    ),
}


out_style: dict = {
        "expand": 1,
        "bgcolor": "#17181d",
        "border_radius": 10,
        "padding":30
    }

class AttackPieChart:
    def __init__(self, attack_stats: dict):
        self.attack_stats = attack_stats
        self.normal_radius = 50
        self.hover_radius = 60
        self.normal_title_style = ft.TextStyle(
            size=8, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
        )
        self.hover_title_style = ft.TextStyle(
            size=18,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        )
        self.attack_colors = self.get_attack_colors()
    
    def get_attack_colors(self):
        return {"DoS":ft.colors.PURPLE, "Сканирование портов":ft.colors.ORANGE, "Сетевые черви":ft.colors.PINK, "Shell-код":ft.colors.RED, "DDoS":ft.colors.BLUE, "Эксплойт":ft.colors.AMBER, "Бэкдор":ft.colors.INDIGO}

    def on_chart_event(self, e: ft.PieChartEvent):
        for idx, section in enumerate(self.chart.sections):
            if idx == e.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
        self.chart.update()

    def get_chart(self):
        chart_sections = []
        for attack in self.attack_stats.keys():            
            chart_sections.append(ft.PieChartSection(
                self.attack_stats[attack],
                title=f"{attack}\n{self.attack_stats[attack]/sum(self.attack_stats.values())*100:.2f}%",
                title_style=self.normal_title_style,
                color=self.attack_colors[attack],
                radius=self.normal_radius,
            ))
        self.chart = ft.PieChart(
        sections=chart_sections,             
        sections_space=0,
        center_space_radius=40,
        on_chart_event=self.on_chart_event,
        expand=True,
        )
        return self.chart




class BaseChart(ft.LineChart):
    def __init__(self, line_color):
        super().__init__(**base_chart_style)

        self.points: list = []

        self.min_x = (int(min(self.points, key=lambda x: x[0] [0]))) if self.points else None
        self.max_x = (int(max(self.points, key=lambda x: x[0] [0]))) if self.points else None

        self.line = ft.LineChartData(
            color=line_color,
            stroke_width=2,
            curved=True,
            stroke_cap_round=True,
            below_line_gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.colors.with_opacity(0.25, line_color),
                    "transparent"
                ],
            ),
        )

        self.line.data_points = self.points
        self.data_series = [self.line]

    def create_data_points(self, x, y):
        self.points.append(
            ft.LineChartDataPoint(
                x, y, selected_below_line=ft.ChartPointLine(
                        width=0.5, color="white54", dash_pattern=[2,4]
                    ),
                    selected=ft.ChartCirclePoint(stroke_width=1),
                )
            )
        self.update()

class GraphOut(ft.Container):
    def __init__(self):
        super().__init__(**out_style)
        self.chart = BaseChart(line_color="red500")
        self.content = ft.Column(
            horizontal_alignment='center',
            controls=[
                ft.Text(value="Количество принятых пакетов за секунду", text_align="center"),                
                self.chart,                
            ]
        )
        self.x = 0

class RecentAttackCounter(ft.UserControl):
    def __init__(self, recent_attacks):
        self.recent_attacks_count = recent_attacks
        self.icon = None
        self.text_color = None
        if self.recent_attacks_count != 0:
            self.icon = ft.Icon(name=ft.icons.WARNING_OUTLINED, color=ft.colors.RED, size=85)
        else:
            self.icon = ft.Icon(name=ft.icons.CHECK, color=ft.colors.BLUE, size=85) 
        super().__init__()

    def update_counter(self, recent_attacks):
        self.recent_attacks_count = recent_attacks
        #print(self.recent_attacks_count)
        self.controls[0].controls[1].content.controls[1].value = f"{self.recent_attacks_count}"        
        if self.recent_attacks_count != 0:
            self.controls[0].controls[1].content.controls[0] = ft.Icon(name=ft.icons.WARNING_OUTLINED, color=ft.colors.RED, size=85)
        else:
            self.controls[0].controls[1].content.controls[0] = ft.Icon(name=ft.icons.CHECK, color=ft.colors.BLUE, size=85)
        self.update()
    

    def build(self):
        return ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(value="Количество инцидентов текущего дня", text_align=ft.TextAlign.CENTER),                                           
                        ft.Container(
                            alignment=ft.alignment.center,                                
                            padding=0,
                            expand=True,                                
                            #bgcolor=ft.colors.with_opacity(0.025, ft.colors.WHITE10),
                            content=ft.Column(
                                    horizontal_alignment="center",
                                    controls=[
                                    self.icon,
                                    ft.Text(value=f"{self.recent_attacks_count}", size=42, text_align="center", weight="bold"),
                                    ft.Text(value="недавних инцидентов", size=18, text_align="center")
                                                ]
                                            ),                                
                                    )                                
                            ],
                        )

class BarChart(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=2,
                        width=30,                        
                        tooltip="Утро\nСиний: DDoS",
                        border_radius=0,
                        rod_stack_items=[
                            ft.BarChartRodStackItem(
                                from_y=0,
                                to_y=1,
                                color=ft.colors.BLUE,
                                #tooltip="Утро: Shell-код",                            
                            ),
                            ft.BarChartRodStackItem(
                                from_y=1,
                                to_y=2,
                                color=ft.colors.PURPLE,
                                #tooltip="Утро: DDoS",                            
                            )
                        ]
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=1,
                        width=30,
                        color=ft.colors.RED,
                        tooltip="День\nКрасный: Shell-код",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.GREY,
                        tooltip="Вечер",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.GREY,
                        tooltip="Ночь",
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=1,
                        width=30,
                        color=ft.colors.BLUE,
                        tooltip="Утро\nСиний: DDoS",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.BLUE,
                        tooltip="День",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.BLUE,
                        tooltip="Вечер",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.BLUE,
                        tooltip="Ночь",
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=2,
                        width=30,                        
                        tooltip="Утро\nСиний: DDoS\nЖелтый: Сетевой червь",
                        border_radius=0,
                        rod_stack_items=[
                            ft.BarChartRodStackItem(
                                from_y=0,
                                to_y=1,
                                color=ft.colors.BLUE,
                                #tooltip="Утро: Shell-код",                            
                            ),
                            ft.BarChartRodStackItem(
                                from_y=1,
                                to_y=2,
                                color=ft.colors.PINK,
                                #tooltip="Утро: DDoS",                            
                            )
                        ]
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.GREY,
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=1,
                        width=30,
                        color=ft.colors.AMBER,
                        tooltip="Вечер\nЯнтарный: Эксплойт",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.GREY,
                        tooltip="Ночь",
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=3,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=1,
                        width=30,                        
                        tooltip="Утро\nОранжевый: Сканирование портов",
                        border_radius=0,
                        rod_stack_items=[
                            ft.BarChartRodStackItem(
                                from_y=0,
                                to_y=1,
                                color=ft.colors.ORANGE,
                                #tooltip="Утро: Shell-код",                            
                            ),
                            #ft.BarChartRodStackItem(
                            #    from_y=2,
                            #    to_y=4,
                            #    color=ft.colors.BLUE,
                                #tooltip="Утро: DDoS",                            
                            #)
                        ]
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=1,
                        width=30,
                        color=ft.colors.INDIGO,
                        tooltip="День\nИндиго: Бэкдор",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.GREY,
                        tooltip="Вечер",
                        border_radius=0,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0.01,
                        width=1,
                        color=ft.colors.GREY,
                        tooltip="Ночь",
                        border_radius=0,
                    ),
                ],
            ),
        ],
        border=ft.border.all(1, ft.colors.GREY_400),
        left_axis=ft.ChartAxis(
            labels_size=40, title=ft.Text("Атаки по времени суток"), title_size=40
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0, label=ft.Container(ft.Text("17.12.2023"), padding=1)
                ),
                ft.ChartAxisLabel(
                    value=1, label=ft.Container(ft.Text("18.12.2023"), padding=1)
                ),
                ft.ChartAxisLabel(
                    value=2, label=ft.Container(ft.Text("19.12.2023"), padding=1)
                ),
                ft.ChartAxisLabel(
                    value=3, label=ft.Container(ft.Text("20.12.2023"), padding=1)
                ),
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
        max_y=4,
        #interactive=True,
        expand=True,
        )
        return chart
 

class StatsPageClass(ft.UserControl):
    def __init__(self, recent_attacks, attack_stats, points):
        self.attack_stats = attack_stats
        self.recent_attack_counter = RecentAttackCounter(recent_attacks)
        self.attack_piechart = AttackPieChart(attack_stats)
        #self.time_chart = TimeChart(points)
        self.time_chart = GraphOut()        
        self.stats_piechart = self.StatsPieChart()
        self.recent_attack_warner = self.RecentAttackWarner()
        self.stats_timechart = self.StatsTimeChart()
        self.bar_chart = self.BarChart()
        super().__init__()

    def StatsPieChart(self):
        piechart_container = ft.Container(
                        margin=10,
                        padding=2,                                                 
                        expand=True,
                        #bgcolor=ft.colors.GREEN_300,
                        border=ft.border.all(1, ft.colors.RED_600),
                        alignment=ft.alignment.center,
                        border_radius=10,
                        content=ft.Column(
                            horizontal_alignment="center",
                            controls=[
                                ft.Text(value="Статистика по обнаруженным атакам", text_align="center"),
                                self.attack_piechart.get_chart()
                            ]
                        )
                        )
        return piechart_container

    def StatsTimeChart(self):
        timechart_container = ft.Container(
                        margin=10,
                        padding=2,                                                 
                        expand=True,
                        #bgcolor=ft.colors.GREEN_300,
                        alignment=ft.alignment.center,
                        border=ft.border.all(1, ft.colors.RED_600),
                        border_radius=10,
                        content=ft.Column(
                            alignment=ft.alignment.center,
                            expand=True,
                            controls=[                                                         
                                self.time_chart,                                                                                           
                            ]
                        )
                    )
        return timechart_container

    def RecentAttackWarner(self):
        recent_attack_warner = ft.Container(
                        margin=10,
                        padding=2,                                                 
                        expand=True,
                        #bgcolor=ft.colors.GREEN_300,
                        #alignment=ft.alignment.center,
                        border=ft.border.all(1, ft.colors.RED_600),
                        border_radius=10,
                        content=self.recent_attack_counter
                    )
        return recent_attack_warner

    def BarChart(self):
        return ft.Container(
                            margin=5,
                            padding=5, 
                            expand=1,
                            #bgcolor=ft.colors.RED_300,
                            border=ft.border.all(1, ft.colors.RED_600),
                            alignment=ft.alignment.center,
                            border_radius=10,
                            content=BarChart()
                        )
    
    def build(self):
        return ft.Column(
            spacing=1,                   
            controls=[
                    ft.Row(   # Верхняя строка (для пакетного анализатора)
                    expand=True,                 
                    controls=[                        
                        ft.Container(
                            margin=15,
                            #padding=10                            
                            expand=True, 
                            #bgcolor=ft.colors.RED_300,
                            border=ft.border.all(0.5, ft.colors.RED_600),
                            alignment=ft.alignment.center,
                            border_radius=10,                                                   
                            content=ft.Column(
                                    controls=[
                                        ft.Row(
                                        expand=1,                                
                                        controls=[
                                        ft.Column(
                                            expand=1,
                                            controls=[
                                                    self.recent_attack_warner                                                    
                                                    ]
                                                ),
                                        ft.Column(
                                            expand=2,
                                            controls=[
                                                    self.stats_piechart                                                    
                                                ]
                                                ),
                                            ]
                                        ),
                                ]
                            )
                        )
                    ]
                ),               
                    ft.Row( # Нижняя строка (для статистики)
                    expand=1,                 
                    controls=[                        
                            ft.Container(
                            margin=15,
                            padding=0, 
                            expand=1,
                            #bgcolor=ft.colors.RED_300,
                            #border=ft.border.all(1, ft.colors.RED_600),
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
                                                    #self.stats_piechart
                                                    self.stats_timechart
                                                    ]
                                                ),
                                        ft.Column(
                                            expand=2,
                                            controls=[
                                                    self.bar_chart
                                                    
                                                ]
                                                ),                                        
                                            ]
                                        ),
                                ]
                            )
                            #content=ft.Text('PAGE 1: ROW 2', size=100)
                                    )
                                ] 
                            )
                ]
            )

def BuildStatsPage(animation_style, recent_attacks, attack_stats, points):          
    return ft.Container(
        alignment=ft.alignment.center,
        offset=ft.transform.Offset(0,0),
        animate_offset=animation_style,
        bgcolor="#1f2128",
        content=StatsPageClass(recent_attacks, attack_stats, points)
        )