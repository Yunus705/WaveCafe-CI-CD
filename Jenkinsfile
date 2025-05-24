pipeline {
  agent any
  environment {
    IMAGE_NAME = 'yunus05/wavecafe'
  }
  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/yunus705/WaveCafe.git'
      }
    }
    stage('Build') {
      steps {
        script {
          docker.build("${IMAGE_NAME}")
        }
      }
    }
    stage('Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          script {
            docker.withRegistry('', 'dockerhub-creds') {
              docker.image("${IMAGE_NAME}").push('latest')
            }
          }
        }
      }
    }
    stage('Deploy') {
      steps {
        sh 'docker-compose down || true'
        sh 'docker-compose up -d'
      }
    }
  }
}