pipeline {
    agent any
    stages {
        stage("build") {
            steps {
                sh "python utils/test_import_xlsx.py"
            }
        }
        stage("test") {
            steps {
                echo "testing"
                sh "pytest"
            }
        }
        stage("deploy") {
            steps {
                sh "python main.py"
            }
        }
    }   
}
