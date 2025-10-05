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
                    def color = bat(script: 'type current_color.txt', returnStdout: true).trim()
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
                    def color = bat(script: 'type current_color.txt', returnStdout: true).trim()
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
                    def color = bat(script: 'type current_color.txt', returnStdout: true).trim()
                    if (color == 'green') {
                        powershell '''
                                   (Get-Content nginx.conf) -replace '8082', '8081' | Set-Content nginx.conf
                                   '''

                    } else {
                        powershell '''
                                  (Get-Content nginx.conf) -replace '8082', '8081' | Set-Content nginx.conf
                                 '''

                    }
                    bat 'docker exec nginx2-web-1 nginx -s reload || echo "Nginx reload skipped, container not running"'

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
