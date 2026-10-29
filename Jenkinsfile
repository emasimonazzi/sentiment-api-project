pipeline {
    agent any

    // Trigger automatico: ogni 2 minuti Jenkins controlla se ci sono nuovi commit su GitHub
    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {

        // Build: crea le immagini Docker
        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        // Test: esegue unit test e test di integrazione 
        stage('Test') {
            steps {
                sh 'docker run --rm sentiment-api python -m pytest -v'
            }
        }

        // Deploy: avvia i container
        stage('Deploy') {
            steps {
                sh 'docker compose up -d'
            }
        }

        // controlla che l'API pubblicata risponda
        stage('Smoke test') {
            steps {
                sh 'sleep 5'
                sh '''
                    curl -f -X POST http://host.docker.internal:8000/predict \
                         -H "Content-Type: application/json" \
                         -d '{"review": "This product is amazing! I love it."}'
                '''
            }
        }
    }

    // Notifiche: eseguite alla fine, in base al risultato
    post {
        success {
            echo 'SUCCESSO: la pipeline è stata completata e l API è in produzione.'
        }
        failure {
            echo 'ERRORE: la pipeline è fallita. Controllare il Console Output.'
        }
    }
}