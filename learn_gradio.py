'''
demo:该脚本使用Gradio创建一个简单的Web界面,展示如何动态添加和显示日志信息。
'''

import time
from datetime import datetime
import pandas as pd
import gradio as gr

df = pd.DataFrame({
    "A" : [14, 4, 5, 4, 1], 
    "B" : [5, 2, 54, 3, 2], 
    "C" : [20, 20, 7, 3, 8], 
    "D" : [14, 3, 6, 2, 6], 
    "E" : [23, 45, 64, 32, 23]
})

def add_log(new_message, history_logs):
    """添加新日志到历史记录中"""
    # 生成带时间戳的日志
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_log = f"[{timestamp}] {new_message}\n"

    # 合并新日志和历史日志
    updated_logs = history_logs + formatted_log

    # 返回更新后的日志（用于显示）和更新后的历史记录（用于状态保存）
    return updated_logs, updated_logs

def clear_logs():
    """清空所有日志"""
    return "", ""

def simulate_process(history_logs):
    """模拟一个过程，动态添加日志"""
    # 初始日志
    logs = history_logs + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 程序开始运行...\n"
    yield logs, logs
    time.sleep(1)

    # 处理中日志
    logs = logs + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在处理数据...\n"
    yield logs, logs
    time.sleep(2)

    # 完成日志
    logs = logs + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 数据处理完成\n"
    yield logs, logs
    time.sleep(1)

    # 结束日志
    logs = logs + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 程序运行结束\n"
    yield logs, logs

# Customize theme
theme = gr.themes.Soft().set(
    shadow_drop='3px 3px 7px 0 rgb(0 0 0 / 0.7)',
    shadow_drop_lg='5px 5px 11px 0 rgb(0 0 0 / 0.7)',
    block_shadow='*shadow_drop_lg',
    block_shadow_dark='*shadow_drop_lg',
)


# Customize 1. body background, 2. table style via CSS
CSS = """
.gradio-container { background-image: linear-gradient(135deg, #415f6e, #81D8CF); }
.dataframe {background-color: gray; box-shadow: 5px 5px 11px 0 rgb(0 0 0 / 0.7);}
"""

with gr.Blocks(theme=theme, title="动态日志展示", css=CSS) as demo:
    gr.Markdown("# 动态日志展示示例")

    # 状态变量用于保存历史日志
    log_history = gr.State("")
    with gr.Row():
        # 日志显示文本框
        log_display = gr.Textbox(
            label="日志输出",
            lines=16,
            max_lines=16,
            interactive=False
        )
        file_list1 = gr.FileExplorer(
            file_count="single",
            root_dir="./notebooks", glob="*.ipynb", label='上传PDF',
            max_height=400, min_height=400)
        # 定时刷新组件

    with gr.Row():
        # 输入新日志的文本框
        new_log_input = gr.Textbox(
            label="添加新日志",
            placeholder="输入要添加的日志信息..."
        )
        with gr.Column():
            # 手动添加日志按钮
            add_button = gr.Button("添加日志", variant="primary")
            # 模拟程序运行按钮（自动添加日志）
            simulate_button = gr.Button("模拟程序运行", variant="secondary")

    # 清空日志按钮
    clear_button = gr.Button("清空日志", variant="secondary")
    table = gr.Dataframe(df, label="数据预览", interactive=False, elem_classes="dataframe")


    # 绑定事件
    add_button.click(
        fn=add_log,
        inputs=[new_log_input, log_history],
        outputs=[log_display, log_history]
    )

    clear_button.click(
        fn=clear_logs,
        inputs=[],
        outputs=[log_display, log_history]
    )

    simulate_button.click(
        fn=simulate_process,
        inputs=[log_history],
        outputs=[log_display, log_history]
    )
# end demo

def main():
    """启动Gradio应用"""
    demo.launch(server_name="0.0.0.0")

if __name__ == "__main__":
    main()
