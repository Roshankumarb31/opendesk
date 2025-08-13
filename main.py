import flet as ft
import subprocess
import json
import os
import psutil
import webbrowser

class AppLauncher:
    def __init__(self):
        self.config_file = "launcher_config.json"
        self.apps_config = self.load_config()

    def load_config(self):
        """Load saved configuration from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass 
        return {"launch_items": []}

    def save_config(self):
        """Save current configuration to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.apps_config, f, indent=2)

    def launch_item(self, item):
        """Launch a specific item based on its type"""
        try:
            app_type = item["type"]
            if app_type == "VS Code":
                path = item.get("path", "").strip()
                if path and os.path.exists(path):
                    subprocess.Popen(["code", path], shell=True)
                else:
                    subprocess.Popen(["code"], shell=True)
                return True

            elif app_type == "File Explorer":
                path = item.get("path", "").strip()
                if path and os.path.exists(path):
                    subprocess.Popen(["explorer", path], shell=True)
                else:
                    subprocess.Popen(["explorer"], shell=True)
                return True

            elif app_type == "Command Prompt":
                path = item.get("path", "").strip()
                if path and os.path.exists(path):
                    subprocess.Popen(f'start cmd /k "cd /d {path}"', shell=True)
                else:   
                    subprocess.Popen("start cmd", shell=True)

            elif app_type == "PowerShell":
                path = item.get("path", "").strip()
                if path and os.path.exists(path):
                    subprocess.Popen(f'start powershell -NoExit -Command "Set-Location \'{path}\'"', shell=True)
                else:
                    subprocess.Popen("start powershell", shell=True)



            elif app_type == "Teams":
                subprocess.Popen(["start", "ms-teams:"], shell=True)
                return True
                
            elif app_type == "Outlook":
                subprocess.Popen(["start", "outlook"], shell=True)
                return True
                
            elif app_type == "MongoDB Compass":
                # Try common MongoDB Compass installation paths
                compass_paths = [
                    "C:\\Users\\{}\\AppData\\Local\\MongoDBCompass\\MongoDBCompass.exe".format(os.environ.get('USERNAME')),
                    "C:\\Program Files\\MongoDB Compass\\MongoDBCompass.exe"
                ]
                launched = False
                for path in compass_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path], shell=True)
                        launched = True
                        break
                if not launched:
                    # Try to launch via Windows search
                    subprocess.Popen(["start", "MongoDB Compass"], shell=True)
                return True
                
            elif app_type == "GitHub Desktop":
                # Try common GitHub Desktop paths
                github_paths = [
                    "C:\\Users\\{}\\AppData\\Local\\GitHubDesktop\\GitHubDesktop.exe".format(os.environ.get('USERNAME')),
                    "C:\\Program Files\\GitHub Desktop\\GitHubDesktop.exe"
                ]
                launched = False
                for path in github_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path], shell=True)
                        launched = True
                        break
                if not launched:
                    subprocess.Popen(["start", "Github Desktop"], shell=True)
                return True
                
            elif app_type == "Postman":
                # Try common Postman paths
                postman_paths = [
                    "C:\\Users\\{}\\AppData\\Local\\Postman\\Postman.exe".format(os.environ.get('USERNAME')),
                    "C:\\Program Files\\Postman\\Postman.exe"
                ]
                launched = False
                for path in postman_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path], shell=True)
                        launched = True
                        break
                if not launched:
                    subprocess.Popen(["start", "Postman"], shell=True)
                return True
                
            elif app_type == "Notepad":
                subprocess.Popen(["notepad"], shell=True)
                return True





            elif app_type == "Website":
                url = item.get("path", "").strip()
                browser = item.get("browser", "chrome")
                # Add protocol if missing
                if url and not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                if url:
                    try:
                        if browser == "chrome":
                            subprocess.Popen(["start", "chrome", url], shell=True)
                        elif browser == "edge":
                            subprocess.Popen(["start", "msedge", url], shell=True)
                        elif browser == "brave":
                            subprocess.Popen(["start", "brave", url], shell=True)
                        elif browser == "firefox":
                            subprocess.Popen(["start", "firefox", url], shell=True)
                        else:
                            subprocess.Popen(["start", url], shell=True)
                    except Exception as e:
                        print(f"Failed to open with {browser}, using default browser: {e}")
                        subprocess.Popen(["start", url], shell=True)
                return True

        except Exception as e:
            print(f"Error launching {item['name']}: {e}")
            return False
        return False

    def close_all_windows(self):
        """Close all non-essential windows"""
        closed_count = 0
        target_processes = [
            "Code.exe", "explorer.exe", "cmd.exe", "powershell.exe",
            "chrome.exe", "msedge.exe", "brave.exe", "firefox.exe",
            "notepad.exe", "notepad++.exe", "Teams.exe", "OUTLOOK.EXE",
            "MongoDBCompass.exe", "GitHubDesktop.exe", "Postman.exe"
        ]
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name in target_processes:
                    if proc_name == "explorer.exe":
                        if len(proc.children()) > 0:  # Fixed: Changed &gt; to >
                            proc.terminate()
                            closed_count += 1
                    else:
                        proc.terminate()
                        closed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return closed_count

