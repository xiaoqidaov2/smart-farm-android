from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.core.text import LabelBase
from kivy.utils import platform
from kivy.resources import resource_find
import os
import os.path

import threading
import time
from nle_api import NLECloudAPI

# Configuration
DEFAULT_DEVICE_ID = "372699"
DEFAULT_API_URL = "http://api.nlecloud.com"
# 本地测试请改为:
# DEFAULT_API_URL = "http://127.0.0.1:5000"

# Sensor Mapping
SENSORS_MAP = {
    "guangzhao_sum": {"name": "光照传感器", "unit": "Lux", "icon": "white-balance-sunny"},
    "temperature": {"name": "温度传感器", "unit": "℃", "icon": "thermometer"},
    "humidity": {"name": "湿度传感器", "unit": "%RH", "icon": "water-percent"},
    "CO2": {"name": "CO2浓度", "unit": "ppm", "icon": "molecule-co2"},
    "Soil_temperture": {"name": "土壤温度", "unit": "℃", "icon": "thermometer-lines"},
    "Soil_moisture": {"name": "土壤湿度", "unit": "%", "icon": "water"},
    "Soil_sanility": {"name": "土壤盐度", "unit": "mg/L", "icon": "shaker-outline"},
    "Nhanl": {"name": "氮含量", "unit": "mg/kg", "icon": "bottle-tonic"},
    "Phanl": {"name": "磷含量", "unit": "mg/kg", "icon": "bottle-tonic-plus"},
    "jia": {"name": "钾含量", "unit": "mg/kg", "icon": "bottle-tonic-outline"},
    "PH": {"name": "土壤PH", "unit": "", "icon": "ph"},
    "zigbee_fun": {"name": "光照", "unit": "Lux", "icon": "brightness-6"},
}

ACTUATORS_MAP = {
    "fun": {"name": "风扇", "icon": "fan"},
    "LVD": {"name": "绿灯", "icon": "lightbulb"},
}

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        # Logo/Title
        layout.add_widget(MDLabel(
            text="智绘农芯",
            halign="center",
            theme_text_color="Primary",
            font_style="H4",
            bold=True
        ))
        layout.add_widget(MDLabel(
            text="Smart Farm Core", 
            halign="center", 
            theme_text_color="Secondary", 
            font_style="Subtitle1"
        ))
        
        # Inputs
        self.user_field = MDTextField(
            hint_text="账号", 
            icon_right="account",
            mode="rectangle"
        )
        layout.add_widget(self.user_field)
        
        self.pwd_field = MDTextField(
            hint_text="密码", 
            icon_right="key", 
            password=True,
            mode="rectangle"
        )
        layout.add_widget(self.pwd_field)

        self.device_field = MDTextField(
            text=DEFAULT_DEVICE_ID,
            hint_text="设备ID",
            icon_right="raspberry-pi",
            mode="rectangle"
        )
        layout.add_widget(self.device_field)

        self.server_field = MDTextField(
            text=DEFAULT_API_URL,
            hint_text="服务器地址",
            icon_right="server-network",
            mode="rectangle"
        )
        layout.add_widget(self.server_field)
        
        # Login Button
        btn = MDFillRoundFlatButton(
            text="登 录", 
            font_size=20,
            size_hint_x=1,
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        btn.bind(on_release=self.do_login)
        layout.add_widget(btn)
        
        self.add_widget(layout)

    def do_login(self, instance):
        username = self.user_field.text
        password = self.pwd_field.text
        device_id = self.device_field.text
        api_url = self.server_field.text
        
        if not username or not password:
            self.show_error("请输入账号和密码")
            return

        app = MDApp.get_running_app()
        app.device_id = device_id
        app.nle = NLECloudAPI(base_url=api_url) # Re-init with new URL
        
        # Async Login
        threading.Thread(target=self.login_thread, args=(username, password)).start()

    def login_thread(self, username, password):
        app = MDApp.get_running_app()
        success, msg = app.nle.login(username, password)
        Clock.schedule_once(lambda dt: self.post_login(success, msg))

    def post_login(self, success, msg):
        if success:
            MDApp.get_running_app().change_screen('dashboard')
        else:
            self.show_error(msg)

    def show_error(self, text):
        dialog = MDDialog(title="提示", text=text, buttons=[MDFillRoundFlatButton(text="确定", on_release=lambda x: dialog.dismiss())])
        dialog.open()

class SensorCard(MDCard):
    icon = StringProperty("sensor")
    title = StringProperty("Sensor")
    value = StringProperty("--")
    unit = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(12)
        self.spacing = dp(4)
        self.size_hint = (1, None)
        self.height = dp(110)
        self.radius = [12]
        self.elevation = 0.5
        self.md_bg_color = (1, 1, 1, 1)
        self.line_color = (0, 0, 0, 0.05)
        self.shadow_offset = (0, 1)

        # Header with Icon and Title
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24), spacing=dp(8))
        # Icon
        header.add_widget(MDIconButton(
            icon=self.icon, 
            icon_size=dp(20), 
            theme_text_color="Custom", 
            text_color=MDApp.get_running_app().theme_cls.primary_color,
            pos_hint={'center_y': 0.5},
            size_hint=(None, None),
            size=(dp(24), dp(24))
        ))
        # Title
        header.add_widget(MDLabel(
            text=self.title, 
            halign='left', 
            theme_text_color="Secondary", 
            font_style="Caption",
            valign='middle'
        ))
        self.add_widget(header)
        
        # Spacer
        self.add_widget(MDLabel(size_hint_y=None, height=dp(10)))

        # Value
        self.value_label = MDLabel(
            text=f"{self.value}", 
            halign='center', 
            font_style="H5",
            theme_text_color="Primary",
            bold=True
        )
        self.add_widget(self.value_label)
        
        # Unit
        self.unit_label = MDLabel(
            text=self.unit,
            halign='center',
            font_style="Overline",
            theme_text_color="Secondary"
        )
        self.add_widget(self.unit_label)

    def update_value(self, new_val):
        self.value = str(new_val)
        self.value_label.text = f"{self.value}"

