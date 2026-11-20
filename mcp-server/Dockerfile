# Construir desde la raíz del repo:  docker build -f mcp-server/Dockerfile -t odoo-mcp-vg .
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY mcp-server/requirements.txt /app/mcp-server/requirements.txt
RUN pip install -r /app/mcp-server/requirements.txt
COPY odoo-cli/odoo_cli.py /app/odoo-cli/odoo_cli.py
COPY mcp-server/server.py /app/mcp-server/server.py
RUN useradd -m mcp
USER mcp
ENV PORT=8080
EXPOSE 8080
CMD ["python", "/app/mcp-server/server.py"]
