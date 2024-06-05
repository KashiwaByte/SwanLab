#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2023-12-02 13:23:42
@File: swanlab\utils\file.py
@IDE: vscode
@Description:
    文件操作
"""
import os
import re
import ujson
import yaml


# ---------------------------------- 一些格式检查的工具函数 ----------------------------------


def is_ipv4(string: str) -> bool:
    """判断字符串是否是一个ipv4地址

    Parameters
    ----------
    string : str
        待检查的字符串

    Returns
    -------
    bool
        如果是ipv4地址，返回True，否则返回False
    """
    pattern = re.compile(r"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$")
    return isinstance(string, str) and pattern.match(string)


def is_port(string: str) -> bool:
    """判断字符串是否是一个端口号

    Parameters
    ----------
    string : str
        待检查的字符串

    Returns
    -------
    bool
        如果是端口号，返回True，否则返回False
    """
    if not is_int(string):
        return False
    port = int(string)
    return 0 <= port <= 65535


def is_int(string: str) -> bool:
    """判断字符串是否可以转换为整数

    Parameters
    ----------
    string : str
        待检查的字符串

    Returns
    -------
    bool
        如果可以转换为整数，返回True，否则返回False
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def check_string(target: str) -> bool:
    """
    检查是否为字符串，且不能全空格，也不能为空字符串
    :param target: 待检查的字符串
    :return: bool
    :raises:
        :raise TypeError: name不是字符串
    """
    if not isinstance(target, str):
        raise TypeError(f"name: {target} is not a string: {type(target)}")
    # 利用正则表达式匹配非空格字符
    if re.match(r"^\s*$", target):
        return False
    # 利用正则表达式匹配非空字符串
    if re.match(r"^\s*$", target) or target == "":
        return False
    return True


def check_load_json_yaml(file_path: str, paramter_name: str = "init_path"):
    # 不是字符串
    if not isinstance(file_path, str):
        raise TypeError("{} must be a string, but got {}".format(paramter_name, type(file_path)))
    # 检查file_path的后缀是否是json/yaml，否则报错
    path_suffix = file_path.split(".")[-1]
    if not file_path.endswith((".json", ".yaml", ".yml")):
        raise ValueError(
            "{} must be a json or yaml file ('.json', '.yaml', '.yml'), but got {}, please check if the content of config_file is correct.".format(
                paramter_name, path_suffix
            )
        )
    # 转换为绝对路径
    file_path = os.path.abspath(file_path)
    # 读取配置文件
    # 如果文件不存在或者不是文件
    if (not os.path.exists(file_path)) or (not os.path.isfile(file_path)):
        raise FileNotFoundError("{} not found, please check if the file exists.".format(paramter_name))
    # 为空
    if os.path.getsize(file_path) == 0:
        raise ValueError("{} is empty, please check if the content of config_file is correct.".format(paramter_name))
    # 无权限读取
    if not os.access(file_path, os.R_OK):
        raise PermissionError(
            "No permission to read {}, please check if you have the permission.".format(paramter_name)
        )
    load = ujson.load if path_suffix == "json" else yaml.safe_load
    with open(file_path, "r") as f:
        # 读取配置文件的内容
        file_data = load(f)
        # 如果读取的内容不是字典类型，则报错
        if not isinstance(file_data, dict):
            raise TypeError("The configuration file must be a dictionary, but got {}".format(type(file_data)))
    return file_data


# ---------------------------------- 实验、项目相关 ----------------------------------


def _auto_cut(name: str, value: str, max_len: int, cut: bool) -> str:
    """
    检查长度
    :param name: 参数名称
    :param value: 参数值
    :param max_len: 最大长度
    :return: str 检查后的字符串
    :raises
        :raise IndexError: cut为False且name超出长度
    """
    if len(value) > max_len:
        if cut:
            value = value[:max_len]
        else:
            raise IndexError(f"Name: {name} is too long, which must be less than {max_len} characters")
    return value


def check_proj_name_format(name: str, auto_cut: bool = True) -> str:
    """
    检查项目名格式，必须是0-9a-zA-Z以及连字符(_-)
    最大长度为100个字符

    Parameters
    ----------
    name : str
        待检查的字符串
    auto_cut : bool, optional
        如果超出长度，是否自动截断，默认为True
        如果为False，则超出长度会抛出异常

    Returns
    -------
    str
        检查后的字符串

    Raises
    ------
    TypeError
        name不是字符串，或者name为空字符串
    ValueError
        name不符合规定格式
    IndexError
        name超出长度
    """
    max_len = 100
    if not check_string(name) or not re.match(r"^[0-9a-zA-Z_-]+$", name):
        raise ValueError(f"Project name `{name}` is invalid, which must be 0-9, a-z, A-Z, _ , -")
    name = name.strip()
    return _auto_cut("project", name, max_len, auto_cut)


def check_exp_name_format(name: str, auto_cut: bool = True) -> str:
    """
    检查实验名称格式，最大长度为100个字符，一个中文字符算一个字符
    其他不做限制，实验名称可以包含任何字符

    Parameters
    ----------
    name : str
        待检查的字符串
    auto_cut : bool, optional
        如果超出长度，是否自动截断，默认为True
        如果为False，则超出长度会抛出异常

    Returns
    -------
    str
        检查后的字符串

    Raises
    ------
    TypeError
        name不是字符串
    ValueError
        name为空字符串
    IndexError
        name超出长度
    """
    max_len = 100
    if not check_string(name):
        raise ValueError(f"Experiment name `{name}` is an empty string.")
    # 检查长度
    return _auto_cut("experiment", name, max_len, auto_cut)


def check_desc_format(description: str, auto_cut: bool = True):
    """检查实验描述
    不能超过255个字符，可以包含任何字符

    Parameters
    ----------
    description : str
        需要检查和处理的描述信息
    auto_cut : bool
        如果超出长度，是否裁剪并抛弃多余部分

    Returns
    -------
    str
        检查后的字符串，同时会去除字符串头尾的空格

    Raises
    ------
    IndexError
        name超出长度
    """
    max_length = 255
    check_string(description)
    description = description.strip()
    return _auto_cut("description", description, max_length, auto_cut)


def check_key_format(key: str, auto_cut=True) -> str:
    """检查key字符串格式
    不能超过255个字符，可以包含任何字符，不允许.和/以及空格开头

    Parameters
    ----------
    key : str
        待检查的字符串
    auto_cut : bool, optional
        如果超出长度，是否自动截断，默认为True
        如果为False，则超出长度会抛出异常

    Returns
    -------
    str
        检查后的字符串

    Raises
    ------
    TypeError
        key不是字符串，或者key为空字符串
    ValueError
        key不符合规定格式
    IndexError
        key超出长度,此时auto_cut为False
    """
    max_len = 255
    if not isinstance(key, str):
        raise TypeError(f"tag: {key} is not a string")
    # 删除头尾空格
    key = key.lstrip().rstrip()
    if not check_string(key):
        raise ValueError(f"tag: {key} is an empty string")
    if key.startswith((".", "/")):
        raise ValueError(f"tag: {key} can't start with '.' or '/' and blank space")
    # 检查长度
    return _auto_cut("tag", key, max_len, auto_cut)
