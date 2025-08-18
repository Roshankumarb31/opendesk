import flet as ft
from utils import AppIcons
from confirmation_dialogs import ConfirmationPage

class UIManager:
    def __init__(self, page, config_manager, app_launcher, startup_manager, config):
        self.page = page
        self.config_manager = config_manager
        self.app_launcher = app_launcher
        self.startup_manager = startup_manager
        self.config = config

        self.items_column = ft.Column(spacing=8)
        self.status_text = ft.Text("Ready!", color="#B4BACC", size=12, weight=ft.FontWeight.W_500)
        self.confirmation_page = ConfirmationPage(page, self)

        # Dark theme palette
        self.Colors = {
            'bg': '#16171C',        # page background
            'surface': '#21222A',   # cards/rows
            'primary': '#4B8CFF',   # accents and icons
            'accent': '#FFD952',    # important switches
            'danger': '#FF4B7A',    # error/delete
            'gray': '#23242B',      # inputs backgrounds
            'shadow': '#14151A',    # subtle shadow
            'text': '#ECECF1',      # main text
            'subtext': '#8E93A8'    # secondary text
        }

    def setup_ui(self):
        self.page.title = "OpenDesk Simple Launcher (Dark)"
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.bgcolor = self.Colors['bg']
        self.show_main_page()

    def create_header(self):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Text("⚡", size=24, color=self.Colors['primary']),
                        bgcolor=self.Colors['gray'],
                        border_radius=8,
                        width=40, height=40,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.Text("OpenDesk", size=18, weight=ft.FontWeight.BOLD, color=self.Colors['text']),
                        ft.Text("Elegant App Launcher", size=11, color=self.Colors['subtext'])
                    ], spacing=1)
                ], spacing=10),
                ft.Container(
                    content=ft.Row([
                        ft.TextField(
                            hint_text="Search app...",
                            width=220,
                            height=35,
                            bgcolor=self.Colors['gray'],
                            border_color="transparent",
                            content_padding=ft.padding.all(10),
                            hint_style=ft.TextStyle(color=self.Colors['subtext'], size=13),
                            color=self.Colors['text'],
                            on_change=self.filter_items
                        )
                    ])
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=22,
            bgcolor=self.Colors['surface'],
            border_radius=14,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=14,
                color=self.Colors['shadow'],
                offset=ft.Offset(0, 2)
            )
        )

    def create_startup_panel(self):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.POWER_SETTINGS_NEW, color=self.Colors['accent'], size=20),
                ft.Text("Auto-launch OpenDesk with Windows", size=13, color=self.Colors['subtext']),
                ft.Switch(
                    value=self.startup_manager.is_in_startup(),
                    on_change=self.toggle_startup,
                    active_color=self.Colors['primary'],
                    scale=0.85
                )
            ]),
            padding=16,
            bgcolor=self.Colors['gray'],
            border_radius=12
        )
    




    def create_action_bar(self):
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ROCKET_LAUNCH, color="#000000", size=16),
                        ft.Text("Launch All", color="#000000", size=13, weight=ft.FontWeight.W_500)
                    ], spacing=6, tight=True),
                    bgcolor=self.Colors['primary'],
                    color="#000",
                    on_click=self.launch_selected,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    )
                ),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_BOX, color="#ffffff", size=16),
                        ft.Text("Select All", color="#ffffff", size=13, weight=ft.FontWeight.W_500)
                    ], spacing=6, tight=True),
                    bgcolor='#464757',
                    color="#FFF",
                    on_click=self.toggle_select_all,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    )
                ),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DELETE_SWEEP, color="#000000", size=16),
                        ft.Text("Delete All", color="#000000", size=13, weight=ft.FontWeight.W_500)
                    ], spacing=6, tight=True),
                    bgcolor=self.Colors['danger'],
                    color="#FFF",
                    on_click=self.show_delete_all_confirmation,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    )
                ),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE, color="#000000", size=16),
                        ft.Text("Close All", color="#000000", size=13, weight=ft.FontWeight.W_500)
                    ], spacing=6, tight=True),
                    bgcolor=self.Colors['accent'],
                    color="#FFF",
                    on_click=self.show_close_all_confirmation,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    )
                )


            ], spacing=12),
            padding=ft.padding.only(left=8, bottom=8)
        )



    def create_app_row(self, item, index):
        app_icon = AppIcons.get_icon(item.get("type", "VS Code"))
        enabled = item.get("enabled", True)
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(app_icon, size=18),
                    width=34, height=34,
                    bgcolor=self.Colors['gray'],
                    border_radius=7,
                    alignment=ft.alignment.center
                ),
                ft.TextField(
                    value=item.get("name", ""),
                    hint_text="Name",
                    width=120,
                    bgcolor="transparent",
                    border_color="transparent",
                    color=self.Colors['text'],
                    text_size=14,
                    on_change=lambda e: self.update_item_name(item, e.control.value)
                ),
                ft.Dropdown(
                    value=item.get("type", "VS Code"),
                    options=[ft.dropdown.Option(t) for t in [
                        "VS Code", "File Explorer", "Command Prompt", "PowerShell",
                        "Website", "Teams", "Outlook", "MongoDB Compass",
                        "GitHub Desktop", "Postman", "Notepad"]],
                    width=120,
                    bgcolor=self.Colors['gray'],
                    border_color="transparent",
                    color=self.Colors['subtext'],
                    on_change=lambda e: self.update_item_type(item, e.control.value, index)
                ),
                ft.TextField(
                    value=item.get("path", ""),
                    hint_text="Path/URL",
                    width=180,
                    bgcolor=self.Colors['gray'],
                    border_color="transparent",
                    color=self.Colors['text'],
                    text_size=13,
                    on_change=lambda e: self.update_item_path(item, e.control.value)
                ),
                ft.Switch(
                    value=enabled,
                    scale=0.8,
                    active_color=self.Colors['primary'],
                    on_change=lambda e: self.update_item_enabled(item, e.control.value)
                ),
                ft.IconButton(
                    icon=ft.Icons.PLAY_ARROW,
                    tooltip="Launch",
                    icon_color=self.Colors['primary'],
                    bgcolor=self.Colors['surface'],
                    on_click=lambda e: self.launch_single_item(item)
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    tooltip="Delete",
                    icon_color=self.Colors['danger'],
                    bgcolor=self.Colors['surface'],
                    on_click=lambda e: self.delete_item(index)
                )
            ], spacing=12),
            padding=10,
            bgcolor=self.Colors['surface'] if enabled else self.Colors['gray'],
            border_radius=9,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=9,
                color=self.Colors['shadow'],
                offset=ft.Offset(0, 2)
            ),
            margin=ft.margin.only(bottom=5)
        )

    def show_main_page(self):
        self.page.controls.clear()
        main_content = ft.Column([
            self.create_header(),
            self.create_startup_panel(),
            self.create_action_bar(),
            ft.Container(
                content=ft.Row([
                    ft.Text("Applications", size=15, weight=ft.FontWeight.BOLD, color=self.Colors['text']),
                    ft.Container(
                        content=ft.Text("+ Add New", color="#000000", size=13, weight=ft.FontWeight.W_500),
                        bgcolor=self.Colors['primary'],
                        border_radius=8,
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        on_click=self.add_new_item
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.symmetric(horizontal=8, vertical=8)
            ),
            ft.Container(
                content=ft.Column([self.items_column], scroll=ft.ScrollMode.AUTO, expand=True),
                expand=True,
                padding=ft.padding.symmetric(horizontal=12, vertical=0),
                bgcolor=self.Colors['surface'],
                border_radius=13
            ),
            ft.Container(
                content=self.status_text,
                padding=10
            )
        ], spacing=14, expand=True)
        self.page.add(main_content)
        self.refresh_ui()
        self.page.update()

    def refresh_ui(self):
        self.items_column.controls.clear()
        launch_items = self.config.get("launch_items", [])
        for i, item in enumerate(launch_items):
            self.items_column.controls.append(self.create_app_row(item, i))
        self.page.update()

    def filter_items(self, e):
        term = e.control.value.lower()
        self.items_column.controls.clear()
        for i, item in enumerate(self.config.get('launch_items', [])):
            if term in item.get("name", "").lower() or term in item.get("type", "").lower():
                self.items_column.controls.append(self.create_app_row(item, i))
        self.page.update()

    def update_status(self, msg, color=None):
        self.status_text.value = msg
        self.status_text.color = color or self.Colors['subtext']
        self.status_text.update()

    def update_item_type(self, item, new_type, idx):
        item["type"] = new_type
        self.config_manager.save_config(self.config)
        self.refresh_ui()

    def update_item_name(self, item, new_name):
        item["name"] = new_name
        self.config_manager.save_config(self.config)

    def update_item_path(self, item, new_path):
        item["path"] = new_path
        self.config_manager.save_config(self.config)

    def update_item_enabled(self, item, enabled):
        item["enabled"] = enabled
        self.config_manager.save_config(self.config)
        self.refresh_ui()

    def delete_item(self, index):
        launch_items = self.config.get("launch_items", [])
        if 0 <= index < len(launch_items):
            del launch_items[index]
            self.config_manager.save_config(self.config)
            self.refresh_ui()
            self.update_status("Deleted app.", self.Colors['danger'])

    def add_new_item(self, e):
        new_item = {
            "type": "VS Code",
            "name": f"New App {len(self.config.get('launch_items', [])) + 1}",
            "path": "",
            "browser": "chrome",
            "enabled": True
        }
        self.config.setdefault("launch_items", []).append(new_item)
        self.config_manager.save_config(self.config)
        self.refresh_ui()
        self.update_status("Added new app!", self.Colors['primary'])

    def launch_selected(self, e):
        items = [i for i in self.config.get("launch_items", []) if i.get("enabled", True)]
        launched = 0
        for item in items:
            if self.app_launcher.launch_item(item):
                launched += 1
        self.update_status(f"Launched {launched} apps.", self.Colors['primary'])

    def toggle_select_all(self, e):
        launch_items = self.config.get("launch_items", [])
        if not launch_items:
            return
        all_enabled = all(item.get("enabled", True) for item in launch_items)
        for item in launch_items:
            item["enabled"] = not all_enabled
        self.config_manager.save_config(self.config)
        self.refresh_ui()
        if all_enabled:
            self.update_status("All apps deselected.", self.Colors['subtext'])
        else:
            self.update_status("All apps selected.", self.Colors['primary'])

    def delete_all(self, e):
        if "launch_items" in self.config:
            count = len(self.config["launch_items"])
            self.config["launch_items"].clear()
            self.config_manager.save_config(self.config)
            self.refresh_ui()

    def close_all(self, e):
        count = self.app_launcher.close_all_windows()

    def show_confirmation_dialog(self, title, content_text, confirm_text, confirm_action):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(content_text),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: dlg.dismiss()),
                ft.TextButton(confirm_text, on_click=lambda e: [dlg.dismiss(), confirm_action()])
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def show_delete_all_confirmation(self, e=None):
        self.confirmation_page.show_delete_confirmation()


    def delete_all_actual(self):
        self.delete_all(None)  # Or pass appropriate event

    def show_close_all_confirmation(self, e=None):
        self.confirmation_page.show_close_confirmation()

    def close_all_actual(self):
        self.close_all(None)


    def launch_single_item(self, item):
        if self.app_launcher.launch_item(item):
            self.update_status(f"Launched {item.get('name', 'Unknown')}.", self.Colors['primary'])
        else:
            self.update_status(f"Failed to launch {item.get('name', 'Unknown')}.", self.Colors['danger'])

    def toggle_startup(self, e):
        enable = e.control.value
        if enable:
            if self.startup_manager.add_to_startup():
                self.update_status("Added to Windows startup.", self.Colors['primary'])
            else:
                self.update_status("Failed to add to startup.", self.Colors['danger'])
                e.control.value = False
        else:
            if self.startup_manager.remove_from_startup():
                self.update_status("Removed from Windows startup.", self.Colors['accent'])
            else:
                self.update_status("Failed to remove from startup.", self.Colors['danger'])
                e.control.value = True
        e.control.update()
