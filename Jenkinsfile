pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ghcr.io/${env.GITHUB_ACTOR}/cicd-api:latest"
        STAGING_PORT = "8081"
        SONAR_HOST_URL = credentials('sonar-host-url')
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage("Stage 1: Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Stage 2: Lint") {
            steps {
                sh """
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    flake8 app/ --max-line-length=120 --count
                """
            }
        }

        stage("Stage 3: Build & Test") {
            steps {
                sh """
                    . venv/bin/activate
                    pip install -r requirements.txt
                    cd app
                    python -m pytest test_main.py --cov=. --cov-report=xml:../coverage.xml --cov-report=term -v
                """
            }
            post {
                always {
                    junit "coverage.xml"
                }
            }
        }

        stage("Stage 4: SonarQube Scan") {
            steps {
                withSonarQubeEnv("SonarQube") {
                    sh """
                        . venv/bin/activate
                        sonar-scanner \
                            -Dsonar.organization=cicd-org \
                            -Dsonar.projectKey=cicd-api \
                            -Dsonar.sources=app/ \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage("Stage 5: Quality Gate") {
            steps {
                timeout(time: 5, unit: "MINUTES") {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage("Stage 6: Security Scan") {
            steps {
                sh """
                    docker build -t ${DOCKER_IMAGE} .
                    trivy image --severity HIGH,CRITICAL --exit-code 1 ${DOCKER_IMAGE}
                """
            }
        }

        stage("Stage 7: Push") {
            steps {
                script {
                    docker.withRegistry("https://ghcr.io", "ghcr-credentials") {
                        docker.image(DOCKER_IMAGE).push("latest")
                        docker.image(DOCKER_IMAGE).push("${env.BUILD_NUMBER}")
                    }
                }
            }
        }

        stage("Stage 8: IaC Apply") {
            steps {
                dir("infra") {
                    sh """
                        terraform init
                        terraform apply -auto-approve \
                            -var="docker_image=${DOCKER_IMAGE}" \
                            -var="staging_port=${STAGING_PORT}"
                    """
                }
            }
        }

        stage("Stage 9: Smoke Test") {
            steps {
                sh """
                    sleep 5
                    curl -sf http://localhost:${STAGING_PORT}/health || exit 1
                    echo "Smoke test passed: staging is healthy"
                """
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed. Check logs for details."
        }
        success {
            echo "Pipeline completed successfully. Staging available at http://localhost:${STAGING_PORT}"
        }
        cleanup {
            sh "rm -rf venv coverage.xml"
        }
    }
}
