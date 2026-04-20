FROM oraclelinux:8

# Atualização de pacotes e instalação de dependências (Apache, Python3 e Dos2Unix)
RUN dnf update -y && \
    dnf install -y httpd python3 python3-pip dos2unix dnf-plugins-core && \
    pip3 install requests python-dotenv

# Instalação do Oracle Instant Client (Estratégia robusta para OCI/ARM)
RUN dnf install -y oraclelinux-developer-release-el8 && \
    dnf config-manager --set-enabled ol8_oracle_instantclient && \
    dnf install -y oracle-instantclient-basic oracle-instantclient-sqlplus && \
    dnf clean all

# Configuração do Apache (ServerName e Logs para o Docker)
RUN echo "ServerName localhost" >> /etc/httpd/conf/httpd.conf && \
    ln -sf /dev/stdout /var/log/httpd/access_log && \
    ln -sf /dev/stderr /var/log/httpd/error_log

# Configuração para permitir execução CGI
RUN sed -i 's/#AddHandler cgi-script .cgi/AddHandler cgi-script .cgi/' /etc/httpd/conf/httpd.conf && \
    echo "LoadModule cgi_module modules/mod_cgi.so" > /etc/httpd/conf.modules.d/01-cgi.conf && \
    sed -i '/<Directory "\/var\/www\/cgi-bin">/,/<\/Directory>/ s/AllowOverride None/AllowOverride None\n    Options +ExecCGI\n    AddHandler cgi-script .cgi .sh .py/' /etc/httpd/conf/httpd.conf

# Criar redirecionamento automático da raiz para o sistema OGM
RUN echo '<meta http-equiv="refresh" content="0; url=/cgi-bin/index.cgi">' > /var/www/html/index.html

# Copiando os scripts Backend e Frontend
COPY src/backend/* /usr/local/bin/
COPY src/frontend/* /var/www/cgi-bin/

# Corrigir fins de linha (CRLF para LF) e permissões
RUN dos2unix /usr/local/bin/*.sh /usr/local/bin/*.py /var/www/cgi-bin/*.cgi && \
    chown -R root:apache /usr/local/bin/ /var/www/cgi-bin/ && \
    chmod 750 /usr/local/bin/*.sh /usr/local/bin/*.py && \
    chmod 755 /var/www/cgi-bin/*.cgi

# Expondo a porta HTTP padrão
EXPOSE 80

# Inicializando o Apache em foreground
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
