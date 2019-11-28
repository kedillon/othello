# Build as:
#    sudo ./init.sh && sudo docker build -t torch_image_cuda10 .
# Run as:
#    sudo nvidia-docker run -d 
#                           -p 8422:22 \
#                           --name torch \
#                           --hostname torch \
#                           --restart always \
#                           torch_image_cuda10
# Then ssh into the instance as:
#    ssh -p 8422 localhost
#
##################
## We'll start from an pytorch cuda10+cudnn7 image
##################

FROM pytorch/pytorch:1.2-cuda10.0-cudnn7-devel

###################
## MOTD
###################

RUN echo "export PATH=/opt/conda/bin:$PATH" >> /etc/profile

###################
## Install required packages and a few utilities.
###################

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt install -y emacs git less zip unzip tzdata ssh htop

###################
## Set up timezone info
###################

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

###################
## Set up ssh
###################

# sshd requires that this directory exist
RUN mkdir -p /var/run/sshd

# need a few tweaks to sshd_config so that X11 forwarding will work
RUN sed -i -e 's/.*X11Forwarding.*/X11Forwarding yes/' \
           -e 's/.*X11DisplayOffset.*/X11DisplayOffset 10/' \
           -e 's/.*X11UseLocalhost.*/X11UseLocalhost no/' \
        /etc/ssh/sshd_config
RUN echo "\nX11UseLocalhost no\n" >> /etc/ssh/sshd_config

###################
## Add users, ssh keys.
###################

COPY setup /root
RUN /root/setup.sh

###################
## When the container runs start sshd and wait
###################
CMD /usr/sbin/sshd && tail -f /dev/null
