#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quest3/3s 临时 Root 提权工具
一键提取 Quest3/3s 临时 Root

项目灵感: https://github.com/F-19-F/IonStackQuest3
感谢B站UP主: "我是一个小依旧"
相关视频: https://b23.tv/FS958OJ
漏洞: CVE-2026-43499
"""

import sys
import os
import subprocess
import threading
import time
import re
import select
import webbrowser
import json
import shutil
from queue import Queue, Empty

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLineEdit, QTextBrowser, QLabel,
    QMessageBox, QDialog, QFrame, QSizePolicy, QMenu, QAction,
    QScrollBar, QSpacerItem, QDialogButtonBox, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer, QSize, QMutex, QUrl, QPoint
from PyQt5.QtGui import QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QPalette, QKeySequence, QDesktopServices


# ==================== 全局样式表 (Catppuccin Mocha 深色主题) ====================
STYLE_SHEET = """
QMainWindow {
    background-color: transparent;
}
QWidget#centralWidget {
    background-color: #1e1e2e;
    border-radius: 12px;
    border: 1px solid #313244;
}

/* 自定义标题栏 */
QFrame#titleBar {
    background-color: #181825;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border-bottom: 1px solid #313244;
}
QLabel#titleLogo {
    color: #cba6f7;
    font-size: 15px;
    font-weight: bold;
    padding: 0px 6px;
}
QPushButton#winBtn {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 6px;
    font-size: 14px;
    min-width: 32px;
    min-height: 28px;
    color: #cdd6f4;
}
QPushButton#winBtn:hover {
    background-color: #313244;
    color: #cba6f7;
}
QPushButton#winBtn:pressed {
    background-color: #45475a;
}
QPushButton#closeBtn {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 6px;
    font-size: 14px;
    min-width: 32px;
    min-height: 28px;
    color: #cdd6f4;
}
QPushButton#closeBtn:hover {
    background-color: #f38ba8;
    color: #1e1e2e;
}
QPushButton#closeBtn:pressed {
    background-color: #e07694;
    color: #1e1e2e;
}

/* 标签页 */
QTabWidget::pane {
    border: 1px solid #313244;
    background-color: #181825;
    border-radius: 8px;
    top: -1px;
}
QTabBar::tab {
    background-color: #181825;
    color: #6c7086;
    padding: 8px 18px;
    border: 1px solid #313244;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
    font-size: 13px;
    min-width: 100px;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    color: #cba6f7;
    border-bottom: 2px solid #cba6f7;
}
QTabBar::tab:hover:!selected {
    background-color: #313244;
    color: #cdd6f4;
}

/* 按钮 */
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 9px 22px;
    font-size: 13px;
    font-weight: bold;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #45475a;
    border-color: #cba6f7;
    color: #cba6f7;
}
QPushButton:pressed {
    background-color: #cba6f7;
    color: #1e1e2e;
}
QPushButton:disabled {
    background-color: #181825;
    color: #45475a;
    border-color: #313244;
}

/* 开始执行按钮 - 绿色 */
QPushButton#executeBtn {
    background-color: #a6e3a1;
    color: #1e1e2e;
    border: 1px solid #a6e3a1;
    font-weight: bold;
}
QPushButton#executeBtn:hover {
    background-color: #b5e8b1;
    border-color: #b5e8b1;
}
QPushButton#executeBtn:pressed {
    background-color: #8ad88a;
    color: #1e1e2e;
}
QPushButton#executeBtn:disabled {
    background-color: #313244;
    color: #6c7086;
    border-color: #313244;
}

/* 开始提权按钮 - 红色/粉色 */
QPushButton#rootBtn {
    background-color: #f38ba8;
    color: #1e1e2e;
    border: 1px solid #f38ba8;
    font-weight: bold;
}
QPushButton#rootBtn:hover {
    background-color: #f5a0b7;
    border-color: #f5a0b7;
}
QPushButton#rootBtn:pressed {
    background-color: #e07694;
    color: #1e1e2e;
}
QPushButton#rootBtn:disabled {
    background-color: #313244;
    color: #6c7086;
    border-color: #313244;
}

/* 停止按钮 - 橙色 */
QPushButton#stopBtn {
    background-color: #fab387;
    color: #1e1e2e;
    border: 1px solid #fab387;
    font-weight: bold;
}
QPushButton#stopBtn:hover {
    background-color: #fbc5a3;
    border-color: #fbc5a3;
}
QPushButton#stopBtn:disabled {
    background-color: #313244;
    color: #6c7086;
    border-color: #313244;
}

/* 获取Root按钮 - 青色 */
QPushButton#getRootBtn {
    background-color: #94e2d5;
    color: #1e1e2e;
    border: 1px solid #94e2d5;
    font-weight: bold;
}
QPushButton#getRootBtn:hover {
    background-color: #a6e8dc;
    border-color: #a6e8dc;
}
QPushButton#getRootBtn:pressed {
    background-color: #7cd0c1;
    color: #1e1e2e;
}
QPushButton#getRootBtn:disabled {
    background-color: #313244;
    color: #6c7086;
    border-color: #313244;
}

/* 新建会话按钮 */
QPushButton#newSessionBtn {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: 1px solid #89b4fa;
    font-weight: bold;
}
QPushButton#newSessionBtn:hover {
    background-color: #a0c4fb;
    border-color: #a0c4fb;
}

/* 关于按钮 */
QPushButton#aboutBtn {
    background-color: #b4befe;
    color: #1e1e2e;
    border: 1px solid #b4befe;
    font-weight: bold;
}
QPushButton#aboutBtn:hover {
    background-color: #c6d0fe;
    border-color: #c6d0fe;
}

/* 输入框 */
QLineEdit {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 13px;
    font-family: 'Consolas', 'Courier New', monospace;
}
QLineEdit:focus {
    border: 1px solid #cba6f7;
}

/* 终端输出区域 */
QTextBrowser {
    background-color: #11111b;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    padding: 10px;
    selection-background-color: #313244;
}

/* 标签 */
QLabel {
    color: #cdd6f4;
    font-size: 13px;
}
QLabel#statusLabel {
    color: #6c7086;
    font-size: 12px;
    padding: 2px 8px;
}
QLabel#fileStatusOK {
    color: #a6e3a1;
    font-size: 12px;
    padding: 3px 10px;
    background-color: #181825;
    border-radius: 4px;
    font-weight: bold;
}
QLabel#fileStatusMISS {
    color: #f38ba8;
    font-size: 12px;
    padding: 3px 10px;
    background-color: #181825;
    border-radius: 4px;
    font-weight: bold;
}

/* 框架 */
QFrame#toolbarFrame {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 10px;
}
QFrame#statusFrame {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 6px;
}
QFrame#inputFrame {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 8px;
}
QFrame#fileStatusFrame {
    background-color: #11111b;
    border: 1px solid #313244;
    border-radius: 6px;
}

