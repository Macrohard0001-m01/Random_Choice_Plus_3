import time
import json
import os
from datetime import datetime, date

class ChooseManager:
    def __init__(self):
        self.history_file = "choose_history.json"
        self.today_file = "choose_today.json"
        self.load_history()
        self.load_today()
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history_data = json.load(f)
            else:
                self.history_data = {}
        except:
            self.history_data = {}
    
    def load_today(self):
        """加载今日记录"""
        today_str = str(date.today())
        try:
            if os.path.exists(self.today_file):
                with open(self.today_file, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
                    self.today_data = all_data.get(today_str, {})
            else:
                self.today_data = {}
        except:
            self.today_data = {}
    
    def save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def save_today(self):
        """保存今日记录"""
        today_str = str(date.today())
        try:
            all_data = {}
            if os.path.exists(self.today_file):
                with open(self.today_file, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
            all_data[today_str] = self.today_data
            with open(self.today_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def record_choice(self, name):
        """记录选择结果"""
        # 记录到历史
        if name in self.history_data:
            self.history_data[name] += 1
        else:
            self.history_data[name] = 1
        
        # 记录到今日
        if name in self.today_data:
            self.today_data[name] += 1
        else:
            self.today_data[name] = 1
        
        self.save_history()
        self.save_today()
    
    def get_choice_count(self, name, mode):
        """获取指定模式的点名次数"""
        if mode == "today_balance":
            return self.today_data.get(name, 0)
        elif mode in ["history_balance", "smart_balance"]:
            return self.history_data.get(name, 0)
        else:
            return 0
    
    def clear_history(self):
        """清空历史记录"""
        self.history_data = {}
        self.save_history()
    
    def clear_today(self):
        """清空今日记录"""
        self.today_data = {}
        self.save_today()
    
    def reset_all(self):
        """重置所有记录"""
        self.clear_history()
        self.clear_today()

# 全局实例
choose_manager = ChooseManager()