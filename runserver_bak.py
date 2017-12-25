from flask import Flask
from flask import request
from maven_config import get_simple_maven_config
from npm_config import get_simple_npm_config
from default_config import get_simple_default_config
import json
from myjenkins import server
import logging
from log_util import logger
import traceback

log = logging.getLogger('mylogger')

app = Flask(__name__)
# print('app:', app)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    """
    接收git提交参数，默认提交处理
    :return: 
    """
    try:
        # print("\n\n\n\n1111111111")
        # print('method:', request.methodd)
        # print("ret:", type(ret), retaa)
        ret = request.data.decode('utf-8')
        data = json.loads(ret)
        print('data:', type(data), data)
        # for k, v in data.items():
        #     print('k:', k, 'v:', v)
        # git提交类型
        event = data['object_kind']
        # print('event:', event)
        branch = data['ref']
        branch_name = branch if branch.find('/') < 0 else branch[branch.rfind('/') + 1:]
        # print('branch_name:', branch_name)
        # if event == 'push':
        #     if branch_name.startswith('release-'):
        #         default_push(data)
        #     elif branch_name.startswith('develop') and request.args.get('dev') == '1' or request.args.get('dev') == 'true':
        #         default_push(data)
        # elif event == 'tag_push':
        #     default_push(data)

        # if event == 'push':
        #     default_push(data)
        # elif event == 'tag_push':
        #     default_push(data)

        if branch_name != 'master' and event == 'push' or event == 'tag_push':
            if branch_name.startswith('release-') or branch_name.startswith('develop') and request.args.get('dev') == '1' or request.args.get('dev') == 'true':
                default_push(data)
        return 'Hello Webhook!'
    except Exception as e:
        logger.error(traceback.format_exc())

@app.route('/<j_n>', methods=['GET', 'POST'])
def webhook_jdk_npm(j_n):
    """
    接收git提交参数，处理以分支和url是jdk和npm类型
    :param j_n: 
    :return: 
    """
    # 获取JDK版本
    try:
        print("\n\n\n\n2222222222")
        build_name = j_n
        print('build_name:', build_name)
        # POST
        print("method:", request.method)
        # 请求类型
        print('request:', request)
        # 请求头
        print('request-headers:', request.headers)
        # git提交信息
        post_url = request.args.get('dev')
        print('post_url:', post_url)
        # re_dev = post_url[post_url.rfind('?') + 1:]
        # print('re_dev:', re_dev)
        ret = request.data.decode('utf-8')
        data = json.loads(ret)
        print('data:', type(data), data)
        for k, v in data.items():
            print('k:', k, 'v:', v)
        # git提交类型
        event = data['object_kind']
        print('event:', event)
        branch = data['ref']
        branch_name = branch if branch.find('/') < 0 else branch[branch.rfind('/') + 1:]
        print('branch_name:', branch_name)
        # if event == 'push':
        #     if branch_name.startswith('release-'):
        #         release_push_jdk_npm(data, j_n)
        #     elif branch_name.startswith('develop') and request.args.get('dev') == '1' or request.args.get('dev') == 'true':
        #         release_push_jdk_npm(data, j_n)
        #
        # elif event == 'tag_push':
        #     if j_n.startswith('jdk') or j_n.startswith('npm'):
        #         release_push_jdk_npm(data, j_n)
        #     # elif j_n.startswith('npm'):
        #     #     release_push_jdk_npm(data, j_n)

        # if event == 'push':
        #     if branch_name.startswith('release-'):
        #         release_push_jdk_npm(data, j_n)
        # elif event == 'tag_push':
        #     if j_n.startswith('jdk') or j_n.startswith('npm'):
        #         release_push_jdk_npm(data, j_n)
        #     # elif j_n.startswith('npm'):
        #     #     release_push_jdk_npm(data, j_n)

        if branch_name != 'master' and event == 'push' or event == 'tag_push':
            if branch_name.startswith('release-') or j_n.startswith('jdk') or j_n.startswith('npm') or branch_name.startswith('develop') and request.args.get('dev') == '1' or request.args.get('dev') == 'true':
                release_push_jdk_npm(data, j_n)


        return 'Hello Webhook!'
    except Exception as e:
        log.error(e)

def release_push_jdk_npm(data, j_n):
    """
    传入对应的参数，用来构建代码
    :param data: 
    :param j_n: 
    :return: 
    """
    try:
        print('release_push_data:', data, j_n)
        create_build_jdk_npm(data['project']['url'], data['ref'], j_n)
    except Exception as e:
        log.error(e)

def default_push(data):
    """
    传入对应的参数，用来构建代码
    :param data: 
    :return: 
    """
    try:
        print('release_push_data:', data)
        create_build_default(data['project']['url'], data['ref'])
    except Exception as e:
        log.error(e)



def create_build_default(git_url, branch):
    """
    构建默认提交类型
    :param git_url: 
    :param branch: 
    :return: 
    """
    try:
        print("kwargs:", git_url, branch)
        branch_name = branch if branch.find('/') < 0 else branch[branch.rfind('/') + 1:]
        pro_name = "CI__" + git_url[git_url.rindex('/') + 1:git_url.rindex(".git")] + "__" + branch_name
        config = get_simple_default_config(url=git_url, branch=branch)
        print('config:', config)
        if not server.get_job_name(pro_name):
            server.create_job(pro_name, config)
        server.build_job(pro_name)
        # server.reconfig_job(pro_name, config)
    except Exception as e:
        log.error(e)

def create_build_jdk_npm(git_url, branch, build_name):
    """
    构建以jdk和npm方式提交的类型
    :param git_url: 
    :param branch: 
    :param build_name: 
    :return: 
    """
    try:
        print("kwargs:", git_url, branch, build_name)
        branch_name = branch if branch.find('/') < 0 else branch[branch.rfind('/') + 1:]
        pro_name = "CI__" + git_url[git_url.rindex('/') + 1:git_url.rindex(".git")] + "__" + branch_name
        print('pro_name:', pro_name)
        if build_name == 'jdk7':
            build_name = 'JDK_7u79'
            config = get_simple_maven_config(url=git_url, branch=branch, jdk_version=build_name)
        elif build_name == 'jdk8':
            build_name = 'JDK_8u112'
            config = get_simple_maven_config(url=git_url, branch=branch, jdk_version=build_name)
        elif build_name == 'npm':
            config = get_simple_npm_config(url=git_url, branch=branch)
        else:
            print("build_name:::", build_name)

        print("config:", config)
        if not server.get_job_name(pro_name):
            server.create_job(pro_name, config)
        server.build_job(pro_name)
        # server.reconfig_job(pro_name, config)
    except Exception as e:
        log.error(e)

if __name__ == '__main__':
    app.run('0.0.0.0')