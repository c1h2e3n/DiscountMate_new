pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'DiscountMate'
    }

    stages {
        stage('Clone the code') {
            steps {
                script {
                    git 'your-git-repository-url'
                    echo 'Code cloned successfully'
                }
            }
        }

        stage('Building stage: Building Docker image and run container') {
            steps {
                script {
                    docker.build("-t ${DOCKER_IMAGE}:latest .")
                    docker.run("-d -p 8700:3040 --name my-container ${DOCKER_IMAGE}:latest")
                    echo 'Docker image built and container started successfully'
                }
            }
        }

        stage('Testing stage: Test the code using jest testing units') {
            steps {
                script {
                    docker.exec("-it my-container /bin/bash -c 'cd /app && npm test'")
                    echo 'Code tested successfully'
                }
            }
        }


        stage('Deplyong stage: Using Docker Compose') {
            steps {
                script {
                    // Use Docker Compose to deploy to a test environment
                    sh 'docker-compose -f docker-compose.test.yml up -d'
                    echo 'Code deployed to test environment successfully'
                }
            }
        }
    }
}