def main(page: ft.Page):
    page.title = "Simple Developer Launcher"
    page.window_width = 700
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK

    launcher = AppLauncher()
    
    # Global variables
    items_column = ft.Column()
    status_text = ft.Text("Ready", color=ft.Colors.GREEN)

    def update_status(message, color=ft.Colors.GREEN):
        status_text.value = message
        status_text.color = color
        page.update()

    def create_item_row(item, index):
        """Create a row with dropdown, name field, path field, and browser dropdown"""
        # App type dropdown
        type_dropdown = ft.Dropdown(
            width=120,
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
            on_change=lambda e: update_item_type(item, e.control.value, index)
        )  # Fixed: Added missing closing parenthesis

        # Name field
        name_field = ft.TextField(
            value=item.get("name", ""),
            hint_text="Item name",
            width=120,
            dense=True,
            on_change=lambda e: update_item_name(item, e.control.value)
        )  # Fixed: Added missing closing parenthesis

        # Path/URL field
        path_hint = "URL" if item.get("type") == "Website" else "Path (optional)"
        path_field = ft.TextField(
            value=item.get("path", ""),
            hint_text=path_hint,
            width=200,
            dense=True,
            on_change=lambda e: update_item_path(item, e.control.value)
        )  # Fixed: Added missing closing parenthesis

        # Browser dropdown (only for websites)
        browser_dropdown = ft.Dropdown(
            width=80,
            value=item.get("browser", "chrome"),
            options=[
                ft.dropdown.Option("chrome"),
                ft.dropdown.Option("edge"),
                ft.dropdown.Option("brave"),
                ft.dropdown.Option("firefox"),
            ],
            visible=item.get("type") == "Website",
            on_change=lambda e: update_item_browser(item, e.control.value)
        )  # Fixed: Added missing closing parenthesis

        # Enable checkbox
        enable_checkbox = ft.Checkbox(
            value=item.get("enabled", True),
            on_change=lambda e: update_item_enabled(item, e.control.value)
        )  # Fixed: Added missing closing parenthesis

        # Delete button
        delete_button = ft.IconButton(
            ft.Icons.DELETE,
            icon_color=ft.Colors.RED,
            on_click=lambda e: delete_item(index)
        )  # Fixed: Added missing closing parenthesis

        return ft.Row([
            enable_checkbox,
            type_dropdown,
            name_field,
            path_field,
            browser_dropdown,
            delete_button
        ])

    def update_item_type(item, new_type, index):
        item["type"] = new_type
        launcher.save_config()
        refresh_ui()

    def update_item_name(item, new_name):
        item["name"] = new_name
        launcher.save_config()

    def update_item_path(item, new_path):
        item["path"] = new_path
        launcher.save_config()

    def update_item_browser(item, new_browser):
        item["browser"] = new_browser
        launcher.save_config()

    def update_item_enabled(item, enabled):
        item["enabled"] = enabled
        launcher.save_config()

    def delete_item(index):
        if index < len(launcher.apps_config["launch_items"]):  # Fixed: Changed &lt; to <
            del launcher.apps_config["launch_items"][index]
            launcher.save_config()
            refresh_ui()

    def add_new_item(e):
        """Add a new launch item"""
        new_item = {
            "type": "VS Code",
            "name": "New Item",
            "path": "",
            "browser": "chrome",
            "enabled": True
        }  # Fixed: Added missing closing brace
        launcher.apps_config["launch_items"].append(new_item)
        launcher.save_config()
        refresh_ui()

    def launch_selected(e):
        """Launch all enabled items"""
        launched_count = 0
        for item in launcher.apps_config["launch_items"]:
            if item.get("enabled", True):
                if launcher.launch_item(item):
                    launched_count += 1
        update_status(f"Launched {launched_count} items", ft.Colors.GREEN)

    def refresh_ui():
        """Refresh the UI with current data"""
        items_column.controls.clear()
        for i, item in enumerate(launcher.apps_config["launch_items"]):
            items_column.controls.append(create_item_row(item, i))
        page.update()

    def close_all(e):
        """Navigate to close confirmation page"""
        show_close_confirmation_page()

    def show_close_confirmation_page():
        """Show a separate page for close confirmation"""
        # Clear the current page
        page.controls.clear()
        
        # Create the close confirmation page
        page.add(
            ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(height=50),  # Spacer
                    ft.Text("⚠️ Close All Applications", 
                           size=32, 
                           weight=ft.FontWeight.BOLD,
                           text_align=ft.TextAlign.CENTER),
                    
                    ft.Container(height=30),  # Spacer
                    
                    # Warning message
                    ft.Container(
                        content=ft.Text(
                            "Are you sure you want to close all applications?\n\n"
                            "This will close:\n"
                            "• VS Code\n"
                            "• Browsers (Chrome, Edge, Brave, Firefox)\n"
                            "• Terminals (CMD, PowerShell)\n"
                            "• File Explorers\n"
                            "• Microsoft Teams\n"
                            "• Outlook\n"
                            "• MongoDB Compass\n"
                            "• GitHub Desktop\n"
                            "• Postman\n"
                            "• Notepad",
                            size=16,
                            text_align=ft.TextAlign.CENTER
                        ),
                        bgcolor=ft.Colors.RED_100,
                        padding=20,
                        border_radius=10,
                        border=ft.border.all(2, ft.Colors.RED_300)
                    ),
                    
                    ft.Container(height=50),  # Spacer
                    
                    # Buttons
                    ft.Row([
                        ft.ElevatedButton(
                            "❌ No, Take Me Back",
                            on_click=lambda e: show_main_page(),
                            bgcolor=ft.Colors.GREY_600,
                            color=ft.Colors.WHITE,
                            width=200,
                            height=50,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                            )
                        ),
                        ft.Container(width=50),  # Spacer between buttons
                        ft.ElevatedButton(
                            "✅ Yes, Close All",
                            on_click=lambda e: execute_close_all(),
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            width=200,
                            height=50,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                            )
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER)
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40
            )
        )
        page.update()

    def execute_close_all():
        """Actually close all windows and show result"""
        # Show loading message
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Container(height=100),
                    ft.ProgressRing(),
                    ft.Container(height=20),
                    ft.Text("Closing applications...", size=18)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40
            )
        )
        page.update()
        
        # Actually close the processes
        closed_count = launcher.close_all_windows()
        
        # Show result page
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Container(height=100),
                    ft.Text("✅ Done!", 
                           size=32, 
                           weight=ft.FontWeight.BOLD,
                           color=ft.Colors.GREEN),
                    ft.Container(height=20),
                    ft.Text(f"Closed {closed_count} processes", 
                           size=18),
                    ft.Container(height=50),
                    ft.ElevatedButton(
                        "🏠 Back to Main",
                        on_click=lambda e: show_main_page(),
                        bgcolor=ft.Colors.BLUE,
                        color=ft.Colors.WHITE,
                        width=200,
                        height=50,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40
            )
        )
        page.update()

    def show_main_page():
        """Show the main launcher page"""
        # Clear the page
        page.controls.clear()
        
        # Recreate the main page content
        nonlocal items_column, status_text
        
        # Status text
        status_text = ft.Text("Ready", color=ft.Colors.GREEN)
        
        # Create UI elements
        items_column = ft.Column()
        
        # Main layout
        page.add(
            ft.Container(
                content=ft.Column([
                    # Title
                    ft.Text("🚀 Simple Developer Launcher",
                            size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    
                    # Control buttons
                    ft.Row([
                        ft.ElevatedButton("🚀 Launch Selected",
                                        on_click=launch_selected,
                                        bgcolor=ft.Colors.GREEN,
                                        color=ft.Colors.WHITE),
                        ft.ElevatedButton("❌ Close All",
                                        on_click=close_all,
                                        bgcolor=ft.Colors.RED,
                                        color=ft.Colors.WHITE),
                        ft.ElevatedButton("➕ Add New Item",
                                        on_click=add_new_item,
                                        bgcolor=ft.Colors.BLUE,
                                        color=ft.Colors.WHITE),
                    ]),
                    ft.Divider(),
                    
                    # Items section
                    ft.Text("Launch Items", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column([items_column], scroll=ft.ScrollMode.AUTO),
                        border=ft.border.all(1, ft.Colors.GREY),
                        padding=10,
                        border_radius=5,
                        height=400,
                    ),
                    
                    # Status
                    ft.Row([
                        ft.Text("Status: "),
                        status_text
                    ])
                ]),
                padding=20
            )
        )
        
        # Initialize UI
        refresh_ui()
        page.update()

    # Initialize the main page
    show_main_page()

if __name__ == "__main__":
    ft.app(target=main)
