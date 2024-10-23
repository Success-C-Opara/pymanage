pipeline {
    agent any

    environment {
        AWS_SSH_KEY = credentials('my-aws-ssh-key') // Jenkins credential ID for your SSH key
        EC2_USER = 'ec2-user' // EC2 instance user
        EC2_IP = '3.86.43.12' // Replace with your EC2 instance's public IP
        DOCKER_IMAGE = 'djangopet' // Name for your Docker image (without tag)
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Success-C-Opara/pymanage.git' // Your GitHub repo
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t $DOCKER_IMAGE:latest .'
                }
            }
        }

        stage('Save Docker Image') {
            steps {
                script {
                    // Save the Docker image to a tar file
                    sh 'docker save -o djangopet.tar $DOCKER_IMAGE:latest'
                    // Copy the tar file to the EC2 instance
                    sh 'scp -o StrictHostKeyChecking=no -i $AWS_SSH_KEY djangopet.tar $EC2_USER@$EC2_IP:/tmp/'
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    // Load the Docker image on the EC2 instance and run the container
                    sh '''
                        ssh -o StrictHostKeyChecking=no -i $AWS_SSH_KEY $EC2_USER@$EC2_IP "
                        set -e; # Exit immediately if a command exits with a non-zero status
                        docker load -i /tmp/djangopet.tar &&
                        docker stop djangopet || true &&
                        docker rm djangopet || true &&
                        docker run -d --name djangopet -p 8000:8000 $DOCKER_IMAGE:latest &&
                        rm /tmp/djangopet.tar # Clean up tar file after deployment
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
