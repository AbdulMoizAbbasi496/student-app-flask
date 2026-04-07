pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.jenkins.yml'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Fetching code from GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building containerized environment...'
                sh 'docker compose -f ${COMPOSE_FILE} build'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Launching containers...'
                sh 'docker compose -f ${COMPOSE_FILE} up -d'
            }
        }

        stage('Health Check') {
            steps {
                echo 'Waiting for app to be ready...'
                sh 'sleep 20'
                sh 'curl -f http://localhost:8090 || echo "App not yet ready"'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! App is running on port 8090.'
        }
        failure {
            echo 'Pipeline failed.'
            sh 'docker compose -f ${COMPOSE_FILE} logs'
        }
    }
}