from random import choice
from flet import *
from packet_page import BuildPacketPage, PacketRow
from notification_page import BuildNotificationPage
from stats_page import BuildStatsPage
from log_page import BuildLogPage
from admin_log_page import BuildAdminLogPage
from sidebar import BlackSidebar
from packet_analyzer import PacketAnalyzer
import time
import pyshark
from pynput import keyboard # Для тестов
import threading # Для тестов

h = 750;w=350
capture = pyshark.FileCapture("./traffic_cap1.pcapng")

class App(UserControl):
  def __init__(self,pg):
    super().__init__()    
    self.pg = pg
    self.pg.title = "Система \"Интелкласс\""      
    self.packet_analyzer = PacketAnalyzer(capture, self)        
    self.animation_style = animation.Animation(500,AnimationCurve.DECELERATE)
    self.dlg_modal = AlertDialog(
        modal=True,
        title=Text("Уведомление"),
        content=Text("Отчёт сформирован"),
        actions=[
            TextButton("Закрыть", on_click=self.close_dlg),
        ],
        actions_alignment=MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    self.counter = 0
    self.is_attacked = False
    self.command = ""
    self.group_len = 0
    self.keys = []    
    self.build_ui()
    #self.init_analyze()
    self.work()

  def open_dlg_modal(self):
      self.pg.dialog = self.dlg_modal
      self.dlg_modal.open = True
      self.pg.update()

  def close_dlg(self, e):
        self.dlg_modal.open = False
        self.pg.update()

  def build_command_value(self):
        command_value = ""
        for k in self.keys[:-1]:
            command_value+=k
        return command_value

  def on_press(self, key):
      try:
          key_str = key.char
      except AttributeError:
          key_str = f"{key}"
      #print(key_str)
      if key_str == "Key.space":
          key_str = " "
      if key_str == "Key.f1":
          self.command =  self.build_command_value()
          self.packet_page.content.scroll_flag = True
      self.keys.append(key_str)        
      if key_str == "Key.enter":
          self.command =  self.build_command_value()          
          self.keys.clear()      
      if key == keyboard.Key.esc:
          self.is_running = False
          self.stop_listener()

  def stop_listener(self):
      if self.listener:
          self.listener.stop()

  def work(self):
        counter_thread = threading.Thread(target=self.init_analyze)
        counter_thread.start()

        with threading.Lock():
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

        counter_thread.join()

  def init_analyze(self):      
    self.stats_page.content.stats_timechart.update()
    self.stats_page.content.update()
    #self.stats_page.content.time_chart.get_data_points()
    while True: 
      self.update_packets_list()
      self.check_intrusion()
      self.update_stats()
      time.sleep(0.5)

  def update_packets_list(self): #считать новую группу пакетов    
    new_group = self.packet_analyzer.get_packet_group()
    self.group_len = len(new_group)       
    for pkt in new_group:
      self.packet_page.content.packet_list_row.controls[0].content.controls.append(self.get_packet(pkt))
      if self.packet_page.content.scroll_flag:
        self.packet_page.content.packet_list_row.controls[0].content.scroll_to(offset=-1)
    self.packet_page.content.packet_list_row.update()


  def get_packet(self, new_packet):
    return Container(
      expand=True,      
      padding=0,                           
      #bgcolor=colors.GREY_400,
      border=border.all(0.5, colors.BLACK),
      alignment=alignment.center,      
      content=PacketRow(new_packet, self)      
    )

  def check_intrusion(self): #проверить на наличие атаки
    if self.command in self.packet_analyzer.commands_dict:
        self.packet_analyzer.commands_dict[self.command]()
        self.is_attacked = True
    self.command = ""

  def update_stats(self): #обновить статистику
    if self.is_attacked:
      self.update_attack_counter()
      self.stats_page.content.attack_stats['DDoS'] += 1
      chart_sections = []
      attack_colors = {"DoS":colors.PURPLE, "Сканирование портов":colors.ORANGE, "Сетевые черви":colors.YELLOW, "Shell-код":colors.RED, "DDoS":colors.BLUE, "Эксплойт":colors.AMBER, "Бэкдор":colors.INDIGO}
      for attack in self.stats_page.content.attack_stats.keys():            
        chart_sections.append(PieChartSection(
                  self.stats_page.content.attack_stats[attack],
                  title=f"{attack}\n{self.stats_page.content.attack_stats[attack]/sum(self.stats_page.content.attack_stats.values())*100:.2f}%",
                  title_style=TextStyle(
            size=8, color=colors.WHITE, weight=FontWeight.BOLD
        ),
                  color=attack_colors[attack],
                  radius=50,
              ))
        self.stats_page.content.stats_piechart.content.controls[1].sections=chart_sections
        self.stats_page.content.stats_piechart.content.controls[1].update()
    self.is_attacked = False
    self.stats_page.content.time_chart.chart.create_data_points(
                    x=self.stats_page.content.time_chart.x,
                    y=self.group_len,
                )
    self.stats_page.content.time_chart.x += 1

      
  
  def update_attack_counter(self):          
    self.packet_analyzer.recent_attacks += 1    
    self.stats_page.content.recent_attack_warner.content.update_counter(self.packet_analyzer.recent_attacks)
      
  def build_ui(self):
    self.side_bar_column = BlackSidebar(self.switch_page)     
    self.indicator = Container(
      height=40,
      bgcolor='red',
      offset=transform.Offset(0,0),
      animate_offset=animation.Animation(500,AnimationCurve.DECELERATE)
    )
    self.packet_page = BuildPacketPage(self.animation_style)
    self.notification_page = BuildNotificationPage(self.animation_style)
    self.stats_page = BuildStatsPage(self.animation_style, self.packet_analyzer.recent_attacks, self.packet_analyzer.attack_stats, self.packet_analyzer.intrusion_counts)
    self.log_page = BuildLogPage(self, self.animation_style, self.packet_analyzer.attack_logs)
    self.saveme = FilePicker(on_result=self.log_page.content.mysavefile)
    self.pg.overlay.append(self.saveme)
    self.admin_log_page = BuildAdminLogPage(self, self.animation_style, self.packet_analyzer.admin_logs)   
    self.switch_control = {
      'page1':self.packet_page,
      'page2':self.notification_page,
      'page3':self.stats_page,
      'page4':self.log_page,
      'page5':self.admin_log_page
    }
    self.pg.add(
      Container(
        bgcolor='black',
        expand=True,
        content=Row(
          spacing=0,
          controls=[
            Container(
              #expand=True,
              width=self.side_bar_column.width,
              # bgcolor='green',
              border=border.only(right=border.BorderSide(width=1,color='#22888888'),),
              content=Column(
                alignment='spaceBetween',
                controls=[                  
                  Container(
                    height=500,
                    content=Row(
                      spacing=0,
                      controls=[
                        Container(
                          expand=True,
                          content=self.side_bar_column,
                        ),
                        Container(
                          width=3,
                          content=Column(
                            controls=[
                              self.indicator,
                            ]
                          ),
                        ),
                      ]
                    )
                  ),
                  Container(
                    height=50,
                  ),
                ]
              )
            ),
            Container(
              expand=True,
              content=Stack(
                controls=[
                  self.packet_page,
                  self.notification_page,
                  self.stats_page,
                  self.log_page,
                  self.admin_log_page,
                ]
              )
            ),
          ]
        )
      )
    )
    for page in self.switch_control:
      self.switch_control[page].offset.x = 2
      self.switch_control[page].update()
    self.switch_control["page1"].offset.x = 0
    self.switch_control["page1"].update()

  def switch_page(self,e,point):    
    for page in self.switch_control:
      self.switch_control[page].offset.x = 2
      self.switch_control[page].update()
    self.switch_control[point].offset.x = 0
    self.switch_control[point].update()
    self.indicator.offset.y = e.control.data
    self.indicator.update()