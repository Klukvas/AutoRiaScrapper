pipeline {
    agent any
    stages {
       stage('init') {
          steps {
             sh "pipenv install"
          }
       }
       stage(test) {
           steps {
               sh 'pipenv run pytest -s -vv'
           }
       }
    }
 }