class ControlCard(MDCard):
    title = StringProperty("Control")
    api_tag = StringProperty("")
    icon = StringProperty("toggle-switch")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = [dp(20), dp(10), dp(20), dp(10)]
        self.spacing = dp(15)
        self.size_hint = (1, None)
        self.height = dp(80)
        self.radius = [12]
        self.elevation = 0
        self.md_bg_color = (1, 1, 1, 1)
        self.line_color = (0, 0, 0, 0.05)
        self.shadow_offset = (0, 1)
        self.shadow_softness = 2
        
        # Icon
        self.add_widget(MDIconButton(
            icon=self.icon, 
            icon_size=dp(32), 
            theme_text_color="Custom", 
            text_color=MDApp.get_running_app().theme_cls.primary_color,
            pos_hint={'center_y': 0.5},
            size_hint=(None, None),
            size=(dp(48), dp(48))
        ))
        
        # Label
        self.add_widget(MDLabel(
            text=self.title, 
            font_style="Subtitle1", 
            halign="left",
            valign="middle",
            bold=True,
            size_hint_x=1
        ))
        
        # Switch Container to prevent overflow
        switch_container = MDBoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=dp(60),
        )
        self.switch = MDSwitch()
        self.switch.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.switch.bind(active=self.on_switch_active)
        switch_container.add_widget(self.switch)
        self.add_widget(switch_container)

    def on_switch_active(self, instance, value):
        app = MDApp.get_running_app()
        # 1 for On, 0 for Off
        val_to_send = 1 if value else 0
        threading.Thread(target=self.control_thread, args=(app, self.api_tag, val_to_send)).start()

    def control_thread(self, app, api_tag, value):
        success, msg = app.nle.control_device(app.device_id, api_tag, value)
        if not success:
            print(f"Control Failed: {msg}")
            # Optionally revert switch state if failed, but requires main thread call

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sensor_widgets = {}
        self.md_bg_color = (0.96, 0.96, 0.96, 1) # Light gray background for contrast
        self.build_ui()
        self.active = False

    def build_ui(self):
        root = MDBoxLayout(orientation='vertical')
        
        # Custom Flat White Header
        header = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(56),
            padding=[dp(16), 0, dp(8), 0],
            md_bg_color=(1, 1, 1, 1)
        )
        
        # Title
        header.add_widget(MDLabel(
            text="智绘农芯监控中心",
            font_style="H6",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().theme_cls.primary_color,
            bold=True,
            valign='center',
        ))
        
        # Refresh Button
        refresh_btn = MDIconButton(
            icon="refresh",
            theme_text_color="Custom",
            text_color=MDApp.get_running_app().theme_cls.primary_color,
            pos_hint={'center_y': 0.5},
            on_release=lambda x: self.refresh_data()
        )
        header.add_widget(refresh_btn)
        
        root.add_widget(header)

        # Content - Scrollable
        from kivymd.uix.scrollview import MDScrollView
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(20), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Sensors Section
        header_sensor = MDBoxLayout(size_hint_y=None, height=dp(40))
        header_sensor.add_widget(MDLabel(
            text="环境监测", 
            font_style="H6", 
            bold=True,
            theme_text_color="Primary"
        ))
        content.add_widget(header_sensor)
        
        sensor_grid = MDGridLayout(cols=2, spacing=dp(16), size_hint_y=None)
        sensor_grid.bind(minimum_height=sensor_grid.setter('height'))
        
        for key, info in SENSORS_MAP.items():
            card = SensorCard(
                title=info['name'],
                unit=info['unit'],
                icon=info['icon']
            )
            self.sensor_widgets[key] = card
            sensor_grid.add_widget(card)
            
        content.add_widget(sensor_grid)
        
        # Controls Section
        header_control = MDBoxLayout(size_hint_y=None, height=dp(40))
        header_control.add_widget(MDLabel(
            text="设备控制", 
            font_style="H6", 
            bold=True,
            theme_text_color="Primary"
        ))
        content.add_widget(header_control)
        
        for key, info in ACTUATORS_MAP.items():
            card = ControlCard(title=info['name'], api_tag=key, icon=info['icon'])
            content.add_widget(card)

        scroll.add_widget(content)
        root.add_widget(scroll)
        
        self.add_widget(root)

    def on_enter(self):
        self.active = True
        self.refresh_data()
        # Auto refresh every 5 seconds
        self.auto_refresh_event = Clock.schedule_interval(self.refresh_data, 5)

    def on_leave(self):
        self.active = False
        if hasattr(self, 'auto_refresh_event'):
            self.auto_refresh_event.cancel()

    def refresh_data(self, *args):
        app = MDApp.get_running_app()
        threading.Thread(target=self.fetch_data_thread, args=(app,)).start()

    def fetch_data_thread(self, app):
        data, msg = app.nle.get_sensor_data(app.device_id)
        if data:
            Clock.schedule_once(lambda dt: self.update_ui(data))

    def update_ui(self, data):
        # data is a list of sensor objects usually: [{'ApiTag': 'abc', 'Value': 123}, ...]
        if not data:
            return
            
        for point in data:
            tag = point.get('ApiTag')
            val = point.get('Value')
            if tag in self.sensor_widgets:
                self.sensor_widgets[tag].update_value(val)

