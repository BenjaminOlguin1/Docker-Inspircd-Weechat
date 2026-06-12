FROM debian:bookworm-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    perl \
    pkg-config \
    libssl-dev \
    libgnutls28-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clonar el repositorio
WORKDIR /tmp
RUN git clone --depth 1 --branch insp4 https://github.com/inspircd/inspircd.git

WORKDIR /tmp/inspircd

# Ejecutar el script de configuración
RUN perl ./configure --prefix=/opt/inspircd \
    --binary-dir=/opt/inspircd/bin \
    --config-dir=/opt/inspircd/conf \
    --module-dir=/opt/inspircd/modules \
    --log-dir=/opt/inspircd/logs \
    --disable-interactive \
    --disable-ownership

# Compilar e instalar
RUN make install

# Usuario no privilegiado
RUN useradd -m -u 1000 inspircd

# Directorio de configuración como volumen
VOLUME /opt/inspircd/conf
VOLUME /opt/inspircd/logs

# Puerto IRC estándar
EXPOSE 6667 6697

# Cambiar propietario
RUN chown -R inspircd:inspircd /opt/inspircd

USER inspircd

# Ejecutar InspIRCd
CMD ["/opt/inspircd/bin/inspircd", "--nofork"]