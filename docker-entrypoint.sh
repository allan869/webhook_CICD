#!/bin/sh

set -e

: ${API_TOKEN:=29ee58af6fe897d7429e5b367a8019f5}
if [ -n "$APIToken" ]; then
    sed -i "s@#API_TOKEN#@$APIToken@g" myjenkins.py.template
fi

: ${JENKINS_URL:=http://jenkins-test.cctv.cn/}
if [ -n "$JenkinsUrl" ]; then
    sed -i "s@#JENKINS_URL#@$JenkinsUrl@g" myjenkins.py.template
fi

: ${USER_NAME:=zhangkai}
if [ -n "$UserName" ]; then
    sed -i "s@#USER_NAME#@$UserName@g" myjenkins.py.template
fi

mv myjenkins.py.template myjenkins.py

exec "$@"