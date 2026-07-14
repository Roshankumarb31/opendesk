import flet as ft
from utils import AppIcons
from confirmation_dialogs import ConfirmationPage
from platform_adapter import VERSION, detect_available_terminals, detect_available_file_managers

APP_TYPES = [
    "VS Code", "File Explorer", "Command Prompt", "PowerShell",
    "Website", "Teams", "Outlook", "MongoDB Compass",
    "GitHub Desktop", "Postman", "Notepad", "Custom App"
]

class UIManager:
    def __init__(self, page, config_manager, app_launcher, startup_manager, config):
        self.page = page
        self.config_manager = config_manager
        self.app_launcher = app_launcher
        self.startup_manager = startup_manager
        self.config = config

        self.status_text = ft.Text("Ready!", color="#B4BACC", size=12, weight=ft.FontWeight.W_500)
        self.confirmation_page = ConfirmationPage(page, self)

        self.file_picker = ft.FilePicker(on_result=self.on_file_picker_result)
        self.page.overlay.append(self.file_picker)
        self.current_item = None
        self._file_picker_action = None
        self._import_config_data = None

        self._apply_theme()
        self._command_palette_open = False

    def _apply_theme(self):
        theme = self.config.get("theme", {})
        self.C = {
            'bg': theme.get('bg', '#16171C'),
            'surface': theme.get('surface', '#21222A'),
            'primary': theme.get('primary', '#4B8CFF'),
            'accent': theme.get('accent', '#FFD952'),
            'danger': theme.get('danger', '#FF4B7A'),
            'gray': theme.get('gray', '#23242B'),
            'text': theme.get('text', '#ECECF1'),
            'subtext': theme.get('subtext', '#FFFFFF'),
        }

    def setup_ui(self):
        self.page.title = "OpenDesk Launcher"
        self.page.window_width = 1100
        self.page.window_height = 750
        self.page.bgcolor = self.C['bg']
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        self.page.on_keyboard_event = self._on_keyboard
        self.show_main_page()

    def _on_keyboard(self, e):
        if e.key == " " and (e.ctrl or e.meta):
            e.handled = True
            self.toggle_command_palette()
        elif e.key == "Escape":
            if self._command_palette_open:
                self.show_main_page()

    def toggle_command_palette(self):
        if self._command_palette_open:
            self.show_main_page()
        else:
            self._show_command_palette()

    def _show_command_palette(self):
        self._command_palette_open = True
        search_field = ft.TextField(
            hint_text="Search and launch app...",
            autofocus=True,
            width=500,
            height=45,
            bgcolor=self.C['gray'],
            border_color=self.C['primary'],
            content_padding=ft.padding.all(12),
            color=self.C['text'],
            text_size=16,
            on_change=lambda e: self._update_palette_results(e, results_column, search_field)
        )
        results_column = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO)

        def on_result_click(item):
            self._command_palette_open = False
            self.app_launcher.launch_item(item)
            self.show_main_page()
            self.update_status(f"Launched {item.get('name', 'Unknown')}.", self.C['primary'])

        def update_results(e):
            self._update_palette_results(e, results_column, search_field)

        search_field.on_change = update_results
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Container(height=80),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.SEARCH, color=self.C['subtext'], size=20),
                                ft.Text("Command Palette", size=14, color=self.C['subtext'],
                                        weight=ft.FontWeight.W_500)
                            ], spacing=8),
                            search_field,
                            ft.Container(
                                content=results_column,
                                height=300,
                                expand=True
                            ),
                            ft.Text("Ctrl+Space to open  |  ↑↓ to navigate  |  Enter to launch",
                                    size=11, color=self.C['subtext'])
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                        width=560,
                        padding=20,
                        bgcolor=self.C['surface'],
                        border_radius=14,
                        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color="#00000080", offset=ft.Offset(0, 4))
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.alignment.center
            )
        )
        self.page.update()
        self._update_palette_results(None, results_column, search_field)

    def _update_palette_results(self, e, results_column, search_field):
        term = (search_field.value or "").lower()
        items = self.config.get("launch_items", [])
        if term:
            items = [i for i in items if term in i.get("name", "").lower() or term in i.get("type", "").lower()]
        items = [i for i in items if i.get("enabled", True)]
        items = items[:20]
        results_column.controls.clear()
        for item in items:
            icon = AppIcons.get_icon(item.get("type", "VS Code"), item.get("path"))
            icon_widget = ft.Image(src=icon, width=20, height=20) if isinstance(icon, str) and icon.endswith(".png") else ft.Text(icon, size=16)
            results_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        icon_widget,
                        ft.Column([
                            ft.Text(item.get("name", ""), size=14, color=self.C['text']),
                            ft.Text(item.get("type", ""), size=11, color=self.C['subtext'])
                        ], spacing=1, expand=True),
                        ft.Icon(ft.Icons.PLAY_ARROW, size=16, color=self.C['primary'])
                    ], spacing=10),
                    padding=10,
                    border_radius=8,
                    bgcolor=self.C['gray'],
                    on_click=lambda _, i=item: self._palette_launch(i, results_column, search_field)
                )
            )
        if not results_column.controls:
            results_column.controls.append(
                ft.Container(
                    content=ft.Text("No matching apps found", color=self.C['subtext'], size=13),
                    padding=20, alignment=ft.alignment.center
                )
            )
        self.page.update()

    def _palette_launch(self, item, results_column, search_field):
        self._command_palette_open = False
        self.app_launcher.launch_item(item)
        self.show_main_page()
        self.update_status(f"Launched {item.get('name', 'Unknown')}.", self.C['primary'])

    def on_file_picker_result(self, e: ft.FilePickerResultEvent):
        action = self._file_picker_action
        self._file_picker_action = None
        if action == "browse_folder" and e.path and self.current_item:
            self.current_item["path"] = e.path
            self.config_manager.save_config(self.config)
            self.refresh_ui()
            self.update_status(f"Selected: {e.path}", self.C['primary'])
        elif action == "browse_file" and e.files and self.current_item:
            self.current_item["path"] = e.files[0].path
            self.config_manager.save_config(self.config)
            self.refresh_ui()
            self.update_status(f"Selected: {e.files[0].path}", self.C['primary'])
        elif action == "export_config" and e.path:
            if self.config_manager.export_config(e.path):
                self.update_status(f"Config exported to {e.path}", self.C['primary'])
            else:
                self.update_status("Failed to export config", self.C['danger'])
        elif action == "import_config" and e.files:
            data = self.config_manager.import_config(e.files[0].path)
            if data is not None:
                self._show_import_options(data)
            else:
                self.update_status("Failed to import config", self.C['danger'])

    def _show_import_options(self, imported_data):
        count = len(imported_data.get("launch_items", []))
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Import Configuration"),
            content=ft.Text(f"Found {count} apps in the imported file.\n\nChoose how to import:"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self._dismiss_dialog(dlg)),
                ft.TextButton("Replace All", on_click=lambda e: self._do_import_replace(imported_data, dlg)),
                ft.TextButton("Merge", on_click=lambda e: self._do_import_merge(imported_data, dlg)),
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _dismiss_dialog(self, dlg):
        dlg.open = False
        self.page.update()

    def _do_import_replace(self, data, dlg):
        self.config["launch_items"] = data.get("launch_items", [])
        if "theme" in data:
            self.config["theme"] = data["theme"]
        if "settings" in data:
            self.config["settings"] = data["settings"]
        self.config_manager.save_config(self.config)
        dlg.open = False
        self._apply_theme()
        self.refresh_ui()
        self.update_status(f"Imported {len(self.config['launch_items'])} apps (replaced).", self.C['primary'])

    def _do_import_merge(self, data, dlg):
        existing = self.config.setdefault("launch_items", [])
        existing.extend(data.get("launch_items", []))
        if "theme" in data and data["theme"] != self.config.get("theme"):
            for k, v in data["theme"].items():
                self.config.setdefault("theme", {})[k] = v
        self.config_manager.save_config(self.config)
        dlg.open = False
        self._apply_theme()
        self.refresh_ui()
        self.update_status(f"Merged: {len(self.config['launch_items'])} total apps.", self.C['primary'])

    def _make_icon_widget(self, app_icon):
        if isinstance(app_icon, str) and app_icon.endswith(".png"):
            return ft.Image(src=app_icon, width=24, height=24)
        return ft.Text(app_icon, size=18)

    def create_header(self):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Text("⚡", size=24, color=self.C['primary']),
                        bgcolor=self.C['gray'],
                        border_radius=8,
                        width=40, height=40,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Text("OpenDesk", size=18, weight=ft.FontWeight.BOLD, color=self.C['text']),
                            ft.Container(
                                content=ft.Text(f"v{VERSION}", size=10, color=self.C['subtext'],
                                                weight=ft.FontWeight.W_500),
                                bgcolor=self.C['gray'],
                                border_radius=4,
                                padding=ft.padding.symmetric(horizontal=6, vertical=2)
                            )
                        ], spacing=6),
                        ft.Text("Developer Launcher", size=11, color=self.C['subtext'])
                    ], spacing=1)
                ], spacing=10),
                ft.Row([
                    ft.TextField(
                        hint_text="Search app... (Ctrl+Space)",
                        width=240,
                        height=35,
                        bgcolor=self.C['gray'],
                        border_color="transparent",
                        content_padding=ft.padding.all(10),
                        hint_style=ft.TextStyle(color=self.C['subtext'], size=12),
                        color=self.C['text'],
                        text_size=13,
                        on_change=self.filter_items
                    ),
                    ft.IconButton(
                        icon=ft.Icons.INFO_OUTLINE,
                        icon_color=self.C['subtext'],
                        icon_size=20,
                        tooltip="About OpenDesk",
                        on_click=self.show_about_dialog
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        icon_color=self.C['subtext'],
                        icon_size=20,
                        tooltip="Settings",
                        on_click=self.show_settings_dialog
                    )
                ], spacing=4)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=22,
            bgcolor=self.C['surface'],
            border_radius=14,
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=14, color='#14151A', offset=ft.Offset(0, 2))
        )

    def show_about_dialog(self, e=None):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Text("⚡", size=24),
                ft.Text("OpenDesk", size=20, weight=ft.FontWeight.BOLD)
            ], spacing=8),
            content=ft.Column([
                ft.Text(f"Version {VERSION}", size=14, color=self.C['subtext']),
                ft.Text("A sleek developer launcher for Windows & Linux.", size=13, color=self.C['subtext']),
                ft.Container(height=10),
                ft.Text("Built with Python + Flet", size=12, color=self.C['subtext'], italic=True),
                ft.Container(height=10),
                ft.Text("GitHub: Roshankumarb31/opendesk", size=12, color=self.C['primary']),
                ft.Text("MIT License © 2025 Roshan Kumar B", size=11, color=self.C['subtext'])
            ], spacing=2, width=350),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self._dismiss_dialog(dlg))
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def show_settings_dialog(self, e=None):
        from platform_adapter import SYSTEM
        theme = self.config.get("theme", {})
        settings = self.config.get("settings", {})

        fields = {}
        for key in ["bg", "surface", "primary", "accent", "danger", "gray", "text", "subtext"]:
            fields[key] = ft.TextField(
                value=theme.get(key, ""), label=key.capitalize(),
                width=120, height=40, text_size=12,
                bgcolor=self.C['gray'], border_color="transparent",
                color=self.C['text']
            )

        terminals = detect_available_terminals()
        file_managers = detect_available_file_managers()

        term_dd = ft.Dropdown(
            value=settings.get("terminal_profile", "auto"),
            options=[ft.dropdown.Option(k, text=k.replace("_", " ").title()) for k in ["auto"] + terminals],
            width=250, bgcolor=self.C['gray'], border_color="transparent",
            color=self.C['text']
        )
        fm_dd = ft.Dropdown(
            value=settings.get("file_manager", "auto"),
            options=[ft.dropdown.Option(k, text=k.replace("_", " ").title() if k != "auto" else "Auto Detect") for k in ["auto"] + file_managers],
            width=250, bgcolor=self.C['gray'], border_color="transparent",
            color=self.C['text']
        )

        def save_settings(e):
            for key, field in fields.items():
                if field.value:
                    self.config.setdefault("theme", {})[key] = field.value
            self.config.setdefault("settings", {})["terminal_profile"] = term_dd.value
            self.config["settings"]["file_manager"] = fm_dd.value
            self.config_manager.save_config(self.config)
            self._apply_theme()
            dlg.open = False
            self.refresh_ui()
            self.update_status("Settings saved.", self.C['primary'])

        def reset_theme(e):
            from config_manager import DEFAULT_THEME
            for key, val in DEFAULT_THEME.items():
                if key in fields:
                    fields[key].value = val
            self.page.update()

        color_row = ft.Column(
            [ft.Row([fields[k] for k in row], spacing=8) for row in
             [["bg", "surface", "gray"], ["text", "subtext", "primary"], ["accent", "danger"]]],
            spacing=6
        )

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Settings", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Theme Colors", size=14, weight=ft.FontWeight.W_500),
                    color_row,
                    ft.Container(
                        content=ft.TextButton("Reset to Default", on_click=reset_theme),
                        alignment=ft.alignment.center
                    ),
                    ft.Divider(height=20),
                    ft.Text("Terminal Profile", size=14, weight=ft.FontWeight.W_500),
                    term_dd,
                    ft.Container(height=10),
                    ft.Text("File Manager", size=14, weight=ft.FontWeight.W_500),
                    fm_dd,
                ], spacing=4, width=420, scroll=ft.ScrollMode.AUTO),
                height=450
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self._dismiss_dialog(dlg)),
                ft.TextButton("Save", on_click=save_settings)
            ]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def create_reorderable_list(self, filtered_items=None):
        launch_items = filtered_items if filtered_items is not None else self.config.get('launch_items', [])
        controls = []
        for idx, item in enumerate(launch_items):
            app_icon = AppIcons.get_icon(item.get('type', 'VS Code'), item.get('path'))
            enabled = item.get('enabled', True)
            needs_folder_browse = item.get('type', '') in ['VS Code', 'File Explorer', 'Command Prompt', 'PowerShell']
            is_website = item.get('type', '') == 'Website'
            is_custom = item.get('type', '') == 'Custom App'
            controls.append(
                ft.Container(
                    key=str(idx),
                    content=self._create_row_content(
                        item, idx, app_icon, enabled, needs_folder_browse, is_website, is_custom
                    )
                )
            )

        def on_reorder(e):
            if e.old_index == e.new_index:
                return
            launch_items.insert(e.new_index, launch_items.pop(e.old_index))
            self.config_manager.save_config(self.config)

        self.reorderable_list = ft.ReorderableListView(
            expand=True,
            on_reorder=on_reorder,
            controls=controls
        )
        return self.reorderable_list

    def _create_row_content(self, item, index, app_icon, enabled, needs_folder_browse, is_website, is_custom):
        icon_widget = self._make_icon_widget(app_icon)
        group_val = item.get("group", "")

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.DRAG_INDICATOR, size=16, color=self.C['subtext']),
                    width=20, alignment=ft.alignment.center
                ),
                ft.Container(
                    content=icon_widget,
                    width=34, height=34,
                    bgcolor=self.C['gray'],
                    border_radius=7,
                    alignment=ft.alignment.center
                ),
                ft.TextField(
                    value=item.get("name", ""),
                    hint_text="Name",
                    width=100, bgcolor="transparent",
                    border_color="transparent",
                    color=self.C['text'], text_size=13,
                    on_change=lambda e: self.update_item_name(item, e.control.value)
                ),
                ft.Dropdown(
                    value=item.get("type", "VS Code"),
                    options=[ft.dropdown.Option(k, text=k, text_style=ft.TextStyle(color="#A59E9E")) for k in APP_TYPES],
                    width=130, bgcolor=self.C['gray'], border_color="transparent",
                    color=self.C['text'],
                    on_change=lambda e: self.update_item_type(item, e.control.value, index)
                ),
                ft.Row([
                    ft.TextField(
                        value=item.get("path", ""),
                        hint_text="App path" if is_custom else ("URL" if is_website else "Path"),
                        width=110 if is_custom else (100 if is_website else (120 if needs_folder_browse else 150)),
                        bgcolor=self.C['gray'], border_color="transparent",
                        color=self.C['text'], text_size=12,
                        on_change=lambda e: self.update_item_path(item, e.control.value)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.FOLDER_OPEN, tooltip="Browse",
                        icon_color=self.C['primary'], bgcolor=self.C['surface'],
                        on_click=lambda e: self.browse_file(item, is_custom)
                    ) if needs_folder_browse or is_custom else ft.Container(width=0)
                ], spacing=3),
                ft.Dropdown(
                    value=item.get("browser", "chrome"),
                    options=[ft.dropdown.Option(b, text=b.title(), text_style=ft.TextStyle(color="#A59E9E"))
                             for b in ["chrome", "edge", "brave", "firefox"]],
                    width=90, bgcolor=self.C['gray'], border_color="transparent",
                    color=self.C['text'], visible=is_website,
                    on_change=lambda e: self.update_item_browser(item, e.control.value)
                ) if is_website else ft.Container(width=0),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY_OFF, size=14, color=self.C['subtext']),
                        ft.Switch(value=item.get("incognito", False), scale=0.5,
                                  active_color=self.C['accent'],
                                  on_change=lambda e: self.update_item_incognito(item, e.control.value))
                    ], spacing=1),
                    visible=is_website,
                ) if is_website else ft.Container(width=0),
                ft.TextField(
                    value=group_val,
                    hint_text="Group",
                    width=60, bgcolor="transparent",
                    border_color="transparent",
                    color=self.C['subtext'], text_size=11,
                    on_change=lambda e: self._update_item_group(item, e.control.value)
                ),
                ft.Switch(value=enabled, scale=0.7, active_color=self.C['primary'],
                          on_change=lambda e: self.update_item_enabled(item, e.control.value)),
                ft.IconButton(icon=ft.Icons.PLAY_ARROW, tooltip="Launch",
                              icon_color=self.C['primary'], bgcolor=self.C['surface'],
                              on_click=lambda e: self.launch_single_item(item)),
                ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, tooltip="Delete",
                              icon_color=self.C['danger'], bgcolor=self.C['surface'],
                              on_click=lambda e: self.delete_item(index))
            ], spacing=4),
            padding=8, bgcolor=self.C['surface'] if enabled else self.C['gray'],
            border_radius=9,
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=9, color='#14151A', offset=ft.Offset(0, 2)),
            margin=ft.margin.only(bottom=4)
        )

    def _update_item_group(self, item, group):
        if group:
            item["group"] = group
        else:
            item.pop("group", None)
        self.config_manager.save_config(self.config)

    def create_startup_panel(self):
        from platform_adapter import SYSTEM
        label = "Auto-launch at startup" if SYSTEM != "Windows" else "Auto-launch with Windows"
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.POWER_SETTINGS_NEW, color=self.C['accent'], size=18),
                ft.Text(label, size=12, color=self.C['subtext']),
                ft.Switch(
                    value=self.startup_manager.is_in_startup(),
                    on_change=self.toggle_startup,
                    active_color=self.C['primary'],
                    scale=0.8
                ),
                ft.Container(expand=True),
                ft.Text("Ctrl+Space  ", size=10, color=self.C['subtext'], italic=True),
                ft.Container(
                    content=ft.Text("Quick Launch", size=10, color="#000000", weight=ft.FontWeight.W_500),
                    bgcolor=self.C['accent'], border_radius=4,
                    padding=ft.padding.symmetric(horizontal=6, vertical=2)
                )
            ]),
            padding=12, bgcolor=self.C['gray'], border_radius=10
        )

    def _pill(self, text, icon, on_click, bg, fg):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=fg, size=15),
                ft.Text(text, color=fg, size=12, weight=ft.FontWeight.W_600)
            ], spacing=5, tight=True),
            bgcolor=bg,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=14, vertical=7),
            on_click=on_click,
        )

    def create_action_bar(self):
        groups = self._get_all_groups()
        return ft.Container(
            content=ft.Row([
                self._pill("Launch All", ft.Icons.ROCKET_LAUNCH, self.launch_selected, self.C['primary'], "#000000"),
                self._pill("Select All", ft.Icons.CHECK_BOX, self.toggle_select_all, "#464757", "#ffffff"),
                ft.Dropdown(
                    value="", width=140, bgcolor=self.C['gray'], border_color="transparent",
                    color=self.C['text'],
                    options=[ft.dropdown.Option("", text="All Groups")] +
                            [ft.dropdown.Option(g, text=g) for g in groups],
                    on_change=self._filter_by_group
                ),
                ft.Container(expand=True),
                self._pill("Import", ft.Icons.UPLOAD_FILE, self.import_config_action, "#464757", "#ffffff"),
                self._pill("Export", ft.Icons.DOWNLOAD, self.export_config_action, "#464757", "#ffffff"),
                self._pill("Delete All", ft.Icons.DELETE_SWEEP, self.show_delete_all_confirmation, self.C['danger'], "#000000"),
                self._pill("Close All", ft.Icons.CLOSE, self.show_close_all_confirmation, self.C['accent'], "#000000"),
            ], spacing=8, scroll=ft.ScrollMode.AUTO),
            padding=ft.padding.only(left=6, bottom=6, top=2)
        )

    def _get_all_groups(self):
        groups = set()
        for item in self.config.get("launch_items", []):
            g = item.get("group", "")
            if g:
                groups.add(g)
        return sorted(groups)

    def _filter_by_group(self, e):
        group = e.control.value
        if not group:
            self.refresh_ui()
            return
        items = [i for i in self.config.get("launch_items", []) if i.get("group", "") == group]
        self._show_filtered(items, f"Group: {group}")

    def _show_filtered(self, items, label):
        self.page.controls.clear()
        main_content = ft.Column([
            self.create_header(),
            self.create_startup_panel(),
            self.create_action_bar(),
            ft.Container(
                content=ft.Row([
                    ft.Text(label, size=14, weight=ft.FontWeight.BOLD, color=self.C['text']),
                    ft.Text(f"({len(items)} items)", size=11, color=self.C['subtext']),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Text("✕ Clear Filter", size=11, color=self.C['primary']),
                        on_click=lambda e: self.refresh_ui()
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.symmetric(horizontal=8, vertical=6)
            ),
            ft.Container(
                content=self.create_reorderable_list(filtered_items=items),
                expand=True,
                padding=ft.padding.symmetric(horizontal=12, vertical=0),
                bgcolor=self.C['surface'], border_radius=13
            ),
            ft.Container(content=self.status_text, padding=10)
        ], spacing=12, expand=True)
        self.page.add(main_content)
        self.page.update()

    def browse_file(self, item, is_custom):
        self.current_item = item
        if is_custom:
            self._file_picker_action = "browse_file"
            self.file_picker.pick_files(dialog_title="Select Executable", allow_multiple=False)
        else:
            self._file_picker_action = "browse_folder"
            self.file_picker.get_directory_path(dialog_title=f"Select Folder")

    def show_main_page(self):
        self._command_palette_open = False
        self.page.controls.clear()
        main_content = ft.Column([
            self.create_header(),
            self.create_startup_panel(),
            self.create_action_bar(),
            ft.Container(
                content=ft.Row([
                    ft.Text("Applications", size=14, weight=ft.FontWeight.BOLD, color=self.C['text']),
                    ft.Container(
                        content=ft.Text("+ Add New", color="#000000", size=12, weight=ft.FontWeight.W_500),
                        bgcolor=self.C['primary'], border_radius=8,
                        padding=ft.padding.symmetric(horizontal=14, vertical=6),
                        on_click=self.add_new_item
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.symmetric(horizontal=8, vertical=6)
            ),
            ft.Container(
                content=self.create_reorderable_list(),
                expand=True,
                padding=ft.padding.symmetric(horizontal=12, vertical=0),
                bgcolor=self.C['surface'], border_radius=13
            ),
            ft.Container(content=self.status_text, padding=8)
        ], spacing=10, expand=True)
        self.page.add(main_content)
        self.page.update()

    def refresh_ui(self):
        self.show_main_page()

    def filter_items(self, e):
        term = e.control.value.lower()
        if not term:
            self.refresh_ui()
            return
        items = [
            item for item in self.config.get('launch_items', [])
            if term in item.get("name", "").lower() or term in item.get("type", "").lower()
        ]
        self.page.controls.clear()
        main_content = ft.Column([
            self.create_header(),
            self.create_startup_panel(),
            self.create_action_bar(),
            ft.Container(
                content=ft.Row([
                    ft.Text(f"Search: {len(items)}/{len(self.config.get('launch_items', []))}",
                            size=14, weight=ft.FontWeight.BOLD, color=self.C['text']),
                    ft.Container(
                        content=ft.Text("✕ Clear", size=11, color=self.C['primary']),
                        on_click=lambda e: self._clear_search()
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.symmetric(horizontal=8, vertical=6)
            ),
            ft.Container(
                content=self.create_reorderable_list(filtered_items=items),
                expand=True,
                padding=ft.padding.symmetric(horizontal=12, vertical=0),
                bgcolor=self.C['surface'], border_radius=13
            ),
            ft.Container(content=self.status_text, padding=10)
        ], spacing=12, expand=True)
        self.page.add(main_content)
        self.page.update()

    def _clear_search(self):
        self.refresh_ui()

    def update_status(self, msg, color=None):
        self.status_text.value = msg
        self.status_text.color = color or self.C['subtext']
        try:
            if hasattr(self.status_text, 'page') and self.status_text.page is not None:
                self.status_text.update()
        except AssertionError:
            pass

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

    def update_item_browser(self, item, browser):
        item["browser"] = browser
        self.config_manager.save_config(self.config)
        self.update_status(f"Browser: {browser.title()}", self.C['primary'])

    def update_item_incognito(self, item, incognito):
        item["incognito"] = incognito
        self.config_manager.save_config(self.config)

    def delete_item(self, index):
        launch_items = self.config.get("launch_items", [])
        if 0 <= index < len(launch_items):
            del launch_items[index]
            self.config_manager.save_config(self.config)
            self.refresh_ui()
            self.update_status("Deleted app.", self.C['danger'])

    def add_new_item(self, e):
        launch_items = self.config.get("launch_items", [])
        existing_names = [item.get("name", "") for item in launch_items]
        import re
        used_numbers = []
        for name in existing_names:
            match = re.search(r"New App (\d+)", name)
            if match:
                used_numbers.append(int(match.group(1)))
        used_numbers.sort()
        next_number = 1
        for num in used_numbers:
            if num == next_number:
                next_number += 1
            elif num > next_number:
                break
        new_item = {
            "type": "VS Code",
            "name": f"New App {next_number}",
            "path": "",
            "browser": "chrome",
            "incognito": False,
            "enabled": True
        }
        self.config.setdefault("launch_items", []).append(new_item)
        self.config_manager.save_config(self.config)
        self.refresh_ui()
        self.update_status(f"Added New App {next_number}!", self.C['primary'])

    def launch_selected(self, e):
        items = self.app_launcher.get_enabled_items(self.config)
        launched = self.app_launcher.launch_group(items)
        self.update_status(f"Launched {launched} apps.", self.C['primary'])

    def toggle_select_all(self, e):
        launch_items = self.config.get("launch_items", [])
        if not launch_items:
            return
        all_enabled = all(item.get("enabled", True) for item in launch_items)
        for item in launch_items:
            item["enabled"] = not all_enabled
        self.config_manager.save_config(self.config)
        self.refresh_ui()
        self.update_status("All apps selected." if not all_enabled else "All apps deselected.", self.C['primary'])

    def delete_all(self, e):
        if "launch_items" in self.config:
            self.config["launch_items"].clear()
            self.config_manager.save_config(self.config)
            self.refresh_ui()

    def close_all(self, e):
        count = self.app_launcher.close_all_windows()
        self.update_status(f"Closed {count} processes.", self.C['accent'])

    def show_confirmation_dialog(self, title, content_text, confirm_text, confirm_action):
        dlg = ft.AlertDialog(
            modal=True, title=ft.Text(title),
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
        self.delete_all(None)

    def show_close_all_confirmation(self, e=None):
        self.confirmation_page.show_close_confirmation()

    def close_all_actual(self):
        self.close_all(None)

    def launch_single_item(self, item):
        if self.app_launcher.launch_item(item):
            self.update_status(f"Launched {item.get('name', 'Unknown')}.", self.C['primary'])
        else:
            self.update_status(f"Failed to launch {item.get('name', 'Unknown')}.", self.C['danger'])

    def toggle_startup(self, e):
        enable = e.control.value
        from platform_adapter import SYSTEM
        platform_label = "startup" if SYSTEM != "Windows" else "Windows startup"
        if enable:
            if self.startup_manager.add_to_startup():
                self.update_status(f"Added to {platform_label}.", self.C['primary'])
            else:
                self.update_status("Failed to add to startup.", self.C['danger'])
                e.control.value = False
        else:
            if self.startup_manager.remove_from_startup():
                self.update_status(f"Removed from {platform_label}.", self.C['accent'])
            else:
                self.update_status("Failed to remove from startup.", self.C['danger'])
                e.control.value = True
        e.control.update()

    def import_config_action(self, e):
        self._file_picker_action = "import_config"
        self.file_picker.pick_files(
            dialog_title="Import Configuration",
            allow_multiple=False,
            allowed_extensions=["json"]
        )

    def export_config_action(self, e):
        self._file_picker_action = "export_config"
        self.file_picker.save_file(
            dialog_title="Export Configuration",
            file_name="opendesk_config_backup.json"
        )
