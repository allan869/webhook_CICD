#!/usr/bin/env python
# coding:utf-8
import jenkins
import logging
import traceback
from log_util import logger

APIToken = '29ee58af6fe897d7429e5b367a8019f5'
JenkinsUrl = 'http://jenkins-test.cctv.cn/'
UserName = 'zhangkai'
server = jenkins.Jenkins(JenkinsUrl, username=UserName, password=APIToken)

log = logging.getLogger('mylogger')
s = 0
while s < 5:
    s += 1
    try:
        log.info('jenkins Connecting... ')
        # user = server.get_whoami()
        # log.info('jenkins Connected: ', server.get_job_info('webhook__webhook-test__release-test'))
        break
    except Exception as e:
        log.error(traceback.format_exc())
        continue

def main():
    pass

if __name__ == '__main__':
    main()