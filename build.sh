#!/bin/bash

# Instalación de torch compatible con torchaudio
pip install torch==2.0.0+cpu torchvision==0.15.1+cpu torchaudio==2.0.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Instalar resto de dependencias
pip install -r requirements-core.txt
