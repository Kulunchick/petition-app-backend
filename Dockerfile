ARG PYTHON=3.11
# build stage
FROM python:${PYTHON}-slim AS builder
RUN apt-get update

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# run stage
FROM python:${PYTHON}-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .

EXPOSE 8000

ENV PORT 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]