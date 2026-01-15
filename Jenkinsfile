
pipeline {
    agent any
    environment {
        IMAGE_NAME = "flask-ci-cd-demo"
        IMAGE_TAG = "latest"
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
                    set -eux
                    python3 --version
                    pip3 --version

                    # Create virtual environment
                    python3 -m venv .venv
                    . .venv/bin/activate

                    # Install dependencies
                    pip install --upgrade pip
                    pip install -r app/requirements.txt

                    # Run tests and generate JUnit XML
                    mkdir -p reports
                    pytest -q app/tests --junitxml=reports/pytest-junit.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/pytest-junit.xml'
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
            when { expression { env.BRANCH_NAME == 'master' } }
            steps {
                sh '''
                    # Stop and remove old container if exists
                    docker ps -aq --filter "name=flask-demo" | xargs -r docker rm -f

                    # Run new container mapping host port 5000
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
