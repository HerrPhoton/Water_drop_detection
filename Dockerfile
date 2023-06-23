FROM python:3.9

ENV QT_DEBUG_PLUGINS=1
RUN python -m pip install --upgrade pip
WORKDIR /detector

COPY requirements.txt .

RUN apt update && apt install -y zip htop screen libgl1-mesa-glx libxcb-util-dev
RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install pytest

RUN  apt-get update && apt-get -y install xserver-xorg &&\
    apt install -y libxkbcommon-x11-0 &&\
    apt-get install -y libxcb*

COPY src ./src
COPY tests ./tests
COPY main.py .

RUN echo "Unit-tests run"
RUN python tests/test_BatchManager.py
RUN python tests/test_SaveBatch.py
RUN python tests/test_SaveLoadModel.py
RUN python tests/test_TestNetwork.py
RUN echo "Unit-tests run completed"

RUN echo "Application run"
CMD ["python", "main.py"]