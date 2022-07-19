pipeline {
    agent any
    stages {
       stage('init') {
          steps {
             bat 'pipenv install'
          }
       }
       stage('test') {
           steps {
               bat 'pipenv run pytest -s -vv'
           }
       }
    }
 }