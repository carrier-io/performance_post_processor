node {
  properties([pipelineTriggers([pollSCM('* * * * *')])])
  try {
    stage('Checkout') {
      git credentialsId: 'performance_post_processor',
        url: 'git@github.com:carrier-io/performance_post_processor.git'
      message = sh(returnStdout: true, script: "git log -1 HEAD --pretty=format:'%s'").trim()
    }
    stage('Zip') {
      sh 'pip install -r requirements.txt'
      sh 'zip -r post_processing.zip . -x Jenkinsfile -x package/* -x *.git* '
      sh 'mv post_processing.zip package/post_processing.zip'
    }
    stage('Push') {
      if (message == "Auto Commit") {
        print "[Debug] Skipping stage"
      }
      else {
        sshagent(['performance_post_processor']) {
          sh 'git add . && git commit -m "Auto Commit" && git push origin master'
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
