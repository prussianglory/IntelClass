import flet as ft
import flet_material as fm
import asyncio
from main_window import App
import hashlib
import usb.core

PRIMARY = "teal"
fm.Theme.set_theme(theme=PRIMARY)


dummy_user_list: list = [
    [ hashlib.sha512('saburov_vs'.encode('utf-8')).hexdigest(),
     'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86']]

auth_flag = False

class CustomInputField(ft.UserControl):
    def __init__(self, password: bool, title: str):
        self.input: ft.Control = ft.TextField(
            height=45,
            border_color="#bbbbbb",
            border_width=0.6,
            cursor_height=14,
            cursor_width=1,
            cursor_color="white",
            color="white",
            text_size=13,
            bgcolor=fm.Theme.bgcolor,
            password=password,
            on_focus= lambda e: self.focus_shadow(e),
            on_blur= lambda e: self.blur_shadow(e),
            on_change=lambda e: self.set_loader_animation(e)

        )

        self.input_box: ft.Container = ft.Container(
            expand=True,
            content=self.input,
            animate=ft.Animation(300, "ease"),
            shadow=None,
        )

        self.loader: ft.Control = ft.ProgressBar(
            value=0,
            bar_height=1.25,
            color=PRIMARY,
            bgcolor="transparent",
            
        )
        self.status: ft.Control = fm.CheckBox(
            shape="circle",
            value=False,
            disabled=True,
            offset=ft.Offset(1,0),
            bottom=0,
            right=1,
            top=1,
            animate_opacity=ft.Animation(200, "linear"),
            animate_offset=ft.Animation(350, "ease"),
            opacity=0
        )

        self.object = self.create_input(title)

        super().__init__()

    async def set_ok(self):
        self.loader.value = 0
        self.loader.update()
        
        self.status.offset = ft.Offset(-0.5, 0)
        self.status.opacity = 1
        self.update()

        await asyncio.sleep(1)

        self.status.content.value = True
        self.status.animate_checkbox(e=None)
        self.status.update()

    def focus_shadow(self, e):
        self.input.border_color = PRIMARY
        self.input_box.shadow = ft.BoxShadow(
            spread_radius=6,
            blur_radius=8,
            color=ft.colors.with_opacity(0.25, "black"),
            offset=ft.Offset(4,4)
        )
        self.update()
        self.set_loader_animation(e=None)


    def blur_shadow(self, e):
        self.input_box.shadow = None
        self.input.border_color = "#bbbbbb"
        self.update()
        self.set_loader_animation(e=None)

    def set_loader_animation(self, e):
        if len(self.input.value) != 0:
            self.loader.value = None
        else:
            self.loader.value = 0

        self.loader.update()


    def create_input(self, title):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Text(title, size=11, weight="bold", color="#bbbbbb"),
                ft.Stack(
                    controls=[
                        self.input_box, 
                        self.status
                    ],
                ),
                self.loader,
            ]
        )
    
    def build(self):
        return self.object



class AuthFormUI(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.title = "Вход в систему Интелкласс"
        self.page.bgcolor = fm.Theme.bgcolor
        self.page.window_width=450
        self.page.window_height=550
        self.page.window_resizable = False
        self.page.horizontal_alignment="center"
        self.page.vertical_alignment="center"
        self.page.window_center()
        self.username = CustomInputField(False, "Логин")
        self.password = CustomInputField(True, "Пароль")
        '''
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ошибка верификации подписи"),
            content=ft.Text("Один из файлов был модифицирован"),
            actions=[
                ft.TextButton("Закрыть", on_click=self.close_dlg),
            ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
        '''
        self.submit = ft.OutlinedButton(
            width=400, height=45, text="Войти в систему", on_click=lambda e: asyncio.run(self.validate_entries(e))
        )        
        self.build_ui()
        self.update()
    def open_dlg_modal(self):
        self.page.dialog = dlg_modal
        self.dlg_modal.open = True
        self.page.update()
    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()
    async def validate_entries(self, e):
        username_value = self.username.input.value
        password_value = self.password.input.value
        if self.check_usb_key():
            for user, password in dummy_user_list:
                if hashlib.sha512(username_value.encode('utf-8')).hexdigest() == user and hashlib.sha512(password_value.encode('utf-8')).hexdigest() == str(password):
                    await asyncio.sleep(0.05)
                    await self.username.set_ok()
                    await asyncio.sleep(0.05)
                    await self.password.set_ok()
                    self.update()
                    self.page.window_destroy()
                    global auth_flag
                    auth_flag = True
        else:
            print('Ключ не найден!')
                

    def check_usb_key(self):
        #device =  usb.core.find(idVendor=0x0951, idProduct=0x1665)
        #if device is not None:
        #    return True
        #return False
        return True
    '''
    def signature_verification(self, key_directory):
        current_directory = os.getcwd()
        file_list = os.listdir(current_directory)
        key_list = os.listdir(key_directory)
        sgn_files = [file for file in file_list if file.lower().endswith('.sgn')]
        key_files = [file for file in file_list if file.lower().endswith('.key')]
        for i in range(len(sgn_list)):
            try:
                pkcs1_15.new(key_files[i]).verify(h, sgn_files[i])
            except ValueError:
                self.open_dlg_modal()
                return False
        return True
    '''   
    def build_ui(self):        
        self.page.add(ft.Container(
            width=450,
            height=550,
            bgcolor=ft.colors.with_opacity(0.01, "white"),
            border_radius=10,
            content=ft.Column(
                horizontal_alignment="center",
                alignment="center",
                controls=[
                    ft.Text("Вход в систему",size=21, weight="w800", color=ft.colors.with_opacity(0.85, "white")),
                    ft.Divider(height=25, color="transparent"),
                    self.username,
                    ft.Divider(height=5, color="transparent"),
                    self.password,
                    #ft.Divider(height=25, color="transparent"),
                    self.submit,
                ],
            )
        )
        )

ft.app(target=AuthFormUI)
if auth_flag:
    ft.app(target=App)