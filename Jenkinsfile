pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: ' https://github.com/Asfand543/bluegreen.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker build -t blue-app:latest ./app'
                bat 'docker build -t green-app:latest ./app'
            }
        }

        stage('Deploy Blue Environment') {
            steps {
                bat 'docker-compose up -d blue nginx'
            }
        }

        stage('Test Blue Environment') {
          steps {
             script {
             // Wait for services to be ready
                bat 'timeout 30 | docker-compose logs -f nginx &'
                bat 'timeout 10'
            
             // Test with retry logic
                bat '''
                    set MAX_RETRIES=5
                    set RETRY_COUNT=0
                   :RETRY
                    curl -f http://localhost:8080/ || (
                      echo "Attempt !RETRY_COUNT! failed, waiting 5 seconds..."
                       timeout 5
                       set /a RETRY_COUNT+=1
                       if !RETRY_COUNT! leq !MAX_RETRIES! goto RETRY
                       exit 1
                     )
            }
           }    '''
        }
    


        stage('Switch to Green Environment') {
            steps {
                script {
                    bat "sed -i 's/server blue:5000;/server green:5000;/' nginx/nginx.conf"
                    bat 'docker-compose up -d nginx'
                }
            }
        }

        stage('Test Green Environment') {
            steps {
                bat 'curl -f http://localhost:8080 || exit 1'
            }
        }

        stage('Clean Up Old Containers') {
            steps {
                bat 'docker stop blue || true && docker rm blue || true'
            }
        }
    }
}
