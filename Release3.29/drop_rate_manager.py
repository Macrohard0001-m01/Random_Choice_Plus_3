import json
import os
from datetime import datetime, timedelta

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

# 全局实例
drop_rate_manager = DropRateManager()