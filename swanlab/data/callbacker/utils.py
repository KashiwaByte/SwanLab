"""
@author: cunyue
@file: utils.py
@time: 2025/6/20 15:28
@description: 回调工具
"""

import os

from rich.text import Text

from swanlab.core_python import get_client
from swanlab.env import is_windows
from swanlab.log import swanlog
from swanlab.package import get_package_latest_version, get_package_version


def print_train_begin(run_dir: str = None):
    """
    训练开始时的打印信息
    :param run_dir: 运行目录
    """
    swanlog.debug("SwanLab Runtime has initialized")
    swanlog.debug("SwanLab will take over all the print information of the terminal from now on")
    swanlog.info("Tracking run with swanlab version " + get_package_version())
    local_path = Text(_fmt_windows_path(run_dir), "magenta bold")
    swanlog.info("Run data will be saved locally in", local_path)


def print_train_finish(run_name: str):
    """
    打印结束信息
    """
    swanlog.info("Experiment", Text(run_name, "yellow"), "has completed")


def print_watch(swanlog_dir):
    """
    watch命令提示打印
    :param swanlog_dir: swanlog目录
    """
    swanlog.info(
        "🌟 Run `",
        Text("swanlab watch {}".format(_fmt_windows_path(swanlog_dir)), "bold"),
        "` to view SwanLab Experiment Dashboard locally",
        sep="",
    )


def print_sync(run_dir: str):
    """
    提示用户可以通过命令上传日志到远程服务器
    """
    swanlog.info(
        " ☁️ Run `",
        Text("swanlab sync {}".format(_fmt_windows_path(run_dir))),
        "` to sync logs to remote server",
        sep="",
    )


def _fmt_windows_path(path: str) -> str:
    """这主要针对windows环境，输入的绝对路径可能不包含盘符，这里进行补充
    主要是用于打印效果
    如果不是windows环境，直接返回path，相当于没有调用这个函数

    Parameters
    ----------
    path : str
        待转换的路径

    Returns
    -------
    str
        增加了盘符的路径
    """
    if not is_windows():
        return path
    if not os.path.isabs(path):
        return path
    need_add = len(path) < 3 or path[1] != ":"
    # 处理反斜杠, 保证路径的正确性
    path = path.replace("/", "\\")
    if need_add:
        return os.path.join(os.getcwd()[:2], path)
    return path


def check_latest_version():
    """
    获取指定包的最新版本号
    """
    latest_version = get_package_latest_version()
    local_version = get_package_version()
    if latest_version is not None and latest_version != local_version:
        swanlog.info(f"swanlab version {latest_version} is available!  Upgrade: `pip install -U swanlab`")


def print_cloud_web():
    """
    显示云端实验的链接
    """
    http = get_client()
    proj_url, exp_url = http.web_proj_url, http.web_exp_url
    swanlog.info("🏠 View project at", Text(proj_url, "blue underline"))
    swanlog.info("🚀 View run at", Text(exp_url, "blue underline"))
    return exp_url


def show_button_html(experiment_url):
    """
    用于在jupyter前端显示云端的环境iframe和按钮
    :param experiment_url: 实验链接
    """
    try:
        # noinspection PyPackageRequirements
        from IPython.display import HTML, display

        iframe_h5 = f'<iframe src="{experiment_url}" width=100% height="600" frameborder="no"></iframe>'
        js_code = f"""
        <script>
            function showIframe() {{
                var iframeHtml = '{iframe_h5}';
                document.getElementById('iframeContainer').innerHTML = iframeHtml;
            }}
        </script>
        """

        total_h5 = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Show Iframe</title>
    {js_code}