/* 滚动条 */
QScrollBar:vertical {
    background: #11111b;
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #313244;
    min-height: 30px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #45475a;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: #11111b;
    height: 10px;
    margin: 0px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background: #313244;
    min-width: 30px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #45475a;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* 对话框 */
QDialog, QMessageBox {
    background-color: #1e1e2e;
}
QMessageBox QLabel {
    color: #cdd6f4;
    font-size: 14px;
    min-width: 0px;
}
QMessageBox QPushButton {
    min-width: 80px;
    padding: 7px 18px;
}
QMessageBox QTextEdit, QMessageBox QPlainTextEdit {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
}
QDialog QLabel {
    color: #cdd6f4;
}
QDialogButtonBox QPushButton {
    min-width: 80px;
    padding: 7px 18px;
}

/* 无边框主题对话框 (与主界面风格一致) */
QWidget#dialogOuter {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 12px;
}
QFrame#dialogHead {
    background-color: #181825;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border-bottom: 1px solid #313244;
}
QLabel#dialogTitleLabel {
    color: #cba6f7;
    font-size: 13px;
    font-weight: bold;
}
QPushButton#dialogCloseBtn {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    color: #cdd6f4;
    font-size: 13px;
}
QPushButton#dialogCloseBtn:hover {
    background-color: #f38ba8;
    color: #1e1e2e;
}
QPushButton#dialogCloseBtn:pressed {
    background-color: #e07694;
    color: #1e1e2e;
}
"""


# ==================== ANSI 颜色映射 ====================
ANSI_FG = {
    30: "#45475a",   # 黑
    31: "#f38ba8",   # 红
    32: "#a6e3a1",   # 绿
    33: "#f9e2af",   # 黄
    34: "#89b4fa",   # 蓝
    35: "#cba6f7",   # 品红
    36: "#94e2d5",   # 青
    37: "#cdd6f4",   # 白
    90: "#6c7086",   # 亮黑
    91: "#eba0ac",   # 亮红
    92: "#94e2d5",   # 亮绿
    93: "#f9e2af",   # 亮黄
    94: "#89dceb",   # 亮蓝
    95: "#f5c2e7",   # 亮品红
    96: "#89dceb",   # 亮青
    97: "#ffffff",   # 亮白
}

ANSI_BG = {
    40: "#11111b",
    41: "#f38ba8",
    42: "#a6e3a1",
    43: "#f9e2af",
    44: "#89b4fa",
    45: "#cba6f7",
    46: "#94e2d5",
    47: "#cdd6f4",
    100: "#45475a",
    101: "#eba0ac",
    102: "#94e2d5",
    103: "#f9e2af",
    104: "#89dceb",
    105: "#f5c2e7",
    106: "#89dceb",
    107: "#ffffff",
}


def parse_ansi_and_append(text_browser, text, default_fg="#cdd6f4", default_bg=None, add_newline=True):
    """解析带ANSI转义码的文本并追加到QTextBrowser中"""
    cursor = text_browser.textCursor()
    cursor.movePosition(QTextCursor.End)

    # ANSI 正则
    ansi_pattern = re.compile(r'\x1b\[([0-9;]*)m')
    pos = 0

    # 当前格式状态
    cur_fg = default_fg
    cur_bg = default_bg
    cur_bold = False
    cur_italic = False
    cur_underline = False

    for match in ansi_pattern.finditer(text):
        # 先插入匹配前的普通文本
        if match.start() > pos:
            segment = text[pos:match.start()]
            if segment:
                fmt = QTextCharFormat()
                fmt.setForeground(QColor(cur_fg))
                if cur_bg:
                    fmt.setBackground(QColor(cur_bg))
                if cur_bold:
                    fmt.setFontWeight(QFont.Bold)
                if cur_italic:
                    fmt.setFontItalic(True)
                if cur_underline:
                    fmt.setFontUnderline(True)
                cursor.insertText(segment, fmt)

        # 解析ANSI参数
        code_str = match.group(1)
        codes = [int(c) for c in code_str.split(';') if c]
        if not codes:
            codes = [0]

        i = 0
        while i < len(codes):
            code = codes[i]
            if code == 0:
                cur_fg = default_fg
                cur_bg = default_bg
                cur_bold = False
                cur_italic = False
                cur_underline = False
            elif code == 1:
                cur_bold = True
            elif code == 3:
                cur_italic = True
            elif code == 4:
                cur_underline = True
            elif code == 22:
                cur_bold = False
            elif code == 23:
                cur_italic = False
            elif code == 24:
                cur_underline = False
            elif code in ANSI_FG:
                cur_fg = ANSI_FG[code]
            elif code in ANSI_BG:
                cur_bg = ANSI_BG[code]
            elif code == 38 or code == 48:
                # 256色 / RGB 扩展：简化处理，跳过或粗略映射
                if i + 1 < len(codes) and codes[i+1] == 5 and i + 2 < len(codes):
                    # 256色，简单忽略
                    i += 2
                elif i + 1 < len(codes) and codes[i+1] == 2 and i + 4 < len(codes):
                    i += 4
            i += 1

        pos = match.end()

    # 插入剩余文本
    if pos < len(text):
        segment = text[pos:]
        if segment:
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(cur_fg))
            if cur_bg:
                fmt.setBackground(QColor(cur_bg))
            if cur_bold:
                fmt.setFontWeight(QFont.Bold)
            if cur_italic:
                fmt.setFontItalic(True)
            if cur_underline:
                fmt.setFontUnderline(True)
            cursor.insertText(segment, fmt)

    if add_newline:
        cursor.insertText("\n")
    text_browser.setTextCursor(cursor)
    sb = text_browser.verticalScrollBar()
    sb.setValue(sb.maximum())


# ==================== 输出类型颜色 ====================
COLORS = {
    "info": "#89b4fa",      # 蓝色 - 信息
    "success": "#a6e3a1",   # 绿色 - 成功
    "error": "#f38ba8",     # 红色 - 错误
    "warning": "#f9e2af",   # 黄色 - 警告
    "command": "#cba6f7",   # 紫色 - 命令
    "output": "#cdd6f4",    # 白色 - 普通输出
    "system": "#6c7086",    # 灰色 - 系统
    "device": "#fab387",    # 橙色 - 设备状态
}


# ==================== 智能解码 ====================
def decode_bytes_smart(data):
    """智能解码字节流，支持多种编码"""
    if not data:
        return ''
    enc_order = ['utf-8', 'gbk', 'gb18030', 'cp936', 'shift_jis', 'big5', 'latin-1']
    last_err = None
    for enc in enc_order:
        try:
            return data.decode(enc, errors='strict')
        except (UnicodeDecodeError, LookupError) as e:
            last_err = e
            continue
    try:
        result = data.decode('utf-8', errors='replace')
        if result.count('\ufffd') > len(result) // 4:
            try:
                result = data.decode('gb18030', errors='replace')
            except Exception:
                pass
        return result
    except Exception:
        return str(data)


# ==================== 跨平台 subprocess 配置 ====================
IS_WINDOWS = sys.platform == 'win32'

if IS_WINDOWS:
    import ctypes
    # Windows: 抑制子进程崩溃弹窗 ("X已停止工作")
    try:
        # SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX
        ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002)
    except Exception:
        pass

    _SUBPROCESS_STARTUPINFO = subprocess.STARTUPINFO()
    _SUBPROCESS_STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _SUBPROCESS_STARTUPINFO.wShowWindow = 0  # SW_HIDE
    _SUBPROCESS_CREATIONFLAGS = subprocess.CREATE_NO_WINDOW
else:
    _SUBPROCESS_STARTUPINFO = None
    _SUBPROCESS_CREATIONFLAGS = 0


def _subprocess_common_kwargs():
    """返回跨平台 subprocess 公共参数"""
    kwargs = {}
    if IS_WINDOWS:
        kwargs['startupinfo'] = _SUBPROCESS_STARTUPINFO
        kwargs['creationflags'] = _SUBPROCESS_CREATIONFLAGS
    return kwargs


_ADB_CANDIDATES = [
    r"C:\platform-tools\adb.exe",
    r"C:\Android\platform-tools\adb.exe",
    r"C:\Android\sdk\platform-tools\adb.exe",
    r"C:\Program Files (x86)\Android\android-sdk\platform-tools\adb.exe",
    r"C:\Program Files\Android\android-sdk\platform-tools\adb.exe",
    "%LOCALAPPDATA%\\Android\\Sdk\\platform-tools\\adb.exe",
    "%USERPROFILE%\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe",
]

_ADB_CFG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.adb_config.json')


def adb_find_paths():
    """扫描系统中所有可用的 adb 可执行文件路径（去重）"""
    found = []
    seen = set()

    def add(p):
        p = os.path.expandvars(os.path.expanduser(p)).strip()
        if not p:
            return
        if os.path.isfile(p):
            key = os.path.normcase(p)
            if key not in seen:
                seen.add(key)
                found.append(p)

    for p in _ADB_CANDIDATES:
        add(p)
    which = shutil.which('adb')
    if which:
        add(which)
    adb_name = 'adb.exe' if IS_WINDOWS else 'adb'
    for d in os.environ.get('PATH', '').split(os.pathsep):
        if d:
            add(os.path.join(d, adb_name))
    return found


def load_adb_config():
    """读取已保存的 adb 路径配置，无效时返回 None"""
    try:
        with open(_ADB_CFG_FILE, 'r') as f:
            data = json.load(f)
            p = data.get('adb', '')
        if p and os.path.isfile(os.path.expandvars(os.path.expanduser(p))):
            return os.path.expandvars(os.path.expanduser(p))
    except Exception:
        pass
    return None


def save_adb_config(path):
    try:
        with open(_ADB_CFG_FILE, 'w') as f:
            json.dump({'adb': path}, f)
    except Exception:
        pass


def ensure_adb_selected():
    """首次启动：扫描 adb 并弹出路径选择对话框，将选择持久化到配置"""
    global ADB_PATH
    cfg = load_adb_config()
    if cfg:
        ADB_PATH = cfg
        return
    paths = adb_find_paths()
    if paths:
        dlg = AdbPathDialog(paths)
        dlg.exec_()
        chosen = dlg.get_selected() or paths[0]
        ADB_PATH = chosen
        save_adb_config(chosen)
    else:
        ADB_PATH = 'adb'
        try:
            msg = ThemeMessageBox(
                None,
                title=tr('adb_missing_title'),
                text=tr('adb_missing_msg'),
                icon=QMessageBox.standardIcon(QMessageBox.Warning),
                ok_text=tr('ok'))
            msg.exec_()
        except Exception:
            pass


def check_ionstack_conf():
    """启动时检查 ionstack.conf 是否存在，缺失时提示用户先去编译"""
    if os.path.isfile(os.path.join(os.getcwd(), 'ionstack.conf')):
        return
    try:
        msg = ThemeMessageBox(
            None,
            title=tr('ionstack_missing_title'),
            text=tr('ionstack_missing_msg'),
            icon=QMessageBox.standardIcon(QMessageBox.Warning),
            ok_text=tr('ok'))
        msg.exec_()
    except Exception:
        pass


ADB_PATH = load_adb_config() or 'adb'


def adb_cmd(*args):
    """返回使用固定 adb 路径的命令列表"""
    return [ADB_PATH] + list(args)


# ==================== 国际化 (i18n) ====================
_LANG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.lang.json')
LANG = 'zh'

def load_lang():
    global LANG
    try:
        with open(_LANG_FILE, 'r') as f:
            data = json.load(f)
            LANG = data.get('lang', 'zh')
    except Exception:
        LANG = 'zh'

def save_lang(lang):
    global LANG
    LANG = lang
    try:
        with open(_LANG_FILE, 'w') as f:
            json.dump({'lang': lang}, f)
    except Exception:
        pass

load_lang()

# 翻译表
T = {
    'zh': {
        'execute': '▶  开始执行',
        'root': '⚡  开始提权',
        'get_root': '🔓  获取Root',
        'stop': '■  停止',
        'new_session': '＋ 新建会话',
        'lang_switch': '🌐 EN',
        'run': '执行',
        'input_placeholder': '输入 ADB 命令或其他命令，按 Enter 执行... (如: adb devices)',
        'status_ready': '就绪',
        'file_status': '📁 文件状态:',
        'refresh': '🔄 刷新',
        'file_ok': '已就绪',
        'file_miss': '此无文件',
        'welcome_title': '║        Quest3/3s 临时 Root 提权工具  v1.0               ║',
        'about': 'ℹ 关于',
        'about_title': '关于 Quest3/3s Root Tool',
        'exec_done': '执行完成',
        'exec_fail': '执行失败',
        'root_success': '提权成功',
        'root_fail': '提权失败',
        'auto_retry_title': '提权失败',
        'auto_retry_msg': '提权失败',
        'auto_retry_detail': '是否要自动提权？',
        'auto_retry_ok': '确定 - 自动提权',
        'auto_retry_cancel': '取消 - 手动操作',
        'close_confirm': '确认关闭',
        'close_msg': '该会话有任务正在运行，确定要关闭吗？',
        'yes': '是',
        'no': '否',
        'no_device': '当前未检测到已连接的设备',
        'no_device_detail': '请先连接设备并执行「开始执行」',
        'minimize': '最小化',
        'maximize': '最大化/还原',
        'close': '关闭',
        'title': '⚡ Quest3/3s 临时 Root 提权工具',
        'window_title': 'Quest3/3s 临时 Root 提权工具 v1.0',
        'ok': '确定',
        'root_method_title': '获取Root方式',
        'root_method_tip': '请选择获取 Root 的方式:',
        'root_success_title': '✓ 提权成功',
        'root_success_msg': '已成功提权',
        'get_root_success_title': '✓ 获取Root成功',
        'get_root_success_msg': '已使用Magisk获取Root',
        'kernelsu_success_title': '✓ KernelSU 获取Root成功',
        'kernelsu_success_msg': '已使用KernelSU 获取Root[越狱模式]',
        'adb_select_title': '选择 ADB 路径',
        'adb_select_tip': '检测到以下 ADB 安装路径，请选择本工具要使用的:',
        'adb_missing_title': '未检测到 ADB',
        'adb_missing_msg': '未检测到 ADB，请先安装 ADB (Android SDK Platform-Tools)。\n'
                           '可从 https://developer.android.com/tools/releases/platform-tools 下载，\n'
                           '或将 adb.exe 放入本程序目录或常用安装目录后重新打开。',
        'ionstack_missing_title': '未检测到 ionstack.conf',
        'ionstack_missing_msg': '你好像并没有编译过自己系统版本的ionstack\n'
                                '请先去以下地址去编译:\n'
                                'https://github.com/F-19-F/IonStackQuest3\n\n'
                                '编译完成放入软件目录下即可',
        'cancel': '取消',
        'exists': '存在',
        'not_exists': '不存在',
        'seconds': ' 秒',
        'apk_files_start': ' 个APK文件，开始安装...',
        'apk_install_ok': ' 安装成功',
        'apk_install_fail_cont': ' 安装失败（继续）',
        'sec_disconnected': ' 秒: 设备断开!',
        'auto_attempt_tail': ' 次尝试 ',
        'auto_exec_retry_tail': ' 次尝试 - 执行阶段失败，重试...',
        'auto_root_retry_tail': ' 次尝试 - 提权失败，重试...',
        'sec_disc_tail': '秒设备断开，等待重连...',
        'auto_success_tail': ' 次) <<<',
        'checking_files': '正在检查文件...',
        'file_check_failed': '文件检查失败',
        'checking_device_conn': '正在检查设备连接...',
        'rebooting_dev': '正在重启设备...',
        'waiting_dev_disconnect': '等待设备断开...',
        'waiting_dev_reconnect': '等待设备重连...',
        'checking_stability': '正在检查连接稳定性...',
        'pushing_files': '正在推送文件...',
        'executing_root': '正在执行提权命令...',
        'checking_device': '正在检查设备...',
        'checking_magisk_installed': '检查 Magisk 是否已安装...',
        'pushing_busybox': '推送 busybox...',
        'pushing_magisk_apk': '推送 magisk.apk...',
        'pushing_live_setup': '推送 live_setup.sh...',
        'executing_shell': '执行 shell 命令...',
        'in_root_shell': '在 Root Shell 中执行命令...',
        'get_root_done_manual': '获取Root完成(请手动验证)',
        'searching_ksu_files': '搜索 KernelSU 文件...',
        'pushing_ksud': '推送 ksud...',
        'pushing_ko': '推送 kernelsu.ko...',
        'loading_module': '在 Root Shell 中加载内核模块...',
        'auto_executing': '自动提权 - 第{0}次: 执行中...',
        'auto_rooting': '自动提权 - 第{0}次: 提权中...',
        'warn_wait_timeout_reconnect': '  [提示] 等待超时，尝试直接等待重连',
        'checking_stability_10s2': '  检查连接稳定性 (10s)...',
        'status_prefix': '状态: ',
        'start_exec': '  开始执行 - 文件检查与推送',
        'check_file': '  检查文件: ',
        'log_path': '    路径: ',
        'log_status': '    状态: ',
        'check_file': '  检查文件: ',
        'log_path': '    路径: ',
        'log_status': '    状态: ',
        'err_missing_files': '  [错误] 缺少必要文件！',
        'err_preload_missing': '    - preload 文件未找到',
        'err_ionstack_missing': '    - ionstack.conf 文件未找到',
        'warn_place_files': '  请将 preload 和 ionstack.conf 放在程序运行目录下',
        'ok_all_checks': '  [OK] 所有文件检查通过',
        'warn_no_device': '  [警告] 当前未检测到已连接的设备',
        'log_detail': '  详情: ',
        'warn_usb_debug': '  请确保设备已通过 USB 连接并开启 USB 调试',
        'ok_device_connected': '  [OK] 设备已连接',
        'rebooting_device': '  正在执行设备重启...',
        'warn_reboot_abnormal': '  [警告] adb reboot 执行异常，继续等待断开...',
        'device_rebooting': '  设备正在重启中...',
        'waiting_disconnect': '  正在等待设备断开连接...',
        'reset_adb': '  重置 ADB 服务...',
        'ok_adb_reset': '  [OK] ADB 服务已重置',
        'warn_adb_reset_fail': '  [警告] ADB 服务重置失败，继续尝试...',
        'ok_device_disconnected': '  [OK] 设备已断开连接',
        'stopped_exec': '  已停止执行',
        'waiting_reconnect_adb': '  正在等待设备重新连接至 ADB...',
        'reboot_takes_time': '  (设备重启可能需要一些时间，请耐心等待...)',
        'ok_reconnected_waited': '  [OK] 设备已重新连接! (等待了 ',
        'still_waiting': '  仍在等待设备重连... (',
        'err_reconnect_timeout_3m': '  [错误] 设备重连超时 (3分钟)',
        'warn_check_retry': '  请检查设备状态并手动重试',
        'checking_stability_10s': '  正在检查 ADB 连接稳定性 (10秒)...',
        'warn_sec_disconnected': '  [警告] 第 ',
        'waiting_reconnect': '  正在等待设备重新连接...',
        'ok_restart_stability': '  [OK] 设备已重新连接，重新开始稳定性检查',
        'err_reconnect_failed': '  [错误] 设备重连失败',
        'restart_10s_check': '  重新开始 10 秒稳定性检查...',
        'err_unstable_usb': '  [错误] 连接不稳定，请检查 USB 连接',
        'ok_stable': '  [OK] 连接稳定! 稳定性检查通过 (10/10)',
        'pushing_files_to': '  正在推送文件到设备...',
        'err_push_preload': '  [错误] 推送 preload 失败',
        'ok_preload_pushed': '  [OK] preload 推送成功',
        'err_push_ionstack': '  [错误] 推送 ionstack.conf 失败',
        'ok_ionstack_pushed': '  [OK] ionstack.conf 推送成功',
        'err_chmod': '  [错误] chmod 失败',
        'ok_preload_exec': '  [OK] preload 已设置为可执行权限',
        'exec_done_push': '  执行完成! 文件已推送并设置权限',
        'now_click_root': '  现在可以点击「开始提权」进行 Root 提权',
        'start_root': '  开始提权 - 执行 preload',
        'err_no_device': '  [错误] 未检测到已连接的设备',
        'device_model': '  设备型号: ',
        'executing_root_cmds': '  正在执行提权命令...',
        'root_ok_banner': '  >>> 已成功提权! <<<',
        'detected_root_shell': '  检测到 Root Shell: ',
        'warn_root_timeout_5m': '  [警告] 提权超时 (5分钟)',
        'err_no_adb': '  [错误] 未找到 adb 命令',
        'err_exception': '  [错误] 执行异常: ',
        'err_disconnected_rebooted': '  [错误] 设备已断开连接 (可能已重启)',
        'err_no_root_prompt': '  [错误] 未检测到 Root 提示符',
        'root_fail_banner': '  >>> 提权失败，请重新尝试 <<<',
        'getroot_magisk': '  获取 Root - Magisk 环境安装与启动',
        'cmds_4s_interval': '  (所有命令在当前会话执行，间隔4秒)',
        'ok_device_connected': '  [OK] 设备已连接',
        'checking_magisk': '  正在检查 Magisk 是否安装...',
        'ok_magisk_installed': '  [OK] 检测到 Magisk 已安装，跳过APK安装步骤',
        'info_magisk_missing': '  [提示] 未检测到 Magisk，尝试安装当前目录下的APK...',
        'found_apks': '  找到 ',
        'installing_apk': '  正在安装: ',
        'ok_apk_installed': '  [OK] ',
        'warn_apk_install_fail': '  [警告] ',
        'warn_no_apk_dir': '  [警告] 当前目录下未找到APK文件，跳过安装',
        'info_busybox_missing': '  [提示] busybox 此无文件，跳过',
        'info_magiskapk_missing': '  [提示] magisk.apk 此无文件，跳过',
        'err_livesetup_missing': '  [错误] live_setup.sh 此无文件，无法继续',
        'ok_root_shell_direct': '  检测到已提权的 Root Shell，命令将直接在其中执行...',
        'err_send_root_shell': '  [错误] 无法向 Root Shell 发送命令',
        'info_normal_shell': '  [提示] 未检测到已提权的 Root Shell，改用普通 shell 执行',
        'getroot_done_banner': '  >>> 获取Root步骤执行完成! <<<',
        'getroot_done_verify': '  获取Root步骤执行完毕 (可在下方输入框手动验证)',
        'getroot_kernelsu': '  获取 Root - KernelSU 内核模块方式',
        'err_no_root_shell': '  [错误] 未检测到已提权的 Root Shell，请先提权成功',
        'warn_root_first': '  请先点击「开始提权」成功后再使用 KernelSU 方式',
        'searching_ksu': '  正在搜索运行目录下的 ksud 和 kernelsu.ko...',
        'ok_found_ksud': '  [OK] 找到 ksud: ',
        'err_no_ksud': '  [错误] 未找到 ksud 文件',
        'ok_found_ko': '  [OK] 找到 kernelsu.ko: ',
        'err_no_ko': '  [错误] 未找到 kernelsu.ko 文件',
        'warn_place_ksu': '  请将 ksud 与 kernelsu.ko 放在程序运行目录下',
        'err_push_ksud': '  [错误] 推送 ksud 失败',
        'ok_ksud_pushed': '  [OK] ksud 推送成功',
        'err_push_ko': '  [错误] 推送 kernelsu.ko 失败',
        'ok_ko_pushed': '  [OK] kernelsu.ko 推送成功',
        'exec_in_root_term': '  正在提权成功的终端中执行命令...',
        'checking_module_load': '  正在检测内核模块加载结果...',
        'ok_module_hint': '  [OK] 检测到 loaded kernel module 提示',
        'ok_module_lsmod': '  [OK] 检测到 kernelsu 内核模块已加载 (lsmod)',
        'warn_no_load_hint': '  [警告] 未检测到加载成功提示，请查看终端输出',
        'ksu_ok_banner': '  >>> 已使用KernelSU 获取Root[越狱模式] <<<',
        'ksu_verify': '  KernelSU 命令已执行，可在输入框手动验证',
        'ksu_fail_banner': '  >>> KernelSU 获取Root失败 <<<',
        'auto_mode_started': '  >>> 自动提权模式已启动 <<<',
        'auto_loop_desc': '  将自动循环执行 [开始执行] + [开始提权]',
        'auto_until_success': '  直到成功为止 (可点击「停止」终止)',
        'auto_phase1': '--- [自动] 阶段1: 等待设备重连并推送文件 ---',
        'auto_phase2': '--- [自动] 阶段2: 开始提权 ---',
        'auto_attempt_header': '第 ',
        'auto_exec_retry': '  第 ',
        'auto_root_retry': '  第 ',
        'err_missing_core_files': '  [错误] 缺少 preload 或 ionstack.conf 文件',
        'wait_device_conn': '  [等待] 设备未连接，等待重连...',
        'ok_device_connected': '  [OK] 设备已连接',
        'err_reconnect_timeout': '  [错误] 设备重连超时',
        'skip_reboot_wait': '  [跳过主动reboot] 等待设备因上次提权自动重启...',
        'ok_disconnected_rebooting': '  [OK] 设备已断开，确认正在重启',
        'ok_reconnected_wait': '  [OK] 设备已重连 (',
        'warn_sec_disc': '  [警告] 第',
        'ok_reconnected': '  [OK] 设备已重连',
        'ok_conn_stable': '  [OK] 连接稳定',
        'ok_perms_set': '  [OK] 权限设置成功',
        'ok_exec_phase': '  [OK] 执行阶段完成',
        'err_device_offline': '  [错误] 设备未连接',
        'auto_shell_detected': '  >>> 检测到 Root Shell! <<<',
        'auto_shell_kept': '  已保留 Root Shell，可在下方输入框直接发送命令',
        'warn_root_timeout': '  [警告] 提权超时',
        'err_disconnected_auto': '  [错误] 设备已断开 (可能已重启)',
        'auto_success_banner': '  >>> 自动提权成功! (共尝试 ',
        'auto_stopped': '  自动提权已停止',
        'err_bare': '  [错误] ',
        'cmd_timeout': '命令超时',
        'adb_not_found_msg': '未找到 adb 命令，请确保 adb 已安装并添加到 PATH',
        'adb_devices_failed': 'adb devices 执行失败 (rc={0}): {1}',
        'device_offline': '设备已连接但处于离线状态，请尝试重新插拔 USB',
        'device_unauthorized': '设备已连接但未授权 USB 调试，请在设备上点击「允许」并勾选「始终允许」',
        'device_status_abnormal': '设备状态异常: {0}',
        'device_not_detected': '未检测到任何设备连接，请检查 USB 连接和 USB 调试设置',
        'ctrl_c_interrupted': '^C (已中断)',
        'exit_code': '(退出码: {0})',
        'error_prefix': '错误: {0}',
        'welcome_usage': '  使用说明:',
        'welcome_step1': '    1. 将 preload 和 ionstack.conf 放在程序运行目录',
        'welcome_step2': '    2. 连接 Quest3/3s 设备 (USB 调试已开启)',
        'welcome_step3': '    3. ionstack.conf 必须与自己系统相匹配，不匹配的是无法成功的，',
        'welcome_step4': '       所以一定要适配自己系统对应的增量号',
        'welcome_cwd': '  当前工作目录: ',
        'manual_operation': '  已选择手动操作，请重新点击相应按钮',
        'starting_auto_retry': '  正在启动自动提权模式...',
        'stopping_task': '  [停止] 正在停止当前任务...',
        'no_running_task': '  当前没有正在运行的任务',
        'warn_prev_running': '  [警告] 上一个命令仍在执行中',
        'root_shell_closed': '  Root Shell 已关闭，使用普通命令执行',
        'status_get_root_start': '开始获取Root...',
        'status_get_root_failed': '获取Root失败',
        'status_kernelsu_start': '开始KernelSU获取Root...',
        'kernelsu_failed': 'KernelSU 获取Root失败',
        'kernelsu_success': 'KernelSU 获取Root成功',
        'kernelsu_done_manual': 'KernelSU 执行完成(请手动验证)',
        'get_root_done': '获取Root完成',
        'auto_retry_success': '自动提权成功',
        'stopped': '已停止',
        'session_title': '会话 {0}  ',
        'statusbar_ready': '就绪  |  工作目录: ',
        'installed': '已安装',
        'not_installed': '未安装',
        'about_app_title': '⚡ Quest3/3s 临时 Root 提权工具',
    },
    'en': {
        'execute': '▶  Execute',
        'root': '⚡  Root',
        'get_root': '🔓  Get Root',
        'stop': '■  Stop',
        'new_session': '＋ New Session',
        'lang_switch': '🌐 中文',
        'run': 'Run',
        'input_placeholder': 'Enter ADB or other commands, press Enter to execute... (e.g.: adb devices)',
        'status_ready': 'Ready',
        'file_status': '📁 Files:',
        'refresh': '🔄 Refresh',
        'file_ok': 'Ready',
        'file_miss': 'Missing',
        'welcome_title': '║        Quest3/3s Temp Root Tool  v1.0                   ║',
        'about': 'ℹ About',
        'about_title': 'About Quest3/3s Root Tool',
        'exec_done': 'Execute Done',
        'exec_fail': 'Execute Failed',
        'root_success': 'Root Success',
        'root_fail': 'Root Failed',
        'auto_retry_title': 'Root Failed',
        'auto_retry_msg': 'Root failed',
        'auto_retry_detail': 'Auto retry?',
        'auto_retry_ok': 'OK - Auto Root',
        'auto_retry_cancel': 'Cancel - Manual',
        'close_confirm': 'Confirm Close',
        'close_msg': 'A task is running in this session. Close anyway?',
        'yes': 'Yes',
        'no': 'No',
        'no_device': 'No connected device detected',
        'no_device_detail': 'Please connect device and run "Execute" first',
        'minimize': 'Minimize',
        'maximize': 'Maximize/Restore',
        'close': 'Close',
        'title': '⚡ Quest3/3s Temp Root Tool',
        'window_title': 'Quest3/3s Temp Root Tool v1.0',
        'ok': 'OK',
        'root_method_title': 'Get Root Method',
        'root_method_tip': 'Choose root method:',
        'root_success_title': '✓ Root Success',
        'root_success_msg': 'Root obtained successfully',
        'get_root_success_title': '✓ Get Root Success',
        'get_root_success_msg': 'Root obtained with Magisk',
        'kernelsu_success_title': '✓ KernelSU Root Success',
        'kernelsu_success_msg': 'Root obtained with KernelSU [Jailbreak Mode]',
        'adb_select_title': 'Select ADB Path',
        'adb_select_tip': 'ADB installations detected. Choose the one this tool should use:',
        'adb_missing_title': 'ADB Not Found',
        'adb_missing_msg': 'ADB was not found. Please install ADB (Android SDK Platform-Tools).\n'
                           'Download from https://developer.android.com/tools/releases/platform-tools,\n'
                           'or place adb.exe in the app directory or a common install path and reopen.',
        'ionstack_missing_title': 'ionstack.conf Not Found',
        'ionstack_missing_msg': 'It seems you have not compiled an ionstack for your system version.\n'
                                'Please compile it first at:\n'
                                'https://github.com/F-19-F/IonStackQuest3\n\n'
                                'After compiling, place it in the app directory.',
        'cancel': 'Cancel',
        'exists': 'exists',
        'not_exists': 'not found',
        'seconds': 's',
        'apk_files_start': ' APK file(s), installing...',
        'apk_install_ok': ' installed',
        'apk_install_fail_cont': ' install failed (continuing)',
        'sec_disconnected': ': device disconnected!',
        'auto_attempt_tail': ' attempts',
        'auto_exec_retry_tail': ' - execute phase failed, retrying...',
        'auto_root_retry_tail': ' - root failed, retrying...',
        'sec_disc_tail': 's, waiting for reconnect...',
        'auto_success_tail': ' attempts) <<<',
        'checking_files': 'Checking files...',
        'file_check_failed': 'File check failed',
        'checking_device_conn': 'Checking device connection...',
        'rebooting_dev': 'Rebooting device...',
        'waiting_dev_disconnect': 'Waiting for device disconnect...',
        'waiting_dev_reconnect': 'Waiting for device reconnect...',
        'checking_stability': 'Checking connection stability...',
        'pushing_files': 'Pushing files...',
        'executing_root': 'Executing root commands...',
        'checking_device': 'Checking device...',
        'checking_magisk_installed': 'Checking if Magisk is installed...',
        'pushing_busybox': 'Pushing busybox...',
        'pushing_magisk_apk': 'Pushing magisk.apk...',
        'pushing_live_setup': 'Pushing live_setup.sh...',
        'executing_shell': 'Executing shell commands...',
        'in_root_shell': 'Executing in Root Shell...',
        'get_root_done_manual': 'Get Root done (verify manually)',
        'searching_ksu_files': 'Searching KernelSU files...',
        'pushing_ksud': 'Pushing ksud...',
        'pushing_ko': 'Pushing kernelsu.ko...',
        'loading_module': 'Loading kernel module in Root Shell...',
        'auto_executing': 'Auto root - attempt {0}: executing...',
        'auto_rooting': 'Auto root - attempt {0}: rooting...',
        'warn_wait_timeout_reconnect': '  [Info] Wait timeout, trying to wait for reconnect directly',
        'checking_stability_10s2': '  Checking connection stability (10s)...',
        'status_prefix': 'Status: ',
        'start_exec': '  Execute - file check & push',
        'check_file': '  Checking file: ',
        'log_path': '    Path: ',
        'log_status': '    Status: ',
        'check_file': '  Checking file: ',
        'log_path': '    Path: ',
        'log_status': '    Status: ',
        'err_missing_files': '  [Error] Missing required files!',
        'err_preload_missing': '    - preload file not found',
        'err_ionstack_missing': '    - ionstack.conf file not found',
        'warn_place_files': '  Place preload and ionstack.conf in the app directory',
        'ok_all_checks': '  [OK] All file checks passed',
        'warn_no_device': '  [Warn] No connected device detected',
        'log_detail': '  Detail: ',
        'warn_usb_debug': '  Make sure the device is connected via USB with USB debugging enabled',
        'ok_device_connected': '  [OK] Device connected',
        'rebooting_device': '  Rebooting device...',
        'warn_reboot_abnormal': '  [Warn] adb reboot failed, waiting for disconnect...',
        'device_rebooting': '  Device is rebooting...',
        'waiting_disconnect': '  Waiting for device to disconnect...',
        'reset_adb': '  Resetting ADB service...',
        'ok_adb_reset': '  [OK] ADB service reset',
        'warn_adb_reset_fail': '  [Warn] ADB service reset failed, retrying...',
        'ok_device_disconnected': '  [OK] Device disconnected',
        'stopped_exec': '  Stopped',
        'waiting_reconnect_adb': '  Waiting for device to reconnect to ADB...',
        'reboot_takes_time': '  (Device reboot may take a while, please be patient...)',
        'ok_reconnected_waited': '  [OK] Device reconnected! (waited ',
        'still_waiting': '  Still waiting for reconnect... (',
        'err_reconnect_timeout_3m': '  [Error] Reconnect timeout (3 min)',
        'warn_check_retry': '  Check device status and retry manually',
        'checking_stability_10s': '  Checking ADB connection stability (10s)...',
        'warn_sec_disconnected': '  [Warn] Second ',
        'waiting_reconnect': '  Waiting for device to reconnect...',
        'ok_restart_stability': '  [OK] Device reconnected, restarting stability check',
        'err_reconnect_failed': '  [Error] Reconnect failed',
        'restart_10s_check': '  Restarting 10s stability check...',
        'err_unstable_usb': '  [Error] Unstable connection, check the USB cable',
        'ok_stable': '  [OK] Connection stable! Stability check passed (10/10)',
        'pushing_files_to': '  Pushing files to device...',
        'err_push_preload': '  [Error] Push preload failed',
        'ok_preload_pushed': '  [OK] preload pushed',
        'err_push_ionstack': '  [Error] Push ionstack.conf failed',
        'ok_ionstack_pushed': '  [OK] ionstack.conf pushed',
        'err_chmod': '  [Error] chmod failed',
        'ok_preload_exec': '  [OK] preload set as executable',
        'exec_done_push': '  Done! Files pushed and permissions set',
        'now_click_root': '  Now click [Start Root] to get root',
        'start_root': '  Start Root - run preload',
        'err_no_device': '  [Error] No connected device detected',
        'device_model': '  Device model: ',
        'executing_root_cmds': '  Executing root commands...',
        'root_ok_banner': '  >>> Root succeeded! <<<',
        'detected_root_shell': '  Root Shell detected: ',
        'warn_root_timeout_5m': '  [Warn] Root timeout (5 min)',
        'err_no_adb': '  [Error] adb command not found',
        'err_exception': '  [Error] Exception: ',
        'err_disconnected_rebooted': '  [Error] Device disconnected (may have rebooted)',
        'err_no_root_prompt': '  [Error] Root prompt not detected',
        'root_fail_banner': '  >>> Root failed, please retry <<<',
        'getroot_magisk': '  Get Root - Magisk setup & launch',
        'cmds_4s_interval': '  (Commands run in the current session, 4s apart)',
        'ok_device_connected': '  [OK] Device connected',
        'checking_magisk': '  Checking if Magisk is installed...',
        'ok_magisk_installed': '  [OK] Magisk installed, skipping APK install step',
        'info_magisk_missing': '  [Info] Magisk not found, trying to install APK from current dir...',
        'found_apks': '  Found ',
        'installing_apk': '  Installing: ',
        'ok_apk_installed': '  [OK] ',
        'warn_apk_install_fail': '  [Warn] ',
        'warn_no_apk_dir': '  [Warn] No APK found in current dir, skipping install',
        'info_busybox_missing': '  [Info] busybox missing, skipping',
        'info_magiskapk_missing': '  [Info] magisk.apk missing, skipping',
        'err_livesetup_missing': '  [Error] live_setup.sh missing, cannot continue',
        'ok_root_shell_direct': '  Root Shell available, commands will run inside it directly...',
        'err_send_root_shell': '  [Error] Cannot send command to Root Shell',
        'info_normal_shell': '  [Info] No rooted shell, falling back to normal shell',
        'getroot_done_banner': '  >>> Get Root steps done! <<<',
        'getroot_done_verify': '  Get Root steps done (verify in the input box below)',
        'getroot_kernelsu': '  Get Root - KernelSU kernel module method',
        'err_no_root_shell': '  [Error] No rooted shell, run [Start Root] first',
        'warn_root_first': '  Click [Start Root] successfully before using KernelSU',
        'searching_ksu': '  Searching ksud and kernelsu.ko in the app directory...',
        'ok_found_ksud': '  [OK] Found ksud: ',
        'err_no_ksud': '  [Error] ksud file not found',
        'ok_found_ko': '  [OK] Found kernelsu.ko: ',
        'err_no_ko': '  [Error] kernelsu.ko file not found',
        'warn_place_ksu': '  Place ksud and kernelsu.ko in the app directory',
        'err_push_ksud': '  [Error] Push ksud failed',
        'ok_ksud_pushed': '  [OK] ksud pushed',
        'err_push_ko': '  [Error] Push kernelsu.ko failed',
        'ok_ko_pushed': '  [OK] kernelsu.ko pushed',
        'exec_in_root_term': '  Executing commands in the rooted terminal...',
        'checking_module_load': '  Checking kernel module load result...',
        'ok_module_hint': '  [OK] "loaded kernel module" hint detected',
        'ok_module_lsmod': '  [OK] kernelsu module loaded (lsmod)',
        'warn_no_load_hint': '  [Warn] No load-success hint, check terminal output',
        'ksu_ok_banner': '  >>> Root with KernelSU [Jailbreak Mode] <<<',
        'ksu_verify': '  KernelSU commands done, verify in the input box',
        'ksu_fail_banner': '  >>> KernelSU root failed <<<',
        'auto_mode_started': '  >>> Auto root mode started <<<',
        'auto_loop_desc': '  Will loop [Execute] + [Start Root] automatically',
        'auto_until_success': '  Until success (click [Stop] to end)',
        'auto_phase1': '--- [Auto] Phase 1: wait for reconnect & push files ---',
        'auto_phase2': '--- [Auto] Phase 2: start rooting ---',
        'auto_attempt_header': 'Attempt ',
        'auto_exec_retry': '  Attempt ',
        'auto_root_retry': '  Attempt ',
        'err_missing_core_files': '  [Error] Missing preload or ionstack.conf',
        'wait_device_conn': '  [Wait] Device not connected, waiting...',
        'ok_device_connected': '  [OK] Device connected',
        'err_reconnect_timeout': '  [Error] Reconnect timeout',
        'skip_reboot_wait': '  [Skip manual reboot] waiting for the device to auto-reboot from last root attempt...',
        'ok_disconnected_rebooting': '  [OK] Device disconnected, confirming reboot',
        'ok_reconnected_wait': '  [OK] Device reconnected (',
        'warn_sec_disc': '  [Warn] Disconnected at ',
        'ok_reconnected': '  [OK] Device reconnected',
        'ok_conn_stable': '  [OK] Connection stable',
        'ok_perms_set': '  [OK] Permissions set',
        'ok_exec_phase': '  [OK] Execute phase done',
        'err_device_offline': '  [Error] Device not connected',
        'auto_shell_detected': '  >>> Root Shell detected! <<<',
        'auto_shell_kept': '  Root Shell kept alive, send commands in the input box below',
        'warn_root_timeout': '  [Warn] Root timeout',
        'err_disconnected_auto': '  [Error] Device disconnected (may have rebooted)',
        'auto_success_banner': '  >>> Auto root succeeded! (after ',
        'auto_stopped': '  Auto root stopped',
        'err_bare': '  [Error] ',
        'cmd_timeout': 'Command timeout',
        'adb_not_found_msg': 'adb command not found, make sure adb is installed and in PATH',
        'adb_devices_failed': 'adb devices failed (rc={0}): {1}',
        'device_offline': 'Device is connected but offline, try re-plugging the USB',
        'device_unauthorized': 'Device connected but USB debugging not authorized. Tap "Allow" and check "Always allow" on the device',
        'device_status_abnormal': 'Abnormal device status: {0}',
        'device_not_detected': 'No device detected, check USB connection and USB debugging settings',
        'ctrl_c_interrupted': '^C (interrupted)',
        'exit_code': '(exit code: {0})',
        'error_prefix': 'Error: {0}',
        'welcome_usage': '  Usage:',
        'welcome_step1': '    1. Put preload and ionstack.conf in the app directory',
        'welcome_step2': '    2. Connect Quest3/3s (USB debugging enabled)',
        'welcome_step3': '    3. ionstack.conf must match your system, otherwise it will not work,',
        'welcome_step4': "       make sure it fits your system's build number",
        'welcome_cwd': '  Current working dir: ',
        'manual_operation': '  Manual operation selected, please click the button again',
        'starting_auto_retry': '  Starting auto root mode...',
        'stopping_task': '  [Stop] Stopping current task...',
        'no_running_task': '  No task is currently running',
        'warn_prev_running': '  [Warn] Previous command still running',
        'root_shell_closed': '  Root Shell closed, using normal commands',
        'status_get_root_start': 'Starting Get Root...',
        'status_get_root_failed': 'Get Root failed',
        'status_kernelsu_start': 'Starting KernelSU root...',
        'kernelsu_failed': 'KernelSU root failed',
        'kernelsu_success': 'KernelSU root succeeded',
        'kernelsu_done_manual': 'KernelSU done (verify manually)',
        'get_root_done': 'Get Root done',
        'auto_retry_success': 'Auto root succeeded',
        'stopped': 'Stopped',
        'session_title': 'Session {0}  ',
        'statusbar_ready': 'Ready  |  Work dir: ',
        'installed': 'Installed',
        'not_installed': 'Not installed',
        'about_app_title': '⚡ Quest3/3s Temp Root Tool',
    }
}

def tr(key):
    return T.get(LANG, T['zh']).get(key, key)


# ==================== ADB 辅助函数 ====================
def run_adb_command(cmd, timeout=30):
    """执行 ADB 命令并返回结果 (stdout, stderr, rc)"""
    try:
        if isinstance(cmd, str):
            cmd = cmd.split()
        kwargs = _subprocess_common_kwargs()
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout, **kwargs)
        out = decode_bytes_smart(result.stdout)
        err = decode_bytes_smart(result.stderr)
        return out, err, result.returncode
    except subprocess.TimeoutExpired:
        return "", tr('cmd_timeout'), -1
    except FileNotFoundError:
        return "", tr('adb_not_found_msg'), -2
    except Exception as e:
        return "", str(e), -3


def run_adb_reboot():
    """执行 adb reboot - 使用 Popen 非阻塞方式，避免子进程崩溃弹窗"""
    try:
        kwargs = _subprocess_common_kwargs()
        proc = subprocess.Popen(adb_cmd('reboot'),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.DEVNULL, **kwargs)
        # 最多等5秒让 reboot 命令发出，不阻塞太久
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        return True
    except FileNotFoundError:
        return False
    except Exception:
        # reboot 后设备断开，adb 进程可能异常退出，这是正常的
        return True


import queue as _queue


def _create_reader_queue(proc):
    """创建一个后台线程持续读取进程stdout的原始字节，返回queue供主线程消费。
    跨平台兼容（Windows不支持select对pipe的使用）。"""
    q = _queue.Queue()

    def _reader_thread():
        try:
            while True:
                data = os.read(proc.stdout.fileno(), 4096)
                if not data:
                    break
                q.put(data)
        except (OSError, ValueError):
            pass
        q.put(None)  # sentinel 表示EOF

    t = threading.Thread(target=_reader_thread, daemon=True)
    t.start()
    return q


def _read_queue(q, timeout=0.3):
    """从queue中读取一块数据，超时返回None"""
    try:
        return q.get(timeout=timeout)
    except _queue.Empty:
        return None


def _read_proc_output(proc, timeout=0.5):
    """[已弃用] 保留兼容，内部不再使用select"""
    try:
        readable, _, _ = select.select([proc.stdout], [], [], timeout)
    except (ValueError, OSError):
        return None
    if not readable:
        return None
    try:
        data = os.read(proc.stdout.fileno(), 4096)
    except (OSError, ValueError):
        return None
    if not data:
        return None
    return decode_bytes_smart(data)


def adb_kill_all():
    """强制结束所有 adb 进程，清理损坏的 adb server 状态"""
    try:
        if IS_WINDOWS:
            subprocess.run(['taskkill', '/F', '/IM', 'adb.exe'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            timeout=10, **_subprocess_common_kwargs())
        else:
            subprocess.run(['pkill', '-9', 'adb'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            timeout=10, **_subprocess_common_kwargs())
    except Exception:
        pass


def adb_repair_server():
    """彻底重启 adb server，解决 protocol fault / Connection reset by peer 等损坏状态"""
    for _ in range(3):
        run_adb_command(adb_cmd('kill-server'), timeout=10)
        adb_kill_all()
        time.sleep(1)
        run_adb_command(adb_cmd('start-server'), timeout=15)
        _, _, rc = run_adb_command(adb_cmd('devices'), timeout=8)
        if rc == 0:
            return True
        time.sleep(2)
    return False


def adb_devices_raw():
    """执行 adb devices；server 状态损坏时自动彻底重启并重试"""
    run_adb_command(adb_cmd('start-server'), timeout=10)
    stdout, stderr, rc = run_adb_command(adb_cmd('devices'), timeout=8)
    if rc != 0 and adb_repair_server():
        stdout, stderr, rc = run_adb_command(adb_cmd('devices'), timeout=8)
    return stdout, stderr, rc


def check_device_connected():
    """检查设备是否已连接且可用，自动启动adb server。返回 bool"""
    stdout, stderr, rc = adb_devices_raw()
    if rc != 0:
        return False
    lines = stdout.strip().split('\n')
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == 'device':
            return True
    return False


def check_device_status():
    """检查设备状态，返回 (connected: bool, detail: str)"""
    stdout, stderr, rc = adb_devices_raw()
    if rc != 0:
        return False, f"{tr('adb_devices_failed').format(rc, stderr)}"
    lines = stdout.strip().split('\n')
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            status = parts[1]
            if status == 'device':
                return True, None
            elif status == 'unauthorized':
                return False, tr('device_unauthorized')
            elif status == 'offline':
                return False, tr('device_offline')
            else:
                return False, f"{tr('device_status_abnormal').format(status)}"
    return False, tr('device_not_detected')


def get_device_model():
    """获取设备型号"""
    stdout, _, _ = run_adb_command(adb_cmd('shell', 'getprop', 'ro.product.model'), timeout=8)
    return stdout.strip()


# ==================== 工作线程 ====================
class ExecuteWorker(QThread):
    """开始执行 - 文件检查、adb reboot、重连检测、推送文件
    同时打开CMD窗口展示全过程，内置终端也显示状态"""
    output_signal = pyqtSignal(str, str)       # text, color_type
    ansi_output_signal = pyqtSignal(str)       # 带ANSI的原始输出
    status_signal = pyqtSignal(str)            # status text
    finished_signal = pyqtSignal(bool)         # success

    def __init__(self):
        super().__init__()
        self.stop_flag = False
        self._mutex = QMutex()

    def stop(self):
        self.stop_flag = True

    def emit_output(self, text, color_type="output"):
        self.output_signal.emit(text, color_type)

    def emit_ansi(self, text):
        self.ansi_output_signal.emit(text)

    def run(self):
        self.stop_flag = False

        # ---- 步骤1: 检查文件是否存在 ----
        self.status_signal.emit(tr('checking_files'))
        self.emit_output("=" * 56, "system")
        self.emit_output(tr('start_exec'), "info")
        self.emit_output("=" * 56, "system")

        preload_path = os.path.join(os.getcwd(), "preload")
        ionstack_path = os.path.join(os.getcwd(), "ionstack.conf")

        preload_exists = os.path.isfile(preload_path)
        ionstack_exists = os.path.isfile(ionstack_path)

        self.emit_output(f"{tr('check_file')}preload", "system")
        self.emit_output(f"{tr('log_path')}{preload_path}", "system")
        self.emit_output(f"{tr('log_status')}{tr('exists') if preload_exists else tr('not_exists')}",
                         "success" if preload_exists else "error")

        self.emit_output(f"{tr('check_file')}ionstack.conf", "system")
        self.emit_output(f"{tr('log_path')}{ionstack_path}", "system")
        self.emit_output(f"{tr('log_status')}{tr('exists') if ionstack_exists else tr('not_exists')}",
                         "success" if ionstack_exists else "error")

        if not preload_exists or not ionstack_exists:
            self.emit_output("", "output")
            self.emit_output(tr('err_missing_files'), "error")
            if not preload_exists:
                self.emit_output(tr('err_preload_missing'), "error")
            if not ionstack_exists:
                self.emit_output(tr('err_ionstack_missing'), "error")
            self.emit_output(tr('warn_place_files'), "warning")
            self.status_signal.emit(tr('file_check_failed'))
            self.finished_signal.emit(False)
            return

        self.emit_output(tr('ok_all_checks'), "success")
        self.emit_output("", "output")

        # ---- 步骤2: 检查设备连接 ----
        self.status_signal.emit(tr('checking_device_conn'))
        connected, detail = check_device_status()
        if not connected:
            self.emit_output(tr('warn_no_device'), "warning")
            if detail:
                self.emit_output(f"{tr('log_detail')}{detail}", "warning")
            self.emit_output(tr('warn_usb_debug'), "warning")
            self.finished_signal.emit(False)
            return

        device_model = get_device_model()
        self.emit_output(f"{tr('ok_device_connected')}: {device_model}", "success")

        # ---- 步骤3: 执行 adb reboot ----
        self.status_signal.emit(tr('rebooting_dev'))
        self.emit_output("", "output")
        self.emit_output(tr('rebooting_device'), "info")
        self.emit_output("$ adb reboot", "command")

        ok = run_adb_reboot()
        if not ok:
            self.emit_output(tr('warn_reboot_abnormal'), "warning")

        self.emit_output(tr('device_rebooting'), "device")

        # ---- 步骤4: 等待设备断开 ----
        self.status_signal.emit(tr('waiting_dev_disconnect'))
        self.emit_output("", "output")
        self.emit_output(tr('waiting_disconnect'), "system")

        time.sleep(2)
        self.emit_output(tr('reset_adb'), "system")
        if adb_repair_server():
            self.emit_output(tr('ok_adb_reset'), "success")
        else:
            self.emit_output(tr('warn_adb_reset_fail'), "warning")

        disconnect_wait = 0
        while not self.stop_flag and disconnect_wait < 30:
            if not check_device_connected():
                self.emit_output(tr('ok_device_disconnected'), "success")
                break
            time.sleep(1)
            disconnect_wait += 1

        if self.stop_flag:
            self.emit_output(tr('stopped_exec'), "warning")
            self.finished_signal.emit(False)
            return

        # ---- 步骤5: 等待设备重连 ----
        self.status_signal.emit(tr('waiting_dev_reconnect'))
        self.emit_output("", "output")
        self.emit_output(tr('waiting_reconnect_adb'), "info")
        self.emit_output(tr('reboot_takes_time'), "system")

        reconnect_wait = 0
        connected = False
        while not self.stop_flag and reconnect_wait < 180:
            if check_device_connected():
                connected = True
                self.emit_output(f"{tr('ok_reconnected_waited')}{reconnect_wait}{tr('seconds')})", "success")
                break
            if reconnect_wait > 0 and reconnect_wait % 10 == 0:
                self.emit_output(f"{tr('still_waiting')}{reconnect_wait}s)", "system")
            time.sleep(2)
            reconnect_wait += 2

        if self.stop_flag:
            self.emit_output(tr('stopped_exec'), "warning")
            self.finished_signal.emit(False)
            return

        if not connected:
            self.emit_output(tr('err_reconnect_timeout_3m'), "error")
            self.emit_output(tr('warn_check_retry'), "warning")
            self.finished_signal.emit(False)
            return

        # ---- 步骤6: 检查连接稳定性 (10秒) ----
        self.status_signal.emit(tr('checking_stability'))
        self.emit_output("", "output")
        self.emit_output(tr('checking_stability_10s'), "info")

        stable = True
        for i in range(10):
            if self.stop_flag:
                self.emit_output(tr('stopped_exec'), "warning")
                self.finished_signal.emit(False)
                return
            if not check_device_connected():
                self.emit_output(f"{tr('warn_sec_disconnected')}{i+1}{tr('sec_disconnected')}", "error")
                stable = False
                self.emit_output(tr('waiting_reconnect'), "system")
                retry = 0
                reconnected = False
                while not self.stop_flag and retry < 60:
                    if check_device_connected():
                        reconnected = True
                        self.emit_output(tr('ok_restart_stability'), "success")
                        break
                    time.sleep(2)
                    retry += 2
                if not reconnected:
                    self.emit_output(tr('err_reconnect_failed'), "error")
                    self.finished_signal.emit(False)
                    return
                self.emit_output(tr('restart_10s_check'), "info")
                stable = True
                for j in range(10):
                    if self.stop_flag:
                        self.finished_signal.emit(False)
                        return
                    if not check_device_connected():
                        stable = False
                        break
                    if j < 9:
                        time.sleep(1)
                if not stable:
                    break
                else:
                    break
            else:
                if i < 9:
                    time.sleep(1)

        if not stable:
            self.emit_output(tr('err_unstable_usb'), "error")
            self.finished_signal.emit(False)
            return

        self.emit_output(tr('ok_stable'), "success")

        # ---- 步骤7: 推送文件并设置权限 ----
        self.status_signal.emit(tr('pushing_files'))
        self.emit_output("", "output")
        self.emit_output(tr('pushing_files_to'), "info")

        # adb push preload
        self.emit_output("$ adb push preload /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            adb_cmd('push', preload_path, '/data/local/tmp/'), timeout=30)
        if rc != 0:
            self.emit_output(f"{tr('err_push_preload')}: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        if stdout.strip():
            self.emit_output(f"  {stdout.strip()}", "output")
        if stderr.strip():
            self.emit_output(f"  {stderr.strip()}", "output")
        self.emit_output(tr('ok_preload_pushed'), "success")

        # adb push ionstack.conf
        self.emit_output("$ adb push ionstack.conf /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            adb_cmd('push', ionstack_path, '/data/local/tmp/'), timeout=30)
        if rc != 0:
            self.emit_output(f"{tr('err_push_ionstack')}: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        if stdout.strip():
            self.emit_output(f"  {stdout.strip()}", "output")
        if stderr.strip():
            self.emit_output(f"  {stderr.strip()}", "output")
        self.emit_output(tr('ok_ionstack_pushed'), "success")

        # adb shell chmod +x
        self.emit_output("$ adb shell chmod +x /data/local/tmp/preload", "command")
        stdout, stderr, rc = run_adb_command(
            adb_cmd('shell', 'chmod', '+x', '/data/local/tmp/preload'), timeout=10)
        if rc != 0:
            self.emit_output(f"{tr('err_chmod')}: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        self.emit_output(tr('ok_preload_exec'), "success")

        # ---- 完成 ----
        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        self.emit_output(tr('exec_done_push'), "success")
        self.emit_output(tr('now_click_root'), "info")
        self.emit_output("=" * 56, "system")
        self.status_signal.emit(tr('exec_done'))
        self.finished_signal.emit(True)


class RootWorker(QThread):
    """开始提权 - subprocess捕获输出(内置终端显示全过程) + CMD窗口交互"""
    output_signal = pyqtSignal(str, str)
    ansi_output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    success_signal = pyqtSignal()
    failure_signal = pyqtSignal()
    need_auto_retry_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stop_flag = False
        self.process = None
        self._stdin_pipe = None
        self._shell_lock = threading.Lock()

    def stop(self):
        self.stop_flag = True
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass

    def emit_output(self, text, color_type="output"):
        self.output_signal.emit(text, color_type)

    def emit_ansi(self, text):
        self.ansi_output_signal.emit(text)

    def run(self):
        self.stop_flag = False

        self.output_signal.emit("", "output")
        self.emit_output("=" * 56, "system")
        self.emit_output(tr('start_root'), "info")
        self.emit_output("=" * 56, "system")

        self.status_signal.emit(tr('checking_device'))
        connected, detail = check_device_status()
        if not connected:
            self.emit_output(tr('err_no_device'), "error")
            if detail:
                self.emit_output(f"{tr('log_detail')}{detail}", "error")
            self.emit_output(tr('warn_usb_debug'), "warning")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return

        device_model = get_device_model()
        self.emit_output(f"{tr('device_model')}{device_model}", "device")

        self.status_signal.emit(tr('executing_root'))
        self.emit_output("", "output")
        self.emit_output(tr('executing_root_cmds'), "info")
        self.emit_output("$ adb shell /data/local/tmp/preload", "command")
        self.emit_output("", "output")

        root_detected = False

        try:
            self.process = subprocess.Popen(
                adb_cmd('shell', '/data/local/tmp/preload'),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                bufsize=0,
                **_subprocess_common_kwargs()
            )

            reader_q = _create_reader_queue(self.process)
            start_time = time.time()
            pending = ""

            while not self.stop_flag:
                raw = _read_queue(reader_q, 0.3)
                if raw is not None:
                    if raw is None:  # EOF
                        break
                    chunk = decode_bytes_smart(raw)
                    # 立即输出原始内容到内置终端（保留所有原始字符和颜色）
                    self.ansi_output_signal.emit(chunk)

                    # 累积到pending用于检测root提示符
                    pending += chunk
                    lines = pending.split('\n')
                    for line in lines:
                        stripped = line.strip('\r ')
                        if stripped and self._is_root_prompt(stripped):
                            root_detected = True
                            self._stdin_pipe = self.process.stdin
                            self.emit_output("", "output")
                            self.emit_output("=" * 56, "system")
                            self.emit_output(tr('root_ok_banner'), "success")
                            self.emit_output(f"{tr('detected_root_shell')}{stripped}", "success")
                            self.emit_output("=" * 56, "system")
                            self.status_signal.emit(tr('root_success'))
                            self.success_signal.emit()

                            # 不再打开独立CMD窗口，保持内置终端活跃，用户可直接在输入框发送命令
                            # 持续读取输出直到进程退出或停止
                            while not self.stop_flag:
                                raw = _read_queue(reader_q, 0.5)
                                if raw is None:
                                    if self.process.poll() is not None:
                                        break
                                elif raw:
                                    self.ansi_output_signal.emit(decode_bytes_smart(raw))
                            break
                    if lines:
                        pending = lines[-1]
                    if root_detected:
                        break

                elif self.process.poll() is not None:
                    raw = _read_queue(reader_q, 0.1)
                    while raw is not None:
                        if raw:
                            self.ansi_output_signal.emit(decode_bytes_smart(raw))
                        raw = _read_queue(reader_q, 0.1)
                    break

                elapsed = time.time() - start_time
                if elapsed > 300 and not root_detected:
                    self.emit_output(tr('warn_root_timeout_5m'), "warning")
                    break

        except FileNotFoundError:
            self.emit_output(tr('err_no_adb'), "error")
            self.failure_signal.emit()
            self.need_auto_retry_signal.emit()
            self.finished_signal.emit()
            return
        except Exception as e:
            self.emit_output(f"{tr('err_exception')}{str(e)}", "error")
            self.failure_signal.emit()
            self.need_auto_retry_signal.emit()
            self.finished_signal.emit()
            return

        if self.stop_flag:
            self.emit_output("", "output")
            self.emit_output(tr('stopped_exec'), "warning")
            self.finished_signal.emit()
            return

        if not root_detected:
            self.emit_output("", "output")
            if not check_device_connected():
                self.emit_output(tr('err_disconnected_rebooted'), "error")
            else:
                self.emit_output(tr('err_no_root_prompt'), "error")
            self.emit_output(tr('root_fail_banner'), "error")
            self.status_signal.emit(tr('root_fail'))
            self.failure_signal.emit()
            self.need_auto_retry_signal.emit()

        if self.process and not root_detected:
            try:
                self.process.terminate()
            except Exception:
                pass

        self.finished_signal.emit()

    def _is_root_prompt(self, line):
        line = line.strip()
        if not line:
            return False
        # 去掉尾部空格后必须以 # 结尾
        stripped_line = line.rstrip()
        if not stripped_line.endswith('#'):
            return False
        # 排除太长的行（提示符不会太长）
        if len(stripped_line) > 80:
            return False
        # 排除以 # 开头且后面还有内容的行（真正的注释行），但纯 # 提示符不排除
        if stripped_line.startswith('#') and len(stripped_line) > 1:
            return False
        # 排除包含 URL 的行
        if '://' in stripped_line:
            return False
        # 排除包含明显非提示符关键词的行
        exclude_keywords = ['echo', 'printf', 'cat ', 'sed ', 'awk ', 'grep ']
        for kw in exclude_keywords:
            if kw in stripped_line.lower():
                return False
        # 匹配各种 root 提示符格式:
        #   #  / quest3:/ #  / root@quest3:/ #  / quest3:/data/local/tmp #
        return True

    def send_to_shell(self, command):
        with self._shell_lock:
            if self._stdin_pipe and not self._stdin_pipe.closed:
                try:
                    self._stdin_pipe.write((command + '\n').encode('utf-8'))
                    self._stdin_pipe.flush()
                    return True
                except Exception:
                    return False
        return False


class GetRootWorker(QThread):
    """获取root - 单会话执行，检查面具、推文件、执行脚本、启动magisk daemon"""
    output_signal = pyqtSignal(str, str)
    ansi_output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    success_signal = pyqtSignal()
    failure_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    CMD_DELAY = 4  # 命令间延迟4秒

    def __init__(self, root_shell=None):
        super().__init__()
        self.stop_flag = False
        self.process = None
        self._stdin_pipe = None
        self.root_shell = root_shell

    def stop(self):
        self.stop_flag = True
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass

    def emit_output(self, text, color_type="output"):
        self.output_signal.emit(text, color_type)

    def emit_ansi(self, text):
        self.ansi_output_signal.emit(text)

    def _delay(self):
        """执行命令延迟"""
        for _ in range(self.CMD_DELAY * 10):
            if self.stop_flag:
                return False
            time.sleep(0.1)
        return True

    def _run_adb(self, cmd, timeout=60):
        """执行adb命令并渲染ANSI原始输出"""
        self.emit_output(f"$ {' '.join(cmd) if isinstance(cmd, list) else cmd}", "command")
        try:
            kw = _subprocess_common_kwargs()
            if isinstance(cmd, str):
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, cwd=os.getcwd(),
                                        bufsize=0, **kw)
            else:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        bufsize=0, **kw)
            reader_q = _create_reader_queue(proc)
            while not self.stop_flag:
                raw = _read_queue(reader_q, 0.3)
                if raw is not None:
                    if raw is None:  # EOF
                        break
                    self.ansi_output_signal.emit(decode_bytes_smart(raw))
                elif proc.poll() is not None:
                    raw = _read_queue(reader_q, 0.1)
                    while raw is not None:
                        if raw:
                            self.ansi_output_signal.emit(decode_bytes_smart(raw))
                        raw = _read_queue(reader_q, 0.1)
                    break
            rc = proc.wait(timeout=timeout)
            return rc == 0
        except Exception as e:
            self.emit_output(f"{tr('err_bare')}{str(e)}", "error")
            return False

    def run(self):
        self.stop_flag = False

        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        self.emit_output(tr('getroot_magisk'), "info")
        self.emit_output(tr('cmds_4s_interval'), "system")
        self.emit_output("=" * 56, "system")

        # 检查设备
        self.status_signal.emit(tr('checking_device'))
        connected, detail = check_device_status()
        if not connected:
            self.emit_output(tr('err_no_device'), "error")
            if detail:
                self.emit_output(f"{tr('log_detail')}{detail}", "error")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return
        self.emit_output(f"{tr('ok_device_connected')}: {get_device_model()}", "success")

        # 检查Magisk是否已安装
        self.emit_output("", "output")
        self.status_signal.emit(tr('checking_magisk_installed'))
        self.emit_output(tr('checking_magisk'), "info")
        out, err, rc = run_adb_command(
            adb_cmd('shell', 'pm', 'list', 'packages'), timeout=15)
        magisk_installed = 'com.topjohnwu.magisk' in out.lower()
        if magisk_installed:
            self.emit_output(tr('ok_magisk_installed'), "success")
        else:
            self.emit_output(tr('info_magisk_missing'), "warning")
            apk_files = [f for f in os.listdir(os.getcwd()) if f.lower().endswith('.apk')]
            if apk_files:
                self.emit_output(f"{tr('found_apks')}{len(apk_files)}{tr('apk_files_start')}", "info")
                for apk in apk_files:
                    if not self._delay():
                        self.failure_signal.emit(); self.finished_signal.emit(); return
                    apk_path = os.path.join(os.getcwd(), apk)
                    self.emit_output(f"{tr('installing_apk')}{apk}", "info")
                    ok = self._run_adb(adb_cmd('install', '-r', apk_path), timeout=120)
                    if ok:
                        self.emit_output(f"{tr('ok_apk_installed')}{apk}{tr('apk_install_ok')}", "success")
                    else:
                        self.emit_output(f"{tr('warn_apk_install_fail')}{apk}{tr('apk_install_fail_cont')}", "warning")
            else:
                self.emit_output(tr('warn_no_apk_dir'), "warning")

        # ===== push busybox =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit(tr('pushing_busybox'))
        busybox_path = os.path.join(os.getcwd(), "busybox")
        if os.path.isfile(busybox_path):
            self._run_adb(adb_cmd('push', busybox_path, '/data/local/tmp/'), timeout=60)
        else:
            self.emit_output("$ adb push busybox /data/local/tmp/", "command")
            self.emit_output(tr('info_busybox_missing'), "warning")

        # ===== push magisk.apk =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit(tr('pushing_magisk_apk'))
        magisk_apk_path = os.path.join(os.getcwd(), "magisk.apk")
        if os.path.isfile(magisk_apk_path):
            self._run_adb(adb_cmd('push', magisk_apk_path, '/data/local/tmp/'), timeout=60)
        else:
            self.emit_output("$ adb push magisk.apk /data/local/tmp/", "command")
            self.emit_output(tr('info_magiskapk_missing'), "warning")

        # ===== push live_setup.sh =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit(tr('pushing_live_setup'))
        live_setup_path = os.path.join(os.getcwd(), "live_setup.sh")
        if not os.path.isfile(live_setup_path):
            self.emit_output("$ adb push live_setup.sh /data/local/tmp/", "command")
            self.emit_output(tr('err_livesetup_missing'), "error")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return
        self._run_adb(adb_cmd('push', live_setup_path, '/data/local/tmp/'), timeout=60)

        # ===== 在提权成功的 Root Shell 中执行命令 =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return

        root_shell_ok = False
        if self.root_shell and self.root_shell._stdin_pipe:
            try:
                root_shell_ok = not self.root_shell._stdin_pipe.closed
            except Exception:
                root_shell_ok = False

        if root_shell_ok:
            self.status_signal.emit(tr('in_root_shell'))
            self.emit_output("", "output")
            self.emit_output(tr('ok_root_shell_direct'), "success")

            shell_commands = [
                'chmod +x /data/local/tmp/live_setup.sh',
                '/data/local/tmp/live_setup.sh',
                'cd /data/adb',
                'magisk --daemon &',
            ]

            ok = True
            for cmd in shell_commands:
                if self.stop_flag:
                    ok = False
                    break
                self.emit_output(f"# {cmd}", "command")
                sent = self.root_shell.send_to_shell(cmd)
                if not sent:
                    self.emit_output(tr('err_send_root_shell'), "error")
                    ok = False
                    break
                if not self._delay():
                    ok = False
                    break
        else:
            # 没有可用 Root Shell 时退回普通 adb shell 执行
            self.status_signal.emit(tr('executing_shell'))
            self.emit_output("", "output")
            self.emit_output(tr('info_normal_shell'), "warning")
            self.emit_output("$ adb shell", "command")
            self.emit_output("", "output")

            ok = True
            try:
                shell_proc = subprocess.Popen(
                    adb_cmd('shell'),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE,
                    bufsize=0,
                    **_subprocess_common_kwargs()
                )
                reader_q = _create_reader_queue(shell_proc)

                shell_commands = [
                    'chmod +x /data/local/tmp/live_setup.sh',
                    '/data/local/tmp/live_setup.sh',
                    'cd /data/adb',
                    'magisk --daemon &',
                ]

                for cmd in shell_commands:
                    if self.stop_flag:
                        ok = False
                        break
                    self.emit_output(f"# {cmd}", "command")
                    try:
                        shell_proc.stdin.write((cmd + '\n').encode('utf-8'))
                        shell_proc.stdin.flush()
                    except Exception:
                        ok = False
                        break
                    # 读取命令输出
                    cmd_start = time.time()
                    while not self.stop_flag and time.time() - cmd_start < 60:
                        raw = _read_queue(reader_q, 1.0)
                        if raw is None:
                            break
                        if raw:
                            self.ansi_output_signal.emit(decode_bytes_smart(raw))
                        # 短暂等待更多输出
                        extra = _read_queue(reader_q, 0.5)
                        if extra is None:
                            break
                        if extra:
                            self.ansi_output_signal.emit(decode_bytes_smart(extra))
                    if not self._delay():
                        ok = False
                        break

                # 退出 shell
                try:
                    shell_proc.stdin.write(b'exit\n')
                    shell_proc.stdin.flush()
                except Exception:
                    pass

                # 读取剩余输出
                while True:
                    raw = _read_queue(reader_q, 0.5)
                    if raw is None:
                        break
                    if raw:
                        self.ansi_output_signal.emit(decode_bytes_smart(raw))

                try:
                    shell_proc.wait(timeout=5)
                except Exception:
                    try:
                        shell_proc.terminate()
                    except Exception:
                        pass

            except FileNotFoundError:
                self.emit_output(tr('err_no_adb'), "error")
                ok = False
            except Exception as e:
                self.emit_output(f"{tr('err_exception')}{str(e)}", "error")
                ok = False

        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        if ok:
            self.emit_output(tr('getroot_done_banner'), "success")
            self.status_signal.emit(tr('get_root_done'))
            self.success_signal.emit()
        else:
            self.emit_output(tr('getroot_done_verify'), "warning")
            self.status_signal.emit(tr('get_root_done_manual'))
            self.success_signal.emit()
        self.emit_output("=" * 56, "system")

        self.finished_signal.emit()


class KernelSUWorker(QThread):
    """获取root - KernelSU 方式：推送 ksud/kernelsu.ko，在已提权终端加载内核模块"""
    output_signal = pyqtSignal(str, str)
    ansi_output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    success_signal = pyqtSignal(bool)   # detected
    failure_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    CMD_DELAY = 4

    def __init__(self, root_shell=None):
        super().__init__()
        self.stop_flag = False
        self.root_shell = root_shell
        self._obs_queue = _queue.Queue()

    def stop(self):
        self.stop_flag = True

    def emit_output(self, text, color_type="output"):
        self.output_signal.emit(text, color_type)

    def emit_ansi(self, text):
        self.ansi_output_signal.emit(text)

    def feed_output(self, text):
        try:
            self._obs_queue.put(text)
        except Exception:
            pass

    def _read_obs(self, timeout=0.5):
        try:
            return self._obs_queue.get(timeout=timeout)
        except _queue.Empty:
            return None

    def _delay(self):
        """执行命令延迟"""
        for _ in range(self.CMD_DELAY * 10):
            if self.stop_flag:
                return False
            time.sleep(0.1)
        return True

    def _run_adb(self, cmd, timeout=60):
        """执行adb命令并渲染ANSI原始输出"""
        self.emit_output(f"$ {' '.join(cmd) if isinstance(cmd, list) else cmd}", "command")
        try:
            kw = _subprocess_common_kwargs()
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    bufsize=0, **kw)
            reader_q = _create_reader_queue(proc)
            while not self.stop_flag:
                raw = _read_queue(reader_q, 0.3)
                if raw is not None:
                    if raw is None:  # EOF
                        break
                    self.ansi_output_signal.emit(decode_bytes_smart(raw))
                elif proc.poll() is not None:
                    raw = _read_queue(reader_q, 0.1)
                    while raw is not None:
                        if raw:
                            self.ansi_output_signal.emit(decode_bytes_smart(raw))
                        raw = _read_queue(reader_q, 0.1)
                    break
            rc = proc.wait(timeout=timeout)
            return rc == 0
        except Exception as e:
            self.emit_output(f"{tr('err_bare')}{str(e)}", "error")
            return False

    def _find_kernelsu_files(self):
        """搜索运行目录下的 ksud 与 kernelsu.ko，返回 (ksud路径, kernelsu.ko路径)"""
        cwd = os.getcwd()
        try:
            names = os.listdir(cwd)
        except Exception:
            names = []
        ksud_path = None
        ko_path = None
        for n in names:
            full = os.path.join(cwd, n)
            if not os.path.isfile(full):
                continue
            lower = n.lower()
            if ksud_path is None and (lower == 'ksud' or lower.startswith('ksud')):
                ksud_path = full
            if ko_path is None and 'kernelsu' in lower and lower.endswith('.ko'):
                ko_path = full
        return ksud_path, ko_path

    def run(self):
        self.stop_flag = False

        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        self.emit_output(tr('getroot_kernelsu'), "info")
        self.emit_output("=" * 56, "system")

        # 检查设备
        self.status_signal.emit(tr('checking_device'))
        connected, detail = check_device_status()
        if not connected:
            self.emit_output(tr('err_no_device'), "error")
            if detail:
                self.emit_output(f"{tr('log_detail')}{detail}", "error")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return
        self.emit_output(f"{tr('ok_device_connected')}: {get_device_model()}", "success")

        # 检查 Root Shell
        root_shell_ok = False
        if self.root_shell and self.root_shell._stdin_pipe:
            try:
                root_shell_ok = not self.root_shell._stdin_pipe.closed
            except Exception:
                root_shell_ok = False
        if not root_shell_ok:
            self.emit_output(tr('err_no_root_shell'), "error")
            self.emit_output(tr('warn_root_first'), "warning")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return

        # 搜索文件
        self.status_signal.emit(tr('searching_ksu_files'))
        self.emit_output("", "output")
        self.emit_output(tr('searching_ksu'), "info")
        ksud_path, ko_path = self._find_kernelsu_files()
        if ksud_path:
            self.emit_output(f"{tr('ok_found_ksud')}{ksud_path}", "success")
        else:
            self.emit_output(tr('err_no_ksud'), "error")
        if ko_path:
            self.emit_output(f"{tr('ok_found_ko')}{ko_path}", "success")
        else:
            self.emit_output(tr('err_no_ko'), "error")
        if not ksud_path or not ko_path:
            self.emit_output(tr('warn_place_ksu'), "warning")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return

        # 推送文件
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit(tr('pushing_ksud'))
        self.emit_output("", "output")
        self.emit_output(f"$ adb push {ksud_path} /data/local/tmp/", "command")
        if not self._run_adb(adb_cmd('push', ksud_path, '/data/local/tmp/'), timeout=60):
            self.emit_output(tr('err_push_ksud'), "error")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return
        self.emit_output(tr('ok_ksud_pushed'), "success")

        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit(tr('pushing_ko'))
        self.emit_output(f"$ adb push {ko_path} /data/local/tmp/", "command")
        if not self._run_adb(adb_cmd('push', ko_path, '/data/local/tmp/'), timeout=60):
            self.emit_output(tr('err_push_ko'), "error")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return
        self.emit_output(tr('ok_ko_pushed'), "success")

        # 在 Root Shell 中执行命令
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit(tr('loading_module'))
        self.emit_output("", "output")
        self.emit_output(tr('exec_in_root_term'), "info")

        commands = [
            'chmod +x /data/local/tmp/*',
            'cd /data/local/tmp',
            './ksud insmod kernelsu.ko',
        ]

        ok = True
        for cmd in commands:
            if self.stop_flag:
                ok = False
                break
            self.emit_output(f"# {cmd}", "command")
            sent = self.root_shell.send_to_shell(cmd)
            if not sent:
                self.emit_output(tr('err_send_root_shell'), "error")
                ok = False
                break
            if not self._delay():
                ok = False
                break

        detected = False
        if ok:
            self.emit_output("", "output")
            self.emit_output(tr('checking_module_load'), "system")
            wait_end = time.time() + 30
            last_lsmod = 0
            while not self.stop_flag and time.time() < wait_end:
                text = self._read_obs(0.8)
                if text and 'loaded kernel module' in text.lower():
                    detected = True
                    self.emit_output(tr('ok_module_hint'), "success")
                    break
                if time.time() - last_lsmod >= 4:
                    last_lsmod = time.time()
                    out, err, rc = run_adb_command(adb_cmd('shell', 'lsmod'), timeout=8)
                    if rc == 0 and 'kernelsu' in out.lower():
                        detected = True
                        self.emit_output(tr('ok_module_lsmod'), "success")
                        break
            if not detected:
                self.emit_output(tr('warn_no_load_hint'), "warning")

        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        if ok and detected:
            self.emit_output(tr('ksu_ok_banner'), "success")
            self.status_signal.emit(tr('kernelsu_success'))
            self.success_signal.emit(True)
        elif ok:
            self.emit_output(tr('ksu_verify'), "warning")
            self.status_signal.emit(tr('kernelsu_done_manual'))
            self.success_signal.emit(False)
        else:
            self.emit_output(tr('ksu_fail_banner'), "error")
            self.status_signal.emit(tr('kernelsu_failed'))
            self.failure_signal.emit()
        self.emit_output("=" * 56, "system")

        self.finished_signal.emit()


class AutoRetryWorker(QThread):
    """自动重试 - 循环执行 开始执行 + 开始提权 直到成功"""
    output_signal = pyqtSignal(str, str)
    ansi_output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    success_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stop_flag = False
        self.attempt = 0
        self.process = None
        self._stdin_pipe = None
        self._reader_q = None
        self._shell_lock = threading.Lock()

    def stop(self):
        self.stop_flag = True
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass

    def emit_output(self, text, color_type="output"):
        self.output_signal.emit(text, color_type)

    def emit_ansi(self, text):
        self.ansi_output_signal.emit(text)

    def run(self):
        self.stop_flag = False

        self.emit_output("", "output")
        self.emit_output("#" * 56, "warning")
        self.emit_output(tr('auto_mode_started'), "warning")
        self.emit_output(tr('auto_loop_desc'), "warning")
        self.emit_output(tr('auto_until_success'), "warning")
        self.emit_output("#" * 56, "warning")

        while not self.stop_flag:
            self.attempt += 1
            self.emit_output("", "output")
            self.emit_output(f"{'=' * 20} {tr('auto_attempt_header')}{self.attempt}{tr('auto_attempt_tail')} {'=' * 20}", "info")

            self.status_signal.emit(f"{tr('auto_executing').format(self.attempt)}")
            self.emit_output("", "output")
            self.emit_output(tr('auto_phase1'), "info")

            success = self._run_execute_phase()
            if self.stop_flag:
                self.emit_output(tr('auto_stopped'), "warning")
                self.finished_signal.emit()
                return
            if not success:
                self.emit_output(f"{tr('auto_exec_retry')}{self.attempt}{tr('auto_exec_retry_tail')}", "warning")
                time.sleep(2)
                continue

            self.status_signal.emit(f"{tr('auto_rooting').format(self.attempt)}")
            self.emit_output("", "output")
            self.emit_output(tr('auto_phase2'), "info")

            success = self._run_root_phase()
            if self.stop_flag:
                self.emit_output(tr('auto_stopped'), "warning")
                self.finished_signal.emit()
                return
            if success:
                self.emit_output("", "output")
                self.emit_output("#" * 56, "success")
                self.emit_output(f"{tr('auto_success_banner')}{self.attempt}{tr('auto_success_tail')}", "success")
                self.emit_output("#" * 56, "success")
                self.status_signal.emit(tr('auto_retry_success'))
                self.success_signal.emit()

                # 保持 Root Shell 会话存活：持续读取输出直到 shell 退出或用户停止
                while (not self.stop_flag and self.process
                       and self.process.poll() is None):
                    raw = _read_queue(self._reader_q, 0.3)
                    if raw is None:
                        continue
                    self.ansi_output_signal.emit(decode_bytes_smart(raw))

                self.finished_signal.emit()
                return
            else:
                self.emit_output(f"{tr('auto_root_retry')}{self.attempt}{tr('auto_root_retry_tail')}", "warning")
                time.sleep(2)

        self.emit_output(tr('auto_stopped'), "warning")
        self.finished_signal.emit()

    def _run_execute_phase(self):
        preload_path = os.path.join(os.getcwd(), "preload")
        ionstack_path = os.path.join(os.getcwd(), "ionstack.conf")

        if not os.path.isfile(preload_path) or not os.path.isfile(ionstack_path):
            self.emit_output(tr('err_missing_core_files'), "error")
            return False

        if not check_device_connected():
            self.emit_output(tr('wait_device_conn'), "system")
            wait = 0
            while not self.stop_flag and wait < 120:
                if check_device_connected():
                    break
                time.sleep(2)
                wait += 2
            if not check_device_connected():
                self.emit_output(tr('err_reconnect_timeout'), "error")
                return False
        self.emit_output(tr('ok_device_connected'), "success")

        # 不主动 adb reboot：设备会因前次提权失败自动重启，等待其断开后重连即可
        self.emit_output(tr('skip_reboot_wait'), "system")
        disconnect_wait = 0
        while not self.stop_flag and disconnect_wait < 60:
            if not check_device_connected():
                self.emit_output(tr('ok_disconnected_rebooting'), "success")
                break
            time.sleep(1)
            disconnect_wait += 1
        else:
            self.emit_output(tr('warn_wait_timeout_reconnect'), "warning")

        self.emit_output(tr('waiting_dev_reconnect'), "system")
        wait = 0
        connected = False
        while not self.stop_flag and wait < 180:
            if check_device_connected():
                connected = True
                self.emit_output(f"{tr('ok_reconnected_wait')}{wait}s)", "success")
                break
            time.sleep(2)
            wait += 2
        if not connected:
            self.emit_output(tr('err_reconnect_timeout'), "error")
            return False

        self.emit_output(tr('checking_stability_10s2'), "system")
        for i in range(10):
            if self.stop_flag:
                return False
            if not check_device_connected():
                self.emit_output(f"{tr('warn_sec_disc')}{i+1}{tr('sec_disc_tail')}", "warning")
                retry = 0
                while not self.stop_flag and retry < 60:
                    if check_device_connected():
                        self.emit_output(tr('ok_reconnected'), "success")
                        break
                    time.sleep(2)
                    retry += 2
                if not check_device_connected():
                    return False
                stable = True
                for j in range(10):
                    if self.stop_flag or not check_device_connected():
                        stable = False
                        break
                    if j < 9:
                        time.sleep(1)
                if not stable:
                    return False
                break
            if i < 9:
                time.sleep(1)
        self.emit_output(tr('ok_conn_stable'), "success")

        self.emit_output("$ adb push preload /data/local/tmp/", "command")
        _, _, rc = run_adb_command(adb_cmd('push', preload_path, '/data/local/tmp/'), timeout=30)
        if rc != 0:
            self.emit_output(tr('err_push_preload'), "error")
            return False
        self.emit_output(tr('ok_preload_pushed'), "success")

        self.emit_output("$ adb push ionstack.conf /data/local/tmp/", "command")
        _, _, rc = run_adb_command(adb_cmd('push', ionstack_path, '/data/local/tmp/'), timeout=30)
        if rc != 0:
            self.emit_output(tr('err_push_ionstack'), "error")
            return False
        self.emit_output(tr('ok_ionstack_pushed'), "success")

        self.emit_output("$ adb shell chmod +x /data/local/tmp/preload", "command")
        _, _, rc = run_adb_command(adb_cmd('shell', 'chmod', '+x', '/data/local/tmp/preload'), timeout=10)
        if rc != 0:
            self.emit_output(tr('err_chmod'), "error")
            return False
        self.emit_output(tr('ok_perms_set'), "success")
        self.emit_output(tr('ok_exec_phase'), "success")
        return True

    def _run_root_phase(self):
        if not check_device_connected():
            self.emit_output(tr('err_device_offline'), "error")
            return False

        self.emit_output(tr('executing_root_cmds'), "info")
        self.emit_output("$ adb shell /data/local/tmp/preload", "command")

        try:
            process = subprocess.Popen(
                adb_cmd('shell', '/data/local/tmp/preload'),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE, bufsize=0,
                **_subprocess_common_kwargs())

            reader_q = _create_reader_queue(process)
            root_detected = False
            start_time = time.time()
            pending = ""

            while not self.stop_flag:
                raw = _read_queue(reader_q, 0.3)
                if raw is not None:
                    if raw is None:  # EOF
                        break
                    chunk = decode_bytes_smart(raw)
                    self.ansi_output_signal.emit(chunk)
                    pending += chunk
                    lines = pending.split('\n')
                    for line in lines:
                        stripped = line.strip('\r ')
                        if stripped and self._is_root_prompt(stripped):
                            root_detected = True
                            self.emit_output(tr('auto_shell_detected'), "success")
                            self.process = process
                            self._stdin_pipe = process.stdin
                            self._reader_q = reader_q
                            self.emit_output(
                                tr('auto_shell_kept'), "success")
                            break
                    if lines:
                        pending = lines[-1]
                    if root_detected:
                        break
                elif process.poll() is not None:
                    raw = _read_queue(reader_q, 0.1)
                    while raw is not None:
                        if raw:
                            self.ansi_output_signal.emit(decode_bytes_smart(raw))
                        raw = _read_queue(reader_q, 0.1)
                    break
                if time.time() - start_time > 300:
                    self.emit_output(tr('warn_root_timeout'), "warning")
                    break

            if self.stop_flag:
                try: process.terminate()
                except Exception: pass
                return False

            if root_detected:
                return True

            try:
                if process.poll() is None:
                    process.terminate()
            except Exception:
                pass
            if not check_device_connected():
                self.emit_output(tr('err_disconnected_auto'), "error")
            else:
                self.emit_output(tr('err_no_root_prompt'), "error")
            return False
        except Exception as e:
            self.emit_output(f"{tr('err_exception')}{str(e)}", "error")
            return False

    def _is_root_prompt(self, line):
        line = line.strip()
        if not line:
            return False
        stripped_line = line.rstrip()
        if not stripped_line.endswith('#'):
            return False
        if len(stripped_line) > 80:
            return False
        if stripped_line.startswith('#') and len(stripped_line) > 1:
            return False
        if '://' in stripped_line:
            return False
        exclude_keywords = ['echo', 'printf', 'cat ', 'sed ', 'awk ', 'grep ']
        for kw in exclude_keywords:
            if kw in stripped_line.lower():
                return False
        return True

    def send_to_shell(self, command):
        with self._shell_lock:
            if self._stdin_pipe and not self._stdin_pipe.closed:
                try:
                    self._stdin_pipe.write((command + '\n').encode('utf-8'))
                    self._stdin_pipe.flush()
                    return True
                except Exception:
                    return False
        return False


class CommandWorker(QThread):
    """执行用户在输入框中输入的命令"""
    output_signal = pyqtSignal(str, str)
    ansi_output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.stop_flag = False
        self.process = None

    def stop(self):
        self.stop_flag = True
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass

    def run(self):
        self.output_signal.emit(f"$ {self.command}", "command")
        try:
            self.process = subprocess.Popen(
                self.command, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE, bufsize=0, cwd=os.getcwd(),
                **_subprocess_common_kwargs())

            reader_q = _create_reader_queue(self.process)
            while not self.stop_flag:
                raw = _read_queue(reader_q, 0.3)
                if raw is not None:
                    if raw is None:  # EOF
                        break
                    self.ansi_output_signal.emit(decode_bytes_smart(raw))
                elif self.process.poll() is not None:
                    raw = _read_queue(reader_q, 0.1)
                    while raw is not None:
                        if raw:
                            self.ansi_output_signal.emit(decode_bytes_smart(raw))
                        raw = _read_queue(reader_q, 0.1)
                    break

            if self.stop_flag:
                try: self.process.terminate()
                except Exception: pass
                self.output_signal.emit(tr('ctrl_c_interrupted'), "warning")
            else:
                rc = self.process.poll()
                if rc and rc != 0:
                    self.output_signal.emit(f"{tr('exit_code').format(rc)}", "system")
        except Exception as e:
            self.output_signal.emit(f"{tr('error_prefix').format(str(e))}", "error")

        self.finished_signal.emit()


# ==================== 关于对话框 ====================
class ThemeDialog(QDialog):
    """无边框深色对话框 - 与主界面风格一致，含自定义标题栏与关闭按钮"""

    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle(title)
        self._drag_pos = None

        outer = QWidget()
        outer.setObjectName("dialogOuter")
        outer.setAttribute(Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect(outer)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        outer.setGraphicsEffect(shadow)

        main = QVBoxLayout(outer)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        head = QFrame()
        head.setObjectName("dialogHead")
        head.mousePressEvent = self._on_head_press
        head.mouseMoveEvent = self._on_head_move
        head.mouseReleaseEvent = self._on_head_release

        head_layout = QHBoxLayout(head)
        head_layout.setContentsMargins(16, 10, 8, 10)
        head_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("dialogTitleLabel")
        close_btn = QPushButton("✕")
        close_btn.setObjectName("dialogCloseBtn")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.reject)

        head_layout.addWidget(title_label)
        head_layout.addStretch()
        head_layout.addWidget(close_btn)
        main.addWidget(head)

        self.body = QVBoxLayout()
        self.body.setContentsMargins(16, 14, 16, 16)
        self.body.setSpacing(12)
        main.addLayout(self.body)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(outer)

    def _on_head_press(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def _on_head_move(self, event):
        if self._drag_pos is not None and (event.buttons() & Qt.LeftButton):
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def _on_head_release(self, event):
        self._drag_pos = None
        event.accept()


class ThemeMessageBox(ThemeDialog):
    """与软件同风格的提示弹窗"""

    def __init__(self, parent=None, title="", text="", icon=None,
                 ok_text=tr('ok'), cancel_text=None):
        super().__init__(parent, title)
        self._ok_result = True
        self.setMinimumWidth(340)

        row = QHBoxLayout()
        row.setSpacing(12)
        if icon is not None:
            icon_label = QLabel()
            icon_label.setPixmap(
                icon.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            row.addWidget(icon_label)
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: #cdd6f4; font-size: 13px;")
        row.addWidget(text_label, stretch=1)
        self.body.addLayout(row)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        if cancel_text:
            cancel_btn = QPushButton(cancel_text)
            cancel_btn.setCursor(Qt.PointingHandCursor)
            cancel_btn.clicked.connect(self._on_cancel)
            btn_row.addWidget(cancel_btn)
        self.ok_btn = QPushButton(ok_text)
        self.ok_btn.setDefault(True)
        self.ok_btn.setCursor(Qt.PointingHandCursor)
        self.ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(self.ok_btn)
        self.body.addLayout(btn_row)

    def _on_cancel(self):
        self._ok_result = False
        self.reject()

    def is_ok(self):
        return self._ok_result


class AboutDialog(ThemeDialog):
    """关于对话框 - 项目信息、致谢、链接"""

    def __init__(self, parent=None):
        super().__init__(parent, tr('about_title'))
        self.setMinimumSize(560, 480)
        self.resize(580, 500)

        # 标题
        title = QLabel(f"{tr('about_app_title')}  v1.0")
        title.setStyleSheet("color: #cba6f7; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self.body.addWidget(title)

        divider1 = QFrame()
        divider1.setFrameShape(QFrame.HLine)
        divider1.setStyleSheet("color: #313244;")
        self.body.addWidget(divider1)

        # 内容区 (QTextBrowser 支持可点击链接)
        content = QTextBrowser()
        content.setOpenExternalLinks(True)
        content.setStyleSheet("""
            QTextBrowser {
                background-color: #181825;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
            }
        """)
        html = """
        <div style="line-height:1.7">
        <p style="color:#89b4fa;font-weight:bold;margin-bottom:4px;">📌 项目灵感来源</p>
        <p style="margin:0 0 12px 12px;">
            <a href="https://github.com/F-19-F/IonStackQuest3"
               style="color:#94e2d5;text-decoration:underline;">
               https://github.com/F-19-F/IonStackQuest3
            </a>
        </p>

        <p style="color:#f9e2af;font-weight:bold;margin-bottom:4px;">🙏 感谢</p>
        <p style="margin:0 0 12px 12px;">
            特别感谢 B 站 UP 主
            <span style="color:#f38ba8;font-weight:bold;">"我是一个小依旧"</span>
            做出的贡献
        </p>

        <p style="color:#cba6f7;font-weight:bold;margin-bottom:4px;">🎬 相关视频</p>
        <p style="margin:0 0 12px 12px;">
            <a href="https://b23.tv/FS958OJ"
               style="color:#94e2d5;text-decoration:underline;">
               https://b23.tv/FS958OJ
            </a>
            &nbsp;点击链接打开浏览器
        </p>

        <p style="color:#fab387;font-weight:bold;margin-bottom:4px;">🔓 漏洞信息</p>
        <p style="margin:0 0 12px 12px;">
            本工具利用项目提供的漏洞
            <span style="color:#f38ba8;font-weight:bold;">CVE-2026-43499</span>
            来进行权限获取。
        </p>

        <p style="color:#6c7086;font-size:12px;margin-top:16px;">
            ⚠️ 本工具仅供学习研究使用，请遵守相关法律法规，
            因使用本工具造成的任何后果由使用者自行承担。
        </p>
        </div>
        """
        content.setHtml(html)
        self.body.addWidget(content, stretch=1)

        # 按钮
        btns = QDialogButtonBox(QDialogButtonBox.Ok)
        btns.button(QDialogButtonBox.Ok).setText(tr('close'))
        btns.accepted.connect(self.accept)
        self.body.addWidget(btns)


# ==================== 获取Root方式选择对话框 ====================
class RootMethodDialog(ThemeDialog):
    """获取Root方式选择 - Magisk (默认) / KernelSU"""

    def __init__(self, parent=None):
        super().__init__(parent, tr('root_method_title'))
        self._method = None
        self.setMinimumWidth(280)

        tip = QLabel(tr('root_method_tip'))
        tip.setStyleSheet("color: #cdd6f4; font-size: 13px;")
        self.body.addWidget(tip)

        self.magisk_btn = QPushButton("Magisk")
        self.magisk_btn.setDefault(True)
        self.magisk_btn.setMinimumHeight(40)
        self.magisk_btn.setCursor(Qt.PointingHandCursor)
        self.magisk_btn.clicked.connect(lambda: self._choose('magisk'))

        self.kernelsu_btn = QPushButton("KernelSU")
        self.kernelsu_btn.setMinimumHeight(40)
        self.kernelsu_btn.setCursor(Qt.PointingHandCursor)
        self.kernelsu_btn.clicked.connect(lambda: self._choose('kernelsu'))

        self.body.addWidget(self.magisk_btn)
        self.body.addWidget(self.kernelsu_btn)

    def _choose(self, method):
        self._method = method
        self.accept()

    def get_method(self):
        return self._method


# ==================== ADB 路径选择对话框 ====================
class AdbPathDialog(ThemeDialog):
    """首次启动时选择要使用的 adb 安装路径"""

    def __init__(self, paths, parent=None):
        super().__init__(parent, tr('adb_select_title'))
        self._selected = None
        self.setMinimumWidth(540)

        tip = QLabel(tr('adb_select_tip'))
        tip.setStyleSheet("color: #cdd6f4; font-size: 13px;")
        tip.setWordWrap(True)
        self.body.addWidget(tip)

        for p in paths:
            btn = QPushButton(p)
            btn.setMinimumHeight(38)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, x=p: self._choose(x))
            self.body.addWidget(btn)

        row = QHBoxLayout()
        row.addStretch()
        cancel_btn = QPushButton(tr('cancel'))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        row.addWidget(cancel_btn)
        self.body.addLayout(row)

    def _choose(self, path):
        self._selected = path
        self.accept()

    def get_selected(self):
        return self._selected


# ==================== 终端会话组件 ====================
class TerminalSession(QWidget):
    """单个终端会话 - 包含输出区、输入框、按钮"""

    new_session_requested = pyqtSignal()
    language_changed = pyqtSignal()

    def __init__(self, session_id=1, parent=None):
        super().__init__(parent)
        self.session_id = session_id
        self.setObjectName("terminalSession")

        self.execute_worker = None
        self.root_worker = None
        self.get_root_worker = None
        self.kernelsu_worker = None
        self.auto_retry_worker = None
        self.command_worker = None
        self.active_root_shell = None

        self._init_ui()
        self._connect_signals()
        self._refresh_file_status()
        self._print_welcome()

    # ---------- UI ----------
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # ---- 工具栏1: 操作按钮 ----
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbarFrame")
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(12, 8, 12, 8)
        toolbar_layout.setSpacing(10)

        self.execute_btn = QPushButton(tr('execute'))
        self.execute_btn.setObjectName("executeBtn")
        self.execute_btn.setCursor(Qt.PointingHandCursor)

        self.get_root_btn = QPushButton(tr('get_root'))
        self.get_root_btn.setObjectName("getRootBtn")
        self.get_root_btn.setCursor(Qt.PointingHandCursor)

        self.root_btn = QPushButton(tr('root'))
        self.root_btn.setObjectName("rootBtn")
        self.root_btn.setCursor(Qt.PointingHandCursor)

        self.stop_btn = QPushButton(tr('stop'))
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setEnabled(False)

        self.new_session_btn = QPushButton(tr('new_session'))
        self.new_session_btn.setObjectName("newSessionBtn")
        self.new_session_btn.setCursor(Qt.PointingHandCursor)

        self.lang_btn = QPushButton(tr('lang_switch'))
        self.lang_btn.setObjectName("langBtn")
        self.lang_btn.setCursor(Qt.PointingHandCursor)
        self.lang_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 9px 14px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45475a; color: #cba6f7; }
        """)

        toolbar_layout.addWidget(self.execute_btn)
        toolbar_layout.addWidget(self.root_btn)
        toolbar_layout.addWidget(self.get_root_btn)
        toolbar_layout.addWidget(self.stop_btn)
        toolbar_layout.addStretch()

        self.status_label = QLabel(tr('status_ready'))
        self.status_label.setObjectName("statusLabel")
        toolbar_layout.addWidget(self.status_label)

        toolbar_layout.addWidget(self.lang_btn)
        toolbar_layout.addWidget(self.new_session_btn)

        layout.addWidget(toolbar_frame)

        # ---- 工具栏2: 文件状态栏（按钮下方）----
        file_status_frame = QFrame()
        file_status_frame.setObjectName("fileStatusFrame")
        file_status_layout = QHBoxLayout(file_status_frame)
        file_status_layout.setContentsMargins(12, 8, 12, 8)
        file_status_layout.setSpacing(16)

        title_label = QLabel(tr('file_status'))
        title_label.setStyleSheet("color:#6c7086;font-size:12px;font-weight:bold;")
        file_status_layout.addWidget(title_label)

        self.preload_status_label = QLabel("preload: —")
        self.preload_status_label.setObjectName("fileStatusMISS")

        self.ionstack_status_label = QLabel("ionstack.conf: —")
        self.ionstack_status_label.setObjectName("fileStatusMISS")

        file_status_layout.addWidget(self.preload_status_label)
        file_status_layout.addWidget(self.ionstack_status_label)
        file_status_layout.addStretch()

        self.refresh_file_btn = QPushButton(tr('refresh'))
        self.refresh_file_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 4px;
                padding: 3px 10px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #45475a; color:#cba6f7; }
        """)
        self.refresh_file_btn.clicked.connect(self._refresh_file_status)
        file_status_layout.addWidget(self.refresh_file_btn)

        layout.addWidget(file_status_frame)

        # ---- 终端输出区 ----
        self.terminal = QTextBrowser()
        self.terminal.setOpenExternalLinks(False)
        self.terminal.setFont(QFont("Consolas", 11))
        layout.addWidget(self.terminal, stretch=1)

        # ---- 输入区 ----
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(8, 6, 8, 6)
        input_layout.setSpacing(8)

        input_prompt = QLabel("➤")
        input_prompt.setStyleSheet("color: #cba6f7; font-size: 16px; font-weight: bold;")
        input_prompt.setFixedWidth(20)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText(tr('input_placeholder'))
        self.input_box.returnPressed.connect(self._on_input_enter)

        self.run_btn = QPushButton(tr('run'))
        self.run_btn.setObjectName("runBtn")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.clicked.connect(self._on_input_enter)

        input_layout.addWidget(input_prompt)
        input_layout.addWidget(self.input_box, stretch=1)
        input_layout.addWidget(self.run_btn)

        layout.addWidget(input_frame)

    def _connect_signals(self):
        self.execute_btn.clicked.connect(self._on_execute_clicked)
        self.root_btn.clicked.connect(self._on_root_clicked)
        self.stop_btn.clicked.connect(self._on_stop_clicked)
        self.get_root_btn.clicked.connect(self._on_get_root_clicked)
        self.new_session_btn.clicked.connect(self.new_session_requested.emit)
        self.lang_btn.clicked.connect(self._on_lang_switch)

    def _on_lang_switch(self):
        new_lang = 'en' if LANG == 'zh' else 'zh'
        save_lang(new_lang)
        self._update_ui_texts()
        self.language_changed.emit()

    def _update_ui_texts(self):
        """更新所有UI文本到当前语言"""
        self.execute_btn.setText(tr('execute'))
        self.root_btn.setText(tr('root'))
        self.get_root_btn.setText(tr('get_root'))
        self.stop_btn.setText(tr('stop'))
        self.new_session_btn.setText(tr('new_session'))
        self.lang_btn.setText(tr('lang_switch'))
        self.status_label.setText(tr('status_ready'))
        self.input_box.setPlaceholderText(tr('input_placeholder'))
        self.run_btn.setText(tr('run'))

    # ---------- 文件状态 ----------
    def _refresh_file_status(self):
        preload_path = os.path.join(os.getcwd(), "preload")
        ionstack_path = os.path.join(os.getcwd(), "ionstack.conf")

        if os.path.isfile(preload_path):
            self.preload_status_label.setText(f"✅ preload: {tr('file_ok')}")
            self.preload_status_label.setObjectName("fileStatusOK")
        else:
            self.preload_status_label.setText(f"❌ preload: {tr('file_miss')}")
            self.preload_status_label.setObjectName("fileStatusMISS")

        if os.path.isfile(ionstack_path):
            self.ionstack_status_label.setText(f"✅ ionstack.conf: {tr('file_ok')}")
            self.ionstack_status_label.setObjectName("fileStatusOK")
        else:
            self.ionstack_status_label.setText(f"❌ ionstack.conf: {tr('file_miss')}")
            self.ionstack_status_label.setObjectName("fileStatusMISS")

        # 重新应用样式
        self.preload_status_label.style().unpolish(self.preload_status_label)
        self.preload_status_label.style().polish(self.preload_status_label)
        self.ionstack_status_label.style().unpolish(self.ionstack_status_label)
        self.ionstack_status_label.style().polish(self.ionstack_status_label)

    # ---------- 欢迎信息 ----------
    def _print_welcome(self):
        self._append_output(
            "╔══════════════════════════════════════════════════════════╗", "system")
        self._append_output(
            tr('welcome_title'), "info")
        self._append_output(
            "╚══════════════════════════════════════════════════════════╝", "system")
        self._append_output("", "output")
        self._append_output(tr('welcome_usage'), "info")
        self._append_output(
            tr('welcome_step1'), "system")
        self._append_output(
            tr('welcome_step2'), "system")
        self._append_output(
            tr('welcome_step3'), "warning")
        self._append_output(
            tr('welcome_step4'), "warning")
        self._append_output("", "output")
        self._append_output(f"{tr('welcome_cwd')}{os.getcwd()}", "system")
        self._append_output("", "output")

    # ---------- 输出渲染 ----------
    def _append_output(self, text, color_type="output"):
        """追加简单彩色输出（非ANSI）"""
        parse_ansi_and_append(self.terminal, text,
                              default_fg=COLORS.get(color_type, COLORS["output"]))

    def _append_ansi(self, text):
        """追加带ANSI颜色的原始输出（不强制追加换行，保留原始格式）"""
        parse_ansi_and_append(self.terminal, text, add_newline=False)

    # ---------- 按钮状态 ----------
    def _set_buttons_state(self, executing=False):
        self.execute_btn.setEnabled(not executing)
        self.root_btn.setEnabled(not executing)
        self.get_root_btn.setEnabled(not executing)
        self.stop_btn.setEnabled(executing)

    # ---------- 开始执行 ----------
    def _on_execute_clicked(self):
        if self.execute_worker and self.execute_worker.isRunning():
            return
        self._set_buttons_state(True)
        self._refresh_file_status()
        self.execute_worker = ExecuteWorker()
        self.execute_worker.output_signal.connect(self._append_output)
        self.execute_worker.ansi_output_signal.connect(self._append_ansi)
        self.execute_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"{tr('status_prefix')}{s}"))
        self.execute_worker.finished_signal.connect(self._on_execute_finished)
        self.execute_worker.start()

    def _on_execute_finished(self, success):
        self._set_buttons_state(False)
        self.status_label.setText(f"{tr('status_prefix')}{tr('exec_done') if success else tr('exec_fail')}")

    # ---------- 开始提权 ----------
    def _on_root_clicked(self):
        if self.root_worker and self.root_worker.isRunning():
            return
        connected, detail = check_device_status()
        if not connected:
            self._append_output(f"  [警告] {tr('no_device')}", "warning")
            if detail:
                self._append_output(f"{tr('log_detail')}{detail}", "warning")
            self._append_output(f"  {tr('no_device_detail')}", "warning")
            return

        self._set_buttons_state(True)
        self.root_worker = RootWorker()
        self.root_worker.output_signal.connect(self._append_output)
        self.root_worker.ansi_output_signal.connect(self._on_root_shell_output)
        self.root_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"{tr('status_prefix')}{s}"))
        self.root_worker.success_signal.connect(self._on_root_success)
        self.root_worker.failure_signal.connect(self._on_root_failure)
        self.root_worker.need_auto_retry_signal.connect(self._show_auto_retry_dialog)
        self.root_worker.finished_signal.connect(self._on_root_finished)
        self.root_worker.start()

    def _on_root_shell_output(self, text):
        self._append_ansi(text)
        k = self.kernelsu_worker
        if k and k.isRunning():
            k.feed_output(text)

    def _on_root_success(self):
        self.status_label.setText(f"{tr('status_prefix')}{tr('root_success')}")
        self.active_root_shell = self.root_worker
        # 提权成功后恢复按钮可用（RootWorker线程继续保持shell读取输出）
        if not (self.auto_retry_worker and self.auto_retry_worker.isRunning()):
            self._set_buttons_state(False)
        self._show_root_success_popup()

    def _show_root_success_popup(self):
        try:
            msg = ThemeMessageBox(
                self,
                title=tr('root_success_title'),
                text=tr('root_success_msg'),
                icon=QMessageBox.standardIcon(QMessageBox.Information),
                ok_text=tr('ok'))
            msg.exec_()
        except Exception:
            pass

    def _show_get_root_success_popup(self):
        try:
            msg = ThemeMessageBox(
                self,
                title=tr('get_root_success_title'),
                text=tr('get_root_success_msg'),
                icon=QMessageBox.standardIcon(QMessageBox.Information),
                ok_text=tr('ok'))
            msg.exec_()
        except Exception:
            pass

    def _on_root_failure(self):
        self.status_label.setText(f"{tr('status_prefix')}{tr('root_fail')}")

    def _on_root_finished(self):
        # 检查 root shell 是否真的已经退出
        shell_alive = False
        if self.root_worker:
            proc_alive = self.root_worker.process is not None and self.root_worker.process.poll() is None
            pipe_open = self.root_worker._stdin_pipe and not self.root_worker._stdin_pipe.closed
            shell_alive = proc_alive and pipe_open
        if shell_alive:
            return  # shell 仍在活动中，不清除 active_root_shell
        if not (self.auto_retry_worker and self.auto_retry_worker.isRunning()):
            self._set_buttons_state(False)
        self.active_root_shell = None

    # ---------- 获取Root ----------
    def _on_get_root_clicked(self):
        if self.get_root_worker and self.get_root_worker.isRunning():
            return
        if self.kernelsu_worker and self.kernelsu_worker.isRunning():
            return
        connected, detail = check_device_status()
        if not connected:
            self._append_output(f"  [警告] {tr('no_device')}", "warning")
            if detail:
                self._append_output(f"{tr('log_detail')}{detail}", "warning")
            self._append_output(f"  {tr('no_device_detail')}", "warning")
            return

        dlg = RootMethodDialog(self)
        if not dlg.exec_():
            return
        method = dlg.get_method()
        if method == 'kernelsu':
            self._start_kernelsu()
        else:
            self._start_magisk()

    def _start_magisk(self):
        self._set_buttons_state(True)
        self.status_label.setText(f"{tr('status_prefix')}{tr('status_get_root_start')}")
        self.get_root_worker = GetRootWorker(root_shell=self.active_root_shell)
        self.get_root_worker.output_signal.connect(self._append_output)
        self.get_root_worker.ansi_output_signal.connect(self._append_ansi)
        self.get_root_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"{tr('status_prefix')}{s}"))
        self.get_root_worker.success_signal.connect(self._on_get_root_success)
        self.get_root_worker.failure_signal.connect(
            lambda: self.status_label.setText(f"{tr('status_prefix')}{tr('status_get_root_failed')}"))
        self.get_root_worker.finished_signal.connect(self._on_get_root_finished)
        self.get_root_worker.start()

    def _start_kernelsu(self):
        self._set_buttons_state(True)
        self.status_label.setText(f"{tr('status_prefix')}{tr('status_kernelsu_start')}")
        self.kernelsu_worker = KernelSUWorker(root_shell=self.active_root_shell)
        self.kernelsu_worker.output_signal.connect(self._append_output)
        self.kernelsu_worker.ansi_output_signal.connect(self._append_ansi)
        self.kernelsu_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"{tr('status_prefix')}{s}"))
        self.kernelsu_worker.success_signal.connect(self._on_kernelsu_success)
        self.kernelsu_worker.failure_signal.connect(
            lambda: self.status_label.setText(f"{tr('status_prefix')}{tr('kernelsu_failed')}"))
        self.kernelsu_worker.finished_signal.connect(self._on_kernelsu_finished)
        self.kernelsu_worker.start()

    def _on_kernelsu_success(self, detected):
        if detected:
            self.status_label.setText(f"{tr('status_prefix')}{tr('kernelsu_success')}")
            self._show_kernelsu_success_popup()
        else:
            self.status_label.setText(f"{tr('status_prefix')}{tr('kernelsu_done_manual')}")

    def _on_kernelsu_finished(self):
        self._set_buttons_state(False)

    def _show_kernelsu_success_popup(self):
        try:
            msg = ThemeMessageBox(
                self,
                title=tr('kernelsu_success_title'),
                text=tr('kernelsu_success_msg'),
                icon=QMessageBox.standardIcon(QMessageBox.Information),
                ok_text=tr('ok'))
            msg.exec_()
        except Exception:
            pass

    def _on_get_root_success(self):
        self.status_label.setText(f"{tr('status_prefix')}{tr('get_root_done')}")
        self._show_get_root_success_popup()

    def _on_get_root_finished(self):
        self._set_buttons_state(False)

    # ---------- 自动重试 ----------
    def _show_auto_retry_dialog(self):
        QTimer.singleShot(0, self._show_retry_popup)

    def _show_retry_popup(self):
        msg = ThemeMessageBox(
            self,
            title=tr('auto_retry_title'),
            text="{}<br><br>{}".format(tr('auto_retry_msg'), tr('auto_retry_detail')),
            icon=QMessageBox.standardIcon(QMessageBox.Warning),
            ok_text=tr('auto_retry_ok'),
            cancel_text=tr('auto_retry_cancel'))
        msg.exec_()
        if msg.is_ok():
            self._start_auto_retry()
        else:
            self._set_buttons_state(False)
            self._append_output(tr('manual_operation'), "info")

    def _start_auto_retry(self):
        self._append_output("", "output")
        self._append_output(tr('starting_auto_retry'), "warning")
        self._set_buttons_state(True)
        self.stop_btn.setEnabled(True)

        self.auto_retry_worker = AutoRetryWorker()
        self.auto_retry_worker.output_signal.connect(self._append_output)
        self.auto_retry_worker.ansi_output_signal.connect(self._on_root_shell_output)
        self.auto_retry_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"{tr('status_prefix')}{s}"))
        self.auto_retry_worker.success_signal.connect(self._on_auto_retry_success)
        self.auto_retry_worker.finished_signal.connect(self._on_auto_retry_finished)
        self.auto_retry_worker.start()

    def _on_auto_retry_success(self):
        self.status_label.setText(f"{tr('status_prefix')}{tr('auto_retry_success')}")
        self.active_root_shell = self.auto_retry_worker
        self._set_buttons_state(False)
        self._show_root_success_popup()

    def _on_auto_retry_finished(self):
        shell_alive = False
        if self.auto_retry_worker:
            if (self.auto_retry_worker._stdin_pipe
                    and not self.auto_retry_worker._stdin_pipe.closed):
                shell_alive = True
            if (self.auto_retry_worker.process
                    and self.auto_retry_worker.process.poll() is None):
                shell_alive = True
        if (self.auto_retry_worker
                and self.auto_retry_worker.stop_flag):
            shell_alive = False
        if not shell_alive:
            self.active_root_shell = None
            self._set_buttons_state(False)

    # ---------- 停止 ----------
    def _on_stop_clicked(self):
        stopped = False
        for worker in [self.execute_worker, self.get_root_worker,
                       self.kernelsu_worker, self.root_worker,
                       self.auto_retry_worker, self.command_worker]:
            if worker and worker.isRunning():
                worker.stop()
                stopped = True

        if stopped:
            self._append_output("", "output")
            self._append_output(tr('stopping_task'), "warning")
            self.status_label.setText(f"{tr('status_prefix')}{tr('stopped')}")
        else:
            self._append_output(tr('no_running_task'), "system")

        self._set_buttons_state(False)

    # ---------- 输入框命令 ----------
    def _on_input_enter(self):
        command = self.input_box.text().strip()
        if not command:
            return

        if self.active_root_shell and self.active_root_shell._stdin_pipe:
            shell = self.active_root_shell
            proc_dead = shell.process is not None and shell.process.poll() is not None
            if proc_dead or shell._stdin_pipe.closed:
                self.active_root_shell = None
                self._append_output(tr('root_shell_closed'), "system")
            else:
                self._append_output(f"# {command}", "command")
                if shell.send_to_shell(command):
                    self.input_box.clear()
                    return

        if self.command_worker and self.command_worker.isRunning():
            self._append_output(tr('warn_prev_running'), "warning")
            return

        self.input_box.clear()
        self.command_worker = CommandWorker(command)
        self.command_worker.output_signal.connect(self._append_output)
        self.command_worker.ansi_output_signal.connect(self._append_ansi)
        self.command_worker.finished_signal.connect(
            lambda: self.status_label.setText(f"{tr('status_prefix')}{tr('status_ready')}"))
        self.command_worker.start()

    def is_busy(self):
        workers = [self.execute_worker, self.root_worker,
                   self.get_root_worker, self.kernelsu_worker,
                   self.auto_retry_worker, self.command_worker]
        return any(w and w.isRunning() for w in workers)

    def cleanup(self):
        for worker in [self.execute_worker, self.root_worker,
                       self.get_root_worker, self.kernelsu_worker,
                       self.auto_retry_worker, self.command_worker]:
            if worker and worker.isRunning():
                worker.stop()
                worker.wait(3000)


# ==================== 自定义标题栏 ====================
class TitleBar(QFrame):
    """自定义标题栏 - 拖动窗口 + 最小化/最大化/关闭按钮"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(38)
        self._main_window = parent
        self._drag_pos = None
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 6, 0)
        layout.setSpacing(4)

        self.title_label = QLabel(tr('title'))
        self.title_label.setObjectName("titleLogo")
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.min_btn = QPushButton("—")
        self.min_btn.setObjectName("winBtn")
        self.min_btn.setCursor(Qt.PointingHandCursor)
        self.min_btn.clicked.connect(self._on_minimize)

        self.max_btn = QPushButton("☐")
        self.max_btn.setObjectName("winBtn")
        self.max_btn.setCursor(Qt.PointingHandCursor)
        self.max_btn.clicked.connect(self._on_maximize)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self._on_close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

    def _on_minimize(self):
        if self._main_window:
            self._main_window.showMinimized()

    def _on_maximize(self):
        if not self._main_window:
            return
        if self._main_window.isMaximized():
            self._main_window.showNormal()
            self.max_btn.setText("☐")
        else:
            self._main_window.showMaximized()
            self.max_btn.setText("❐")

    def _on_close(self):
        if self._main_window:
            self._main_window.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._main_window:
            self._drag_pos = event.globalPos() - self._main_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None and self._main_window:
            if self._main_window.isMaximized():
                # 最大化状态下拖动则先还原
                self._main_window.showNormal()
                self.max_btn.setText("☐")
                # 根据鼠标在标题栏的相对位置调整还原后窗口位置
                ratio = event.pos().x() / max(self.width(), 1)
                self._drag_pos = QPoint(
                    int(event.globalX() - self._main_window.width() * ratio),
                    event.globalY() - 19)
            self._main_window.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._on_maximize()
            event.accept()


