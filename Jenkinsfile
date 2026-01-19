
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
        sh '''#!/usr/bin/env bash
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
'''
        // Make coverage.xml available to any subsequent stage/agent
        stash name: 'coverage', includes: 'coverage.xml'
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/pytest-junit.xml'
        }
      }
    }

    
stage('SonarQube Analysis') {
  steps {
    // Bring coverage.xml into this workspace if you stashed it earlier
    unstash 'coverage'

    withSonarQubeEnv('sonarqube-server') {
      script {
        def scannerHome = tool 'SonarScanner'   // Must exist in Global Tool Configuration
        sh '''#!/usr/bin/env bash
set -euo pipefail

echo "=== Sonar DIAGNOSTICS ==="
echo "PWD               : $(pwd)"
echo "WORKSPACE         : ${WORKSPACE:-}"
echo "scannerHome       : '"${scannerHome}"'"
echo "scanner binary    : '"${scannerHome}"'/bin/sonar-scanner"
ls -l '"${scannerHome}"'/bin/ || true
echo
echo "Java version:"
java -version || { echo "Java not found on this node. Install JDK (e.g., openjdk-17-jdk) and retry."; exit 1; }
echo
echo "Checking SonarQube availability at: '"${SONAR_HOST_URL}"'/api/server/version"
curl -sfI '"${SONAR_HOST_URL}"'/api/server/version || { echo "Cannot reach SonarQube at ${SONAR_HOST_URL}"; exit 1; }
echo "Sonar is reachable."
echo

echo "Coverage file?"
ls -l coverage.xml || { echo "coverage.xml missing"; exit 1; }
echo

echo "=== Running sonar-scanner -X ==="
'"${scannerHome}"'/bin/sonar-scanner -X \
  -Dsonar.projectKey=flask-ci-cd-demo \
  -Dsonar.sources=app \
  -Dsonar.python.coverage.reportPaths=coverage.xml \
  -Dsonar.host.url='"${SONAR_HOST_URL}"' \
  -Dsonar.token='"${SONAR_TOKEN}"'

echo
echo "=== Looking for report-task.txt (workspace root) ==="
ls -la .
if [ -f "report-task.txt" ]; then
  echo "Found report-task.txt ✅"
else
  echo "report-task.txt not found ❌"
  echo "Searching within 3 levels..."
  find . -maxdepth 3 -name report-task.txt -print || true
  exit 1
fi
'''
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
        sh '''#!/usr/bin/env bash
set -euo pipefail

docker version
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
'''
      }
    }

    stage('Deploy (Run Container)') {
      steps {
        sh '''#!/usr/bin/env bash
set -euo pipefail

docker ps -aq --filter "name=flask-demo" | xargs -r docker rm -f
docker run -d --name flask-demo -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
'''
      }
    }
  }

  post {
    always {
      sh '''#!/usr/bin/env bash
set -euo pipefail
docker images | head -n 10 || true
'''
    }
  }
}
