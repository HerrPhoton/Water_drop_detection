FROM python:3.9

ENV QT_DEBUG_PLUGINS=1
RUN python -m pip install --upgrade pip
WORKDIR /detector

COPY requirements.txt .

RUN apt update && apt install -y zip htop screen libgl1-mesa-glx libxcb-util-dev
RUN pip install --no-cache-dir -r requirements.txt

RUN  apt-get update && apt-get -y install xserver-xorg &&\
    apt install -y libxkbcommon-x11-0 &&\
    apt-get install -y libxcb*

COPY src ./src
COPY main.py .
CMD ["python", "main.py"]