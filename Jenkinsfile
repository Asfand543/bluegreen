pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps 
                git ' https://github.com/Asfand543/bluegreen.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker build -t blue-app:latest ./app'
                sh 'docker build -t green-app:latest ./app'
            }
        }

        stage('Deploy Blue Environment') {
            steps {
                sh 'docker-compose up -d blue nginx'
            }
        }

        stage('Test Blue Environment') {
            steps {
                sh 'curl -f http://localhost:8080 || exit 1'
            }
        }

        stage('Switch to Green Environment') {
            steps {
                script {
                    sh "sed -i 's/server blue:5000;/server green:5000;/' nginx/nginx.conf"
                    sh 'docker-compose up -d nginx'
                }
            }
        }

        stage('Test Green Environment') {
            steps {
                sh 'curl -f http://localhost:8080 || exit 1'
            }
        }

        stage('Clean Up Old Containers') {
            steps {
                sh 'docker stop blue || true && docker rm blue || true'
            }
        }
    }
}
