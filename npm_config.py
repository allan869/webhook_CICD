maven_config = '''

<project>
  <actions/>
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
  <jdk>(System)</jdk>
  <triggers>
    <com.dabsquared.gitlabjenkins.GitLabPushTrigger plugin="gitlab-plugin@1.4.3">
      <spec></spec>
      <triggerOnPush>true</triggerOnPush>
      <triggerOnMergeRequest>true</triggerOnMergeRequest>
      <triggerOpenMergeRequestOnPush>never</triggerOpenMergeRequestOnPush>
      <triggerOnNoteRequest>true</triggerOnNoteRequest>
      <noteRegex>Jenkins please retry a build</noteRegex>
      <ciSkip>true</ciSkip>
      <skipWorkInProgressMergeRequest>true</skipWorkInProgressMergeRequest>
      <setBuildDescription>true</setBuildDescription>
      <branchFilterType>NameBasedFilter</branchFilterType>
      <includeBranchesSpec>develop</includeBranchesSpec>
      <excludeBranchesSpec></excludeBranchesSpec>
      <targetBranchRegex></targetBranchRegex>
    </com.dabsquared.gitlabjenkins.GitLabPushTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>rm -rf dist

alias cnpm=&quot;npm --registry=https://registry.npm.taobao.org --cache=$HOME/.npm/.cache/cnpm --disturl=https://npm.taobao.org/dist --userconfig=$HOME/.cnpmrc&quot;

cnpm install

npm run build

docker build -t reg.cctv.cn/{namespace}/{project_name}:{tag_name} . --pull
docker push reg.cctv.cn/{namespace}/{project_name}:{tag_name}
</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers>
    <jenkins.plugins.nodejs.tools.NpmPackagesBuildWrapper plugin="nodejs@0.2.1">
      <nodeJSInstallationName>NodeJS</nodeJSInstallationName>
    </jenkins.plugins.nodejs.tools.NpmPackagesBuildWrapper>
  </buildWrappers>
</project>
'''

def get_simple_npm_config(url, branch):
    tag_name = branch if branch.find('/') < 0 else branch[branch.rfind('/') + 1:]
    # print('tag_name:', tag_name)
    project_name = url[url.rindex('/') + 1:url.rindex(".git")].lower()
    # print('project_name:', project_name)
    # namespace = url[url.rfind(':') + 1:url.rfind("/")]
    namespace = url[url.rfind(':') + 1:url.rfind("/")].lower()
    # print('namespace:', namespace)
    # print("maven配置：", locals())
    return get_maven_config(**locals())


def get_maven_config(url, branch, project_name, tag_name, namespace):
    return maven_config.format(**locals())


# GET_MAVEN_CONFIG("urlurl", "branch", "project_name", "tag_name")
# print(get_simple_npm_config("git@git.cctv.cn:zhangkai/webhook-test.git", "refs/tags/release-test"))
