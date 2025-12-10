# 随机点名Plus 3 - 智能点名助手

一个基于PyGame开发的课堂点名工具，支持多种点名模式和概率调整，帮助教师实现公平高效的点名

![软件截图](https://github.com/user-attachments/assets/9441861e-0761-40be-93e7-a53a8b0b6509)

---

## 📊 Star History

[![Star History Chart](https://starchart.cc/Macrohard0001/Random_Choice_Plus_3.svg)

---

## ✨ 核心功能

### 🎯 点名模式
- **简单随机**：纯随机点名，可能重复
- **单次不重复**：一轮内不重复点名
- **历史不重复**：避免重复点到历史中被点过的人
- **智能平衡**：根据历史记录自动调整概率
- **今日平衡**：优先选择今日未被点到的学生

### ⚙️ 概率系统
- 可手动调整单个学生的"中奖概率"
- 支持自动根据点名历史调整概率
- 手动配置优先级高于自动计算

### 🎨 界面特性
- 响应式布局，适配不同屏幕尺寸
- 简洁直观的界面设计
- 支持全屏/窗口模式切换
- 右上角显示实时时钟

### 🔄 工作模式
- 主窗口模式：完整的点名界面
- 悬浮按钮模式：最小化为系统托盘按钮
- 休眠模式：闲置后自动进入低功耗状态

---

## 🚀 快速开始

### 环境要求
```bash
Python 3.7 或更高版本
Windows 系统（推荐 Windows 10/11）
```

### 安装步骤
1. 安装依赖库：
```bash
pip install pygame pywin32 PyQt5 chardet
```

2. 准备学生名单：
   - 编辑 `name.txt` 文件，每行一个学生姓名
   - 如需排除某些学生，可编辑 `name_except.txt`

3. 运行程序：
```bash
python plus_main.pyw
```
或直接双击 `plus_main.pyw` 文件

---

## 📁 文件结构

```
random_chooser_plus/
├── plus_main.pyw              # 主程序入口
├── config.ini                 # 配置文件
├── name.txt                   # 学生名单
├── name_except.txt            # 排除名单
├── drop_rates.json           # 爆率配置文件
├── choose_history.json       # 点名历史记录
├── choose_today.json         # 今日点名记录
├── config_editor.py          # 可视化配置编辑器
├── requirements.txt          # 依赖库列表
├── README.md                # 说明文档
└── images/                  # 图片资源文件夹
    ├── 14.ico              # 程序图标
    ├── backgrounds/        # 背景图片
    └── buttons/           # 按钮图标
```

### 主要模块说明
- **`plus_main.pyw`**：程序主入口，负责窗口管理和事件处理
- **`choice_logic.py`**：包含各种点名算法的核心逻辑
- **`choose_manager.py`**：管理点名历史和统计数据
- **`drop_rate_manager.py`**：管理学生的点名概率
- **`config_editor.py`**：PyQt5编写的图形化配置编辑器
- **`animation.py`**：点名动画效果
- **`sleep.py`**：休眠模式实现
- **`pack_up.py`**：悬浮按钮功能

---

## ⚙️ 配置说明

### 主要配置项
```ini
[chooser]
choose_mode = smart_balance      # 点名模式
balance_weight = 0.7            # 平衡算法权重
enable_drop_rate = True         # 是否启用爆率调整
use_manual_override = True      # 是否使用手动配置覆盖自动计算

[Basic]
message_time_length = 5         # 消息显示时间（秒）
use_random_bg = True           # 是否使用随机背景

[sleep]
sleep_time_delay = 30          # 休眠等待时间（秒）
```

### 点名模式详解
| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `repeat` | 纯随机点名，可重复 | 快速提问，不关心重复 |
| `single_no_repeat` | 单轮不重复 | 小组活动，确保每人一次 |
| `history_no_repeat` | 历史不重复 | 长期课程，避免重复点名 |
| `today_balance` | 今日平衡 | 当天课程，平衡点名次数 |
| `history_balance` | 历史平衡 | 整个学期，平衡总体次数 |
| `smart_balance` | 智能平衡 | 综合考虑今日和历史 |

---

## 🔧 使用技巧

### 基础使用
1. **启动程序**：双击 `plus_main.pyw`
2. **开始点名**：点击界面中的"抽选"按钮
3. **查看结果**：屏幕中央显示被点到的学生
4. **重置名单**：名单用完后点击"重置"按钮恢复

### 高级功能
1. **调整概率**：
   - 运行 `python config_editor.py` 打开配置编辑器
   - 在"点名设置"标签页中点击"编辑爆率配置"
   - 可单独设置每个学生的点名概率

2. **悬浮模式**：
   - 点击退出界面中的"收起"按钮
   - 程序会最小化为悬浮按钮
   - 点击悬浮按钮可快速恢复窗口
  ** 注意：打包后此功能可能存在bug **

3. **休眠唤醒**：
   - 程序闲置30秒后自动进入休眠
   - 点击休眠界面的任意位置唤醒
   - 休眠界面显示当前时间和唤醒提示

### 数据管理
- **查看历史**：配置编辑器中可查看点名历史记录
- **重置数据**：可单独重置今日记录或全部历史
- **导出名单**：学生名单为纯文本格式，便于编辑

---

## 🐛 常见问题

### 启动问题
**Q: 程序无法启动，提示缺少模块**
A: 请确保已安装所有依赖：
```bash
pip install pygame pywin32 PyQt5 chardet
```

**Q: 找不到学生名单**
A: 确保项目目录下有 `name.txt` 文件，且文件编码为UTF-8或GBK

### 使用问题
**Q: 点名时没有动画效果**
A: 检查配置文件中的 `animation = True` 设置

**Q: 概率调整没有生效**
A: 确保配置中 `enable_drop_rate = True` 且 `use_manual_override = True`

**Q: 窗口最小化后找不到**
A: 程序可能已打包为悬浮按钮，检查系统托盘区

### 性能问题
**Q: 程序运行卡顿**
A: 可尝试降低动画速度、关闭随机背景功能或者降低fps（Pygame的软件渲染就是sh*t）

---

## 📈 版本更新

### 当前版本：v3.30
- 优化文件结构，合并部分重复代码
- 改进智能爆率控制算法
- 修复配置文件编码问题
- 增强点名平衡逻辑

### 历史版本亮点
- **v3.29**：修复初始化加载问题
- **v3.28**：修复最大化窗口还原问题
- **v3.27**：优化点名均衡算法
- **v3.26**：增加独立配置编辑器
- **v3.25**：增加点名平衡逻辑
- **v3.24**：新增休眠界面

查看完整更新日志请参考 `updatelog.txt`

---

## 🤝 参与贡献

欢迎提交Issue反馈问题或提出改进建议：

1. **问题反馈**：描述具体问题和复现步骤
2. **功能建议**：说明需求场景和预期效果
3. **代码贡献**：Fork项目后提交Pull Request

### 联系开发者

- 📧 邮箱：Macrohard0001_m01@outlook.com
- 🐛 GitHub Issues：[提交问题](https://github.com/Macrohard0001/Random_Choice_Plus_3/issues)

---

## 关于新项目（Random_Choice_Plus_4）
- 我正在用Pygame + ModernGL构建一个极轻量的渲染引擎[Awesome_OpenGL_Render_Engine](https://github.com/Macrohard0001/Awesome_OpenGL_Render_Engine)
- 新项目RCP_4 （还没创建库……/(ㄒoㄒ)/~~）

---

##我正在寻求合作伙伴，有意者请联系Macrohard0001_m01@outlook.com 或直接加入我的组织Macrohard_Studio

---

## 📄 许可证

本项目采用 巨硬简易许可证 开源。允许用于个人用途，但需保留原版权声明；商用需授权；转载请注明来源。

### 免责声明

本软件仅供教学辅助使用，开发者不对因使用本软件造成的任何直接或间接损失负责。

---

**开发者：** Macrohard0001  
**文档最后更新：** 2025年12月10日  
**项目状态：** 稳定可用，持续维护中
