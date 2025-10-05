pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
               git branch: 'main', url: 'https://github.com/Asfand543/bluegreen'

            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def color = bat(script: 'cat current_color.txt', returnStdout: true).trim()
                    if (color == 'blue') {
                        bat 'docker-compose -f docker-compose-green.yml build'
                    } else {
                        bat 'docker-compose -f docker-compose-blue.yml build'
                    }
                }
            }
        }

        stage('Deploy New Version') {
            steps {
                script {
                    def color = bat(script: 'cat current_color.txt', returnStdout: true).trim()
                    if (color == 'blue') {
                        bat 'docker-compose -f docker-compose-green.yml up -d'
                        bat "echo 'green' > current_color.txt"
                    } else {
                        bat 'docker-compose -f docker-compose-blue.yml up -d'
                        bat "echo 'blue' > current_color.txt"
                    }
                }
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    def color = bat(script: 'cat current_color.txt', returnStdout: true).trim()
                    if (color == 'green') {
                        bat "sed -i 's/8081/8082/' nginx.conf"
                    } else {
                        bat "sed -i 's/8082/8081/' nginx.conf"
                    }
                    bat 'docker exec nginx nginx -s reload'
                }
            }
        }

        stage('Clean Old Version') {
            steps {
                script {
                    bat 'docker image prune -f'
                }
            }
        }
    }
}
