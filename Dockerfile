FROM willhallonline/ansible:2.11-alpine-3.16 as base

WORKDIR /tmp

# Install terraform
RUN wget https://releases.hashicorp.com/terraform/1.2.5/terraform_1.2.5_linux_amd64.zip && \
    unzip terraform_1.2.5_linux_amd64.zip && \
    mv terraform /usr/bin/terraform && rm -r *.* && \
    # Install AWS CLI
    apk add --no-cache aws-cli && \
    # Fixed the issue with docopt fail to install
    apk add py3-docopt

# Install azure-cli
RUN apk add --no-cache bash ca-certificates jq curl openssl perl git zip \
    && apk add --no-cache --virtual .build-deps gcc make openssl-dev libffi-dev musl-dev linux-headers \
    && apk add --no-cache libintl icu-libs libc6-compat \
    && apk add --no-cache bash-completion python3-dev \
    && update-ca-certificates && pip install --upgrade pip && pip install --upgrade setuptools \
    && pip install azure-cli

WORKDIR /sincity

COPY ./tools ./tools
COPY setup_cli.sh .
COPY sincity.sh .

# Now setup the sincity CLI
RUN sh -c ./setup_cli.sh && \
    ln -s /sincity/sincity.sh /usr/bin/sincity

FROM base

# The workdir is linked to the running host so he will be able to modify the files locally
WORKDIR /workdir

VOLUME /workdir

# Run a simple shell
CMD ["sh"]