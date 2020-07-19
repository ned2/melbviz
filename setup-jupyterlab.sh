#!/usr/bin/env bash                                                                                                                                                                                 

# plotly -- https://plotly.com/python/getting-started
jupyter labextension install jupyterlab-plotly@4.9.0
jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.9.0

# voila -- https://github.com/voila-dashboards/voila
jupyter labextension install @jupyter-voila/jupyterlab-preview
jupyter serverextension enable voila --sys-prefix

# jupyterlab-code-formatter -- https://jupyterlab-code-formatter.readthedocs.io/en/latest/installation.html
jupyter labextension install @ryantam626/jupyterlab_code_formatter
jupyter serverextension enable --py jupyterlab_code_formatter
