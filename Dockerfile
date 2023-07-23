FROM ubuntu:latest
LABEL authors="akonkina"

ENTRYPOINT ["top", "-b"]