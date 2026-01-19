
pipeline {
  agent any

  environment {
    IMAGE_NAME      = "flask-ci-cd-demo"
    IMAGE_TAG       = "latest"
    SONAR_HOST_URL  = "http://44.220.92.94:9000"
    SONAR_TOKEN     = credentials('sonar-token') // Jenkins secret text credential ID
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: 'master', url: 'https://github.com/mukkamallapradeep/python-ci-cd-demo.git'
      }
    }

    stage('Install & Test') {
      steps {
        sh(
          script: '''
set -euo pipefail

# Create/refresh venv and install deps
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r app/requirements.txt
python -m pip install pytest pytest-cov

# Run tests + coverage and publish JUnit
mkdir -p reports
python -m pytest -q app/tests \
  --junitxml=reports/pytest-junit.xml \
  --cov=app --cov-report=xml

# Sanity check: coverage.xml should exist here for Sonar
test -f coverage.xml
''',
          shell: '/usr/bin/env bash'
        )
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/pytest-junit.xml'
        }
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('sonarqube-server') {
          script {
            def scannerHome = tool 'SonarScanner'
            sh(
              script: """
set -euo pipefail

# Ensure coverage.xml is present in this workspace
test -f coverage.xml

"\${scannerHome}/bin/sonar-scanner" \\
  -Dsonar.projectKey=flask-ci-cd-demo \\
  -Dsonar.sources=app \\
  -Dsonar.python.coverage.reportPaths=coverage.xml \\
  -Dsonar.host.url=${SONAR_HOST_URL} \\
  -Dsonar.token=${SONAR_TOKEN}
""",
              shell: '/usr/bin/env bash'
            )
          }
        }
      }
    }

    // Optional: Enforce Quality Gate (requires SonarQube -> Jenkins webhook configured)
    // stage('Quality Gate') {
    //   steps {
    //     timeout(time: 10, unit: 'MINUTES') {
    //       waitForQualityGate abortPipeline: true
    //     }
    //   }
    // }

    stage('Docker Build') {
      steps {
        sh(
          script: '''
set -euo pipefail

docker version
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
''',
          shell: '/usr/bin/env bash'
        )
      }
    }

    stage('Deploy (Run Container)') {
      steps {
        sh(
          script: '''
set -euo pipefail

docker ps -aq --filter "name=flask-demo" | xargs -r docker rm -f
docker run -d --name flask-demo -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
''',
          shell: '/usr/bin/env bash'
        )
      }
    }
  }

  post {
    always {
      sh(
        script: '''
set -euo pipefail
docker images | head -n 10 || true
''',
        shell: '/usr/bin/env bash'
      )
    }
  }
}
