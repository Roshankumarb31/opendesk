from platform_adapter import is_in_startup, add_to_startup, remove_from_startup

class StartupManager:
    def add_to_startup(self):
        return add_to_startup()

    def remove_from_startup(self):
        return remove_from_startup()

    def is_in_startup(self):
        return is_in_startup()
