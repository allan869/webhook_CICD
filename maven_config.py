maven_config = '''
<maven2-moduleset plugin="maven-plugin@2.13">
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.4.3">
      <gitLabConnection>connect</gitLabConnection>
    </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
    <jenkins.model.BuildDiscarderProperty>
        <strategy class="hudson.tasks.LogRotator">
            <daysToKeep>-1</daysToKeep>
            <numToKeep>5</numToKeep>
            <artifactDaysToKeep>-1</artifactDaysToKeep>
            <artifactNumToKeep>-1</artifactNumToKeep>
        </strategy>
    </jenkins.model.BuildDiscarderProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.0.1">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>{url}</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>{branch}</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <jdk>{jdk_version}</jdk>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <aggregatorStyleBuild>true</aggregatorStyleBuild>
  <incrementalBuild>false</incrementalBuild>
  <ignoreUpstremChanges>false</ignoreUpstremChanges>
  <ignoreUnsuccessfulUpstreams>false</ignoreUnsuccessfulUpstreams>
  <archivingDisabled>false</archivingDisabled>
  <siteArchivingDisabled>false</siteArchivingDisabled>
  <fingerprintingDisabled>false</fingerprintingDisabled>
  <resolveDependencies>false</resolveDependencies>
  <processPlugins>false</processPlugins>
  <mavenValidationLevel>-1</mavenValidationLevel>
  <runHeadless>false</runHeadless>
  <disableTriggerDownstreamProjects>false</disableTriggerDownstreamProjects>
  <blockTriggerWhenBuilding>true</blockTriggerWhenBuilding>
  <settings class="jenkins.mvn.DefaultSettingsProvider"/>
  <globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/>
  <reporters/>
  <publishers/>
  <buildWrappers>
    <hudson.plugins.ws__cleanup.PreBuildCleanup plugin="ws-cleanup@0.32">
      <deleteDirs>false</deleteDirs>
      <cleanupParameter></cleanupParameter>
      <externalDelete></externalDelete>
    </hudson.plugins.ws__cleanup.PreBuildCleanup>
  </buildWrappers>
  <prebuilders/>
  <postbuilders>
    <hudson.tasks.Shell>
      <command>docker build -t reg.cctv.cn/{namespace}/{project_name}:{tag_name} . --pull
docker push reg.cctv.cn/{namespace}/{project_name}:{tag_name}
</command>
    </hudson.tasks.Shell>
  </postbuilders>
  <runPostStepsIfResult>
    <name>UNSTABLE</name>
    <ordinal>1</ordinal>
    <color>YELLOW</color>
    <completeBuild>true</completeBuild>
  </runPostStepsIfResult>
</maven2-moduleset>
'''


def get_simple_maven_config(url, branch, jdk_version):
    tag_name = branch if branch.find('/') < 0 else branch[branch.rfind('/') + 1:]
    # print('tag_name:', tag_name)
    project_name = url[url.rindex('/') + 1:url.rindex(".git")].lower()
    # print('project_name:', project_name)
    
    namespace = url[url.rfind(':') + 1:url.rfind("/")].lower()
    # print('namespace:', namespace)
    # print("maven配置：", locals())
    return get_maven_config(**locals())


def get_maven_config(url, branch, project_name, tag_name, namespace, jdk_version):
    return maven_config.format(**locals())


# GET_MAVEN_CONFIG("urlurl", "branch", "project_name", "tag_name")
# print(get_simple_maven_config("git@git.cctv.cn:zhangkai/webhook-test.git", "refs/tags/release-test"))
