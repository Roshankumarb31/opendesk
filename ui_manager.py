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

        self.file_picker = ft.FilePicker(on_result=self.on_folder_selected)
        self.page.overlay.append(self.file_picker)
        self.current_item = None  # Track which item we're updating

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
            'subtext': "#FFFFFF",    # secondary text
            'dropdown_text': '#FFFFFF'
        }

    def setup_ui(self):
        self.page.title = "OpenDesk Simple Launcher (Dark)"
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.bgcolor = self.Colors['bg']
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
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



    def on_folder_selected(self, e: ft.FilePickerResultEvent):
        if e.path and self.current_item:
            # Update the path field with selected folder/file
            self.current_item["path"] = e.path
            self.config_manager.save_config(self.config)
            self.refresh_ui()
            self.update_status(f"Selected: {e.path}", self.Colors['primary'])

    def create_app_row(self, item, index):
        app_icon = AppIcons.get_icon(item.get("type", "VS Code"))
        enabled = item.get("enabled", True)
        
        # Check if this type needs folder browsing
        needs_folder_browse = item.get("type", "") in [
            "VS Code", "File Explorer", "Command Prompt", "PowerShell"
        ]
        
        return ft.Container(
            content=ft.Row([
                # ... your existing controls (icon, name, dropdown) ...
                
                # Path field with browse button
                ft.Row([
                    ft.TextField(
                        value=item.get("path", ""),
                        hint_text="Path/URL",
                        width=140 if needs_folder_browse else 180,
                        bgcolor=self.Colors['gray'],
                        border_color="transparent",
                        color=self.Colors['text'],
                        text_size=13,
                        on_change=lambda e: self.update_item_path(item, e.control.value)
                    ),
                    # Add browse button for specific types
                    ft.IconButton(
                        icon=ft.Icons.FOLDER_OPEN,
                        tooltip="Browse Folder",
                        icon_color=self.Colors['primary'],
                        bgcolor=self.Colors['surface'],
                        visible=needs_folder_browse,
                        on_click=lambda e: self.browse_folder(item)
                    ) if needs_folder_browse else ft.Container(width=0)
                ], spacing=5),
                
                # ... rest of your existing controls (switch, play, delete) ...
                
            ], spacing=12),
            # ... rest of your container properties ...
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
    

    def update_item_browser(self, item, browser):
        item["browser"] = browser
        self.config_manager.save_config(self.config)
        self.update_status(f"Browser set to {browser.title()}", self.Colors['primary'])

    def update_item_incognito(self, item, incognito):
        item["incognito"] = incognito
        self.config_manager.save_config(self.config)
        mode = "incognito" if incognito else "normal"
        self.update_status(f"Mode set to {mode}", self.Colors['accent'])




    def create_action_bar(self):
        return ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ROCKET_LAUNCH, color="#000000", size=16),
                        ft.Text("Launch Selected", color="#000000", size=13, weight=ft.FontWeight.W_500)
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
        
        # Check if this type needs folder browsing
        needs_folder_browse = item.get("type", "") in [
            "VS Code", "File Explorer", "Command Prompt", "PowerShell"
        ]
        
        # Check if this is a website
        is_website = item.get("type", "") == "Website"
        icon_widget = (
            ft.Image(src=app_icon, width=24, height=24)
            if isinstance(app_icon, str) and app_icon.endswith(".png")
            else ft.Text(app_icon, size=18)
        )
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=icon_widget,
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
                    options=[ft.dropdown.Option(
                        key=t,
                        text=t,
                        text_style=ft.TextStyle(color="#A59E9E")
                    ) for t in ["VS Code", "File Explorer", "Command Prompt", "PowerShell",
                            "Website", "Teams", "Outlook", "MongoDB Compass",
                            "GitHub Desktop", "Postman", "Notepad"]],
                    width=150,
                    bgcolor=self.Colors['gray'],
                    border_color="transparent",
                    color=self.Colors['dropdown_text'],
                    text_style=ft.TextStyle(color=self.Colors['dropdown_text']),
                    on_change=lambda e: self.update_item_type(item, e.control.value, index)
                ),
                
                # URL/Path field
                ft.Row([
                    ft.TextField(
                        value=item.get("path", ""),
                        hint_text="URL (Optional)" if is_website else "Path/URL",
                        width=120 if is_website else (140 if needs_folder_browse else 180),
                        bgcolor=self.Colors['gray'],
                        border_color="transparent",
                        color=self.Colors['text'],
                        text_size=13,
                        on_change=lambda e: self.update_item_path(item, e.control.value)
                    ),
                    # Browse button for file types
                    ft.IconButton(
                        icon=ft.Icons.FOLDER_OPEN,
                        tooltip="Browse Folder",
                        icon_color=self.Colors['primary'],
                        bgcolor=self.Colors['surface'],
                        on_click=lambda e: self.browse_folder(item)
                    ) if needs_folder_browse else ft.Container(width=0)
                ], spacing=5),
                
                # Browser dropdown for websites
                ft.Dropdown(
                    value=item.get("browser", "chrome"),
                    options=[ft.dropdown.Option(
                        key=b,
                        text=b.title(),
                        text_style=ft.TextStyle(color="#A59E9E")
                    ) for b in ["chrome", "edge", "brave", "firefox"]],
                    width=130,
                    bgcolor=self.Colors['gray'],
                    border_color="transparent",
                    color=self.Colors['dropdown_text'],
                    text_style=ft.TextStyle(color=self.Colors['dropdown_text']),
                    visible=is_website,
                    on_change=lambda e: self.update_item_browser(item, e.control.value)
                ) if is_website else ft.Container(width=80),
                
                # Incognito toggle for websites
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY_OFF, size=16, color=self.Colors['subtext']),
                        ft.Switch(
                            value=item.get("incognito", False),
                            scale=0.6,
                            active_color=self.Colors['accent'],
                            on_change=lambda e: self.update_item_incognito(item, e.control.value)
                        )
                    ], spacing=2),
                    visible=is_website,
                    tooltip="Incognito Mode"
                ) if is_website else ft.Container(width=60),
                
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
            ], spacing=8),  # Reduced spacing to fit more controls
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
    def renumber_items(self):
        for i, item in enumerate(self.config.get("launch_items", []), start=1):
            if item.get("name", "").startswith("New App"):
                item["name"] = f"New App {i}"
        self.config_manager.save_config(self.config)

    def browse_folder(self, item):
        self.current_item = item
        item_type = item.get("type", "")
        
        if item_type == "File Explorer":
            # For File Explorer, select a directory
            self.file_picker.get_directory_path(
                dialog_title="Select Folder to Open"
            )
        elif item_type in ["VS Code", "Command Prompt", "PowerShell"]:
            # For these, also select directory (they can open in specific folders)
            self.file_picker.get_directory_path(
                dialog_title=f"Select Folder for {item_type}"
            )
        else:
            # For other types, pick files
            self.file_picker.pick_files(
                dialog_title="Select File",
                allow_multiple=False
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
            self.renumber_items()   # 🔹 Re-number here
            self.refresh_ui()
            self.update_status("Deleted app.", self.Colors['danger'])


    def add_new_item(self, e):
        new_item = {
            "type": "VS Code",
            "name": f"New App {len(self.config.get('launch_items', [])) + 1}",
            "path": "",
            "browser": "chrome",
            "incognito": False,
            "enabled": True
        }
        self.config.setdefault("launch_items", []).append(new_item)
        self.renumber_items()   # 🔹 Re-number after add
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
