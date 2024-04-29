import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def convert_hdr_to_sdr(input_file, output_file, output_dir):
  """将 HDR 视频转换为 SDR 视频。

  参数:
    input_file: 输入 HDR 视频文件的路径。
    output_file: 输出 SDR 视频文件的路径。
    output_dir: 存储输出 SDR 视频文件的目录。

  返回:
    无。
  """

  if not os.path.exists(input_file):
    print(f"输入文件不存在: {input_file}")
    return

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  command = [
  "ffmpeg", "-i", input_file,
  "-vf", "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0.0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p",
  "-c:v", "libx265", "-preset", "medium", "-x265-params",
  "colorprim=bt709:transfer=bt709:colormatrix=bt709",
  "-color_trc", "bt709", "-color_primaries", "bt709", "-colorspace", "bt709",
  "-movflags", "+faststart", "-pix_fmt", "yuv420p",
  output_file
  ]

  print(f'启动 FFmpeg，命令: {" ".join(command)}')
  try:
    subprocess.call(command)
  except Exception as e:
    print(f"视频转换失败: {e}")

def select_input_dir():
    """选择输入文件夹。"""
    input_dir = filedialog.askdirectory(title="选择输入文件夹")
    if input_dir:
        input_dir_entry.set(input_dir)

def select_output_dir():
    """选择输出文件夹。"""
    output_dir = filedialog.askdirectory(title="选择输出文件夹")
    if output_dir:
        output_dir_entry.set(output_dir)

def start_convert():
    """开始转换视频。"""
    input_dir = input_dir_entry.get()
    output_dir = output_dir_entry.get()
    if not input_dir or not output_dir:
        print("请输入输入和输出文件夹路径")
        return
    # 遍历 input_dir 目录中的所有文件
    for filename in os.listdir(input_dir):
        # 获取文件的绝对路径
        input_file = os.path.join(input_dir, filename)
        # 获取文件的扩展名
        ext = os.path.splitext(filename)[1]

        # 仅转换 HDR 视频文件
        if ext.lower() == ".mov":
            # 生成输出文件的名称
            base_filename = os.path.splitext(filename)[0]
            output_file = os.path.join(output_dir, base_filename + ".mp4")

            # 转换视频
            convert_hdr_to_sdr(input_file, output_file, output_dir)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("HDR 视频转 SDR 视频")

    # 创建输入文件夹标签和输入框
    input_dir_label = tk.Label(root, text="输入文件夹：")
    input_dir_entry = tk.Entry(root)

    # 创建输出文件夹标签和输入框
    output_dir_label = tk.Label(root, text="输出文件夹：")
    output_dir_entry = tk.Entry(root)

    # 创建选择输入文件夹按钮
    select_input_dir_button = tk.Button(root, text="选择", command=select_input_dir)

    # 创建选择输出文件夹按钮
    select_output_dir_button = tk.Button(root, text="选择", command=select_output_dir)

    # 创建开始按钮
    start_button = tk.Button(root, text="开始转换", command=start_convert)

    # 布局控件
    input_dir_label.grid(row=0, column=0)
    input_dir_entry.grid(row=0, column=1)
    select_input_dir_button.grid(row=0, column=2)

    output_dir_label.grid(row=1, column=0)
    output_dir_entry.grid(row=1, column=1)
    select_output_dir_button.grid(row=1, column=2)

    start_button.grid(row=2, column=1)

    root.mainloop()
