
pipeline {
    agent any

    environment {
        IMAGE_NAME     = "flask-ci-cd-demo"
        IMAGE_TAG      = "latest"
        SONAR_HOST_URL = "http://44.220.92.94:9000"
        SONAR_TOKEN    = credentials('sonar-token')
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/mukkamallapradeep/python-ci-cd-demo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                set -eux

                # Show Python version available on the node
                python3 --version

                # Create and activate virtual environment
                python3 -m venv .venv
                . .venv/bin/activate

                # Install only dependencies (NO TESTS)
                python -m pip install --upgrade pip
                python -m pip install -r app/requirements.txt
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    // Use Jenkins SonarScanner tool
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh """#!/usr/bin/env bash
set -eux

echo "Running SonarQube Scanner..."

"${scannerHome}/bin/sonar-scanner" \\
  -Dsonar.projectKey=flask-ci-cd-demo \\
  -Dsonar.sources=app \\
  -Dsonar.host.url=${SONAR_HOST_URL} \\
  -Dsonar.token=${SONAR_TOKEN}

echo "SonarQube scan completed."
"""
                    }
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
            steps {
                sh '''
                set -eux
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
