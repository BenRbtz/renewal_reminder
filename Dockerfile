FROM ubuntu:19.04 as base-image

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN groupadd -g 999 app_group \
    && useradd -r -u 999 -g app_group app_user

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install --no-install-recommends -y \
        python3 \
        python3-pip \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 0 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 0 \
    && pip install --upgrade pip


FROM base-image as build-image

ENV POETRY_VERSION=0.12.12

RUN apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        python3-venv \
    && pip install --upgrade \
        setuptools \
        "poetry==$POETRY_VERSION" \
        wheel

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

COPY renewal_reminder /app/renewal_reminder/

RUN poetry install --no-dev \
    && poetry shell \
    && pip wheel --wheel-dir=./wheels .


FROM base-image as run-image

EXPOSE 5000

COPY --from=build-image /app/wheels wheels

RUN pip install wheels/* \
        --no-cache-dir \
    && rm -rf wheels/

USER app_user

CMD ["python", "-m", "renewal_reminder.app"]