# ==================== 主窗口 ====================
class MainWindow(QMainWindow):
    """主窗口 - 自定义圆角无边框窗口，管理多个终端会话标签页"""

    def __init__(self):
        super().__init__()
        self.session_count = 0
        self._init_ui()
        self._add_session()

    def _init_ui(self):
        # 无边框 + 半透明背景 (用于圆角)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle(tr('window_title'))
        self.setMinimumSize(900, 650)
        self.resize(960, 700)

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        # 外阴影效果
        shadow = QGraphicsDropShadowEffect(central)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        central.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- 自定义标题栏 ----
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        # ---- 内容区 ----
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 8, 10, 10)
        content_layout.setSpacing(8)

        # ---- 标签页区域 ----
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_session)

        content_layout.addWidget(self.tab_widget, stretch=1)

        # ---- 底部状态栏 ----
        footer_frame = QFrame()
        footer_frame.setObjectName("statusFrame")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(12, 6, 12, 6)

        self.global_status = QLabel(tr('statusbar_ready') + os.getcwd())
        self.global_status.setObjectName("statusLabel")
        footer_layout.addWidget(self.global_status)
        footer_layout.addStretch()

        adb_status = QLabel(
            "ADB: " + (tr('installed') if self._check_adb() else tr('not_installed')))
        adb_status.setObjectName("statusLabel")
        footer_layout.addWidget(adb_status)

        content_layout.addWidget(footer_frame)

        main_layout.addWidget(content_widget, stretch=1)

    def _check_adb(self):
        try:
            result = subprocess.run(
                adb_cmd('version'), stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, timeout=5,
                **_subprocess_common_kwargs())
            return result.returncode == 0
        except Exception:
            return False

    def _add_session(self):
        self.session_count += 1
        session = TerminalSession(session_id=self.session_count)
        session.new_session_requested.connect(self._add_session)
        session.language_changed.connect(self._on_language_changed)
        self.tab_widget.addTab(session, f"  {tr('session_title').format(self.session_count)}")
        self.tab_widget.setCurrentWidget(session)
        session.input_box.setFocus()

    def _on_language_changed(self):
        """语言切换时更新所有会话和标题"""
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, TerminalSession):
                widget._update_ui_texts()
        self.title_bar.title_label.setText(tr('title'))
        self.setWindowTitle(tr('window_title'))

    def _close_session(self, index):
        if self.tab_widget.count() <= 1:
            self._add_session()

        widget = self.tab_widget.widget(index)
        if widget:
            if isinstance(widget, TerminalSession) and widget.is_busy():
                msg = ThemeMessageBox(
                    self,
                    title=tr('close_confirm'),
                    text=tr('close_msg'),
                    icon=QMessageBox.standardIcon(QMessageBox.Warning),
                    ok_text=tr('yes'),
                    cancel_text=tr('no'))
                msg.exec_()
                if not msg.is_ok():
                    return
            if isinstance(widget, TerminalSession):
                widget.cleanup()
            self.tab_widget.removeTab(index)
            widget.deleteLater()

    def closeEvent(self, event):
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, TerminalSession):
                widget.cleanup()
        event.accept()


# ==================== 入口 ====================
def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    app.setFont(QFont("Microsoft YaHei", 10))

    ensure_adb_selected()
    check_ionstack_conf()

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
