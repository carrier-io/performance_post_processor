node {
  properties([pipelineTriggers([pollSCM('* * * * *')])])
  try {
    stage('Checkout') {
      git 'https://github.com/carrier-io/performance_post_processor.git'
      message = sh(returnStdout: true, script: "git log -1 HEAD --pretty=format:'%s'").trim()
    }
    stage('Zip') {
      sh 'pip install -r requirements.txt'
      sh 'zip -r post_processing.zip . -x Jenkinsfile -x package/* -x *.git* '
    }
    stage('Push') {
      if (message == "Auto Commit") {
        print "[Debug] Skipping stage"
      }
      else {
        sh 'git add . && git commit -m "Auto Commit"'
        withCredentials([usernamePassword(credentialsId: 'testkey', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
          sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/carrier-io/performance_post_processor.git')
        }
      }
    }
  }
  catch (ex) {
    throw ex
  }
  finally {
    cleanWs()
  }
}
