FROM jenkins/jenkins:lts

USER root

# Aggiungiunto il comando docker e il plugin docker compose
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker:cli /usr/local/libexec/docker/cli-plugins /usr/local/libexec/docker/cli-plugins