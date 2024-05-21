pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO_NAME = 'migration-app-reporoot'
        AWS_ACCOUNT_ID = '732170246315'
        ECR_REPO_NAME = 'migration-app-repo'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-username/s3-to-rds-glue.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${732170246315.dkr.ecr.us-east-1.amazonaws.com/migration-app-repo}")
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    sh '$(ws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 732170246315.dkr.ecr.us-east-1.amazonaws.com)'
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    docker.withRegistry("https://${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com", 'ecr:us-east-1:aws-credentials') {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy Infrastructure') {
            steps {
                script {
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Deploy Lambda Function') {
            steps {
                script {
                    def lambdaImageUri = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest"
                    sh "aws lambda update-function-code --function-name lambdaMigrationFunction --image-uri ${arn:aws:lambda:us-east-1:732170246315:function:lambdaMigrationFunctioni}"
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}

