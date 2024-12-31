FROM python:3.13-bookworm AS py-base

LABEL org.opencontainers.image.authors="papaiatis@gmail.com"
LABEL org.opencontainers.image.title="async_worker_svc"
LABEL org.opencontainers.image.description="Python Async Worker Service Example"

RUN pip install poetry==1.8.5

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_HOME=/opt/poetry \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y dumb-init && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf \
      /tmp/* \
      /var/lib/apt/lists/* \
      /var/tmp/*

RUN useradd -ms /bin/bash worker

FROM py-base AS production

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --without dev --no-root --no-ansi && \
    rm -rf $POETRY_CACHE_DIR

COPY async_worker_svc ./async_worker_svc

USER worker
ENTRYPOINT ["/usr/bin/dumb-init", "--", "poetry", "run", "worker"]