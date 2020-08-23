FROM renewal_reminder_base AS app

RUN pip install --upgrade \
        flask \
        setuptools \
        wheel

WORKDIR /app

COPY mock_telegram_bot/app.py /app/

CMD ["python", "app.py"]