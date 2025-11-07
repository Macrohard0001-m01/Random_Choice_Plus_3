# pipe_sender.py
import win32pipe
import win32file
import win32api
import sys

def send_pipe_message(pipe_name, message, timeout=5000):
    """
    向命名管道发送消息
    
    参数:
        pipe_name: 管道名称 (如: r'\\.\pipe\MyAppPipe')
        message: 要发送的消息字符串
        timeout: 超时时间(毫秒)
    
    返回:
        bool: 是否发送成功
        str: 服务器响应
    """
    try:
        print(f"尝试连接到管道: {pipe_name}")
        print(f"发送消息: {message}")
        
        # 连接到管道
        pipe_handle = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,  # 不共享
            None,  # 默认安全属性
            win32file.OPEN_EXISTING,  # 必须已存在
            0,  # 默认属性
            None  # 不指定模板文件
        )
        
        print("管道连接成功")
        
        # 设置管道模式
        win32pipe.SetNamedPipeHandleState(
            pipe_handle,
            win32pipe.PIPE_READMODE_MESSAGE,
            None, None
        )
        
        # 发送消息
        message_bytes = message.encode('utf-8')
        win32file.WriteFile(pipe_handle, message_bytes)
        print("消息发送成功")
        
        # 读取响应
        result, data = win32file.ReadFile(pipe_handle, 4096)
        response = data.decode('utf-8')
        print(f"服务器响应: {response}")
        
        # 关闭管道
        win32file.CloseHandle(pipe_handle)
        
        return True, response
        
    except Exception as e:
        error_code = win32api.GetLastError()
        print(f"发送消息失败，错误代码: {error_code}, 错误: {e}")
        return False, str(e)

# 使用示例
if __name__ == "__main__":
    # 示例用法
    pipe_name = r'\\.\pipe\RandomCallPlusPipe'
    
    if len(sys.argv) > 1:
        message = sys.argv[1]
    else:
        message = "SHOW_WINDOW"  # 默认消息
    
    success, response = send_pipe_message(pipe_name, message)
    
    if success:
        print(f"✓ 消息发送成功: {message}")
        print(f"✓ 服务器响应: {response}")
    else:
        print(f"✗ 消息发送失败: {message}")