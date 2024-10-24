pipeline {
    agent any

    environment {
        AWS_SSH_KEY = credentials('my-aws-ssh-key') // Use the ID of the Jenkins credential for your SSH key
        EC2_USER = 'ec2-user' // Change if using a different user
        EC2_DNS = 'ec2-3-86-43-12.compute-1.amazonaws.com' // Public DNS of your target EC2 instance
        DOCKER_IMAGE = 'djangopet' // Name for your Docker image
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
                    sh 'scp -o StrictHostKeyChecking=no -i $AWS_SSH_KEY djangopet.tar $EC2_USER@$EC2_DNS:/tmp/'
                }
            }
        }

        stage('Deploy to Target EC2') {
            steps {
                script {
                    sh '''
                        ssh -o StrictHostKeyChecking=no -i $AWS_SSH_KEY $EC2_USER@$EC2_DNS "
                        set -e;
                        docker load -i /tmp/djangopet.tar &&
                        docker stop djangopet || true &&
                        docker rm djangopet || true &&
                        docker run -d --name djangopet -p 8000:8000 $DOCKER_IMAGE:latest &&
                        rm /tmp/djangopet.tar
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
