pipeline {
    agent any

    environment {
        PRIVATE_KEY = "/home/ubuntu/keys/linux-key.pem" // path to your .pem file on Jenkins EC2
        IMAGE_NAME = "yunus05/wavecafe"
        APP_SERVER = "ubuntu@172.31.5.49"
        REMOTE_PATH = "/home/ubuntu/wavecafe"
    }

    stages {
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
                sh """
                scp -i ${PRIVATE_KEY} -o StrictHostKeyChecking=no docker-compose.yml ${APP_SERVER}:${REMOTE_PATH}/docker-compose.yml

               // SSH into App Server EC2 and deploy
               ssh -i ${PRIVATE_KEY} -o StrictHostKeyChecking=no ${APP_SERVER} '
               cd ${REMOTE_PATH}
               docker-compose down || true
               docker-compose pull
               docker-compose up -d
              '
              """
            }
        }
      }
}
