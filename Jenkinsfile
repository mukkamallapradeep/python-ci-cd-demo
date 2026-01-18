
pipeline {
    agent any
    environment {
        IMAGE_NAME = "flask-ci-cd-demo"
        IMAGE_TAG = "latest"
        SONAR_HOST_URL = "http://44.197.246.87:9000"
        SONAR_TOKEN = credentials('sonar-token')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/mukkamallapradeep/python-ci-cd-demo.git'
            }
        }
       
        stage('Install & Test') {
          steps {
            sh '''
              set -euxo pipefail
              python3 -m venv .venv
              . .venv/bin/activate
              python -m pip install --upgrade pip
              python -m pip install -r app/requirements.txt
              python -m pip install pytest pytest-cov
              mkdir -p reports
              python -m pytest -q app/tests --junitxml=reports/pytest-junit.xml \
                --cov=app --cov-report=xml
            '''
            stash name: 'coverage', includes: 'coverage.xml'
          }
          post {
            always {
              junit allowEmptyResults: true, testResults: 'reports/pytest-junit.xml'
            }
          }
        }
        
        stage('SonarQube Analysis'){
            steps{
                withSonarQubeEnv('sonarqube-server'){
                    sh '''
                    ..venv/bin/activate
                    sonar-scanner\
                     -Dsonar.projectKey=flask-ci-cd-demo\
                     -Dsonar.sources=app\
                     -Dsonar.host.url=${SONAR_HOST_URL}\
                     -Dsonar.login=${SONAR_TOKEN}
                     '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -eux
                    docker version
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }
       
        stage('Deploy (Run Container)') {
           // when { expression { env.BRANCH_NAME == 'master' } }  // <- env, not evn
          steps {
            sh '''
              docker ps -aq --filter "name=flask-demo" | xargs -r docker rm -f
              docker run -d --name flask-demo -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
            '''
          }
        }

    }
    post {
        always {
            sh 'docker images | head -n 10 || true'
        }
    }
}
