FROM texlive/texlive:latest

# Instalar librsvg2-bin y pandoc para conversiones automáticas y de markdown
RUN apt-get update && \
    apt-get install -y --no-install-recommends librsvg2-bin pandoc && \
    rm -rf /var/lib/apt/lists/*
