pipeline {
    agent any
    environment {
        IMAGE_NAME = "flask-ci-cd-demo"
        IMAGE_TAG = "latest"
    }
    stages{
        stage('Checkout'){
            steps{
                git branch: 'master', url: 'https://github.com/mukkamallapradeep/python-ci-cd-demo.git'
                }
        }
        stage('Install & Test'){
            steps{  
                sh '''
                    python -v
                    pip3 --version || true
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r app/requirements.txt
                    pytest -q app/tests    
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResutls: '**/pytest*.xml'
                }
            }
        }
        stage('Docker Build'){
            steps{
                sh'''
                    docker version
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }
        stage('Deploy (Run Container)'){
            when { expression {evn.BRANCH_NAME == 'master'}}
            steps{
            sh '''
                # stop and remove old container if exists
                docker ps -aq --filter "name=flask-demo" | xargs -r docker rm -f
                #run new container mapping host port 5000
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