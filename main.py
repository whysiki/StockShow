import os
from pathlib import Path
from app import app


def open_index_html():
    """打开 index.html 文件"""
    script_dir = Path(__file__).parent
    index_file = script_dir / "index.html"
    if index_file.exists():
        # 根据操作系统选择打开命令
        if os.name == "nt":  # Windows
            os.system(f"start {index_file}")
        elif os.name == "posix":  # macOS/Linux
            os.system(f"open {index_file}")
        else:
            print("Unsupported OS. Please open the file manually.")
    else:
        print("index.html not found.")


if __name__ == "__main__":

    open_index_html()  # 打开 index.html 文件
    app.run(debug=False, port=5000, use_reloader=False)  # 启动 Flask 应用
