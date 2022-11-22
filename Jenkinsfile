pipeline {
    agent { docker { image 'python:3.10.7-alpine' } }
    stages {
       stage('init') {
          steps {
             sh 'pipenv shell && python3 -m pip install pipenv && pipenv install'
          }
       }
       stage('test') {
           steps {
               sh 'pipenv run pytest -s -vv'
           }
       }
    }
 }