</head>
<body>
    <style>
        .interactive-button {{
            display: flex;
            align-items: center;
            height: 36px;
            border: 0px;
            background-color: #2c8f63;
            color: white;
            padding: 10px 20px;
            transition: background-color 0.3s, transform 0.2s;
        }}

        .interactive-button:hover {{
            background-color: #5cab87;
            cursor: pointer;
        }}

        .interactive-button:active {{ background-color: #217952; transform: scale(0.96); }} </style> <br> <button 
        onclick="showIframe()" class="interactive-button"> <svg style="height: 16px; margin-right: 8px;" viewBox="0 0 
        46 46" fill="none"> <path d="M10.8439 21.1974C10.6414 21.2854 10.4477 21.3925 10.2655 21.5173L10.2069 
        21.5652C10.1839 21.58 10.1625 21.5969 10.1429 21.6159C6.29135 24.6118 4.22831 29.4416 5.32646 34.282C5.94656 
        37.0577 7.50461 39.5348 9.73801 41.2958C11.9714 43.0568 14.7436 43.994 17.5874 43.9495H18.0219C19.8864 
        43.8697 21.7087 43.3694 23.3526 42.486C24.9964 41.6026 26.4193 40.3589 27.5147 38.848C28.61 37.3371 29.3496 
        35.598 29.678 33.761C30.0065 31.9239 29.9153 30.0363 29.4112 28.2395C28.9181 26.4723 27.8919 24.8437 26.9937 
        23.2551C25.4158 20.4653 23.8343 17.6764 22.2492 14.8884C21.7801 14.0647 21.3057 13.2465 20.8419 
        12.4228C20.2315 11.3353 19.2746 10.1519 19.224 8.86183C19.1733 7.57176 20.2235 6.32701 21.5082 
        6.07912C23.9284 5.61801 25.0639 8.24078 25.0693 8.23812C25.363 8.94035 25.9123 9.50489 26.6063 
        9.81764C27.3002 10.1304 28.087 10.168 28.8077 9.92298C29.5283 9.67791 30.1291 9.1684 30.4885 8.49743C30.8479 
        7.82646 30.9392 7.04405 30.7439 6.30835C30.1514 4.37314 28.9133 2.69953 27.2363 1.56656C25.7615 0.511704 
        23.9847 -0.0372109 22.1719 0.00195984C20.9049 0.00893199 19.6532 0.27989 18.4967 0.797557C17.3402 1.31522 
        16.3043 2.06823 15.4551 3.00856C14.49 4.08707 13.7984 5.38193 13.4389 6.78385C13.0794 8.18576 13.0624 9.6536 
        13.3894 11.0635C13.52 11.593 13.6984 12.1095 13.9225 12.6067C14.5595 14.0514 15.4951 15.3681 16.284 
        16.7355C17.2525 18.4147 18.2209 20.0948 19.1893 21.7758C20.1578 23.4568 21.1351 25.1449 22.1213 
        26.8401C22.9209 28.2421 23.7925 29.4682 23.8805 31.1528C23.9175 32.0513 23.7682 32.9479 23.4419 
        33.7859C23.1156 34.6239 22.6194 35.3854 21.9845 36.0223C21.3496 36.6592 20.5897 37.1578 19.7527 
        37.4868C18.9157 37.8157 18.0196 37.9678 17.121 37.9336C14.0024 37.7923 11.6488 35.4814 11.1744 32.4588C10.58 
        28.6419 13.552 26.5469 13.552 26.5469C14.1782 26.1785 14.6497 25.5955 14.8791 24.906C15.1084 24.2166 15.0801 
        23.4673 14.7993 22.7971C14.5186 22.127 14.0044 21.5813 13.3521 21.2611C12.6998 20.941 11.9536 20.8682 11.2517 
        21.0561C11.1174 21.0939 10.9856 21.1402 10.8572 21.1947" fill="white" /> <path d="M42.8101 31.5968C42.8109 
        30.5198 42.7218 29.4445 42.5435 28.3823C42.2663 26.7069 41.7464 25.0808 41.0002 23.5552C40.5524 22.6463 
        39.9874 21.7374 39.1024 21.2417C38.6593 20.9919 38.1589 20.8617 37.6502 20.8639C37.1416 20.8661 36.6423 
        21.0006 36.2013 21.2541C35.7604 21.5077 35.393 21.8716 35.1352 22.3101C34.8775 22.7485 34.7382 23.2466 
        34.7312 23.7552C34.7072 24.8773 35.3149 25.8875 35.768 26.9217C36.5212 28.6453 36.8623 30.5208 36.7642 
        32.3993C36.6661 34.2777 36.1315 36.1075 35.2029 37.7433C35.146 37.8404 35.0952 37.941 35.051 38.0445C34.8623 
        38.4842 34.7635 38.9573 34.7605 39.4358C34.7802 40.1222 35.0356 40.7808 35.4835 41.3011C35.9315 41.8214 
        36.5449 42.1717 37.2207 42.2932C38.8759 42.589 40.1899 41.347 40.8856 39.9609C42.1643 37.3589 42.823 34.4961 
        42.8101 31.5968Z" fill="white" /> <path d="M28.2309 11.8938C28.1761 11.9043 28.1218 11.9176 28.0683 
        11.9338C27.9593 11.9642 27.8611 12.0249 27.7851 12.1088C27.7091 12.1928 27.6584 12.2965 27.6389 
        12.408C27.6193 12.5195 27.6318 12.6343 27.6748 12.7391C27.7178 12.8438 27.7895 12.9343 27.8818 
        12.9999C29.2375 14.0252 30.3809 15.3043 31.2482 16.7662C31.4838 17.1677 31.6888 17.5865 31.8612 
        18.0189C32.0052 18.3921 32.1971 18.8799 32.6822 18.8532C33.0607 18.8346 33.2153 18.512 33.3192 
        18.1895C33.8137 16.5125 33.9678 14.7534 33.7723 13.0159C33.6331 12.0693 33.4155 11.1359 33.122 
        10.2252C33.0775 10.0047 32.9744 9.80029 32.8235 9.6335C32.7273 9.54627 32.6054 9.49262 32.4761 9.4806C32.3468 
        9.46859 32.2171 9.49886 32.1065 9.56687C32.0016 9.65188 31.9115 9.75365 31.8399 9.86806C31.3956 10.4658 
        30.825 10.9581 30.1687 11.3101C29.8377 11.4861 29.4893 11.6272 29.1292 11.7312C28.828 11.8192 28.5215 11.8325 
        28.2309 11.8938Z" fill="white" /> </svg> Display SwanLab Board </button> <br> <div 
        id="iframeContainer"></div> </body> </html>"""

        display(HTML(total_h5))
    except ImportError:
        pass
