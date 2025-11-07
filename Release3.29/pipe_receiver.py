# pipe_receiver.py
import win32pipe
import win32file
import threading
import time
import sys

class PipeReceiver:
    def __init__(self, pipe_name, message_handler=None):
        """
        命名管道接收端
        
        参数:
            pipe_name: 管道名称
            message_handler: 消息处理函数，接收(message)参数，返回响应字符串
        """
        self.pipe_name = pipe_name
        self.message_handler = message_handler or self.default_message_handler
        self.running = False
        self.thread = None
        
    def default_message_handler(self, message):
        """默认消息处理函数"""
        print(f"收到消息: {message}")
        return f"已处理: {message}"
    
    def start(self):
        """启动管道服务器"""
        if self.running:
            print("管道服务器已在运行")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._server_loop, daemon=True)
        self.thread.start()
        print(f"管道服务器已启动: {self.pipe_name}")
    
    def stop(self):
        """停止管道服务器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        print("管道服务器已停止")
    
    def _server_loop(self):
        """服务器主循环"""
        while self.running:
            try:
                # 创建命名管道
                pipe_handle = win32pipe.CreateNamedPipe(
                    self.pipe_name,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                    1,  # 最多1个实例
                    65536, 65536,  # 输入输出缓冲区
                    0,  # 默认超时
                    None  # 默认安全属性
                )
                
                print("等待客户端连接...")
                # 等待客户端连接
                win32pipe.ConnectNamedPipe(pipe_handle, None)
                print("客户端已连接")
                
                try:
                    # 读取消息
                    result, data = win32file.ReadFile(pipe_handle, 4096)
                    message = data.decode('utf-8').strip()
                    print(f"收到消息: {message}")
                    
                    # 处理消息
                    response = self.message_handler(message)
                    
                    # 发送响应
                    response_bytes = response.encode('utf-8')
                    win32file.WriteFile(pipe_handle, response_bytes)
                    print(f"发送响应: {response}")
                    
                except Exception as e:
                    print(f"处理消息时出错: {e}")
                    # 发送错误响应
                    try:
                        error_response = f"ERROR: {str(e)}"
                        win32file.WriteFile(pipe_handle, error_response.encode('utf-8'))
                    except:
                        pass
                finally:
                    # 断开连接
                    win32pipe.DisconnectNamedPipe(pipe_handle)
                    win32file.CloseHandle(pipe_handle)
                    
            except Exception as e:
                print(f"管道服务器错误: {e}")
                time.sleep(1)  # 出错时等待1秒再重试

# 使用示例
if __name__ == "__main__":
    # 自定义消息处理函数
    def custom_handler(message):
        print(f"自定义处理: {message}")
        
        if message == "SHOW_WINDOW":
            # 这里可以调用你的窗口恢复逻辑
            print("执行显示窗口操作")
            return "WINDOW_SHOWN"
        elif message == "GET_STATUS":
            return "RUNNING"
        elif message.startswith("ECHO:"):
            return message[5:]  # 回显消息
        else:
            return f"UNKNOWN_COMMAND: {message}"
    
    # 创建接收器
    pipe_name = r'\\.\pipe\RandomCallPlusPipe'
    receiver = PipeReceiver(pipe_name, custom_handler)
    
    try:
        # 启动服务器
        receiver.start()
        print("管道接收器已启动，按 Ctrl+C 停止...")
        
        # 保持运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n正在停止服务器...")
        receiver.stop()