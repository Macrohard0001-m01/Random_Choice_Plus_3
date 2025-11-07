import sys
import os
import configparser
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QTabWidget, QGroupBox, QLabel, QLineEdit, 
                             QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox, 
                             QPushButton, QTextEdit, QMessageBox, QFileDialog,
                             QScrollArea, QGridLayout, QDialog, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QDialogButtonBox,
                             QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

version=2.0

class DropRateManager:
    def __init__(self):
        self.auto_rates = {}  # 自动计算的爆率
        self.manual_rates = {}  # 手动修改的爆率
        self.history_records = []  # 历史记录
        self.auto_file = "drop_rates_auto.json"
        self.manual_file = "drop_rates_manual.json"
        self.history_file = "draw_history.json"
        self.load_all_data()
    
    def load_all_data(self):
        """加载所有数据"""
        # 加载自动爆率
        try:
            if os.path.exists(self.auto_file):
                with open(self.auto_file, 'r', encoding='utf-8') as f:
                    self.auto_rates = json.load(f)
        except:
            self.auto_rates = {}
        
        # 加载手动爆率
        try:
            if os.path.exists(self.manual_file):
                with open(self.manual_file, 'r', encoding='utf-8') as f:
                    self.manual_rates = json.load(f)
        except:
            self.manual_rates = {}
        
        # 加载历史记录
        self.load_history()
        
        # 基于历史记录重新计算自动爆率
        self.recalculate_auto_rates()
        self.save_auto_rates()
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.history_records = data
                    else:
                        self.history_records = []
        except:
            self.history_records = []
    
    def save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_records, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def recalculate_auto_rates(self):
        """基于历史记录重新计算自动爆率"""
        if not self.history_records:
            return
        
        # 分析历史记录
        name_stats = {}
        total_draws = len(self.history_records)
        
        for record in self.history_records:
            name = record.get('name', '')
            if name:
                if name not in name_stats:
                    name_stats[name] = {'count': 0, 'recent_count': 0}
                name_stats[name]['count'] += 1
        
        # 计算最近7天的点名次数（如果记录中有时间信息）
        seven_days_ago = datetime.now() - timedelta(days=7)
        for record in self.history_records:
            record_time = record.get('timestamp', '')
            if record_time:
                try:
                    record_date = datetime.fromisoformat(record_time)
                    if record_date >= seven_days_ago:
                        name = record.get('name', '')
                        if name in name_stats:
                            name_stats[name]['recent_count'] += 1
                except:
                    pass
        
        # 重新计算自动爆率
        for name, stats in name_stats.items():
            # 智能算法：被点名越多，爆率越低
            total_count = stats['count']
            recent_count = stats.get('recent_count', total_count)
            
            # 基础惩罚（基于总次数）
            base_penalty = min(0.6, total_count * 0.05)  # 每次点名降低5%爆率
            
            # 近期惩罚（基于最近7天次数）
            recent_penalty = min(0.3, recent_count * 0.1)  # 近期点名更重的惩罚
            
            # 计算新爆率
            new_rate = max(0.1, 1.0 - base_penalty - recent_penalty)  # 最低10%
            
            # 只在没有手动配置时更新自动配置
            if name not in self.manual_rates:
                self.auto_rates[name] = round(new_rate, 2)
    
    def save_auto_rates(self):
        """保存自动爆率"""
        try:
            with open(self.auto_file, 'w', encoding='utf-8') as f:
                json.dump(self.auto_rates, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def save_manual_rates(self):
        """保存手动爆率"""
        try:
            with open(self.manual_file, 'w', encoding='utf-8') as f:
                json.dump(self.manual_rates, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def get_drop_rate(self, name, use_manual_override=True):
        """获取爆率（优先使用手动配置）"""
        if use_manual_override and name in self.manual_rates:
            return self.manual_rates[name]
        return self.auto_rates.get(name, 1.0)
    
    def set_drop_rate(self, name, rate, is_manual=True):
        """设置爆率"""
        try:
            rate = float(rate)
            if rate < 0:
                rate = 0.0
            elif rate > 1:
                rate = 1.0
            
            if is_manual:
                self.manual_rates[name] = round(rate, 2)
                return self.save_manual_rates()
            else:
                # 只有在没有手动配置时才更新自动配置
                if name not in self.manual_rates:
                    self.auto_rates[name] = round(rate, 2)
                    return self.save_auto_rates()
                return True
        except:
            return False
    
    def reset_drop_rate(self, name):
        """重置单个爆率（删除手动配置）"""
        if name in self.manual_rates:
            del self.manual_rates[name]
            return self.save_manual_rates()
        return False
    
    def reset_all_manual_rates(self):
        """重置所有手动爆率"""
        self.manual_rates = {}
        return self.save_manual_rates()
    
    def reset_all_auto_rates(self):
        """重置所有自动爆率"""
        self.auto_rates = {}
        return self.save_auto_rates()
    
    def reset_today_history(self):
        """重置当天历史记录"""
        today = datetime.now().date()
        self.history_records = [
            record for record in self.history_records
            if datetime.fromisoformat(record.get('timestamp', '2000-01-01')).date() != today
        ]
        return self.save_history()
    
    def reset_all_history(self):
        """重置所有历史记录"""
        self.history_records = []
        return self.save_history()
    
    def get_all_drop_rates(self):
        """获取所有爆率配置（合并手动和自动）"""
        all_rates = self.auto_rates.copy()
        all_rates.update(self.manual_rates)
        return all_rates
    
    def get_manual_rates(self):
        """获取所有手动爆率"""
        return self.manual_rates.copy()
    
    def get_auto_rates(self):
        """获取所有自动爆率"""
        return self.auto_rates.copy()
    
    def get_history_records(self):
        """获取历史记录"""
        return self.history_records.copy()
    
    def add_history_record(self, name, timestamp=None):
        """添加历史记录"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        record = {
            'name': name,
            'timestamp': timestamp
        }
        self.history_records.append(record)
        self.save_history()
        
        # 重新计算自动爆率
        self.recalculate_auto_rates()
        self.save_auto_rates()
    
    def update_from_list(self, name_list):
        """根据名单更新自动爆率配置（不覆盖手动修改）"""
        updated = False
        new_names = []
        for name in name_list:
            # 只有在没有手动配置时才更新自动配置
            if name not in self.manual_rates and name not in self.auto_rates:
                self.auto_rates[name] = 1.0
                new_names.append(name)
                updated = True
        
        if updated:
            self.save_auto_rates()
            return True, new_names
        return False, []

class DropRateEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("爆率配置编辑器 - 增强版")
        self.setGeometry(200, 200, 1000, 700)
        self.drop_rate_manager = DropRateManager()
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 说明标签
        info_label = QLabel("手动修改的爆率会覆盖自动配置。爆率范围：0.0 - 1.0 (0% - 100%)")
        layout.addWidget(info_label)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["姓名", "最终爆率", "自动爆率", "配置来源"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # 管理按钮区域
        management_group = QGroupBox("爆率管理")
        management_layout = QGridLayout(management_group)
        
        # 第一行按钮
        self.add_btn = QPushButton("添加手动配置")
        self.add_btn.clicked.connect(self.add_row)
        management_layout.addWidget(self.add_btn, 0, 0)
        
        self.delete_btn = QPushButton("删除选中")
        self.delete_btn.clicked.connect(self.delete_selected)
        management_layout.addWidget(self.delete_btn, 0, 1)
        
        self.reset_btn = QPushButton("重置选中")
        self.reset_btn.clicked.connect(self.reset_selected)
        management_layout.addWidget(self.reset_btn, 0, 2)
        
        # 第二行按钮
        self.recalculate_auto_btn = QPushButton("重新计算自动爆率")
        self.recalculate_auto_btn.clicked.connect(self.recalculate_auto_rates)
        management_layout.addWidget(self.recalculate_auto_btn, 1, 0)
        
        self.view_auto_rates_btn = QPushButton("查看自动爆率")
        self.view_auto_rates_btn.clicked.connect(self.view_auto_rates)
        management_layout.addWidget(self.view_auto_rates_btn, 1, 1)
        
        self.view_history_btn = QPushButton("查看历史记录")
        self.view_history_btn.clicked.connect(self.view_history)
        management_layout.addWidget(self.view_history_btn, 1, 2)
        
        # 第三行按钮
        self.reset_today_history_btn = QPushButton("重置当天历史")
        self.reset_today_history_btn.clicked.connect(self.reset_today_history)
        management_layout.addWidget(self.reset_today_history_btn, 2, 0)
        
        self.reset_all_history_btn = QPushButton("重置全部历史")
        self.reset_all_history_btn.clicked.connect(self.reset_all_history)
        management_layout.addWidget(self.reset_all_history_btn, 2, 1)
        
        self.reset_auto_rates_btn = QPushButton("重置自动爆率")
        self.reset_auto_rates_btn.clicked.connect(self.reset_auto_rates)
        management_layout.addWidget(self.reset_auto_rates_btn, 2, 2)
        
        # 第四行按钮
        self.reset_manual_rates_btn = QPushButton("重置手动爆率")
        self.reset_manual_rates_btn.clicked.connect(self.reset_manual_rates)
        management_layout.addWidget(self.reset_manual_rates_btn, 3, 0)
        
        management_layout.addWidget(QLabel("历史记录总数:"), 3, 1)
        self.history_count_label = QLabel("0")
        management_layout.addWidget(self.history_count_label, 3, 2)
        
        layout.addWidget(management_group)
        
        # 确定取消按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def load_data(self):
        all_rates = self.drop_rate_manager.get_all_drop_rates()
        manual_rates = self.drop_rate_manager.get_manual_rates()
        auto_rates = self.drop_rate_manager.get_auto_rates()
        history_records = self.drop_rate_manager.get_history_records()
        
        self.history_count_label.setText(str(len(history_records)))
        self.table.setRowCount(len(all_rates))
        
        for row, (name, final_rate) in enumerate(sorted(all_rates.items())):
            # 姓名
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)
            
            # 最终爆率（可编辑）
            final_rate_item = QTableWidgetItem(f"{final_rate:.2f}")
            self.table.setItem(row, 1, final_rate_item)
            
            # 自动爆率（只读）
            auto_rate = auto_rates.get(name, 1.0)
            auto_rate_item = QTableWidgetItem(f"{auto_rate:.2f}")
            auto_rate_item.setFlags(auto_rate_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, auto_rate_item)
            
            # 配置来源
            source = "手动" if name in manual_rates else "自动"
            source_item = QTableWidgetItem(source)
            source_item.setFlags(source_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, source_item)
    
    def add_row(self):
        """添加新行"""
        name, ok = QInputDialog.getText(self, "添加名字", "请输入姓名:")
        if ok and name:
            # 检查是否已存在
            for row in range(self.table.rowCount()):
                if self.table.item(row, 0).text() == name:
                    QMessageBox.warning(self, "重复", f"名字 {name} 已存在!")
                    return
            
            # 添加新行
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)
            
            final_rate_item = QTableWidgetItem("1.00")
            self.table.setItem(row, 1, final_rate_item)
            
            auto_rate_item = QTableWidgetItem("1.00")
            auto_rate_item.setFlags(auto_rate_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, auto_rate_item)
            
            source_item = QTableWidgetItem("手动")
            source_item.setFlags(source_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, source_item)
    
    def delete_selected(self):
        """删除选中行"""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要删除的行!")
            return
        
        # 从后往前删除，避免索引变化
        for row in sorted(selected_rows, reverse=True):
            name = self.table.item(row, 0).text()
            self.drop_rate_manager.reset_drop_rate(name)
            self.table.removeRow(row)
    
    def reset_selected(self):
        """重置选中行的爆率"""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要重置的行!")
            return
        
        for row in selected_rows:
            name = self.table.item(row, 0).text()
            self.drop_rate_manager.reset_drop_rate(name)
            # 重新加载数据以显示更新后的自动爆率
            self.load_data()
    
    def recalculate_auto_rates(self):
        """重新计算自动爆率"""
        reply = QMessageBox.question(self, "确认重新计算", 
                                   "确定要基于历史记录重新计算自动爆率吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.drop_rate_manager.recalculate_auto_rates()
            self.drop_rate_manager.save_auto_rates()
            self.load_data()
            QMessageBox.information(self, "成功", "自动爆率重新计算完成！")
    
    def view_auto_rates(self):
        """查看自动爆率"""
        auto_rates = self.drop_rate_manager.get_auto_rates()
        if not auto_rates:
            QMessageBox.information(self, "自动爆率", "暂无自动爆率配置")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("自动爆率配置")
        dialog.setGeometry(300, 300, 400, 500)
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = "自动爆率配置（基于历史记录计算）:\n\n"
        for name, rate in sorted(auto_rates.items()):
            content += f"{name}: {rate:.2f}\n"
        
        text_edit.setText(content)
        layout.addWidget(text_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec_()
    
    def view_history(self):
        """查看历史记录"""
        history_records = self.drop_rate_manager.get_history_records()
        if not history_records:
            QMessageBox.information(self, "历史记录", "暂无历史记录")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("点名历史记录")
        dialog.setGeometry(300, 300, 500, 600)
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = f"历史记录总数: {len(history_records)}\n\n"
        
        # 按时间倒序排列
        sorted_records = sorted(history_records, 
                              key=lambda x: x.get('timestamp', ''), 
                              reverse=True)
        
        for record in sorted_records[:100]:  # 显示最近100条
            name = record.get('name', '未知')
            timestamp = record.get('timestamp', '未知时间')
            content += f"{timestamp}: {name}\n"
        
        if len(sorted_records) > 100:
            content += f"\n... 还有 {len(sorted_records) - 100} 条记录"
        
        text_edit.setText(content)
        layout.addWidget(text_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec_()
    
    def reset_today_history(self):
        """重置当天历史记录"""
        reply = QMessageBox.question(self, "确认重置", 
                                   "确定要重置今天的历史记录吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.drop_rate_manager.reset_today_history():
                self.load_data()
                QMessageBox.information(self, "成功", "当天历史记录已重置！")
            else:
                QMessageBox.warning(self, "错误", "重置当天历史记录失败！")
    
    def reset_all_history(self):
        """重置所有历史记录"""
        reply = QMessageBox.question(self, "确认重置", 
                                   "确定要重置所有历史记录吗？\n这将影响自动爆率计算！",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.drop_rate_manager.reset_all_history():
                self.load_data()
                QMessageBox.information(self, "成功", "所有历史记录已重置！")
            else:
                QMessageBox.warning(self, "错误", "重置历史记录失败！")
    
    def reset_auto_rates(self):
        """重置自动爆率"""
        reply = QMessageBox.question(self, "确认重置", 
                                   "确定要重置所有自动爆率吗？\n所有名字将恢复为100%爆率！",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.drop_rate_manager.reset_all_auto_rates():
                self.load_data()
                QMessageBox.information(self, "成功", "自动爆率已重置！")
            else:
                QMessageBox.warning(self, "错误", "重置自动爆率失败！")
    
    def reset_manual_rates(self):
        """重置手动爆率"""
        reply = QMessageBox.question(self, "确认重置", 
                                   "确定要重置所有手动爆率吗？\n将恢复为自动爆率配置！",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.drop_rate_manager.reset_all_manual_rates():
                self.load_data()
                QMessageBox.information(self, "成功", "手动爆率已重置！")
            else:
                QMessageBox.warning(self, "错误", "重置手动爆率失败！")
    
    def accept(self):
        """保存修改"""
        try:
            # 保存所有手动修改
            for row in range(self.table.rowCount()):
                name = self.table.item(row, 0).text()
                rate_text = self.table.item(row, 1).text()
                source = self.table.item(row, 3).text()
                
                try:
                    rate = float(rate_text)
                    if rate < 0 or rate > 1:
                        QMessageBox.warning(self, "错误", f"爆率必须在 0.0 到 1.0 之间: {name}")
                        return
                    
                    # 如果是手动配置，保存到手动文件
                    if source == "手动":
                        self.drop_rate_manager.set_drop_rate(name, rate, is_manual=True)
                    # 如果是自动配置且被修改过，转为手动配置
                    elif source == "自动" and rate != 1.0:
                        self.drop_rate_manager.set_drop_rate(name, rate, is_manual=True)
                    
                except ValueError:
                    QMessageBox.warning(self, "错误", f"爆率格式错误: {name}")
                    return
            
            QMessageBox.information(self, "成功", "爆率配置保存成功!")
            super().accept()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")

class ConfigEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_file = "config.ini"
        self.config = configparser.ConfigParser()
        # 设置配置解析器保持大小写
        self.config.optionxform = str
        self.drop_rate_manager = DropRateManager()
        self.init_ui()
        self.load_config()
        
    def init_ui(self):
        self.setWindowTitle("随机点名Plus配置编辑器")
        self.setGeometry(100, 100, 900, 700)
        
        # 设置图标
        if os.path.exists("./images/14.ico"):
            self.setWindowIcon(QIcon("./images/14.ico"))
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # 创建各个配置页
        self.create_basic_tab()
        self.create_sleep_tab()
        self.create_advanced_tab()
        self.create_performance_tab()
        self.create_chooser_tab()
        self.create_developer_tab()
        
        # 底部按钮
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("保存配置")
        self.save_btn.clicked.connect(self.save_config)
        self.save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 14px; padding: 8px; }")
        
        self.reload_btn = QPushButton("重新加载")
        self.reload_btn.clicked.connect(self.load_config)
        self.reload_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-size: 14px; padding: 8px; }")
        
        self.reset_btn = QPushButton("重置为默认")
        self.reset_btn.clicked.connect(self.reset_to_default)
        self.reset_btn.setStyleSheet("QPushButton { background-color: #ff9800; color: white; font-size: 14px; padding: 8px; }")
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.reload_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
    def create_basic_tab(self):
        """创建基础设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 语言设置
        lang_group = QGroupBox("语言设置")
        lang_layout = QHBoxLayout(lang_group)
        lang_layout.addWidget(QLabel("默认语言:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Chinese", "English"])
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        # 窗口设置
        window_group = QGroupBox("窗口设置")
        window_layout = QGridLayout(window_group)
        
        window_layout.addWidget(QLabel("启动位置控制:"), 0, 0)
        self.start_pos_check = QCheckBox()
        window_layout.addWidget(self.start_pos_check, 0, 1)
        
        window_layout.addWidget(QLabel("启动位置:"), 1, 0)
        self.start_pos_edit = QLineEdit()
        window_layout.addWidget(self.start_pos_edit, 1, 1)
        
        window_layout.addWidget(QLabel("消息显示时间(秒):"), 2, 0)
        self.message_time_spin = QSpinBox()
        self.message_time_spin.setRange(1, 60)
        window_layout.addWidget(self.message_time_spin, 2, 1)
        
        # 背景设置
        bg_group = QGroupBox("背景设置")
        bg_layout = QGridLayout(bg_group)
        
        bg_layout.addWidget(QLabel("初始背景:"), 0, 0)
        self.init_bg_edit = QLineEdit()
        bg_layout.addWidget(self.init_bg_edit, 0, 1)
        self.init_bg_btn = QPushButton("浏览")
        self.init_bg_btn.clicked.connect(lambda: self.browse_file(self.init_bg_edit))
        bg_layout.addWidget(self.init_bg_btn, 0, 2)
        
        bg_layout.addWidget(QLabel("主背景:"), 1, 0)
        self.main_bg_edit = QLineEdit()
        bg_layout.addWidget(self.main_bg_edit, 1, 1)
        self.main_bg_btn = QPushButton("浏览")
        self.main_bg_btn.clicked.connect(lambda: self.browse_file(self.main_bg_edit))
        bg_layout.addWidget(self.main_bg_btn, 1, 2)
        
        bg_layout.addWidget(QLabel("使用随机背景:"), 2, 0)
        self.random_bg_check = QCheckBox()
        bg_layout.addWidget(self.random_bg_check, 2, 1)
        
        bg_layout.addWidget(QLabel("初始背景目录:"), 3, 0)
        self.init_bg_dir_edit = QLineEdit()
        bg_layout.addWidget(self.init_bg_dir_edit, 3, 1)
        self.init_bg_dir_btn = QPushButton("浏览")
        self.init_bg_dir_btn.clicked.connect(lambda: self.browse_directory(self.init_bg_dir_edit))
        bg_layout.addWidget(self.init_bg_dir_btn, 3, 2)
        
        bg_layout.addWidget(QLabel("主背景目录:"), 4, 0)
        self.main_bg_dir_edit = QLineEdit()
        bg_layout.addWidget(self.main_bg_dir_edit, 4, 1)
        self.main_bg_dir_btn = QPushButton("浏览")
        self.main_bg_dir_btn.clicked.connect(lambda: self.browse_directory(self.main_bg_dir_edit))
        bg_layout.addWidget(self.main_bg_dir_btn, 4, 2)
        
        layout.addWidget(lang_group)
        layout.addWidget(window_group)
        layout.addWidget(bg_group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "基础设置")
        
    def create_sleep_tab(self):
        """创建休眠设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        sleep_group = QGroupBox("休眠设置")
        sleep_layout = QGridLayout(sleep_group)
        
        sleep_layout.addWidget(QLabel("休眠背景透明度:"), 0, 0)
        self.sleep_alpha_spin = QSpinBox()
        self.sleep_alpha_spin.setRange(0, 255)
        sleep_layout.addWidget(self.sleep_alpha_spin, 0, 1)
        
        sleep_layout.addWidget(QLabel("休眠背景目录:"), 1, 0)
        self.sleep_bg_dir_edit = QLineEdit()
        sleep_layout.addWidget(self.sleep_bg_dir_edit, 1, 1)
        self.sleep_bg_dir_btn = QPushButton("浏览")
        self.sleep_bg_dir_btn.clicked.connect(lambda: self.browse_directory(self.sleep_bg_dir_edit))
        sleep_layout.addWidget(self.sleep_bg_dir_btn, 1, 2)
        
        sleep_layout.addWidget(QLabel("随机休眠背景:"), 2, 0)
        self.random_sleep_bg_check = QCheckBox()
        sleep_layout.addWidget(self.random_sleep_bg_check, 2, 1)
        
        sleep_layout.addWidget(QLabel("触摸延迟(秒):"), 3, 0)
        self.touch_delay_spin = QDoubleSpinBox()
        self.touch_delay_spin.setRange(0.1, 10.0)
        self.touch_delay_spin.setSingleStep(0.1)
        sleep_layout.addWidget(self.touch_delay_spin, 3, 1)
        
        sleep_layout.addWidget(QLabel("休眠延迟(秒):"), 4, 0)
        self.sleep_delay_spin = QSpinBox()
        self.sleep_delay_spin.setRange(10, 3600)
        sleep_layout.addWidget(self.sleep_delay_spin, 4, 1)
        
        sleep_layout.addWidget(QLabel("休眠FPS:"), 5, 0)
        self.sleep_fps_spin = QSpinBox()
        self.sleep_fps_spin.setRange(10, 240)
        sleep_layout.addWidget(self.sleep_fps_spin, 5, 1)
        
        layout.addWidget(sleep_group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "休眠设置")
        
    def create_advanced_tab(self):
        """创建高级设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        advanced_group = QGroupBox("高级设置")
        advanced_layout = QGridLayout(advanced_group)
        
        advanced_layout.addWidget(QLabel("屏幕尺寸:"), 0, 0)
        self.screen_size_edit = QLineEdit()
        advanced_layout.addWidget(self.screen_size_edit, 0, 1)
        
        advanced_layout.addWidget(QLabel("初始背景透明度:"), 1, 0)
        self.init_alpha_spin = QSpinBox()
        self.init_alpha_spin.setRange(0, 255)
        advanced_layout.addWidget(self.init_alpha_spin, 1, 1)
        
        layout.addWidget(advanced_group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "高级设置")
        
    def create_performance_tab(self):
        """创建性能设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        perf_group = QGroupBox("性能设置")
        perf_layout = QGridLayout(perf_group)
        
        perf_layout.addWidget(QLabel("启用动画:"), 0, 0)
        self.animation_check = QCheckBox()
        perf_layout.addWidget(self.animation_check, 0, 1)
        
        perf_layout.addWidget(QLabel("动画速度:"), 1, 0)
        self.animation_speed_spin = QSpinBox()
        self.animation_speed_spin.setRange(1, 10)
        perf_layout.addWidget(self.animation_speed_spin, 1, 1)
        
        perf_layout.addWidget(QLabel("初始FPS:"), 2, 0)
        self.init_fps_spin = QSpinBox()
        self.init_fps_spin.setRange(30, 240)
        perf_layout.addWidget(self.init_fps_spin, 2, 1)
        
        perf_layout.addWidget(QLabel("主FPS:"), 3, 0)
        self.main_fps_spin = QSpinBox()
        self.main_fps_spin.setRange(30, 240)
        perf_layout.addWidget(self.main_fps_spin, 3, 1)
        
        perf_layout.addWidget(QLabel("进度条速度:"), 4, 0)
        self.bar_speed_spin = QSpinBox()
        self.bar_speed_spin.setRange(1, 20)
        perf_layout.addWidget(self.bar_speed_spin, 4, 1)
        
        layout.addWidget(perf_group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "性能设置")
        
    def create_chooser_tab(self):
        """创建点名设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 文件设置
        file_group = QGroupBox("文件设置")
        file_layout = QGridLayout(file_group)
        
        file_layout.addWidget(QLabel("名单文件:"), 0, 0)
        self.name_file_edit = QLineEdit()
        file_layout.addWidget(self.name_file_edit, 0, 1)
        
        file_layout.addWidget(QLabel("排除名单:"), 1, 0)
        self.except_file_edit = QLineEdit()
        file_layout.addWidget(self.except_file_edit, 1, 1)
        
        file_layout.addWidget(QLabel("爆率文件:"), 2, 0)
        self.drop_rate_file_edit = QLineEdit()
        file_layout.addWidget(self.drop_rate_file_edit, 2, 1)
        
        # 点名模式
        mode_group = QGroupBox("点名模式")
        mode_layout = QGridLayout(mode_group)
        
        mode_layout.addWidget(QLabel("点名模式:"), 0, 0)
        self.choose_mode_combo = QComboBox()
        self.choose_mode_combo.addItems([
            "repeat - 重复点名",
            "single_no_repeat - 单次不重复", 
            "history_no_repeat - 历史不重复",
            "today_balance - 今日平衡",
            "history_balance - 历史平衡",
            "smart_balance - 智能平衡"
        ])
        mode_layout.addWidget(self.choose_mode_combo, 0, 1)
        
        # 新增：手动爆率覆盖选项
        mode_layout.addWidget(QLabel("使用手动爆率覆盖:"), 1, 0)
        self.use_manual_override_check = QCheckBox()
        mode_layout.addWidget(self.use_manual_override_check, 1, 1)
        
        mode_layout.addWidget(QLabel("平衡权重:"), 2, 0)
        self.balance_weight_spin = QDoubleSpinBox()
        self.balance_weight_spin.setRange(0.1, 1.0)
        self.balance_weight_spin.setSingleStep(0.1)
        mode_layout.addWidget(self.balance_weight_spin, 2, 1)
        
        mode_layout.addWidget(QLabel("智能敏感度:"), 3, 0)
        self.smart_sensitivity_spin = QDoubleSpinBox()
        self.smart_sensitivity_spin.setRange(0.1, 1.0)
        self.smart_sensitivity_spin.setSingleStep(0.1)
        mode_layout.addWidget(self.smart_sensitivity_spin, 3, 1)
        
        mode_layout.addWidget(QLabel("启用爆率调整:"), 4, 0)
        self.enable_drop_rate_check = QCheckBox()
        mode_layout.addWidget(self.enable_drop_rate_check, 4, 1)
        
        # 爆率管理按钮
        drop_rate_btn_layout = QHBoxLayout()
        self.edit_drop_rates_btn = QPushButton("编辑爆率配置")
        self.edit_drop_rates_btn.clicked.connect(self.edit_drop_rates)
        drop_rate_btn_layout.addWidget(self.edit_drop_rates_btn)
        
        self.update_drop_rates_btn = QPushButton("从名单更新爆率")
        self.update_drop_rates_btn.clicked.connect(self.update_drop_rates)
        drop_rate_btn_layout.addWidget(self.update_drop_rates_btn)
        
        mode_layout.addLayout(drop_rate_btn_layout, 5, 0, 1, 2)
        
        layout.addWidget(file_group)
        layout.addWidget(mode_group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "点名设置")
        
    def create_developer_tab(self):
        """创建开发者设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        dev_group = QGroupBox("开发者设置")
        dev_layout = QGridLayout(dev_group)
        
        dev_layout.addWidget(QLabel("图标路径:"), 0, 0)
        self.icon_path_edit = QLineEdit()
        dev_layout.addWidget(self.icon_path_edit, 0, 1)
        self.icon_path_btn = QPushButton("浏览")
        self.icon_path_btn.clicked.connect(lambda: self.browse_file(self.icon_path_edit))
        dev_layout.addWidget(self.icon_path_btn, 0, 2)
        
        dev_layout.addWidget(QLabel("字体:"), 1, 0)
        self.font_edit = QLineEdit()
        dev_layout.addWidget(self.font_edit, 1, 1)
        
        dev_layout.addWidget(QLabel("初始显示名字:"), 2, 0)
        self.first_name_edit = QLineEdit()
        dev_layout.addWidget(self.first_name_edit, 2, 1)
        
        dev_layout.addWidget(QLabel("欢迎消息:"), 3, 0)
        self.welcome_msg_edit = QTextEdit()
        self.welcome_msg_edit.setMaximumHeight(80)
        dev_layout.addWidget(self.welcome_msg_edit, 3, 1, 1, 2)
        
        layout.addWidget(dev_group)
        layout.addStretch()
        
        self.tabs.addTab(tab, "开发者设置")
        
    def browse_file(self, line_edit):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            line_edit.setText(file_path)
            
    def browse_directory(self, line_edit):
        """浏览目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择目录")
        if dir_path:
            line_edit.setText(dir_path)
            
    def load_config(self):
        """加载配置文件"""
        try:
            # 如果配置文件不存在，创建一个默认的
            if not os.path.exists(self.config_file):
                self.create_default_config()
                
            # 强制使用UTF-8编码读取配置文件
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config.read_file(f)
            
            self.load_config_to_ui()
            QMessageBox.information(self, "成功", "配置文件加载成功！")
            
        except UnicodeDecodeError:
            # 如果UTF-8读取失败，可能是其他编码，尝试GBK
            try:
                with open(self.config_file, 'r', encoding='gbk') as f:
                    self.config.read_file(f)
                # 重新加载到UI
                self.load_config_to_ui()
                QMessageBox.warning(self, "编码提示", "配置文件使用GBK编码，已成功加载。保存时将转换为UTF-8编码。")
            except:
                # 如果都失败，创建默认配置
                QMessageBox.critical(self, "错误", "配置文件编码无法识别，已创建默认配置。")
                self.create_default_config()
                self.load_config_to_ui()
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载配置文件失败：{str(e)}")
            # 创建默认配置
            self.create_default_config()
            self.load_config_to_ui()
    
    def load_config_to_ui(self):
        """将配置加载到UI界面"""
        # 基础设置
        self.language_combo.setCurrentText(self.config.get('Language', 'defult_language', fallback='Chinese'))
        self.start_pos_check.setChecked(self.config.getboolean('Basic', 'startwindowpositioncontrol', fallback=False))
        self.start_pos_edit.setText(self.config.get('Basic', 'startwindowposition', fallback='0,0'))
        self.message_time_spin.setValue(self.config.getint('Basic', 'message_time_length', fallback=5))
        self.init_bg_edit.setText(self.config.get('Basic', 'init_background', fallback='./images/backgrounds/--background.png'))
        self.main_bg_edit.setText(self.config.get('Basic', 'background_img', fallback='./images/backgrounds/background.png'))
        self.random_bg_check.setChecked(self.config.getboolean('Basic', 'use_random_bg', fallback=True))
        self.init_bg_dir_edit.setText(self.config.get('Basic', 'init_bg_directory', fallback='./images/backgrounds/init_bg'))
        self.main_bg_dir_edit.setText(self.config.get('Basic', 'main_bg_directory', fallback='./images/backgrounds/main_bg'))
        
        # 休眠设置
        self.sleep_alpha_spin.setValue(self.config.getint('sleep', 'sleep_background_alpha', fallback=190))
        self.sleep_bg_dir_edit.setText(self.config.get('sleep', 'sleep_bg_directory', fallback='./images/backgrounds/init_bg'))
        self.random_sleep_bg_check.setChecked(self.config.getboolean('sleep', 'random_sleep_bg', fallback=True))
        self.touch_delay_spin.setValue(self.config.getfloat('sleep', 'touch_delay', fallback=1.0))
        self.sleep_delay_spin.setValue(self.config.getint('sleep', 'sleep_time_delay', fallback=30))
        self.sleep_fps_spin.setValue(self.config.getint('sleep', 'sleepfps', fallback=60))
        
        # 高级设置
        self.screen_size_edit.setText(self.config.get('Advanced', 'screensize', fallback='(960,540)'))
        self.init_alpha_spin.setValue(self.config.getint('Advanced', 'init_background_alpha', fallback=175))
        
        # 性能设置
        self.animation_check.setChecked(self.config.getboolean('Xingneng', 'animation', fallback=True))
        self.animation_speed_spin.setValue(self.config.getint('Xingneng', 'animationspeed', fallback=5))
        self.init_fps_spin.setValue(self.config.getint('Xingneng', 'init_fps', fallback=120))
        self.main_fps_spin.setValue(self.config.getint('main_settings', 'fps', fallback=60))
        self.bar_speed_spin.setValue(self.config.getint('main_settings', 'barspeed', fallback=5))
        
        # 点名设置
        self.name_file_edit.setText(self.config.get('chooser', 'name_text', fallback='name.txt'))
        self.except_file_edit.setText(self.config.get('chooser', 'except_names', fallback='name_except.txt'))
        self.drop_rate_file_edit.setText(self.config.get('chooser', 'drop_rate_file', fallback='drop_rates.json'))
        
        mode = self.config.get('chooser', 'choose_mode', fallback='smart_balance')
        mode_index = {
            'repeat': 0, 'single_no_repeat': 1, 'history_no_repeat': 2,
            'today_balance': 3, 'history_balance': 4, 'smart_balance': 5
        }.get(mode, 5)
        self.choose_mode_combo.setCurrentIndex(mode_index)
        
        # 新增：手动爆率覆盖选项
        self.use_manual_override_check.setChecked(self.config.getboolean('chooser', 'use_manual_override', fallback=True))
        
        self.balance_weight_spin.setValue(self.config.getfloat('chooser', 'balance_weight', fallback=0.7))
        self.smart_sensitivity_spin.setValue(self.config.getfloat('chooser', 'smart_sensitivity', fallback=0.5))
        self.enable_drop_rate_check.setChecked(self.config.getboolean('chooser', 'enable_drop_rate', fallback=False))
        
        # 开发者设置
        self.icon_path_edit.setText(self.config.get('Developer', 'MHicon', fallback='./images/14.ico'))
        self.font_edit.setText(self.config.get('Developer', 'Font', fallback='MicrosoftYaHei UI'))
        self.first_name_edit.setText(self.config.get('Developer', 'firstdraw_lastname', fallback='?'))
        self.welcome_msg_edit.setText(self.config.get('Developer', 'welcomemessage', 
                                                     fallback='欢迎使用随机点名PLUS版，本软件由 Macrohard 开发，欢迎提交issue或汇报BUG'))
            
    def create_default_config(self):
        """创建默认配置文件"""
        # 清空现有配置
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        
        # 设置默认值
        self.config['Language'] = {'defult_language': 'Chinese'}
        self.config['Basic'] = {
            'startwindowpositioncontrol': 'False',
            'startwindowposition': '0,0',
            'init_background': './images/backgrounds/--background.png',
            'background_img': './images/backgrounds/background.png',
            'message_time_length': '5',
            'init_bg_directory': './images/backgrounds/init_bg',
            'main_bg_directory': './images/backgrounds/main_bg',
            'use_random_bg': 'True'
        }
        self.config['sleep'] = {
            'sleep_background_alpha': '190',
            'sleep_bg_directory': './images/backgrounds/init_bg',
            'random_sleep_bg': 'True',
            'touch_delay': '1.0',
            'sleep_time_delay': '30',
            'sleepfps': '60'
        }
        self.config['Advanced'] = {
            'screensize': '(960,540)',
            'init_background_alpha': '175'
        }
        self.config['Xingneng'] = {
            'animation': 'True',
            'animationspeed': '5',
            'init_fps': '120'
        }
        self.config['main_settings'] = {
            'fps': '60',
            'barspeed': '5'
        }
        self.config['chooser'] = {
            'name_text': 'name.txt',
            'except_names': 'name_except.txt',
            'choose_mode': 'smart_balance',
            'use_manual_override': 'True',  # 新增
            'balance_weight': '0.7',
            'smart_sensitivity': '0.5',
            'drop_rate_file': 'drop_rates.json',
            'enable_drop_rate': 'False'
        }
        self.config['Developer'] = {
            'MHicon': './images/14.ico',
            'Font': 'MicrosoftYaHei UI',
            'firstdraw_lastname': '?',
            'welcomemessage': '欢迎使用随机点名PLUS版，本软件由 Macrohard 开发，欢迎提交issue或汇报BUG'
        }
        
        # 保存默认配置
        self.save_config()
            
    def save_config(self):
        """保存配置文件"""
        try:
            # 基础设置
            self.config['Language'] = {
                'defult_language': self.language_combo.currentText()
            }
            
            self.config['Basic'] = {
                'startwindowpositioncontrol': str(self.start_pos_check.isChecked()),
                'startwindowposition': self.start_pos_edit.text(),
                'init_background': self.init_bg_edit.text(),
                'background_img': self.main_bg_edit.text(),
                'message_time_length': str(self.message_time_spin.value()),
                'init_bg_directory': self.init_bg_dir_edit.text(),
                'main_bg_directory': self.main_bg_dir_edit.text(),
                'use_random_bg': str(self.random_bg_check.isChecked())
            }
            
            # 休眠设置
            self.config['sleep'] = {
                'sleep_background_alpha': str(self.sleep_alpha_spin.value()),
                'sleep_bg_directory': self.sleep_bg_dir_edit.text(),
                'random_sleep_bg': str(self.random_sleep_bg_check.isChecked()),
                'touch_delay': str(self.touch_delay_spin.value()),
                'sleep_time_delay': str(self.sleep_delay_spin.value()),
                'sleepfps': str(self.sleep_fps_spin.value())
            }
            
            # 高级设置
            self.config['Advanced'] = {
                'screensize': self.screen_size_edit.text(),
                'init_background_alpha': str(self.init_alpha_spin.value())
            }
            
            # 性能设置
            self.config['Xingneng'] = {
                'animation': str(self.animation_check.isChecked()),
                'animationspeed': str(self.animation_speed_spin.value()),
                'init_fps': str(self.init_fps_spin.value())
            }
            
            self.config['main_settings'] = {
                'fps': str(self.main_fps_spin.value()),
                'barspeed': str(self.bar_speed_spin.value())
            }
            
            # 点名设置
            mode_map = {
                0: 'repeat', 1: 'single_no_repeat', 2: 'history_no_repeat',
                3: 'today_balance', 4: 'history_balance', 5: 'smart_balance'
            }
            
            self.config['chooser'] = {
                'name_text': self.name_file_edit.text(),
                'except_names': self.except_file_edit.text(),
                'choose_mode': mode_map[self.choose_mode_combo.currentIndex()],
                'use_manual_override': str(self.use_manual_override_check.isChecked()),  # 新增
                'balance_weight': str(self.balance_weight_spin.value()),
                'smart_sensitivity': str(self.smart_sensitivity_spin.value()),
                'drop_rate_file': self.drop_rate_file_edit.text(),
                'enable_drop_rate': str(self.enable_drop_rate_check.isChecked())
            }
            
            # 开发者设置
            self.config['Developer'] = {
                'MHicon': self.icon_path_edit.text(),
                'Font': self.font_edit.text(),
                'firstdraw_lastname': self.first_name_edit.text(),
                'welcomemessage': self.welcome_msg_edit.toPlainText()
            }
            
            # 强制使用UTF-8编码保存，覆盖原文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
                
            QMessageBox.information(self, "成功", "配置文件保存成功！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置文件失败：{str(e)}")
            
    def reset_to_default(self):
        """重置为默认值"""
        reply = QMessageBox.question(self, "确认重置", 
                                   "确定要重置所有设置为默认值吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.create_default_config()
            self.load_config_to_ui()
            
    def edit_drop_rates(self):
        """编辑爆率配置"""
        try:
            editor = DropRateEditor(self)
            if editor.exec_() == QDialog.Accepted:
                QMessageBox.information(self, "成功", "爆率配置已更新！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开爆率编辑器失败：{str(e)}")
        
    def update_drop_rates(self):
        """从名单更新爆率"""
        try:
            # 读取名单文件
            name_file = self.name_file_edit.text()
            if not os.path.exists(name_file):
                QMessageBox.warning(self, "错误", f"名单文件不存在：{name_file}")
                return
            
            # 尝试多种编码读取文件
            name_list = []
            encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'utf-16', 'latin-1']
            
            for encoding in encodings:
                try:
                    with open(name_file, 'r', encoding=encoding) as f:
                        name_list = [line.strip() for line in f if line.strip()]
                    if name_list:
                        print(f"成功使用 {encoding} 编码读取名单文件")
                        break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"{encoding} 编码读取失败: {e}")
                    continue
            
            # 如果还是失败，使用错误忽略模式
            if not name_list:
                try:
                    with open(name_file, 'r', encoding='utf-8', errors='ignore') as f:
                        name_list = [line.strip() for line in f if line.strip()]
                    print("使用错误忽略模式读取名单文件")
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"读取名单文件失败：{str(e)}")
                    return
            
            if not name_list:
                QMessageBox.warning(self, "错误", "名单文件为空或无法读取！")
                return
            
            # 更新爆率配置
            updated, new_names = self.drop_rate_manager.update_from_list(name_list)
            
            if updated:
                if new_names:
                    message = f"✅ 已根据名单更新爆率配置\n新增 {len(new_names)} 个名字：{', '.join(new_names[:3])}{'...' if len(new_names) > 3 else ''}"
                else:
                    message = "✅ 爆率配置已更新"
                QMessageBox.information(self, "成功", message)
            else:
                QMessageBox.information(self, "提示", "📝 爆率配置已是最新，无需更新")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"更新爆率配置失败：{str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    editor = ConfigEditor()
    editor.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()