class SmartFarmApp(MDApp):
    device_id = StringProperty(DEFAULT_DEVICE_ID)

    def build(self):
        font_path = resource_find("assets/fonts/simhei.ttf") or resource_find("simhei.ttf")
        if not font_path and platform == "android":
            candidates = [
                "/system/fonts/NotoSansCJK-Regular.ttc",
                "/system/fonts/NotoSansSC-Regular.otf",
                "/system/fonts/SourceHanSansSC-Regular.otf",
                "/system/fonts/DroidSansFallback.ttf",
            ]
            for p in candidates:
                if os.path.exists(p):
                    font_path = p
                    break
        if not font_path and platform != "android":
            p = "C:/Windows/Fonts/simhei.ttf"
            font_path = p if os.path.exists(p) else None
        if font_path:
            LabelBase.register(name="Roboto", fn_regular=font_path, fn_bold=font_path)
            LabelBase.register(name="CJK", fn_regular=font_path, fn_bold=font_path)
        
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        
        if font_path:
            for style in self.theme_cls.font_styles:
                if style != "Icon":
                    self.theme_cls.font_styles[style][0] = "CJK"
            
        self.nle = NLECloudAPI()
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

    def change_screen(self, name):
        self.root.current = name

if __name__ == '__main__':
    SmartFarmApp().run()
