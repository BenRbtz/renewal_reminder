FROM ubuntu:20.04 AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN groupadd -g 999 app_group \
    && useradd -r -u 999 -g app_group app_user

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
        python3 \
        python3-pip \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 0 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 0 \
    && pip install --upgrade pip


FROM base AS app

RUN pip install --upgrade \
        flask \
        setuptools \
        wheel

WORKDIR /app

COPY mock_telegram_bot/app.py /app/

CMD ["python", "app.py"]