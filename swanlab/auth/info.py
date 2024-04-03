#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2024-03-20 14:41:25
@File: swanlab/auth/info.py
@IDE: vscode
@Description:
    定义认证数据格式
"""
import os.path
from ..utils.key import save_key
from ..env import get_swanlab_folder
from swanlab.package import get_host_api
import requests


class LoginInfo:
    """
    登录信息类，负责解析登录接口返回的信息，并且进行保存
    无论接口请求成功还是失败，都会初始化一个LoginInfo对象
    """

    def __init__(self, resp: requests.Response, api_key: str):
        self.__resp = resp
        self.__api_key = api_key

    @property
    def is_fail(self):
        """
        判断登录是否失败
        """
        return self.__resp.status_code != 200

    @property
    def api_key(self):
        """
        获取api_key
        """
        if self.is_fail:
            return None
        return self.__api_key

    def __str__(self) -> str:
        """错误时会返回错误信息"""
        return self.__resp.reason

    def save(self):
        """
        保存登录信息
        """
        path = os.path.join(get_swanlab_folder(), '.netrc')
        return save_key(path, get_host_api(), "user", self.api_key)


class ExpInfo:
    """
    实验信息类，负责解析实验注册接口返回的信息，并且进行保存
    包含实验token和实验信息，也会包含其他的信息
    """

    def __init__(self, token: str, **kwargs):
        self.token = token
        self.kwargs = kwargs
