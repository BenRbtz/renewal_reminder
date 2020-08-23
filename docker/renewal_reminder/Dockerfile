FROM renewal_reminder_base as build

RUN apt-get install -y \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        python3-setuptools \
        python3-venv \
    && pip install --upgrade \
        setuptools \
        poetry\
        wheel

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

COPY renewal_reminder /app/renewal_reminder/

RUN poetry install --no-dev \
    && poetry shell \
    && pip wheel --wheel-dir=./wheels .


FROM renewal_reminder_base as app

EXPOSE 5000

COPY --from=build /app/wheels wheels

RUN pip install wheels/* \
        --no-cache-dir \
    && rm -rf wheels/

USER app_user

CMD ["python", "-m", "renewal_reminder.app"]