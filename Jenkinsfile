pipeline {
    agent any

    environment {
        registryCredential = 'docker-hub' // Docker Hub에 로그인할 때 사용할 자격 증명 ID
        dockerImage = '' // Docker 이미지 변수 초기화
    }

    stages {
        stage('Setup Credentials') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker-hub-username', variable: 'DOCKER_HUB_USERNAME'),
                                     string(credentialsId: 'bastion-username', variable: 'BASTION_USERNAME'),
                                     string(credentialsId: 'bastion-ip', variable: 'BASTION_IP')]) {
                        // 환경 변수 설정
                        env.dockerHubUsername = DOCKER_HUB_USERNAME
                        env.imageName = "face-expression-service" // 이미지 이름
                        env.bastionUsername = BASTION_USERNAME
                        env.bastionIp = BASTION_IP
                        env.fullImageName = "${env.dockerHubUsername}/${env.imageName}" // fullImageName 설정
                    }
                }
            }
        }

        stage('Cloning Repository') {
            steps {
                echo 'Cloning Repository'
                git url: 'https://github.com/KEA-5th-Myaong/face-expression-service.git',
                    branch: 'main',
                    credentialsId: 'github-token'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                echo 'Building and Pushing Docker Image'
                script {
                    def previousBuildId = "${env.BUILD_ID.toInteger() - 1}"
                    def newBuildId = "${env.BUILD_ID.toInteger()}"

                    // 새로운 이미지 빌드 및 푸시
                    dockerImage = docker.build("${env.fullImageName}:${newBuildId}")
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }

                    // 이전 빌드 ID 태그 이미지 삭제
                    sh "docker rmi ${env.fullImageName}:${previousBuildId} || true"
                }
            }
        }

    }

    post {
        success {
            slackSend(channel: '#jenkins', color: '#00FF00', message: """:white_check_mark: Prod 서버 CI/CD 파이프라인 성공 : ${env.JOB_NAME} [${env.BUILD_NUMBER}] 확인 : (${env.BUILD_URL})""")
        }

        failure {
            slackSend(channel: '#jenkins', color: '#FF0000', message: """:octagonal_sign: Prod 서버 CI/CD 파이프라인 실패 : ${env.JOB_NAME} [${env.BUILD_NUMBER}] 확인 : (${env.BUILD_URL})""")
        }
    }
}
