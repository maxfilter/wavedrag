FROM firedrakeproject/firedrake:latest

# Install OS packages
RUN DEBIAN_FRONTEND=noninteractive \
    sudo apt update \
    && sudo apt install -y \
    python3-pip gmsh

COPY . /app/wavedrag

# Install Python packages
RUN pip3 install --upgrade pip --no-cache-dir \
    && pip3 install -r /app/wavedrag/requirements.txt --no-cache-dir

WORKDIR /app/wavedrag
ENTRYPOINT ["/bin/bash"]