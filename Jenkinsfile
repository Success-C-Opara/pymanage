pipeline {
    agent any

    environment {
        AWS_SSH_KEY = credentials('my-aws-ssh-key') // Reference the SSH key stored in Jenkins credentials
        EC2_USER = 'ec2-user'
        EC2_DNS = 'ec2-3-86-43-12.compute-1.amazonaws.com'
        DOCKER_IMAGE = 'djangopet'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Success-C-Opara/pymanage.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        stage('Save Docker Image') {
            steps {
                script {
                    sh "docker save -o ${WORKSPACE}/djangopet.tar ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Transfer Docker Image to EC2') {
            steps {
                script {
                    sshagent(['my-aws-ssh-key']) {
                        sh '''
                            set -x
                            echo "Transferring Docker image to EC2 instance..."
                            echo "User: $EC2_USER"
                            echo "DNS: $EC2_DNS"
                            scp -o StrictHostKeyChecking=no ${WORKSPACE}/djangopet.tar $EC2_USER@$EC2_DNS:/tmp/
                        '''
                    }
                }
            }
        }

        stage('Deploy to Target EC2') {
            steps {
                script {
                    sshagent(['my-aws-ssh-key']) {
                        sh '''
                            ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_DNS << 'EOF'
                            set -e
                            echo "Loading Docker image..."
                            docker load -i /tmp/djangopet.tar
                            echo "Stopping existing container if it exists..."
                            docker stop djangopet || true
                            docker rm djangopet || true
                            echo "Running new container..."
                            docker run -d --name djangopet -p 8000:8000 ${DOCKER_IMAGE}:latest
                            echo "Cleaning up..."
                            rm /tmp/djangopet.tar
                            EOF
                        '''
                    }
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
