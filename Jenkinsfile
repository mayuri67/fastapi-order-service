pipeline {

    agent any

    environment {
        DOCKER_USER = "mayuri67"
        IMAGE_NAME = "fastapi-order-service"
        IMAGE_TAG = "${BUILD_NUMBER}"

        GITOPS_REPO = "https://github.com/mayuri67/order-service-gitops.git"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/mayuri67/fastapi-order-service.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                sh '''
                . venv/bin/activate
                pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASSWORD" | docker login \
                    -u "$DOCKER_USERNAME" --password-stdin

                    docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}

                    docker logout
                    '''
                }
            }
        }

        stage('Update GitOps Repository') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {

                    sh '''
                    git clone https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/YOUR_USERNAME/order-service-gitops.git gitops

                    cd gitops

                    sed -i "s/tag: .*/tag: ${IMAGE_TAG}/" helm/order-service/values.yaml

                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins"

                    git add .
                    git commit -m "Update order-service image to ${IMAGE_TAG}" || true
                    git push origin main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Python CI/CD Pipeline Successful!'
        }

        failure {
            echo 'Python CI/CD Pipeline Failed!'
        }
    }
}