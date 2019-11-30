"""
这是fabric2版本的代码
"""
import os
import random
import time
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from invoke import task


PROJECT_NAME = 'xxsite'
SETTINGS = 'xxsite/xxsite/settings.py'
DEV_VENV = '/home/fire/env_xxsite'
DEPLOY_PATH = '/home/fire/xxsite'
VENV_ACTIVATE = os.path.join(DEPLOY_PATH, 'bin', 'activate')
# PYPI_HOST = '127.0.0.1'
# PYPI_INDEX = 'http://127.0.0.1:8080/simple'
PROCESS_COUNT = 2
PORT_PREFIX = 909


@task
def build(c, version=None, bytescode=False):
    """ 本地打包
        1. 配置版本号
        2. 打包
    Usage:
        fab build --version 1.4
    """
    if not version:
        version = datetime.now().strftime('%m%d%H%M%S')  # 当前时间，月日时分秒

    _version = _Version()
    _version.set(['setup.py', SETTINGS], version)

    result = c.run('echo $SHELL', hide=True)
    user_shell = result.stdout.strip('\n')

    c.run(DEV_VENV + '/bin/python setup.py bdist_wheel', warn=True, shell=user_shell)

    _version.revert()


@task
def deploy(c, whl_file):
    """ 部署指定版本
        1. 确认虚拟环境已经配置
        2. 激活虚拟环境
        3. 上传whl并安装软件包
        4. 上传supervisord.conf并启动

    Usage:
        fab -H myserver -S ssh_config deploy /path/to/whl_file
    """
    _ensure_virtualenv(c)
    _upload_whl(c, DEPLOY_PATH, whl_file)
    with c.prefix('source %s' % VENV_ACTIVATE):
        whl_file_filename = whl_file.split('/')[-1]
        c.run('pip install ' + os.path.join(DEPLOY_PATH, 'tmp', whl_file_filename), warn=True)
        _reload_supervisoird(c, DEPLOY_PATH)


@task
def set_environ(c):
    """
    设置用于项目的环境变量，需要手动输入密码

    Usage:
        fab -H myserver set_environ
    """
    # 随机生成字符串
    secret_key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)',k=50))
    db_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)',k=10))
    command = '\n'.join([
        'XX_SECRET_KEY=%s' % secret_key,
        'XX_DB_PASSWORD=%s' % db_password,
    ])
    c.run('echo -e "%s" |sudo tee -a /etc/environment' % command, pty=True)


@task
def set_db(c):
    """
    配置数据库：(需要手动输入密码)(需要先设置环境变量)
    1. 创建新用户
    2. 创建新数据库
    3. 为新用户授权

    Usage:
        fab -H myserver set_db
    """
    c.run(
        ''.join([
            'sudo mysql --execute=',
            '"',
            "CREATE USER fire@localhost IDENTIFIED BY '$XX_DB_PASSWORD';",
            'CREATE DATABASE xxcontent DEFAULT CHARACTER SET utf8;',
            'GRANT ALL PRIVILEGES ON xxcontent.* to fire@localhost;',
            '"'
        ]),
        pty=True
    )


class _Version:
    origin_record = {}

    def replace(self, f, version):
        with open(f, 'r') as fd:
            origin_content = fd.read()
            content = origin_content.replace('${version}', version)

        with open(f, 'w') as fd:
            fd.write(content)

        self.origin_record[f] = origin_content

    def set(self, file_list, version):
        for f in file_list:
            self.replace(f, version)

    def revert(self):
        for f, content in self.origin_record.items():
            with open(f, 'w') as fd:
                fd.write(content)


def _ensure_virtualenv(c):
    if c.run('test -f %s' % VENV_ACTIVATE, warn=True).ok:
        return True

    if c.run('test -f %s' % DEPLOY_PATH, warn=True).failed:
        c.run('mkdir -p %s' % DEPLOY_PATH)

    c.run('virtualenv --python=python3.6 %s' % DEPLOY_PATH)
    c.run('mkdir -p %s/tmp' % DEPLOY_PATH)  # 创建tmp目录存放pid和log


def _upload_whl(c, deploy_path, whl_file):
    destination = os.path.join(deploy_path, 'tmp')
    c.put(whl_file, destination)


def _upload_conf(c, deploy_path):
    env = Environment(
        loader=FileSystemLoader('conf'),
        autoescape=select_autoescape(['.conf'])
    )
    template = env.get_template('supervisord.conf')
    context = {
        'process_count': PROCESS_COUNT,
        'port_prefix': PORT_PREFIX,
        'deploy_path': deploy_path,
    }
    content = template.render(**context)
    tmp_file = '/tmp/supervisord.conf'
    with open(tmp_file, 'wb') as f:
        f.write(content.encode('utf-8'))

    destination = os.path.join(deploy_path, 'supervisord.conf')
    c.put(tmp_file, destination)


def _reload_supervisoird(c, deploy_path):
    _upload_conf(c, deploy_path)
    c.run('supervisorctl -c %s/supervisord.conf shutdown' % deploy_path, warn=True)
    time.sleep(0.5) # 关闭需要时间，过快会导致出现端口仍在占用的错误
    c.run('supervisord -c %s/supervisord.conf' % deploy_path)
