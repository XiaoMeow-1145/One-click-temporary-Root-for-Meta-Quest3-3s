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
from queue import Queue, Empty

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLineEdit, QTextBrowser, QLabel,
    QMessageBox, QDialog, QFrame, QSizePolicy, QMenu, QAction,
    QScrollBar, QSpacerItem
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer, QSize, QMutex
from PyQt5.QtGui import QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QPalette, QKeySequence


# ==================== 全局样式表 (Catppuccin Mocha 深色主题) ====================
STYLE_SHEET = """
QMainWindow {
    background-color: #1e1e2e;
}
QWidget#centralWidget {
    background-color: #1e1e2e;
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
QLabel#titleLogo {
    color: #cba6f7;
    font-size: 18px;
    font-weight: bold;
    padding: 0px 10px;
}
QLabel#subtitle {
    color: #6c7086;
    font-size: 11px;
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
"""


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


# ==================== ADB 辅助函数 ====================
def run_adb_command(cmd, timeout=30):
    """执行 ADB 命令并返回结果"""
    try:
        if isinstance(cmd, str):
            cmd = cmd.split()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout, result.stderr, result.returncode
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
        while not self.stop_flag and reconnect_wait < 180:  # 最多等待3分钟
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
                # 重新等待连接
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
                # 重置稳定性检查
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
                    break  # 稳定性检查通过
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

        # adb push preload /data/local/tmp/
        self.emit_output("$ adb push preload /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'push', preload_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output(f"  [错误] 推送 preload 失败: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        if stdout.strip():
            self.emit_output(f"  {stdout.strip()}", "output")
        self.emit_output("  [OK] preload 推送成功", "success")

        time.sleep(0.5)

        # adb push ionstack.conf /data/local/tmp/
        self.emit_output("$ adb push ionstack.conf /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'push', ionstack_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output(f"  [错误] 推送 ionstack.conf 失败: {stderr.strip()}", "error")
            self.finished_signal.emit(False)
            return
        if stdout.strip():
            self.emit_output(f"  {stdout.strip()}", "output")
        self.emit_output("  [OK] ionstack.conf 推送成功", "success")

        time.sleep(0.5)

        # adb shell chmod +x /data/local/tmp/preload
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
    """开始提权 - 执行 preload，检测 # 提示符，处理失败"""
    output_signal = pyqtSignal(str, str)
    status_signal = pyqtSignal(str)
    success_signal = pyqtSignal()           # 提权成功
    failure_signal = pyqtSignal()           # 提权失败
    need_auto_retry_signal = pyqtSignal()   # 询问是否自动重试
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

    def run(self):
        self.stop_flag = False

        self.output_signal.emit("", "output")
        self.output_signal.emit("=" * 56, "system")
        self.output_signal.emit("  开始提权 - 执行 preload", "info")
        self.output_signal.emit("=" * 56, "system")

        # 检查设备连接
        self.status_signal.emit("正在检查设备...")
        if not check_device_connected():
            self.output_signal.emit("  [错误] 未检测到已连接的设备", "error")
            self.output_signal.emit("  请确保设备已通过 USB 连接并开启 USB 调试", "warning")
            self.failure_signal.emit()
            self.finished_signal.emit()
            return

        device_model = get_device_model()
        self.output_signal.emit(f"  设备型号: {device_model}", "device")

        # 执行 preload
        self.status_signal.emit("正在执行提权命令...")
        self.output_signal.emit("", "output")
        self.output_signal.emit("  正在执行提权命令...", "info")
        self.output_signal.emit("$ adb shell /data/local/tmp/preload", "command")
        self.output_signal.emit("", "output")

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
                # 非阻塞读取
                try:
                    readable, _, _ = select.select([self.process.stdout], [], [], 0.5)
                except (ValueError, OSError):
                    break

                if readable:
                    line_bytes = self.process.stdout.readline()
                    if not line_bytes:
                        # 进程可能已结束
                        if self.process.poll() is not None:
                            break
                        continue

                    try:
                        line = line_bytes.decode('utf-8', errors='replace').rstrip('\r\n')
                    except Exception:
                        line = str(line_bytes)

                    if line.strip():
                        self.output_signal.emit(line, "output")

                    # 检测 root 提示符 (设备代号 + #)
                    # 典型格式: "quest3:/ #" 或 "quest3:/data/local/tmp #"
                    if self._is_root_prompt(line):
                        root_detected = True
                        self._stdin_pipe = self.process.stdin
                        self.output_signal.emit("", "output")
                        self.output_signal.emit("=" * 56, "system")
                        self.output_signal.emit("  >>> 已成功提权! <<<", "success")
                        self.output_signal.emit(f"  检测到 Root Shell: {line.strip()}", "success")
                        self.output_signal.emit("=" * 56, "system")
                        self.status_signal.emit("提权成功")
                        self.success_signal.emit()

                        # 保持 shell 活跃，继续读取输出
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
                                try:
                                    line = line_bytes.decode('utf-8',
                                        errors='replace').rstrip('\r\n')
                                except Exception:
                                    line = str(line_bytes)
                                if line.strip():
                                    self.output_signal.emit(line, "output")
                            elif self.process.poll() is not None:
                                break
                        break

                # 检查进程是否已结束
                if self.process.poll() is not None:
                    # 读取剩余输出
                    remaining = self.process.stdout.read()
                    if remaining:
                        for line in remaining.decode('utf-8', errors='replace').split('\n'):
                            if line.strip():
                                self.output_signal.emit(line.rstrip(), "output")
                    break

                # 超时检测 (5分钟)
                elapsed = time.time() - start_time
                if elapsed > 300 and not root_detected:
                    self.output_signal.emit("  [警告] 提权超时 (5分钟)", "warning")
                    break

            if self.stop_flag:
                self.output_signal.emit("", "output")
                self.output_signal.emit("  已停止执行", "warning")
                self.finished_signal.emit()
                return

            if root_detected:
                # 成功已在上面处理
                pass
            else:
                # 检查设备是否断开
                self.output_signal.emit("", "output")
                if not check_device_connected():
                    self.output_signal.emit("  [错误] 设备已断开连接 (可能已重启)", "error")
                    self.output_signal.emit("  >>> 提权失败，请重新尝试 <<<", "error")
                    self.output_signal.emit("", "output")
                    self.status_signal.emit("提权失败")
                    self.failure_signal.emit()
                    self.need_auto_retry_signal.emit()
                else:
                    self.output_signal.emit("  [错误] 未检测到 Root 提示符", "error")
                    self.output_signal.emit("  >>> 提权失败，请重新尝试 <<<", "error")
                    self.output_signal.emit("", "output")
                    self.status_signal.emit("提权失败")
                    self.failure_signal.emit()
                    self.need_auto_retry_signal.emit()

        except FileNotFoundError:
            self.output_signal.emit("  [错误] 未找到 adb 命令", "error")
            self.failure_signal.emit()
            self.need_auto_retry_signal.emit()
        except Exception as e:
            self.output_signal.emit(f"  [错误] 执行异常: {str(e)}", "error")
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
        """检测是否为 root shell 提示符"""
        line = line.strip()
        if not line:
            return False
        # 匹配: "device_name:/path #" 或 "device_name:/ #"
        # 也可以是 "device_name:/path # " 等
        patterns = [
            r'^[\w.\-]+:[^\s]*\s*#\s*$',          # quest3:/ #
            r'^[\w.\-]+:[^\s]*\s*#\s*$',           # quest3:/data/local/tmp #
            r'^[\w.\-]+:\s*/\s*#\s*$',             # quest3: / #
        ]
        for pat in patterns:
            if re.match(pat, line):
                return True
        # 简单检测: 行以 # 结尾且包含冒号
        if line.endswith('#') and ':' in line and len(line) < 60:
            # 确保不是路径中的 #
            if not line.startswith('#') and '://' not in line:
                return True
        return False

    def send_to_shell(self, command):
        """向 root shell 发送命令"""
        if self._stdin_pipe and not self._stdin_pipe.closed:
            try:
                self._stdin_pipe.write((command + '\n').encode('utf-8'))
                self._stdin_pipe.flush()
                return True
            except Exception:
                return False
        return False


class AutoRetryWorker(QThread):
    """自动重试 - 循环执行 开始执行 + 开始提权 直到成功"""
    output_signal = pyqtSignal(str, str)
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

            # === 阶段1: 执行 (文件检查 + reboot + 推送) ===
            self.status_signal.emit(f"自动提权 - 第{self.attempt}次: 执行中...")
            self.emit_output("", "output")
            self.emit_output(f"--- [自动] 阶段1: 开始执行 ---", "info")

            success = self._run_execute_phase()
            if self.stop_flag:
                self.emit_output("  自动提权已停止", "warning")
                self.finished_signal.emit()
                return
            if not success:
                self.emit_output(f"  第 {self.attempt} 次尝试 - 执行阶段失败，2秒后重试...", "warning")
                time.sleep(2)
                continue

            # === 阶段2: 提权 ===
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
                self.emit_output(f"  第 {self.attempt} 次尝试 - 提权失败，2秒后重试...", "warning")
                time.sleep(2)

        self.emit_output("  自动提权已停止", "warning")
        self.finished_signal.emit()

    def _run_execute_phase(self):
        """执行阶段"""
        # 检查文件
        preload_path = os.path.join(os.getcwd(), "preload")
        ionstack_path = os.path.join(os.getcwd(), "ionstack.conf")

        if not os.path.isfile(preload_path) or not os.path.isfile(ionstack_path):
            self.emit_output("  [错误] 缺少 preload 或 ionstack.conf 文件", "error")
            return False

        # 检查设备
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

        # adb reboot
        self.emit_output("  正在重启设备...", "info")
        self.emit_output("$ adb reboot", "command")
        run_adb_command(['adb', 'reboot'], timeout=15)

        # 等待断开
        wait = 0
        while not self.stop_flag and wait < 30:
            if not check_device_connected():
                break
            time.sleep(1)
            wait += 1

        # 等待重连
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

        # 稳定性检查 (10秒)
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
                # 重新开始检查
                self.emit_output("  重新开始稳定性检查...", "system")
                stable = True
                for j in range(10):
                    if self.stop_flag:
                        return False
                    if not check_device_connected():
                        stable = False
                        break
                    if j < 9:
                        time.sleep(1)
                if not stable:
                    self.emit_output("  [错误] 连接不稳定", "error")
                    return False
                break
            if i < 9:
                time.sleep(1)

        self.emit_output("  [OK] 连接稳定", "success")

        # 推送文件
        self.emit_output("$ adb push preload /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'push', preload_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output(f"  [错误] 推送 preload 失败", "error")
            return False
        self.emit_output("  [OK] preload 推送成功", "success")

        time.sleep(0.3)

        self.emit_output("$ adb push ionstack.conf /data/local/tmp/", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'push', ionstack_path, '/data/local/tmp/'], timeout=30)
        if rc != 0:
            self.emit_output(f"  [错误] 推送 ionstack.conf 失败", "error")
            return False
        self.emit_output("  [OK] ionstack.conf 推送成功", "success")

        time.sleep(0.3)

        self.emit_output("$ adb shell chmod +x /data/local/tmp/preload", "command")
        stdout, stderr, rc = run_adb_command(
            ['adb', 'shell', 'chmod', '+x', '/data/local/tmp/preload'], timeout=10)
        if rc != 0:
            self.emit_output(f"  [错误] chmod 失败", "error")
            return False
        self.emit_output("  [OK] 权限设置成功", "success")
        self.emit_output("  [OK] 执行阶段完成", "success")
        return True

    def _run_root_phase(self):
        """提权阶段"""
        if not check_device_connected():
            self.emit_output("  [错误] 设备未连接", "error")
            return False

        self.emit_output("  正在执行提权命令...", "info")
        self.emit_output("$ adb shell /data/local/tmp/preload", "command")

        try:
            process = subprocess.Popen(
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
                    readable, _, _ = select.select([process.stdout], [], [], 0.5)
                except (ValueError, OSError):
                    break

                if readable:
                    line_bytes = process.stdout.readline()
                    if not line_bytes:
                        if process.poll() is not None:
                            break
                        continue

                    try:
                        line = line_bytes.decode('utf-8', errors='replace').rstrip('\r\n')
                    except Exception:
                        line = str(line_bytes)

                    if line.strip():
                        self.emit_output(line, "output")

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
                        for line in remaining.decode('utf-8', errors='replace').split('\n'):
                            if line.strip():
                                self.emit_output(line.rstrip(), "output")
                    break

                if time.time() - start_time > 300:
                    self.emit_output("  [警告] 提权超时", "warning")
                    break

            if self.stop_flag:
                try:
                    process.terminate()
                except Exception:
                    pass
                return False

            if root_detected:
                return True
            else:
                if not check_device_connected():
                    self.emit_output("  [错误] 设备已断开 (可能已重启)", "error")
                else:
                    self.emit_output("  [错误] 未检测到 Root 提示符", "error")
                return False

        except Exception as e:
            self.emit_output(f"  [错误] 执行异常: {str(e)}", "error")
            return False

    def _is_root_prompt(self, line):
        """检测是否为 root shell 提示符"""
        line = line.strip()
        if not line:
            return False
        patterns = [
            r'^[\w.\-]+:[^\s]*\s*#\s*$',
        ]
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
    finished_signal = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def run(self):
        self.output_signal.emit(f"$ {self.command}", "command")
        try:
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                bufsize=0,
                cwd=os.getcwd()
            )

            while not self.stop_flag:
                try:
                    readable, _, _ = select.select([process.stdout], [], [], 0.3)
                except (ValueError, OSError):
                    break

                if readable:
                    line_bytes = process.stdout.readline()
                    if not line_bytes:
                        if process.poll() is not None:
                            break
                        continue
                    try:
                        line = line_bytes.decode('utf-8', errors='replace').rstrip('\r\n')
                    except Exception:
                        line = str(line_bytes)
                    self.output_signal.emit(line, "output")
                elif process.poll() is not None:
                    break

            if self.stop_flag:
                try:
                    process.terminate()
                except Exception:
                    pass
                self.output_signal.emit("^C (已中断)", "warning")
            else:
                rc = process.poll()
                if rc and rc != 0:
                    self.output_signal.emit(f"(退出码: {rc})", "system")

        except Exception as e:
            self.output_signal.emit(f"错误: {str(e)}", "error")

        self.finished_signal.emit()


# ==================== 终端会话组件 ====================
class TerminalSession(QWidget):
    """单个终端会话 - 包含输出区、输入框、按钮"""

    def __init__(self, session_id=1, parent=None):
        super().__init__(parent)
        self.session_id = session_id
        self.setObjectName("terminalSession")

        # 工作线程
        self.execute_worker = None
        self.root_worker = None
        self.auto_retry_worker = None
        self.command_worker = None
        self.active_root_shell = None  # RootWorker 引用 (用于交互式 shell)

        self._init_ui()
        self._connect_signals()

        # 欢迎信息
        self._print_welcome()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # ---- 工具栏 ----
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbarFrame")
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(12, 8, 12, 8)
        toolbar_layout.setSpacing(10)

        self.execute_btn = QPushButton("▶  开始执行")
        self.execute_btn.setObjectName("executeBtn")
        self.execute_btn.setCursor(Qt.PointingHandCursor)
        self.execute_btn.setToolTip("检查文件 → adb reboot → 等待重连 → 推送文件")

        self.root_btn = QPushButton("⚡  开始提权")
        self.root_btn.setObjectName("rootBtn")
        self.root_btn.setCursor(Qt.PointingHandCursor)
        self.root_btn.setToolTip("执行 /data/local/tmp/preload 进行 Root 提权")

        self.stop_btn = QPushButton("■  停止")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setToolTip("停止当前正在执行的任务")

        toolbar_layout.addWidget(self.execute_btn)
        toolbar_layout.addWidget(self.root_btn)
        toolbar_layout.addWidget(self.stop_btn)
        toolbar_layout.addStretch()

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setObjectName("statusLabel")
        toolbar_layout.addWidget(self.status_label)

        layout.addWidget(toolbar_frame)

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
        self.input_box.setPlaceholderText("输入 ADB 命令或其他命令，按 Enter 执行... (如: adb devices)")
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

    def _print_welcome(self):
        self._append_output("╔══════════════════════════════════════════════════════════╗", "system")
        self._append_output("║        Quest3/3s 临时 Root 提权工具  v1.0               ║", "info")
        self._append_output("╠══════════════════════════════════════════════════════════╣", "system")
        self._append_output("║  [开始执行] 检查文件 → 重启设备 → 推送文件              ║", "system")
        self._append_output("║  [开始提权] 执行 preload → 检测 Root Shell             ║", "system")
        self._append_output("║  [停止]     终止当前任务 / 自动重试                    ║", "system")
        self._append_output("╚══════════════════════════════════════════════════════════╝", "system")
        self._append_output("", "output")
        self._append_output("  使用说明:", "info")
        self._append_output("    1. 将 preload 和 ionstack.conf 放在程序运行目录", "system")
        self._append_output("    2. 连接 Quest3/3s 设备 (USB 调试已开启)", "system")
        self._append_output("    3. 点击「开始执行」推送文件", "system")
        self._append_output("    4. 点击「开始提权」获取临时 Root", "system")
        self._append_output("    5. 在底部输入框可输入任意命令执行", "system")
        self._append_output("", "output")
        self._append_output(f"  当前工作目录: {os.getcwd()}", "system")
        self._append_output("", "output")

    def _append_output(self, text, color_type="output"):
        """向终端追加彩色输出"""
        color = COLORS.get(color_type, COLORS["output"])
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))

        # 添加时间戳
        timestamp = time.strftime("%H:%M:%S")
        if text.strip():
            cursor.insertText(f"[{timestamp}] ", fmt)

        cursor.insertText(text + "\n", fmt)

        # 自动滚动到底部
        self.terminal.setTextCursor(cursor)
        sb = self.terminal.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _set_buttons_state(self, executing=False):
        """设置按钮状态"""
        self.execute_btn.setEnabled(not executing)
        self.root_btn.setEnabled(not executing)
        self.stop_btn.setEnabled(executing)

    def _on_execute_clicked(self):
        """开始执行"""
        if self.execute_worker and self.execute_worker.isRunning():
            return
        self._set_buttons_state(True)
        self.execute_worker = ExecuteWorker()
        self.execute_worker.output_signal.connect(self._append_output)
        self.execute_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"状态: {s}"))
        self.execute_worker.finished_signal.connect(
            lambda success: self._on_execute_finished(success))
        self.execute_worker.start()

    def _on_execute_finished(self, success):
        self._set_buttons_state(False)
        if success:
            self.status_label.setText("状态: 执行完成")
        else:
            self.status_label.setText("状态: 执行失败")

    def _on_root_clicked(self):
        """开始提权"""
        if self.root_worker and self.root_worker.isRunning():
            return

        # 检查设备连接
        if not check_device_connected():
            self._append_output("  [警告] 当前未检测到已连接的设备", "warning")
            self._append_output("  请先连接设备并执行「开始执行」", "warning")
            return

        self._set_buttons_state(True)
        self.root_worker = RootWorker()
        self.root_worker.output_signal.connect(self._append_output)
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

    def _show_auto_retry_dialog(self):
        """显示自动重试对话框"""
        # 在主线程中显示对话框
        QTimer.singleShot(0, self._show_retry_popup)

    def _show_retry_popup(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("提权失败")
        msg.setIcon(QMessageBox.Warning)
        msg.setText("提权失败，请重新尝试")
        msg.setInformativeText("是否自动提权无需手动？\n\n"
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
        """启动自动重试"""
        self._append_output("", "output")
        self._append_output("  正在启动自动提权模式...", "warning")
        self._set_buttons_state(True)
        self.stop_btn.setEnabled(True)

        self.auto_retry_worker = AutoRetryWorker()
        self.auto_retry_worker.output_signal.connect(self._append_output)
        self.auto_retry_worker.status_signal.connect(
            lambda s: self.status_label.setText(f"状态: {s}"))
        self.auto_retry_worker.success_signal.connect(self._on_auto_retry_success)
        self.auto_retry_worker.finished_signal.connect(self._on_auto_retry_finished)
        self.auto_retry_worker.start()

    def _on_auto_retry_success(self):
        self.status_label.setText("状态: 自动提权成功")

    def _on_auto_retry_finished(self):
        self._set_buttons_state(False)

    def _on_stop_clicked(self):
        """停止执行"""
        stopped = False

        if self.execute_worker and self.execute_worker.isRunning():
            self.execute_worker.stop()
            stopped = True

        if self.root_worker and self.root_worker.isRunning():
            self.root_worker.stop()
            stopped = True

        if self.auto_retry_worker and self.auto_retry_worker.isRunning():
            self.auto_retry_worker.stop()
            stopped = True

        if self.command_worker and self.command_worker.isRunning():
            self.command_worker.stop()
            stopped = True

        if stopped:
            self._append_output("", "output")
            self._append_output("  [停止] 正在停止当前任务...", "warning")
            self.status_label.setText("状态: 已停止")
        else:
            self._append_output("  当前没有正在运行的任务", "system")

        self._set_buttons_state(False)

    def _on_input_enter(self):
        """输入框回车 - 执行命令"""
        command = self.input_box.text().strip()
        if not command:
            return

        # 如果有活跃的 root shell，发送命令到 shell
        if self.active_root_shell and self.active_root_shell._stdin_pipe:
            if not self.active_root_shell._stdin_pipe.closed:
                self._append_output(f"# {command}", "command")
                if self.active_root_shell.send_to_shell(command):
                    self.input_box.clear()
                    return
            else:
                self.active_root_shell = None
                self._append_output("  Root Shell 已关闭，使用普通命令执行", "system")

        # 普通命令执行
        if self.command_worker and self.command_worker.isRunning():
            self._append_output("  [警告] 上一个命令仍在执行中", "warning")
            return

        self.input_box.clear()
        self.command_worker = CommandWorker(command)
        self.command_worker.output_signal.connect(self._append_output)
        self.command_worker.finished_signal.connect(
            lambda: self.status_label.setText("状态: 就绪"))
        self.command_worker.start()

    def is_busy(self):
        """检查是否有任务正在运行"""
        workers = [self.execute_worker, self.root_worker,
                   self.auto_retry_worker, self.command_worker]
        return any(w and w.isRunning() for w in workers)

    def cleanup(self):
        """清理所有线程"""
        for worker in [self.execute_worker, self.root_worker,
                       self.auto_retry_worker, self.command_worker]:
            if worker and worker.isRunning():
                worker.stop()
                worker.wait(3000)


# ==================== 主窗口 ====================
class MainWindow(QMainWindow):
    """主窗口 - 管理多个终端会话标签页"""

    def __init__(self):
        super().__init__()
        self.session_count = 0
        self._init_ui()
        self._add_session()  # 默认创建第一个会话

    def _init_ui(self):
        self.setWindowTitle("Quest3/3s 临时 Root 提权工具 v1.0")
        self.setMinimumSize(900, 650)
        self.resize(960, 700)

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # ---- 顶部标题栏 ----
        header_frame = QFrame()
        header_frame.setObjectName("toolbarFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 10, 16, 10)
        header_layout.setSpacing(12)

        title = QLabel("⚡ Quest3/3s Root Tool")
        title.setObjectName("titleLogo")

        subtitle = QLabel("一键提取临时 Root  |  ADB 终端工具")
        subtitle.setObjectName("subtitle")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()

        # 新建会话按钮
        self.new_session_btn = QPushButton("＋ 新建会话")
        self.new_session_btn.setObjectName("newSessionBtn")
        self.new_session_btn.setCursor(Qt.PointingHandCursor)
        self.new_session_btn.setToolTip("创建新的终端会话")
        self.new_session_btn.clicked.connect(self._add_session)

        header_layout.addWidget(self.new_session_btn)

        main_layout.addWidget(header_frame)

        # ---- 标签页区域 ----
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_session)

        main_layout.addWidget(self.tab_widget, stretch=1)

        # ---- 底部状态栏 ----
        footer_frame = QFrame()
        footer_frame.setObjectName("statusFrame")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(12, 6, 12, 6)

        self.global_status = QLabel("就绪  |  工作目录: " + os.getcwd())
        self.global_status.setObjectName("statusLabel")
        footer_layout.addWidget(self.global_status)
        footer_layout.addStretch()

        adb_status = QLabel("ADB: " + ("已安装" if self._check_adb() else "未安装"))
        adb_status.setObjectName("statusLabel")
        footer_layout.addWidget(adb_status)

        main_layout.addWidget(footer_frame)

    def _check_adb(self):
        """检查 adb 是否可用"""
        try:
            result = subprocess.run(['adb', 'version'], capture_output=True, timeout=5)
            return result.returncode == 0
        except Exception:
            return False

    def _add_session(self):
        """创建新会话"""
        self.session_count += 1
        session = TerminalSession(session_id=self.session_count)
        self.tab_widget.addTab(session, f"  会话 {self.session_count}  ")
        self.tab_widget.setCurrentWidget(session)
        session.input_box.setFocus()

    def _close_session(self, index):
        """关闭会话"""
        if self.tab_widget.count() <= 1:
            # 至少保留一个会话
            self._add_session()

        widget = self.tab_widget.widget(index)
        if widget:
            if isinstance(widget, TerminalSession) and widget.is_busy():
                reply = QMessageBox.question(
                    self, "确认关闭",
                    "该会话有任务正在运行，确定要关闭吗？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return
            if isinstance(widget, TerminalSession):
                widget.cleanup()
            self.tab_widget.removeTab(index)
            widget.deleteLater()

    def closeEvent(self, event):
        """窗口关闭时清理所有线程"""
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, TerminalSession):
                widget.cleanup()
        event.accept()


# ==================== 入口 ====================
def main():
    # 设置高 DPI 支持
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
