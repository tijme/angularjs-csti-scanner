FROM python:stretch
MAINTAINER random_robbie <txt3rob@gmail.com>

# update
RUN apt-get update && apt-get install locales git wget nano -y

# Set default locale for the environment
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

RUN pip install git+https://github.com/tijme/angularjs-csti-scanner.git



CMD ["/bin/bash"]
