#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChestNut Name Picker - 主程序
"""

from src.ui import ClassSelectorUI


def main():
    """主函数，启动应用程序"""
    app = ClassSelectorUI()
    app.run()


if __name__ == "__main__":
    main()
