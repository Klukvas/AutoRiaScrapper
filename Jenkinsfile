pipeline {
    agent { docker { image 'python:3.10.7-alpine' } }
    stages {
       stage('init') {
          steps {
             sh 'python3 -m pip install pipenv &&pipenv shell &&  pipenv install'
          }
       }
       stage('test') {
           steps {
               sh 'pipenv run pytest -s -vv'
           }
       }
    }
 }