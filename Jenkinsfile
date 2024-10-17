pipeline {
    agent any

    environment {
        AWS_SSH_KEY = credentials('my-aws-ssh-key') // Jenkins credential ID for your SSH key
        EC2_USER = 'ec2-user' // Change to your EC2 instance user (e.g., 'ubuntu' for Ubuntu)
        EC2_IP = '35.174.106.155' // Replace with your EC2 instance's public IP
        DOCKER_IMAGE = 'djangopet:latest' // Name for your Docker image
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Success-C-Opara/pymanage.git' // Replace with your GitHub repo
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh '''
                        docker build -t $DOCKER_IMAGE .
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    // Deploy to EC2
                    sh '''
                        ssh -o StrictHostKeyChecking=no -i $AWS_SSH_KEY $EC2_USER@$EC2_IP "
                        docker stop $DOCKER_IMAGE || true &&
                        docker rm $DOCKER_IMAGE || true &&
                        docker run -d -p 8000:8000 $DOCKER_IMAGE
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment was successful!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
