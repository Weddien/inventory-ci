FROM python:3.12.7-slim
WORKDIR /app
RUN useradd --system --no-create-home appuser
COPY inventory.py README.md ./
USER appuser
ENTRYPOINT ["python", "inventory.py"]
CMD ["--help"]
