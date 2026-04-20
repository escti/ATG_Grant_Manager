FROM oraclelinux:8

# Atualização de pacotes e instalação de dependências (Apache e Python3)
RUN dnf update -y && \
    dnf install -y httpd python3 python3-pip && \
    pip3 install requests python-dotenv

# Instalação do Oracle Instant Client nativo do repositório Oracle Linux 8 (Suporte ARM/aarch64)
RUN dnf install -y oracle-instantclient-release-el8 && \
    dnf install -y oracle-instantclient-basic oracle-instantclient-sqlplus && \
    dnf clean all

# Configuração do Apache para permitir execução CGI
RUN sed -i 's/#AddHandler cgi-script .cgi/AddHandler cgi-script .cgi/' /etc/httpd/conf/httpd.conf && \
    sed -i '/<Directory "\/var\/www\/cgi-bin">/,/<\/Directory>/ s/AllowOverride None/AllowOverride None\n    Options +ExecCGI/' /etc/httpd/conf/httpd.conf

# Copiando os scripts Backend e Frontend
COPY src/backend/* /usr/local/bin/
RUN chown root:apache /usr/local/bin/grant_manager.sh /usr/local/bin/grant_reporter.sh /usr/local/bin/jira_validator.py && \
    chmod 750 /usr/local/bin/*.sh && \
    chmod 750 /usr/local/bin/*.py

COPY src/frontend/* /var/www/cgi-bin/
RUN chown root:apache /var/www/cgi-bin/*.cgi && \
    chmod 755 /var/www/cgi-bin/*.cgi

# Expondo a porta HTTP padrão
EXPOSE 80

# Inicializando o Apache em foreground
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
