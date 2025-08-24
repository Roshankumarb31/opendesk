import subprocess
import os
import psutil

class AppLauncher:
    def __init__(self):
        self.username = os.environ.get('USERNAME', '')
    
    def launch_item(self, item):
        """Launch a specific item based on its type"""
        try:
            app_type = item["type"]
            
            if app_type == "VS Code":
                return self._launch_vscode(item)
            elif app_type == "File Explorer":
                return self._launch_explorer(item)
            elif app_type == "Command Prompt":
                return self._launch_cmd(item)
            elif app_type == "PowerShell":
                return self._launch_powershell(item)
            elif app_type == "Website":
                return self._launch_website(item)
            elif app_type == "Teams":
                return self._launch_teams()
            elif app_type == "Outlook":
                return self._launch_outlook()
            elif app_type == "MongoDB Compass":
                return self._launch_mongodb()
            elif app_type == "GitHub Desktop":
                return self._launch_github()
            elif app_type == "Postman":
                return self._launch_postman()
            elif app_type == "Notepad":
                return self._launch_notepad()
            
        except Exception as e:
            print(f"Error launching {item.get('name', 'unknown')}: {e}")
            return False
        
        return False
    
    def _launch_vscode(self, item):
        """Launch VS Code with optional path"""
        path = item.get("path", "").strip()
        if path and os.path.exists(path):
            subprocess.Popen(["code", path], shell=True)
        else:
            subprocess.Popen(["code"], shell=True)
        return True
    
    def _launch_explorer(self, item):
        """Launch File Explorer with optional path"""
        path = item.get("path", "").strip()
        if path and os.path.exists(path):
            subprocess.Popen(["explorer", path], shell=True)
        else:
            subprocess.Popen(["explorer"], shell=True)
        return True
    
    def _launch_cmd(self, item):
        """Launch Command Prompt with optional path"""
        path = item.get("path", "").strip()
        if path and os.path.exists(path):
            subprocess.Popen(f'start cmd /k "cd /d {path}"', shell=True)
        else:
            subprocess.Popen("start cmd", shell=True)
        return True
    
    def _launch_powershell(self, item):
        """Launch PowerShell with optional path"""
        path = item.get("path", "").strip()
        if path and os.path.exists(path):
            subprocess.Popen(f'start powershell -NoExit -Command "Set-Location \'{path}\'"', shell=True)
        else:
            subprocess.Popen("start powershell", shell=True)
        return True
    

    
    def _launch_website(self, item):
        """Launch website in specified browser with incognito option or just open browser if URL missing"""
        url = item.get("path", "").strip()
        browser = item.get("browser", "chrome")
        incognito = item.get("incognito", False)

        # Add protocol if missing (only when url provided)
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            # Build browser commands (with or without URL)
            if incognito:
                browser_commands = {
                    "chrome": ["start", "chrome", "--incognito"] + ([url] if url else []),
                    "edge": ["start", "msedge", "--inprivate"] + ([url] if url else []),
                    "brave": ["start", "brave", "--incognito"] + ([url] if url else []),
                    "firefox": ["start", "firefox", "--private-window"] + ([url] if url else []),
                }
            else:
                browser_commands = {
                    "chrome": ["start", "chrome"] + ([url] if url else []),
                    "edge": ["start", "msedge"] + ([url] if url else []),
                    "brave": ["start", "brave"] + ([url] if url else []),
                    "firefox": ["start", "firefox"] + ([url] if url else []),
                }

            cmd = browser_commands.get(browser, ["start"] + ([url] if url else []))
            subprocess.Popen(cmd, shell=True)
            return True
        except Exception:
            # Fallback to default handler: open URL if present, else open default browser/home
            if url:
                subprocess.Popen(["start", url], shell=True)
            else:
                # Try starting a generic browser protocol — this typically opens default browser
                subprocess.Popen(["start", ""], shell=True)
            return True



    
    def _launch_teams(self):
        """Launch Microsoft Teams"""
        subprocess.Popen(["start", "ms-teams:"], shell=True)
        return True
    
    def _launch_outlook(self):
        """Launch Outlook (works with built-in or installed version)"""
        try:
            # Try Outlook protocol (UWP or installed Office)
            subprocess.Popen("start outlookmail:", shell=True)
            return True
        except Exception:

            # Try legacy Office executable (if exists)
            subprocess.Popen("start outlook", shell=True)
            return True
        



    
    def _launch_mongodb(self):
        """Launch MongoDB Compass"""
        return self._launch_app_by_paths([
            f"C:\\Users\\{self.username}\\AppData\\Local\\MongoDBCompass\\MongoDBCompass.exe",
            "C:\\Program Files\\MongoDB Compass\\MongoDBCompass.exe"
        ], "MongoDB Compass")
    
    def _launch_github(self):
        """Launch GitHub Desktop"""
        return self._launch_app_by_paths([
            f"C:\\Users\\{self.username}\\AppData\\Local\\GitHubDesktop\\GitHubDesktop.exe",
            "C:\\Program Files\\GitHub Desktop\\GitHubDesktop.exe"
        ], "Github Desktop")
    
    def _launch_postman(self):
        """Launch Postman"""
        return self._launch_app_by_paths([
            f"C:\\Users\\{self.username}\\AppData\\Local\\Postman\\Postman.exe",
            "C:\\Program Files\\Postman\\Postman.exe"
        ], "Postman")
    
    def _launch_notepad(self):
        """Launch Notepad"""
        subprocess.Popen(["notepad"], shell=True)
        return True
    
    def _launch_app_by_paths(self, paths, fallback_name):
        """Try launching app from multiple possible paths"""
        for path in paths:
            if os.path.exists(path):
                subprocess.Popen([path], shell=True)
                return True
        
        # Fallback to Windows search
        subprocess.Popen(["start", fallback_name], shell=True)
        return True
    
    def close_all_windows(self):
        """Close all non-essential windows"""
        closed_count = 0
        target_processes = [
            "Code.exe", "explorer.exe", "cmd.exe", "powershell.exe",
            "chrome.exe", "msedge.exe", "brave.exe", "firefox.exe",
            "notepad.exe", "Notepad.exe", "notepad++.exe", 
            "Teams.exe", "OUTLOOK.EXE",
            "MongoDBCompass.exe", "GitHubDesktop.exe", "Postman.exe",
            "olk.exe","ms-teams.exe"
        ]


        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name in target_processes:
                    if proc_name == "explorer.exe":
                        if len(proc.children()) > 0:
                            proc.terminate()
                            closed_count += 1
                    else:
                        proc.terminate()
                        closed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return closed_count

