
# setup python virtual environment:

C:\tools\Python311\python.exe -m venv env_api
D:\venv\env_api\Scripts\activate

python.exe -m pip install --upgrade pip
pip install --upgrade wheel setuptools

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126


pip install fastapi uvicorn transformers torch slowapi

NVIDIA RTX 4000 (Quadro RTX 4000) has a compute capability of 7.5
NVIDIA RTX 4000 Ada Lovelace has a compute capability of 8.9

