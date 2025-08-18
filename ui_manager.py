import flet as ft
from utils import AppIcons, format_path_display

class UIManager:
    def __init__(self, page, config_manager, app_launcher, startup_manager, config):
        self.page = page
        self.config_manager = config_manager
        self.app_launcher = app_launcher
        self.startup_manager = startup_manager
        self.config = config

        # UI state
        self.items_grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=280,
            child_aspect_ratio=1.2,
            spacing=20,
            run_spacing=20,
        )
        self.status_text = ft.Text("Ready to launch! 🚀", color="#10b981", size=13, weight=ft.FontWeight.W_500)
        
        # Futuristic color palette
        self.colors = {
            'bg_primary': '#0a0e27',
            'bg_secondary': '#1a1d3a',
            'sidebar': '#151831',
            'card_bg': '#1e2139',
            'accent_blue': '#4facfe',
            'accent_purple': '#8b5cf6',
            'accent_pink': '#ec4899',
            'accent_green': '#10b981',
            'accent_orange': '#f59e0b',
            'text_primary': '#ffffff',
            'text_secondary': '#94a3b8',
            'border': '#2d3748'
        }

    def setup_ui(self):
        """Initialize the stunning main UI"""
        self.page.title = "⚡ OpenDesk - Ultimate Launcher"
        self.page.window_width = 1400
        self.page.window_height = 800
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = self.colors['bg_primary']
        self.page.padding = 0
        
        self.show_main_page()

    def create_sidebar(self):
        """Create stunning sidebar with navigation - FIXED VERSION"""
        return ft.Container(
            width=280,
            bgcolor=self.colors['sidebar'],
            content=ft.Column([
                # Logo section
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text("⚡", size=32, color="#ffffff"),
                                width=60, height=60,
                                bgcolor=self.colors['accent_blue'],  # Simplified gradient
                                border_radius=16,
                                alignment=ft.alignment.center,
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=20,
                                    color=f"{self.colors['accent_blue']}40",
                                    offset=ft.Offset(0, 8)
                                )
                            ),
                            ft.Column([
                                ft.Text("OpenDesk", size=24, weight=ft.FontWeight.BOLD, color=self.colors['text_primary']),
                                ft.Text("Ultimate Launcher", size=12, color=self.colors['accent_blue'])
                            ], spacing=2, expand=True)  # FIXED: Added expand=True instead of flex
                        ], spacing=16),
                        
                        # Quick stats
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(str(len(self.config.get('launch_items', []))), 
                                               size=28, weight=ft.FontWeight.BOLD, color=self.colors['accent_green']),
                                        ft.Text("Apps", size=11, color=self.colors['text_secondary'])
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                                    expand=True  # FIXED: Changed flex=1 to expand=True
                                ),
                                ft.Container(width=1, height=40, bgcolor=self.colors['border']),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("✨", size=20),
                                        ft.Text("Ready", size=11, color=self.colors['text_secondary'])
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                                    expand=True  # FIXED: Changed flex=1 to expand=True
                                )
                            ]),
                            bgcolor=f"{self.colors['card_bg']}80",
                            border_radius=12,
                            padding=16,
                            margin=ft.margin.only(top=20)
                        )
                    ]),
                    padding=24
                ),

                # Navigation items
                ft.Container(
                    content=ft.Column([
                        self.create_nav_item("🏠", "Dashboard", True),
                        self.create_nav_item("⚙️", "Settings", False),
                        self.create_nav_item("📊", "Analytics", False),
                        self.create_nav_item("🎨", "Themes", False),
                    ]),
                    padding=ft.padding.symmetric(horizontal=16)
                ),

                # Startup toggle in sidebar
                ft.Container(
                    content=ft.Column([
                        ft.Text("Quick Controls", size=14, weight=ft.FontWeight.W_600, color=self.colors['text_secondary']),
                        ft.Container(height=8),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.ROCKET_LAUNCH, color=self.colors['accent_orange'], size=20),
                                ft.Column([
                                    ft.Text("Auto-start", size=13, weight=ft.FontWeight.W_500, color=self.colors['text_primary']),
                                    ft.Text("Launch with Windows", size=10, color=self.colors['text_secondary'])
                                ], spacing=0, expand=True),
                                ft.Switch(
                                    value=self.startup_manager.is_in_startup(),
                                    on_change=self.toggle_startup,
                                    active_color=self.colors['accent_green'],
                                    scale=0.8
                                )
                            ]),
                            bgcolor=f"{self.colors['card_bg']}60",
                            border_radius=12,
                            padding=12,
                            border=ft.border.all(1, f"{self.colors['border']}40")
                        )
                    ]),
                    padding=16,
                    margin=ft.margin.only(top=20)
                ),

                # Status section
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CIRCLE, color=self.colors['accent_green'], size=8),
                        self.status_text
                    ], spacing=8),
                    padding=16,
                    margin=ft.margin.only(top=20)
                )
            ], spacing=0),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=30,
                color="#00000030",
                offset=ft.Offset(8, 0)
            )
        )

    def create_nav_item(self, icon, text, active=False):
        """Create navigation item"""
        return ft.Container(
            content=ft.Row([
                ft.Text(icon, size=18),
                ft.Text(text, size=14, weight=ft.FontWeight.W_500, 
                       color=self.colors['text_primary'] if active else self.colors['text_secondary'])
            ], spacing=12),
            bgcolor=f"{self.colors['accent_blue']}20" if active else "transparent",
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            margin=ft.margin.only(bottom=4),
            border=ft.border.all(1, f"{self.colors['accent_blue']}40" if active else "transparent")
        )

    def create_header(self):
        """Create main content header"""
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("Your Applications", size=28, weight=ft.FontWeight.BOLD, color=self.colors['text_primary']),
                    ft.Text("Launch your favorite apps with style ✨", size=14, color=self.colors['text_secondary'])
                ], spacing=4),
                
                ft.Row([
                    # Search bar
                    ft.Container(
                        content=ft.TextField(
                            hint_text="🔍 Search apps...",
                            hint_style=ft.TextStyle(color=self.colors['text_secondary'], size=14),
                            color=self.colors['text_primary'],
                            border_color="transparent",
                            bgcolor=f"{self.colors['card_bg']}80",
                            width=300,
                            height=45,
                            border_radius=25,
                            content_padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            on_change=self.filter_items
                        )
                    ),
                    
                    # Action buttons
                    self.create_gradient_button("🚀 Launch All", self.launch_selected, self.colors['accent_green']),
                    self.create_gradient_button("➕ Add App", self.add_new_item, self.colors['accent_blue']),
                    self.create_icon_btn(ft.Icons.REFRESH, self.refresh_ui, self.colors['accent_orange']),
                ], spacing=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=32,
            bgcolor=f"{self.colors['bg_secondary']}80"
        )

    def create_gradient_button(self, text, on_click, color):
        """Create gradient button - simplified"""
        return ft.Container(
            content=ft.Text(text, color="#ffffff", size=13, weight=ft.FontWeight.W_600),
            bgcolor=color,
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            on_click=on_click,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=f"{color}40",
                offset=ft.Offset(0, 4)
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )

    def create_icon_btn(self, icon, on_click, color):
        """Create icon button"""
        return ft.Container(
            content=ft.Icon(icon, color="#ffffff", size=20),
            width=45, height=45,
            bgcolor=color,
            border_radius=12,
            on_click=on_click,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=f"{color}40",
                offset=ft.Offset(0, 4)
            )
        )

    def create_app_card(self, item, index):
        """Create stunning app card"""
        app_icon = AppIcons.get_icon(item.get("type", "VS Code"))
        is_enabled = item.get("enabled", True)
        
        # Dynamic colors based on app type
        card_colors = {
            "VS Code": self.colors['accent_blue'],
            "Website": self.colors['accent_purple'],
            "File Explorer": self.colors['accent_green'],
            "Command Prompt": "#1f2937",
            "Teams": "#6366f1"
        }
        
        card_color = card_colors.get(item.get("type", "VS Code"), self.colors['accent_blue'])
        
        return ft.Container(
            content=ft.Column([
                # Card header with icon and status
                ft.Row([
                    ft.Container(
                        content=ft.Text(app_icon, size=24),
                        width=50, height=50,
                        bgcolor=f"{card_color}20",
                        border_radius=12,
                        alignment=ft.alignment.center
                    ),
                    ft.Switch(
                        value=is_enabled,
                        on_change=lambda e: self.update_item_enabled(item, e.control.value),
                        active_color=self.colors['accent_green'],
                        scale=0.8
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # App name
                ft.TextField(
                    value=item.get("name", ""),
                    hint_text="App name",
                    color=self.colors['text_primary'],
                    bgcolor="transparent",
                    border_color="transparent",
                    text_size=16,
                    text_style=ft.TextStyle(weight=ft.FontWeight.W_600),  # Fixed: Use text_style instead
                    on_change=lambda e: self.update_item_name(item, e.control.value)
                ),

                # App type
                ft.Dropdown(
                    value=item.get("type", "VS Code"),
                    options=[
                        ft.dropdown.Option("VS Code"),
                        ft.dropdown.Option("File Explorer"),
                        ft.dropdown.Option("Command Prompt"),
                        ft.dropdown.Option("PowerShell"),
                        ft.dropdown.Option("Website"),
                        ft.dropdown.Option("Teams"),
                        ft.dropdown.Option("Outlook"),
                        ft.dropdown.Option("MongoDB Compass"),
                        ft.dropdown.Option("GitHub Desktop"),
                        ft.dropdown.Option("Postman"),
                        ft.dropdown.Option("Notepad"),
                    ],
                    bgcolor=f"{self.colors['card_bg']}80",
                    border_color=self.colors['border'],
                    color=self.colors['text_secondary'],
                    text_size=12,
                    on_change=lambda e: self.update_item_type(item, e.control.value, index)
                ),

                # Path field
                ft.TextField(
                    value=item.get("path", ""),
                    hint_text="Path/URL (optional)",
                    color=self.colors['text_secondary'],
                    bgcolor=f"{self.colors['bg_primary']}60",
                    border_color=self.colors['border'],
                    border_radius=8,
                    text_size=11,
                    on_change=lambda e: self.update_item_path(item, e.control.value)
                ),

                # Action buttons
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.PLAY_ARROW, color="#ffffff", size=16),
                        width=36, height=36,
                        bgcolor=self.colors['accent_green'],
                        border_radius=8,
                        on_click=lambda e: self.launch_single_item(item),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE_OUTLINE, color="#ffffff", size=16),
                        width=36, height=36,
                        bgcolor=self.colors['accent_pink'],
                        border_radius=8,
                        on_click=lambda e: self.delete_item(index),
                        alignment=ft.alignment.center
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ], spacing=12),
            
            bgcolor=self.colors['card_bg'],
            border_radius=16,
            padding=20,
            border=ft.border.all(1, f"{card_color}30"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color="#00000040",
                offset=ft.Offset(0, 8)
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            opacity=1.0 if is_enabled else 0.6
        )

    def show_main_page(self):
        """Show the stunning main page"""
        self.page.controls.clear()
        
        # Main layout with sidebar
        main_layout = ft.Row([
            self.create_sidebar(),
            
            # Main content area
            ft.Container(
                content=ft.Column([
                    self.create_header(),
                    
                    # Apps grid
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=self.items_grid,
                                expand=True,
                                padding=32
                            )
                        ], expand=True),
                        expand=True,
                        bgcolor=self.colors['bg_secondary']
                    )
                ], spacing=0, expand=True),
                expand=True
            )
        ], spacing=0, expand=True)

        self.page.add(main_layout)
        self.refresh_ui()
        self.page.update()

    def refresh_ui(self):
        """Refresh the apps grid"""
        self.items_grid.controls.clear()
        launch_items = self.config.get("launch_items", [])
        
        for i, item in enumerate(launch_items):
            card = self.create_app_card(item, i)
            self.items_grid.controls.append(card)
        
        self.page.update()

    def filter_items(self, e):
        """Filter apps in real-time"""
        search_term = e.control.value.lower()
        self.items_grid.controls.clear()
        
        launch_items = self.config.get("launch_items", [])
        
        for i, item in enumerate(launch_items):
            name = item.get("name", "").lower()
            item_type = item.get("type", "").lower()
            
            if search_term in name or search_term in item_type:
                card = self.create_app_card(item, i)
                self.items_grid.controls.append(card)
        
        self.page.update()

    def update_status(self, message, color=None):
        """Update status with color"""
        if color is None:
            color = self.colors['accent_green']
        self.status_text.value = message
        self.status_text.color = color
        self.status_text.update()

    # All your existing methods remain the same:
    def update_item_type(self, item, new_type, index):
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
            item_name = launch_items[index].get("name", "Unknown")
            del launch_items[index]
            self.config_manager.save_config(self.config)
            self.refresh_ui()
            self.update_status(f"🗑️ Deleted {item_name}", self.colors['accent_pink'])

    def add_new_item(self, e):
        new_item = {
            "type": "VS Code",
            "name": f"New App {len(self.config.get('launch_items', [])) + 1}",
            "path": "",
            "browser": "chrome",
            "enabled": True
        }
        
        if "launch_items" not in self.config:
            self.config["launch_items"] = []
        
        self.config["launch_items"].append(new_item)
        self.config_manager.save_config(self.config)
        self.refresh_ui()
        self.update_status("➕ Added new app!", self.colors['accent_blue'])

    def launch_selected(self, e):
        launch_items = self.config.get("launch_items", [])
        enabled_items = [item for item in launch_items if item.get("enabled", True)]
        
        if not enabled_items:
            self.update_status("⚠️ No apps selected for launch", self.colors['accent_orange'])
            return

        launched_count = 0
        for item in enabled_items:
            if self.app_launcher.launch_item(item):
                launched_count += 1

        self.update_status(f"🚀 Launched {launched_count} apps successfully!", self.colors['accent_green'])

    def launch_single_item(self, item):
        if self.app_launcher.launch_item(item):
            self.update_status(f"✅ Launched {item.get('name', 'Unknown')}", self.colors['accent_green'])
        else:
            self.update_status(f"❌ Failed to launch {item.get('name', 'Unknown')}", self.colors['accent_pink'])

    def toggle_startup(self, e):
        enable_startup = e.control.value
        
        if enable_startup:
            if self.startup_manager.add_to_startup():
                self.update_status("✅ Added to Windows startup", self.colors['accent_green'])
            else:
                self.update_status("❌ Failed to add to startup", self.colors['accent_pink'])
                e.control.value = False
        else:
            if self.startup_manager.remove_from_startup():
                self.update_status("🚫 Removed from Windows startup", self.colors['accent_orange'])
            else:
                self.update_status("❌ Failed to remove from startup", self.colors['accent_pink'])
                e.control.value = True
        
        e.control.update()
