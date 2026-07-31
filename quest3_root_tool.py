#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quest3/3s 临时 Root 提权工具
一键提取 Quest3/3s 临时 Root

"""

import sys
import os
import subprocess
import threading
import time
import re
import select
import webbrowser
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
    min-width: 300px;
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


def parse_ansi_and_append(text_browser, text, default_fg="#cdd6f4", default_bg=None):
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


# ==================== ADB 辅助函数 ====================
def run_adb_command(cmd, timeout=30):
    """执行 ADB 命令并返回结果 (stdout, stderr, rc)"""
    try:
        if isinstance(cmd, str):
            cmd = cmd.split()
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        out = decode_bytes_smart(result.stdout)
        err = decode_bytes_smart(result.stderr)
        return out, err, result.returncode
    except subprocess.TimeoutExpired:
        return "", "命令超时", -1
    except FileNotFoundError:
        return "", "未找到 adb 命令，请确保 adb 已安装并添加到 PATH", -2
    except Exception as e:
        return "", str(e), -3


def check_device_connected():
    """检查设备是否已连接且可用"""
    stdout, stderr, rc = run_adb_command(['adb', 'devices'], timeout=5)
    if rc != 0:
        return False
    lines = stdout.strip().split('\n')
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) >= 2 and parts[1] == 'device':
            return True
    return False


def get_device_model():
    """获取设备型号"""
    stdout, _, _ = run_adb_command(['adb', 'shell', 'getprop', 'ro.product.model'], timeout=5)
    return stdout.strip()


# ==================== 工作线程 ====================
class ExecuteWorker(QThread):
    """开始执行 - 文件检查、adb reboot、重连检测、推送文件"""
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
        self.status_signal.emit("正在检查文件...")
        self.emit_output("=" * 56, "system")
        self.emit_output("  开始执行 - 文件检查与推送", "info")
        self.emit_output("=" * 56, "system")

        preload_path = os.path.join(os.getcwd(), "preload")
        ionstack_path = os.path.join(os.getcwd(), "ionstack.conf")

        preload_exists = os.path.isfile(preload_path)
        ionstack_exists = os.path.isfile(ionstack_path)

        self.emit_output(f"  检查文件: preload", "system")
        self.emit_output(f"    路径: {preload_path}", "system")
        self.emit_output(f"    状态: {'存在' if preload_exists else '不存在'}",
                         "success" if preload_exists else "error")

        self.emit_output(f"  检查文件: ionstack.conf", "system")
        self.emit_output(f"    路径: {ionstack_path}", "system")
        self.emit_output(f"    状态: {'存在' if ionstack_exists else '不存在'}",
                         "success" if ionstack_exists else "error")

        if not preload_exists or not ionstack_exists:
            self.emit_output("", "output")
            self.emit_output("  [错误] 缺少必要文件！", "error")
            if not preload_exists:
                self.emit_output("    - preload 文件未找到", "error")
            if not ionstack_exists:
                self.emit_output("    - ionstack.conf 文件未找到", "error")
            self.emit_output("  请将 preload 和 ionstack.conf 放在程序运行目录下", "warning")
            self.status_signal.emit("文件检查失败")
            self.finished_signal.emit(False)
            return

        self.emit_output("  [OK] 所有文件检查通过", "success")
        self.emit_output("", "output")

        # ---- 步骤2: 检查设备连接 ----
        self.status_signal.emit("正在检查设备连接...")
        if not check_device_connected():
            self.emit_output("  [警告] 当前未检测到已连接的设备", "warning")
            self.emit_output("  请确保设备已通过 USB 连接并开启 USB 调试", "warning")
            self.finished_signal.emit(False)
            return

        device_model = get_device_model()
        self.emit_output(f"  [OK] 设备已连接: {device_model}", "success")

        # ---- 步骤3: 执行 adb reboot ----
        self.status_signal.emit("正在重启设备...")
        self.emit_output("", "output")
        self.emit_output("  正在执行设备重启...", "info")
        self.emit_output("$ adb reboot", "command")

        stdout, stderr, rc = run_adb_command(['adb', 'reboot'], timeout=15)
        if rc != 0 and "device" not in stderr.lower():
            self.emit_output(f"  [警告] reboot 命令返回: {stderr.strip()}", "warning")

        self.emit_output("  设备正在重启中...", "device")

        # ---- 步骤4: 等待设备断开 ----
        self.status_signal.emit("等待设备断开...")
        self.emit_output("", "output")
        self.emit_output("  正在等待设备断开连接...", "system")
        disconnect_wait = 0
        while not self.stop_flag and disconnect_wait < 30:
            if not check_device_connected():
                self.emit_output("  [OK] 设备已断开连接", "success")
                break
            time.sleep(1)
            disconnect_wait += 1

        if self.stop_flag:
            self.emit_output("  已停止执行", "warning")
            self.finished_signal.emit(False)
            return

        # ---- 步骤5: 等待设备重连 ----
        self.status_signal.emit("等待设备重连...")
        self.emit_output("", "output")
        self.emit_output("  正在等待设备重新连接至 ADB...", "info")
        self.emit_output("  (设备重启可能需要一些时间，请耐心等待...)", "system")

        reconnect_wait = 0
        connected = False
        while not self.stop_flag and reconnect_wait < 180:
            if check_device_connected():
                connected = True
                self.emit_output(f"  [OK] 设备已重新连接! (等待了 {reconnect_wait} 秒)", "success")
                break
            if reconnect_wait > 0 and reconnect_wait % 10 == 0:
                self.emit_output(f"  仍在等待设备重连... ({reconnect_wait}s)", "system")
            time.sleep(2)
            reconnect_wait += 2

        if self.stop_flag:
            self.emit_output("  已停止执行", "warning")
            self.finished_signal.emit(False)
            return

        if not connected:
            self.emit_output("  [错误] 设备重连超时 (3分钟)", "error")
            self.emit_output("  请检查设备状态并手动重试", "warning")
            self.finished_signal.emit(False)
            return

        # ---- 步骤6: 检查连接稳定性 (10秒) ----
        self.status_signal.emit("正在检查连接稳定性...")
        self.emit_output("", "output")
        self.emit_output("  正在检查 ADB 连接稳定性 (10秒)...", "info")

        stable = True
        for i in range(10):
            if self.stop_flag:
                self.emit_output("  已停止执行", "warning")
                self.finished_signal.emit(False)
                return
            if not check_device_connected():
                self.emit_output(f"  [警告] 第 {i+1} 秒: 设备断开!", "error")
                stable = False
                self.emit_output("  正在等待设备重新连接...", "system")
                retry = 0
                reconnected = False
                while not self.stop_flag and retry < 60:
                    if check_device_connected():
                        reconnected = True
                        self.emit_output(f"  [OK] 设备已重新连接，重新开始稳定性检查", "success")
                        break
                    time.sleep(2)
                    retry += 2
                if not reconnected:
                    self.emit_output("  [错误] 设备重连失败", "error")
                    self.finished_signal.emit(False)
                    return
                self.emit_output("  重新开始 10 秒稳定性检查...", "info")
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
            self.emit_output("  [错误] 连接不稳定，请检查 USB 连接", "error")
            self.finished_signal.emit(False)
            return

        self.emit_output("  [OK] 连接稳定! 稳定性检查通过 (10/10)", "success")

        # ---- 步骤7: 推送文件并设置权限 ----
        self.status_signal.emit("正在推送文件...")
        self.emit_output("", "output")
        self.emit_output("  正在推送文件到设备...", "info")

        # adb push preload
        self.emit_output("$ adb push preload /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'push', preload_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output(f"  [错误] 推送 preload 失败: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        if stdout.strip():
            self.emit_output(f"  {stdout.strip()}", "output")
        if stderr.strip():
            self.emit_output(f"  {stderr.strip()}", "output")
        self.emit_output("  [OK] preload 推送成功", "success")

        time.sleep(4)

        # adb push ionstack.conf
        self.emit_output("$ adb push ionstack.conf /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'push', ionstack_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output(f"  [错误] 推送 ionstack.conf 失败: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        if stdout.strip():
            self.emit_output(f"  {stdout.strip()}", "output")
        if stderr.strip():
            self.emit_output(f"  {stderr.strip()}", "output")
        self.emit_output("  [OK] ionstack.conf 推送成功", "success")

        time.sleep(4)

        # adb shell chmod +x
        self.emit_output("$ adb shell chmod +x /data/local/tmp/preload", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'shell', 'chmod', '+x', '/data/local/tmp/preload'], timeout=10)
        if rc != 0:
            self.emit_output(f"  [错误] chmod 失败: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        self.emit_output("  [OK] preload 已设置为可执行权限", "success")

        # ---- 完成 ----
        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        self.emit_output("  执行完成! 文件已推送并设置权限", "success")
        self.emit_output("  现在可以点击「开始提权」进行 Root 提权", "info")
        self.emit_output("=" * 56, "system")
        self.status_signal.emit("执行完成")
        self.finished_signal.emit(True)


class RootWorker(QThread):
    """开始提权 - 执行 preload，检测 # 提示符"""
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
        self.emit_output("  开始提权 - 执行 preload", "info")
        self.emit_output("=" * 56, "system")

        self.status_signal.emit("正在检查设备...")
        if not check_device_connected():
            self.emit_output("  [错误] 未检测到已连接的设备", "error")
            self.emit_output("  请确保设备已通过 USB 连接并开启 USB 调试", "warning")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return

        device_model = get_device_model()
        self.emit_output(f"  设备型号: {device_model}", "device")

        self.status_signal.emit("正在执行提权命令...")
        self.emit_output("", "output")
        self.emit_output("  正在执行提权命令...", "info")
        self.emit_output("$ adb shell /data/local/tmp/preload", "command")
        self.emit_output("", "output")

        try:
            self.process = subprocess.Popen(
                ['adb', 'shell', '/data/local/tmp/preload'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                bufsize=0
            )

            root_detected = False
            start_time = time.time()

            while not self.stop_flag:
                try:
                    readable, _, _ = select.select([self.process.stdout], [], [], 0.5)
                except (ValueError, OSError):
                    break

                if readable:
                    line_bytes = self.process.stdout.readline()
                    if not line_bytes:
                        if self.process.poll() is not None:
                            break
                        continue

                    line = decode_bytes_smart(line_bytes).rstrip('\r\n')
                    if line.strip():
                        # 先按ANSI渲染（保留原始终端颜色）
                        self.ansi_output_signal.emit(line)

                    if self._is_root_prompt(line):
                        root_detected = True
                        self._stdin_pipe = self.process.stdin
                        self.emit_output("", "output")
                        self.emit_output("=" * 56, "system")
                        self.emit_output("  >>> 已成功提权! <<<", "success")
                        self.emit_output(f"  检测到 Root Shell: {line.strip()}", "success")
                        self.emit_output("=" * 56, "system")
                        self.status_signal.emit("提权成功")
                        self.success_signal.emit()

                        while not self.stop_flag:
                            try:
                                readable, _, _ = select.select(
                                    [self.process.stdout], [], [], 0.5)
                            except (ValueError, OSError):
                                break
                            if readable:
                                line_bytes = self.process.stdout.readline()
                                if not line_bytes:
                                    break
                                line = decode_bytes_smart(line_bytes).rstrip('\r\n')
                                if line.strip():
                                    self.ansi_output_signal.emit(line)
                            elif self.process.poll() is not None:
                                break
                        break

                if self.process.poll() is not None:
                    remaining = self.process.stdout.read()
                    if remaining:
                        for line in decode_bytes_smart(remaining).split('\n'):
                            if line.strip():
                                self.ansi_output_signal.emit(line.rstrip())
                    break

                elapsed = time.time() - start_time
                if elapsed > 300 and not root_detected:
                    self.emit_output("  [警告] 提权超时 (5分钟)", "warning")
                    break

            if self.stop_flag:
                self.emit_output("", "output")
                self.emit_output("  已停止执行", "warning")
                self.finished_signal.emit()
                return

            if not root_detected:
                self.emit_output("", "output")
                if not check_device_connected():
                    self.emit_output("  [错误] 设备已断开连接 (可能已重启)", "error")
                    self.emit_output("  >>> 提权失败，请重新尝试 <<<", "error")
                    self.status_signal.emit("提权失败")
                    self.failure_signal.emit()
                    self.need_auto_retry_signal.emit()
                else:
                    self.emit_output("  [错误] 未检测到 Root 提示符", "error")
                    self.emit_output("  >>> 提权失败，请重新尝试 <<<", "error")
                    self.status_signal.emit("提权失败")
                    self.failure_signal.emit()
                    self.need_auto_retry_signal.emit()

        except FileNotFoundError:
            self.emit_output("  [错误] 未找到 adb 命令", "error")
            self.failure_signal.emit()
            self.need_auto_retry_signal.emit()
        except Exception as e:
            self.emit_output(f"  [错误] 执行异常: {str(e)}", "error")
            self.failure_signal.emit()
            self.need_auto_retry_signal.emit()
        finally:
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
        patterns = [
            r'^[\w.\-]+:[^\s]*\s*#\s*$',
            r'^[\w.\-]+:\s*/\s*#\s*$',
        ]
        for pat in patterns:
            if re.match(pat, line):
                return True
        if line.endswith('#') and ':' in line and len(line) < 60:
            if not line.startswith('#') and '://' not in line:
                return True
        return False

    def send_to_shell(self, command):
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

    def __init__(self):
        super().__init__()
        self.stop_flag = False
        self.process = None
        self._stdin_pipe = None

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
        """执行adb命令并渲染ANSI输出"""
        self.emit_output(f"$ {' '.join(cmd) if isinstance(cmd, list) else cmd}", "command")
        try:
            if isinstance(cmd, str):
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, cwd=os.getcwd(),
                                        bufsize=0)
            else:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        bufsize=0)
            while not self.stop_flag:
                try:
                    readable, _, _ = select.select([proc.stdout], [], [], 0.3)
                except (ValueError, OSError):
                    break
                if readable:
                    bs = proc.stdout.readline()
                    if not bs:
                        break
                    line = decode_bytes_smart(bs).rstrip('\r\n')
                    if line.strip():
                        self.ansi_output_signal.emit(line)
                elif proc.poll() is not None:
                    break
            rc = proc.wait(timeout=timeout)
            return rc == 0
        except Exception as e:
            self.emit_output(f"  [错误] {str(e)}", "error")
            return False

    def run(self):
        self.stop_flag = False

        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        self.emit_output("  获取 Root - Magisk 环境安装与启动", "info")
        self.emit_output("  (所有命令在当前会话执行，间隔4秒)", "system")
        self.emit_output("=" * 56, "system")

        # 检查设备
        self.status_signal.emit("正在检查设备...")
        if not check_device_connected():
            self.emit_output("  [错误] 未检测到已连接的设备", "error")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return
        self.emit_output(f"  [OK] 设备已连接: {get_device_model()}", "success")

        # 检查Magisk是否已安装
        self.emit_output("", "output")
        self.status_signal.emit("检查 Magisk 是否已安装...")
        self.emit_output("  正在检查 Magisk 是否安装...", "info")
        out, err, rc = run_adb_command(
            ['adb', 'shell', 'pm', 'list', 'packages'], timeout=15)
        magisk_installed = 'com.topjohnwu.magisk' in out.lower()
        if magisk_installed:
            self.emit_output("  [OK] 检测到 Magisk 已安装，跳过APK安装步骤", "success")
        else:
            self.emit_output("  [提示] 未检测到 Magisk，尝试安装当前目录下的APK...", "warning")
            apk_files = [f for f in os.listdir(os.getcwd()) if f.lower().endswith('.apk')]
            if apk_files:
                self.emit_output(f"  找到 {len(apk_files)} 个APK文件，开始安装...", "info")
                for apk in apk_files:
                    if not self._delay():
                        self.failure_signal.emit(); self.finished_signal.emit(); return
                    apk_path = os.path.join(os.getcwd(), apk)
                    self.emit_output(f"  正在安装: {apk}", "info")
                    ok = self._run_adb(['adb', 'install', '-r', apk_path], timeout=120)
                    if ok:
                        self.emit_output(f"  [OK] {apk} 安装成功", "success")
                    else:
                        self.emit_output(f"  [警告] {apk} 安装失败（继续）", "warning")
            else:
                self.emit_output("  [警告] 当前目录下未找到APK文件，跳过安装", "warning")

        # ===== push busybox =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit("推送 busybox...")
        busybox_path = os.path.join(os.getcwd(), "busybox")
        if os.path.isfile(busybox_path):
            self._run_adb(['adb', 'push', busybox_path, '/data/local/tmp/'], timeout=60)
        else:
            self.emit_output("$ adb push busybox /data/local/tmp/", "command")
            self.emit_output("  [提示] busybox 此无文件，跳过", "warning")

        # ===== push magisk.apk =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit("推送 magisk.apk...")
        magisk_apk_path = os.path.join(os.getcwd(), "magisk.apk")
        if os.path.isfile(magisk_apk_path):
            self._run_adb(['adb', 'push', magisk_apk_path, '/data/local/tmp/'], timeout=60)
        else:
            self.emit_output("$ adb push magisk.apk /data/local/tmp/", "command")
            self.emit_output("  [提示] magisk.apk 此无文件，跳过", "warning")

        # ===== push live_setup.sh =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit("推送 live_setup.sh...")
        live_setup_path = os.path.join(os.getcwd(), "live_setup.sh")
        if not os.path.isfile(live_setup_path):
            self.emit_output("$ adb push live_setup.sh /data/local/tmp/", "command")
            self.emit_output("  [错误] live_setup.sh 此无文件，无法继续", "error")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return
        self._run_adb(['adb', 'push', live_setup_path, '/data/local/tmp/'], timeout=60)

        # ===== chmod +x live_setup.sh =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit("设置 live_setup.sh 执行权限...")
        self._run_adb(['adb', 'shell', 'chmod', '+x', '/data/local/tmp/live_setup.sh'])

        # ===== 执行 /data/local/tmp/live_setup.sh =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit("执行 live_setup.sh...")
        self.emit_output("", "output")
        self.emit_output("  正在执行 live_setup.sh ...", "info")
        ok = self._run_adb(['adb', 'shell', '/data/local/tmp/live_setup.sh'], timeout=300)
        if not ok:
            self.emit_output("  [警告] live_setup.sh 返回非零，继续后续步骤", "warning")

        # ===== cd /data/adb; magisk --daemon =====
        if not self._delay():
            self.failure_signal.emit(); self.finished_signal.emit(); return
        self.status_signal.emit("启动 magisk --daemon...")
        self.emit_output("", "output")
        self.emit_output("  正在启动 magisk --daemon ...", "info")
        ok = self._run_adb(['adb', 'shell', 'sh', '-c', 'cd /data/adb && magisk --daemon'], timeout=60)

        self.emit_output("", "output")
        self.emit_output("=" * 56, "system")
        if ok:
            self.emit_output("  >>> 获取Root步骤执行完成! <<<", "success")
            self.status_signal.emit("获取Root完成")
            self.success_signal.emit()
        else:
            self.emit_output("  获取Root步骤执行完毕 (可在下方输入框手动验证)", "warning")
            self.status_signal.emit("获取Root完成(请手动验证)")
            self.success_signal.emit()
        self.emit_output("  请在下方输入框输入命令进行验证: adb shell su -c id", "info")
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

    def stop(self):
        self.stop_flag = True

    def emit_output(self, text, color_type="output"):
        self.output_signal.emit(text, color_type)

    def emit_ansi(self, text):
        self.ansi_output_signal.emit(text)

    def run(self):
        self.stop_flag = False

        self.emit_output("", "output")
        self.emit_output("#" * 56, "warning")
        self.emit_output("  >>> 自动提权模式已启动 <<<", "warning")
        self.emit_output("  将自动循环执行 [开始执行] + [开始提权]", "warning")
        self.emit_output("  直到成功为止 (可点击「停止」终止)", "warning")
        self.emit_output("#" * 56, "warning")

        while not self.stop_flag:
            self.attempt += 1
            self.emit_output("", "output")
            self.emit_output(f"{'=' * 20} 第 {self.attempt} 次尝试 {'=' * 20}", "info")

            self.status_signal.emit(f"自动提权 - 第{self.attempt}次: 执行中...")
            self.emit_output("", "output")
            self.emit_output(f"--- [自动] 阶段1: 开始执行 ---", "info")

            success = self._run_execute_phase()
            if self.stop_flag:
                self.emit_output("  自动提权已停止", "warning")
                self.finished_signal.emit()
                return
            if not success:
                self.emit_output(f"  第 {self.attempt} 次尝试 - 执行阶段失败，重试...", "warning")
                time.sleep(2)
                continue

            self.status_signal.emit(f"自动提权 - 第{self.attempt}次: 提权中...")
            self.emit_output("", "output")
            self.emit_output(f"--- [自动] 阶段2: 开始提权 ---", "info")

            success = self._run_root_phase()
            if self.stop_flag:
                self.emit_output("  自动提权已停止", "warning")
                self.finished_signal.emit()
                return
            if success:
                self.emit_output("", "output")
                self.emit_output("#" * 56, "success")
                self.emit_output(f"  >>> 自动提权成功! (共尝试 {self.attempt} 次) <<<", "success")
                self.emit_output("#" * 56, "success")
                self.status_signal.emit("自动提权成功")
                self.success_signal.emit()
                self.finished_signal.emit()
                return
            else:
                self.emit_output(f"  第 {self.attempt} 次尝试 - 提权失败，重试...", "warning")
                time.sleep(2)

        self.emit_output("  自动提权已停止", "warning")
        self.finished_signal.emit()

    def _run_execute_phase(self):
        preload_path = os.path.join(os.getcwd(), "preload")
        ionstack_path = os.path.join(os.getcwd(), "ionstack.conf")

        if not os.path.isfile(preload_path) or not os.path.isfile(ionstack_path):
            self.emit_output("  [错误] 缺少 preload 或 ionstack.conf 文件", "error")
            return False

        if not check_device_connected():
            self.emit_output("  [等待] 设备未连接，等待重连...", "system")
            wait = 0
            while not self.stop_flag and wait < 120:
                if check_device_connected():
                    break
                time.sleep(2)
                wait += 2
            if not check_device_connected():
                self.emit_output("  [错误] 设备重连超时", "error")
                return False
        self.emit_output("  [OK] 设备已连接", "success")

        self.emit_output("  正在重启设备...", "info")
        self.emit_output("$ adb reboot", "command")
        run_adb_command(['adb', 'reboot'], timeout=15)

        wait = 0
        while not self.stop_flag and wait < 30:
            if not check_device_connected():
                break
            time.sleep(1)
            wait += 1

        self.emit_output("  等待设备重连...", "system")
        wait = 0
        connected = False
        while not self.stop_flag and wait < 180:
            if check_device_connected():
                connected = True
                self.emit_output(f"  [OK] 设备已重连 ({wait}s)", "success")
                break
            time.sleep(2)
            wait += 2
        if not connected:
            self.emit_output("  [错误] 设备重连超时", "error")
            return False

        self.emit_output("  检查连接稳定性 (10s)...", "system")
        for i in range(10):
            if self.stop_flag:
                return False
            if not check_device_connected():
                self.emit_output(f"  [警告] 第{i+1}秒设备断开，等待重连...", "warning")
                retry = 0
                while not self.stop_flag and retry < 60:
                    if check_device_connected():
                        self.emit_output("  [OK] 设备已重连", "success")
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
        self.emit_output("  [OK] 连接稳定", "success")

        self.emit_output("$ adb push preload /data/local/tmp/", "command")
        _, _, rc = run_adb_command(['adb', 'push', preload_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output("  [错误] 推送 preload 失败", "error")
            return False
        self.emit_output("  [OK] preload 推送成功", "success")
        time.sleep(4)

        self.emit_output("$ adb push ionstack.conf /data/local/tmp/", "command")
        _, _, rc = run_adb_command(['adb', 'push', ionstack_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output("  [错误] 推送 ionstack.conf 失败", "error")
            return False
        self.emit_output("  [OK] ionstack.conf 推送成功", "success")
        time.sleep(4)

        self.emit_output("$ adb shell chmod +x /data/local/tmp/preload", "command")
        _, _, rc = run_adb_command(['adb', 'shell', 'chmod', '+x', '/data/local/tmp/preload'], timeout=10)
        if rc != 0:
            self.emit_output("  [错误] chmod 失败", "error")
            return False
        self.emit_output("  [OK] 权限设置成功", "success")
        self.emit_output("  [OK] 执行阶段完成", "success")
        return True

    def _run_root_phase(self):
        if not check_device_connected():
            self.emit_output("  [错误] 设备未连接", "error")
            return False

        self.emit_output("  正在执行提权命令...", "info")
        self.emit_output("$ adb shell /data/local/tmp/preload", "command")

        try:
            process = subprocess.Popen(
                ['adb', 'shell', '/data/local/tmp/preload'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE, bufsize=0)

            root_detected = False
            start_time = time.time()

            while not self.stop_flag:
                try:
                    readable, _, _ = select.select([process.stdout], [], [], 0.5)
                except (ValueError, OSError):
                    break
                if readable:
                    line_bytes = process.stdout.readline()
                    if not line_bytes:
                        if process.poll() is not None:
                            break
                        continue
                    line = decode_bytes_smart(line_bytes).rstrip('\r\n')
                    if line.strip():
                        self.ansi_output_signal.emit(line)
                    if self._is_root_prompt(line):
                        root_detected = True
                        self.emit_output("  >>> 检测到 Root Shell! <<<", "success")
                        try:
                            process.terminate()
                        except Exception:
                            pass
                        break
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        for line in decode_bytes_smart(remaining).split('\n'):
                            if line.strip():
                                self.ansi_output_signal.emit(line.rstrip())
                    break
                if time.time() - start_time > 300:
                    self.emit_output("  [警告] 提权超时", "warning")
                    break

            if self.stop_flag:
                try: process.terminate()
                except Exception: pass
                return False

            if root_detected:
                return True
            if not check_device_connected():
                self.emit_output("  [错误] 设备已断开 (可能已重启)", "error")
            else:
                self.emit_output("  [错误] 未检测到 Root 提示符", "error")
            return False
        except Exception as e:
            self.emit_output(f"  [错误] 执行异常: {str(e)}", "error")
            return False

    def _is_root_prompt(self, line):
        line = line.strip()
        if not line:
            return False
        patterns = [r'^[\w.\-]+:[^\s]*\s*#\s*$']
        for pat in patterns:
            if re.match(pat, line):
                return True
        if line.endswith('#') and ':' in line and len(line) < 60:
            if not line.startswith('#') and '://' not in line:
                return True
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
                stdin=subprocess.PIPE, bufsize=0, cwd=os.getcwd())

            while not self.stop_flag:
                try:
                    readable, _, _ = select.select([self.process.stdout], [], [], 0.3)
                except (ValueError, OSError):
                    break
                if readable:
                    bs = self.process.stdout.readline()
                    if not bs:
                        if self.process.poll() is not None:
                            break
                        continue
                    line = decode_bytes_smart(bs).rstrip('\r\n')
                    if line.strip():
                        self.ansi_output_signal.emit(line)
                elif self.process.poll() is not None:
                    break

            if self.stop_flag:
                try: self.process.terminate()
                except Exception: pass
                self.output_signal.emit("^C (已中断)", "warning")
            else:
                rc = self.process.poll()
                if rc and rc != 0:
                    self.output_signal.emit(f"(退出码: {rc})", "system")
        except Exception as e:
            self.output_signal.emit(f"错误: {str(e)}", "error")

        self.finished_signal.emit()


# ==================== 关于对话框 ====================
class AboutDialog(QDialog):
    """关于对话框 - 项目信息、致谢、链接"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于 Quest3/3s Root Tool")
        self.setMinimumSize(560, 480)
        self.resize(580, 500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 标题
        title = QLabel("⚡ Quest3/3s 临时 Root 提权工具  v1.0")
        title.setStyleSheet("color: #cba6f7; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        divider1 = QFrame()
        divider1.setFrameShape(QFrame.HLine)
        divider1.setStyleSheet("color: #313244;")
        layout.addWidget(divider1)

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
        layout.addWidget(content, stretch=1)

        # 按钮
        btns = QDialogButtonBox(QDialogButtonBox.Ok)
        btns.button(QDialogButtonBox.Ok).setText("关闭")
        btns.accepted.connect(self.accept)
        layout.addWidget(btns)


# ==================== 终端会话组件 ====================
class TerminalSession(QWidget):
    """单个终端会话 - 包含输出区、输入框、按钮"""

    new_session_requested = pyqtSignal()

    def __init__(self, session_id=1, parent=None):
        super().__init__(parent)
        self.session_id = session_id
        self.setObjectName("terminalSession")

        self.execute_worker = None
        self.root_worker = None
        self.get_root_worker = None
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

        self.execute_btn = QPushButton("▶  开始执行")
        self.execute_btn.setObjectName("executeBtn")
        self.execute_btn.setCursor(Qt.PointingHandCursor)
        self.execute_btn.setToolTip("检查文件 → adb reboot → 等待重连 → 推送文件")

        self.get_root_btn = QPushButton("🔓  获取Root")
        self.get_root_btn.setObjectName("getRootBtn")
        self.get_root_btn.setCursor(Qt.PointingHandCursor)
        self.get_root_btn.setToolTip(
            "安装APK→push busybox/magisk/live_setup→chmod→执行脚本→magisk --daemon (单会话，每条间隔4秒)")

        self.root_btn = QPushButton("⚡  开始提权")
        self.root_btn.setObjectName("rootBtn")
        self.root_btn.setCursor(Qt.PointingHandCursor)
        self.root_btn.setToolTip("执行 /data/local/tmp/preload 进行 Root 提权")

        self.stop_btn = QPushButton("■  停止")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setToolTip("停止当前正在执行的任务")

        self.new_session_btn = QPushButton("＋ 新建会话")
        self.new_session_btn.setObjectName("newSessionBtn")
        self.new_session_btn.setCursor(Qt.PointingHandCursor)
        self.new_session_btn.setToolTip("创建新的终端会话")

        toolbar_layout.addWidget(self.execute_btn)
        toolbar_layout.addWidget(self.root_btn)
        toolbar_layout.addWidget(self.get_root_btn)
        toolbar_layout.addWidget(self.stop_btn)
        toolbar_layout.addStretch()

        self.status_label = QLabel("就绪")
        self.status_label.setObjectName("statusLabel")
        toolbar_layout.addWidget(self.status_label)

        toolbar_layout.addWidget(self.new_session_btn)

        layout.addWidget(toolbar_frame)

        # ---- 工具栏2: 文件状态栏（按钮下方）----
        file_status_frame = QFrame()
        file_status_frame.setObjectName("fileStatusFrame")
        file_status_layout = QHBoxLayout(file_status_frame)
        file_status_layout.setContentsMargins(12, 8, 12, 8)
        file_status_layout.setSpacing(16)

        title_label = QLabel("📁 文件状态:")
        title_label.setStyleSheet("color:#6c7086;font-size:12px;font-weight:bold;")
        file_status_layout.addWidget(title_label)

        self.preload_status_label = QLabel("preload: —")
        self.preload_status_label.setObjectName("fileStatusMISS")

        self.ionstack_status_label = QLabel("ionstack.conf: —")
        self.ionstack_status_label.setObjectName("fileStatusMISS")

        file_status_layout.addWidget(self.preload_status_label)
        file_status_layout.addWidget(self.ionstack_status_label)
        file_status_layout.addStretch()

        self.refresh_file_btn = QPushButton("🔄 刷新")
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
        self.input_box.setPlaceholderText(
            "输入 ADB 命令或其他命令，按 Enter 执行... (如: adb devices)")
        self.input_box.returnPressed.connect(self._on_input_enter)

        self.run_btn = QPushButton("执行")
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

    # ---------- 文件状态 ----------
    def _refresh_file_status(self):
        preload_path = os.path.join(os.getcwd(), "preload")
        ionstack_path = os.path.join(os.getcwd(), "ionstack.conf")

        if os.path.isfile(preload_path):
            self.preload_status_label.setText("✅ preload: 已就绪")
            self.preload_status_label.setObjectName("fileStatusOK")
        else:
            self.preload_status_label.setText("❌ preload: 此无文件")
            self.preload_status_label.setObjectName("fileStatusMISS")

        if os.path.isfile(ionstack_path):
            self.ionstack_status_label.setText("✅ ionstack.conf: 已就绪")
            self.ionstack_status_label.setObjectName("fileStatusOK")
        else:
            self.ionstack_status_label.setText("❌ ionstack.conf: 此无文件")
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
            "║        Quest3/3s 临时 Root 提权工具                       ║", "info")
        self._append_output(
            "╠══════════════════════════════════════════════════════════╣", "system")
        self._append_output(
            "║  项目灵感: https://github.com/F-19-F/IonStackQuest3       ║", "system")
        self._append_output(
            "║  感谢B站UP主:我是一个小依旧                                ║", "system")
        self._append_output(
            "║  相关视频: https://b23.tv/FS958OJ                         ║", "system")
        self._append_output(
            "║  系统漏洞: CVE-2026-43499                                 ║", "system")
        self._append_output(
            "╚══════════════════════════════════════════════════════════╝", "system")
        self._append_output("", "output")
        self._append_output("  使用说明:", "info")
        self._append_output(
            "请查看原项目地址https://github.com/F-19-F/IonStackQuest3" \
            "使用说明您需要编译自己系统对应的文件才可以继续", "system")
        self._append_output("", "output")
        self._append_output(f"  当前工作目录: {os.getcwd()}", "system")
        self._append_output("", "output")

    # ---------- 输出渲染 ----------
    def _append_output(self, text, color_type="output"):
        """追加简单彩色输出（非ANSI）"""
        parse_ansi_and_append(self.terminal, text,
                              default_fg=COLORS.get(color_type, COLORS["output"]))

    def _append_ansi(self, text):
        """追加带ANSI颜色的原始输出"""
        parse_ansi_and_append(self.terminal, text)

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
            lambda s: self.status_label.setText(f"状态: {s}"))
        self.execute_worker.finished_signal.connect(self._on_execute_finished)
        self.execute_worker.start()

    def _on_execute_finished(self, success):
        self._set_buttons_state(False)
        self.status_label.setText("状态: 执行完成" if success else "状态: 执行失败")

    # ---------- 开始提权 ----------
    def _on_root_clicked(self):
        if self.root_worker and self.root_worker.isRunning():
            return
        if not check_device_connected():
            self._append_output("  [警告] 当前未检测到已连接的设备", "warning")
            self._append_output("  请先连接设备并执行「开始执行」", "warning")
            return

        self._set_buttons_state(True)
        self.root_worker = RootWorker()
        self.root_worker.output_signal.connect(self._append_output)
        self.root_worker.ansi_output_signal.connect(self._append_ansi)
        self.root_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"状态: {s}"))
        self.root_worker.success_signal.connect(self._on_root_success)
        self.root_worker.failure_signal.connect(self._on_root_failure)
        self.root_worker.need_auto_retry_signal.connect(self._show_auto_retry_dialog)
        self.root_worker.finished_signal.connect(self._on_root_finished)
        self.root_worker.start()

    def _on_root_success(self):
        self.status_label.setText("状态: 提权成功")
        self.active_root_shell = self.root_worker

    def _on_root_failure(self):
        self.status_label.setText("状态: 提权失败")

    def _on_root_finished(self):
        if not (self.auto_retry_worker and self.auto_retry_worker.isRunning()):
            self._set_buttons_state(False)
        self.active_root_shell = None

    # ---------- 获取Root ----------
    def _on_get_root_clicked(self):
        if self.get_root_worker and self.get_root_worker.isRunning():
            return
        if not check_device_connected():
            self._append_output("  [警告] 当前未检测到已连接的设备", "warning")
            self._append_output("  请先连接设备并确认 adb devices 可见", "warning")
            return

        self._set_buttons_state(True)
        self.status_label.setText("状态: 开始获取Root...")
        self.get_root_worker = GetRootWorker()
        self.get_root_worker.output_signal.connect(self._append_output)
        self.get_root_worker.ansi_output_signal.connect(self._append_ansi)
        self.get_root_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"状态: {s}"))
        self.get_root_worker.success_signal.connect(
            lambda: self.status_label.setText("状态: 获取Root完成"))
        self.get_root_worker.failure_signal.connect(
            lambda: self.status_label.setText("状态: 获取Root失败"))
        self.get_root_worker.finished_signal.connect(self._on_get_root_finished)
        self.get_root_worker.start()

    def _on_get_root_finished(self):
        self._set_buttons_state(False)

    # ---------- 自动重试 ----------
    def _show_auto_retry_dialog(self):
        QTimer.singleShot(0, self._show_retry_popup)

    def _show_retry_popup(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("提权失败")
        msg.setIcon(QMessageBox.Warning)
        msg.setText("提权失败，请重新尝试")
        msg.setInformativeText(
            "是否自动提权无需手动？\n\n"
            "点击「确定」: 自动循环执行 [开始执行] + [开始提权] 直到成功\n"
            "点击「取消」: 返回手动操作")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.button(QMessageBox.Ok).setText("确定 - 自动提权")
        msg.button(QMessageBox.Cancel).setText("取消 - 手动操作")
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self._start_auto_retry()
        else:
            self._set_buttons_state(False)
            self._append_output("  已选择手动操作，请重新点击相应按钮", "info")

    def _start_auto_retry(self):
        self._append_output("", "output")
        self._append_output("  正在启动自动提权模式...", "warning")
        self._set_buttons_state(True)
        self.stop_btn.setEnabled(True)

        self.auto_retry_worker = AutoRetryWorker()
        self.auto_retry_worker.output_signal.connect(self._append_output)
        self.auto_retry_worker.ansi_output_signal.connect(self._append_ansi)
        self.auto_retry_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"状态: {s}"))
        self.auto_retry_worker.success_signal.connect(
            lambda: self.status_label.setText("状态: 自动提权成功"))
        self.auto_retry_worker.finished_signal.connect(self._on_auto_retry_finished)
        self.auto_retry_worker.start()

    def _on_auto_retry_finished(self):
        self._set_buttons_state(False)

    # ---------- 停止 ----------
    def _on_stop_clicked(self):
        stopped = False
        for worker in [self.execute_worker, self.get_root_worker,
                       self.root_worker, self.auto_retry_worker,
                       self.command_worker]:
            if worker and worker.isRunning():
                worker.stop()
                stopped = True

        if stopped:
            self._append_output("", "output")
            self._append_output("  [停止] 正在停止当前任务...", "warning")
            self.status_label.setText("状态: 已停止")
        else:
            self._append_output("  当前没有正在运行的任务", "system")

        self._set_buttons_state(False)

    # ---------- 输入框命令 ----------
    def _on_input_enter(self):
        command = self.input_box.text().strip()
        if not command:
            return

        if self.active_root_shell and self.active_root_shell._stdin_pipe:
            if not self.active_root_shell._stdin_pipe.closed:
                self._append_output(f"# {command}", "command")
                if self.active_root_shell.send_to_shell(command):
                    self.input_box.clear()
                    return
            else:
                self.active_root_shell = None
                self._append_output("  Root Shell 已关闭，使用普通命令执行", "system")

        if self.command_worker and self.command_worker.isRunning():
            self._append_output("  [警告] 上一个命令仍在执行中", "warning")
            return

        self.input_box.clear()
        self.command_worker = CommandWorker(command)
        self.command_worker.output_signal.connect(self._append_output)
        self.command_worker.ansi_output_signal.connect(self._append_ansi)
        self.command_worker.finished_signal.connect(
            lambda: self.status_label.setText("状态: 就绪"))
        self.command_worker.start()

    def is_busy(self):
        workers = [self.execute_worker, self.root_worker,
                   self.get_root_worker, self.auto_retry_worker,
                   self.command_worker]
        return any(w and w.isRunning() for w in workers)

    def cleanup(self):
        for worker in [self.execute_worker, self.root_worker,
                       self.get_root_worker, self.auto_retry_worker,
                       self.command_worker]:
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

        self.title_label = QLabel("⚡ Quest3/3s 临时 Root 提权工具")
        self.title_label.setObjectName("titleLogo")
        layout.addWidget(self.title_label)
        layout.addStretch()

        self.min_btn = QPushButton("—")
        self.min_btn.setObjectName("winBtn")
        self.min_btn.setCursor(Qt.PointingHandCursor)
        self.min_btn.setToolTip("最小化")
        self.min_btn.clicked.connect(self._on_minimize)

        self.max_btn = QPushButton("☐")
        self.max_btn.setObjectName("winBtn")
        self.max_btn.setCursor(Qt.PointingHandCursor)
        self.max_btn.setToolTip("最大化/还原")
        self.max_btn.clicked.connect(self._on_maximize)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setToolTip("关闭")
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
        self.setWindowTitle("Quest3/3s 临时 Root 提权工具 v1.0")
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

        self.global_status = QLabel("就绪  |  工作目录: " + os.getcwd())
        self.global_status.setObjectName("statusLabel")
        footer_layout.addWidget(self.global_status)
        footer_layout.addStretch()

        adb_status = QLabel(
            "ADB: " + ("已安装" if self._check_adb() else "未安装"))
        adb_status.setObjectName("statusLabel")
        footer_layout.addWidget(adb_status)

        content_layout.addWidget(footer_frame)

        main_layout.addWidget(content_widget, stretch=1)

    def _check_adb(self):
        try:
            result = subprocess.run(
                ['adb', 'version'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, timeout=5)
            return result.returncode == 0
        except Exception:
            return False

    def _add_session(self):
        self.session_count += 1
        session = TerminalSession(session_id=self.session_count)
        session.new_session_requested.connect(self._add_session)
        self.tab_widget.addTab(session, f"  会话 {self.session_count}  ")
        self.tab_widget.setCurrentWidget(session)
        session.input_box.setFocus()

    def _close_session(self, index):
        if self.tab_widget.count() <= 1:
            self._add_session()

        widget = self.tab_widget.widget(index)
        if widget:
            if isinstance(widget, TerminalSession) and widget.is_busy():
                reply = QMessageBox.question(
                    self, "确认关闭",
                    "该会话有任务正在运行，确定要关闭吗？",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply != QMessageBox.Yes:
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

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
