from platform_adapter import get_app_icon, ICON_MAP, FALLBACK_ICON

class AppIcons:
    ICON_MAP = ICON_MAP
    FALLBACK_ICON = FALLBACK_ICON
    get_icon = staticmethod(get_app_icon)
