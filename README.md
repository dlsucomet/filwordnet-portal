# FilWordNet Portal
![badge][badge-python]
![badge][badge-plotly]
![badge][badge-flask]
![badge][badge-render]<br>
![badge][badge-github-actions]
[![Deploy to Render](https://github.com/dlsucomet/filwordnet-portal/actions/workflows/deploy-to-render.yml/badge.svg)](https://github.com/dlsucomet/filwordnet-portal/actions/workflows/deploy-to-render.yml)

This is the web portal for **FilWordNet** &mdash; a language resource for Filipino and Philippine English built from text analysis network science and natural language processing.

## Link to Deployed Version
🔗 https://filwordnet.onrender.com/

## Running the App Locally

1. Create a copy of this repository by running:
   ```
   git clone https://github.com/dlsucomet/filwordnet-portal
   ```

2. On this project's root directory, run the following command to install the necessary dependencies:
   ```
   python -m pip install -r requirements.txt
   ```

3. Run the following command to launch the app:
   ```
   python src/app.py
   ```

   Then, access the following URL on your browser:
   ```
   localhost:8049
   ```

## Built Using
This app is built using [Dash](https://dash.plotly.com/), a Python-based web application framework on top of Plotly.js, React, and Flask.

For the FilWordNet API, refer to this (private) [repository](https://github.com/dlsucomet/filwordnet-api). [FastAPI](https://fastapi.tiangolo.com/) is used as the asynchronous server gateway interface (ASGI) framework, with [Uvicorn](https://www.uvicorn.org/) as the ASGI server. The API endpoints are exposed over a secure tunnel created via [ngrok](https://ngrok.com). 

## Authors
- **Mark Edward M. Gonzales**<br>
  mark_gonzales@dlsu.edu.ph <br>
  gonzales.markedward@gmail.com

- **Phoebe Clare L. Ong**<br>
  phoebs_ong@dlsu.edu.ph <br>
  ongphoebeclare@gmail.com

This is part of the **Diachronic Representation and Linguistic Study of Filipino Word Senses Across Social and Digital Media Contexts** project funded by the [Department of Science and Technology – Philippine Council for Industry, Energy, and Emerging Technology Research and Development](https://pcieerd.dost.gov.ph/) (DOST-PCIEERD).

The project is led by Dr. Briane Paul V. Samson and co-proponents Dr. Charibeth K. Cheng and Ms. Unisse C. Chua of the Department of Software Technology, College of Computer Studies, De La Salle University.

[badge-python]: https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=white
[badge-plotly]: https://img.shields.io/badge/Plotly-239120?style=flat&logo=plotly&logoColor=white
[badge-scikit]: https://img.shields.io/badge/scikit_learn-F7931E?style=flat&logo=scikit-learn&logoColor=white
[badge-render]: https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=whit
[badge-github-actions]: https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white
[badge-flask]: https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white
