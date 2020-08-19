node {
  properties([pipelineTriggers([pollSCM('* * * * *')])])
  try {
    stage('Checkout') {
      git credentialsId: 'performance_post_processor',
        url: 'git@github.com:carrier-io/performance_post_processor.git'
      message = sh(returnStdout: true, script: "git log -1 HEAD --pretty=format:'%s'").trim()
    }
    stage('Zip') {
      docker.image("greene1337/zipthis").inside {
          sh "pip3 install -r requirements.txt -t . && zip -r post_processing.zip . -x Jenkinsfile -x package/* -x *.git* && mv post_processing.zip package/post_processing.zip && cd package && ls -la"
      }
    }
    stage('Push') {
      if (message == "Auto Commit") {
        print "[Debug] Skipping stage"
      }
      else {
        sshagent(['performance_post_processor']) {
          sh 'git add package/post_processing.zip && git commit -m "Auto Commit" && git push origin master'
        }
      }
    }
  }
  catch (ex) {
    throw ex
  }
  finally {
    cleanWs()
    sh 'docker rmi greene1337/zipthis --force'
  }
}
