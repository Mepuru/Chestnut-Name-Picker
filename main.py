#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChestNut Name Picker - 主程序
"""

import sys


def setup_dpi_awareness():
    """设置 DPI 感知，解决高分辨率缩放问题"""
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def main():
    """主函数，启动应用程序"""
    setup_dpi_awareness()
    
    from src.ui import ClassSelectorUI
    app = ClassSelectorUI()
    app.run()


if __name__ == "__main__":
    main()
