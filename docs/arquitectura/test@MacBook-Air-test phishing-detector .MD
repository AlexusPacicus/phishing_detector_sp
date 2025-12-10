test@MacBook-Air-test phishing-detector % tree -L 4
.
├── api
├── carpeta sin título
│   ├── app
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── features.cpython-313.pyc
│   │   │   ├── main.cpython-313.pyc
│   │   │   ├── model.cpython-313.pyc
│   │   │   └── schemas.cpython-313.pyc
│   │   ├── features.py
│   │   ├── main.py
│   │   ├── model.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── azure_ai
│   │   ├── __pycache__
│   │   │   └── fastapi_azure.cpython-313.pyc
│   │   ├── azure_ai.md
│   │   ├── azure_prompt.md
│   │   └── fastapi_azure.py
│   ├── Dockerfile
│   ├── EDA
│   │   ├── balance_clases.png
│   │   ├── domain_entropy_boxplot.png
│   │   ├── eda_comparativo_v2.ipynb
│   │   ├── eda_fn_fp_v2.ipynb
│   │   ├── EDA_prototipo.ipynb
│   │   ├── imagenes
│   │   │   ├── eda_boxplots_proto_v2.png
│   │   │   ├── eda_correlaciones_proto_v2.png
│   │   │   ├── eda_entidades_proto_v2.png
│   │   │   ├── eda_resumen_variaciones_proto_v2.png
│   │   │   └── eda_sectores_proto_v2.png
│   │   ├── netloc_len_boxplot.png
│   │   └── tlds_por_clase.png
│   ├── entrenamiento
│   │   ├── entrenamiento_prototipo.ipynb
│   │   ├── img
│   │   │   ├── confusion_matrix.png
│   │   │   ├── feature_importance_grouped_clean.png
│   │   │   ├── precision_recall_curve.png
│   │   │   ├── precision_recall_threshold.png
│   │   │   ├── recall_por_campana.png
│   │   │   ├── recall_por_sector.png
│   │   │   └── roc_auc.png
│   │   └── readme.md
│   ├── features
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── features_constantes.cpython-313.pyc
│   │   │   ├── features.cpython-310.pyc
│   │   │   └── features.cpython-313.pyc
│   │   ├── correlaciones_features.ipynb
│   │   ├── features_.md
│   │   ├── features_base.py
│   │   ├── features_inclusion1.csv
│   │   ├── features_prototipo_con_sector_entidad.csv
│   │   ├── features_prototipo.csv
│   │   ├── features_sectores_prototipo.ipynb
│   │   ├── features_v2_final_autowhitelist.py
│   │   ├── features.ipynb
│   │   ├── img
│   │   │   ├── contains_equal_barplot.png
│   │   │   ├── contains_percent_barplot.png
│   │   │   ├── domain_entropy_hist.png
│   │   │   ├── domain_length_hist.png
│   │   │   ├── free_hosting_barplot.png
│   │   │   ├── num_params_hist.png
│   │   │   ├── protocol_barplot.png
│   │   │   ├── suspicious_path_token_barplot.png
│   │   │   ├── tld_group_barplot.png
│   │   │   └── trusted_path_token_barplot.png
│   │   └── Untitled.ipynb
│   ├── LICENSE
│   ├── limpieza
│   │   ├── legitimas
│   │   │   ├── consolidar_legitimas.ipynb
│   │   │   ├── limpieza_legitimas_banca.ipynb
│   │   │   ├── limpieza_legitimas_cripto.ipynb
│   │   │   ├── limpieza_legitimas_ecommerce.ipynb
│   │   │   ├── limpieza_legitimas_energia.ipynb
│   │   │   └── plantilla
│   │   ├── limpieza_tf.md
│   │   └── phishing
│   │       ├── phishing_ds_prototipo.ipynb
│   │       ├── phishing-database
│   │       ├── phishtank
│   │       ├── scoring
│   │       └── tweetfeed
│   ├── prueba_urls_nuevas.ipynb
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── scraping
│   │   ├── automatizacion_openfish.ipynb
│   │   ├── scraping_cripto.ipynb
│   │   ├── scraping_ecommerce.ipynb
│   │   ├── scraping_energia.ipynb
│   │   ├── scraping_logistica.ipynb
│   │   ├── scraping_openphish.ipynb
│   │   ├── scraping_pago.ipynb
│   │   ├── scraping_publico.ipynb
│   │   ├── scraping_rrss.ipynb
│   │   ├── scraping_saas.ipynb
│   │   ├── scraping_streaming.ipynb
│   │   ├── scraping_teleco.ipynb
│   │   ├── scraping_turismo.ipynb
│   │   ├── scraping_url_banca.ipynb
│   │   └── tweet.ipynb
│   ├── tests
│   │   ├── __pycache__
│   │   │   ├── test_api.cpython-313-pytest-8.3.4.pyc
│   │   │   └── test_features.cpython-313-pytest-8.3.4.pyc
│   │   ├── test_api.py
│   │   ├── test_features_v2.py
│   │   └── test_features.py
│   ├── tranco.csv
│   ├── Untitled.ipynb
│   └── Untitled1.ipynb
├── data
│   ├── clean
│   │   ├── dataset_base_v21.csv
│   │   ├── dataset_v1_features.csv
│   │   ├── dataset_v1.csv
│   │   ├── inclusion_v2.csv
│   │   ├── legitimas
│   │   │   └── legitimas_final.csv
│   │   └── phishing
│   │       └── phishing_prototipo.csv
│   ├── dataset
│   │   └── readme.md
│   ├── interim
│   │   ├── legitimas
│   │   │   ├── banca
│   │   │   ├── cripto
│   │   │   ├── ecommerce
│   │   │   ├── eleccion_legitimas_v1_comparadas.csv
│   │   │   ├── energia
│   │   │   └── legitimas_consolidado.csv
│   │   ├── phishing
│   │   │   ├── database-phishing_scored.csv
│   │   │   ├── database-phishing_scored.parquet
│   │   │   ├── dataset_infra_es_comprometida.csv
│   │   │   ├── dataset_tokens_full.csv
│   │   │   ├── feed_scored_v1_20251010_165910_score_4to7.csv
│   │   │   ├── feed_scored_v1_20251010_165910_score_gt7.csv
│   │   │   ├── feed_scored_v1_20251010_165910_score_le4.csv
│   │   │   ├── feed_scored_v1_20251010_165910.csv
│   │   │   ├── feed_scored_v1_20251010_170655_score_4to7.csv
│   │   │   ├── feed_scored_v1_20251010_170655_score_gt7.csv
│   │   │   ├── feed_scored_v1_20251010_170655_score_le4.csv
│   │   │   ├── feed_scored_v1_20251010_170655.csv
│   │   │   ├── feed_scored_v1_full.csv
│   │   │   ├── filtrado_1_tf_no.csv
│   │   │   ├── phishing_final.csv
│   │   │   ├── phishing_v2_150.csv
│   │   │   ├── phishing_v2_limpieza_manual.csv
│   │   │   ├── phishing_v2.csv
│   │   │   ├── phishing-database_v2
│   │   │   ├── phishtank_candidatas_segunda.csv
│   │   │   ├── primer_phishingrepo_para_excel.csv
│   │   │   ├── primer_phishingrepo.csv
│   │   │   ├── tweetfeed_bloque2_candidatas.csv
│   │   │   └── tweetfeed_es_sin_marca_para_revision.csv
│   │   └── README.md
│   ├── raw
│   │   ├── legitimas
│   │   │   ├── banca
│   │   │   ├── cripto
│   │   │   ├── ecommerce
│   │   │   ├── energia
│   │   │   ├── logistica_legitimas_crudo.csv
│   │   │   ├── publico_legitimas_crudo.csv
│   │   │   ├── rrss_legitimas_crudo.csv
│   │   │   ├── saas_legitimas_crudo.csv
│   │   │   ├── streaming_legitimas_crudo.csv
│   │   │   ├── teleco_legitimas_crudo.csv
│   │   │   └── viajes_legitimas_crudo.csv
│   │   └── phishing
│   │       ├── database-phishing.txt
│   │       ├── openphish
│   │       ├── phishstats
│   │       ├── phishtank
│   │       ├── TweetFeed
│   │       ├── urlhaus
│   │       ├── urlhaus_online_20250826_230004.csv
│   │       ├── urlhaus_online_20250827_230006.csv
│   │       ├── urlhaus_online_20250828_230004.csv
│   │       ├── urlhaus_online_20250829_230232.csv
│   │       ├── urlhaus_online_20250831_230006.csv
│   │       ├── urlhaus_online_20250901_230004.csv
│   │       ├── urlhaus_online_20250902_230004.csv
│   │       ├── urlhaus_online_20250909_230006.csv
│   │       ├── urlhaus_online_20250910_110004.csv
│   │       ├── urlhaus_online_20250910_230004.csv
│   │       └── urlhaus_online_20250911_230004.csv
│   └── Readme_data.md
├── docs
│   ├── arquitectura
│   ├── dominios_espanyoles.csv
│   ├── dominios_espanyoles.md
│   ├── EDA
│   │   ├── EDA_comparativo_v2.md
│   │   └── eda_v1.md
│   ├── features
│   │   ├── analisis_errores_features_v2.md
│   │   ├── features_v2_completo.md
│   │   ├── features_v2_formulas.md
│   │   ├── features_v2_prompt.md
│   │   ├── features_v2_tecnico_2.md
│   │   ├── features_v2_tecnico_maestro.md
│   │   ├── features_v2_tecnico.md
│   │   └── revision_features_v2.md
│   ├── features_v2.md
│   ├── global_neutral_domains.csv
│   ├── inclusion
│   │   ├── phishing_v2.md
│   │   ├── README_inclusion_phishing_v2.md
│   │   └── readme_legitimas_v2.md
│   ├── limpieza
│   │   └── v1
│   │       ├── limpieza_manual_pt.md
│   │       ├── limpieza_prototipo_legitimas.md
│   │       ├── limpieza_prototipo_phishing.md
│   │       └── readme.md
│   ├── scoring
│   │   └── scoring.md
│   ├── tokens
│   └── tokens_por_sector.csv
├── extract_features_dataset_v1.py
├── features
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── features_constantes.cpython-310.pyc
│   │   ├── features_constantes.cpython-313.pyc
│   │   ├── features_v2.cpython-310.pyc
│   │   └── features_v2.cpython-313.pyc
│   ├── features_constantes.py
│   └── features_v2.py
├── logs
│   ├── cron.log
│   ├── recolector_openphish.log
│   ├── recolector_phishing.log
│   ├── recolector_phishstats.log
│   ├── recolector_phishtank.log
│   ├── recolector_urlhaus.log
│   └── update_tweetfeed.log
├── models
│   ├── best_pipeline_logreg.joblib
│   ├── best_pipeline_metadata.json
│   ├── logreg_phishing_final.joblib
│   └── readme.md
├── notebooks
│   ├── domain_complexity.ipynb
│   ├── EDA_features_v2.ipynb
│   ├── prueba_features_v21.ipynb
│   └── validacion_features_v2.ipynb
├── outputs
│   ├── inclusion_v2
│   │   └── predicciones_inclusion_v2.csv
│   └── phishing_v2
│       └── distribucion_scores.png
├── phishing-env
│   ├── bin
│   │   ├── accelerate
│   │   ├── accelerate-config
│   │   ├── accelerate-estimate-memory
│   │   ├── accelerate-launch
│   │   ├── accelerate-merge-weights
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── Activate.ps1
│   │   ├── debugpy
│   │   ├── debugpy-adapter
│   │   ├── dotenv
│   │   ├── f2py
│   │   ├── fastapi
│   │   ├── fonttools
│   │   ├── gunicorn
│   │   ├── hf
│   │   ├── httpx
│   │   ├── huggingface-cli
│   │   ├── ipython
│   │   ├── ipython3
│   │   ├── isympy
│   │   ├── jlpm
│   │   ├── jsonpointer
│   │   ├── jsonschema
│   │   ├── jupyter
│   │   ├── jupyter-dejavu
│   │   ├── jupyter-events
│   │   ├── jupyter-execute
│   │   ├── jupyter-kernel
│   │   ├── jupyter-kernelspec
│   │   ├── jupyter-lab
│   │   ├── jupyter-labextension
│   │   ├── jupyter-labhub
│   │   ├── jupyter-migrate
│   │   ├── jupyter-nbconvert
│   │   ├── jupyter-notebook
│   │   ├── jupyter-run
│   │   ├── jupyter-server
│   │   ├── jupyter-troubleshoot
│   │   ├── jupyter-trust
│   │   ├── normalizer
│   │   ├── numpy-config
│   │   ├── pip
│   │   ├── pip3
│   │   ├── pip3.13
│   │   ├── py.test
│   │   ├── pybabel
│   │   ├── pyftmerge
│   │   ├── pyftsubset
│   │   ├── pygmentize
│   │   ├── pyjson5
│   │   ├── pytest
│   │   ├── python -> python3
│   │   ├── python3 -> /opt/anaconda3/bin/python3
│   │   ├── python3.13 -> python3
│   │   ├── send2trash
│   │   ├── tiny-agents
│   │   ├── tldextract
│   │   ├── torchfrtrace
│   │   ├── torchrun
│   │   ├── tqdm
│   │   ├── transformers
│   │   ├── transformers-cli
│   │   ├── ttx
│   │   ├── uvicorn
│   │   ├── watchfiles
│   │   ├── websockets
│   │   └── wsdump
│   ├── etc
│   │   └── jupyter
│   │       ├── jupyter_notebook_config.d
│   │       └── jupyter_server_config.d
│   ├── include
│   │   └── python3.13
│   ├── lib
│   │   └── python3.13
│   │       └── site-packages
│   ├── pyvenv.cfg
│   └── share
│       ├── applications
│       │   ├── jupyter-notebook.desktop
│       │   └── jupyterlab.desktop
│       ├── icons
│       │   └── hicolor
│       ├── jupyter
│       │   ├── kernels
│       │   ├── lab
│       │   ├── labextensions
│       │   └── nbconvert
│       └── man
│           └── man1
├── README.md
├── scripts
│   ├── __pycache__
│   │   ├── features_v2.cpython-313.pyc
│   │   ├── scoring_utils.cpython-310.pyc
│   │   ├── scoring_v1.cpython-310.pyc
│   │   └── scoring_v2.cpython-313.pyc
│   ├── aut_phishstats.py
│   ├── aut_phishtank.py
│   ├── automatizacion_openphish.py
│   ├── eval_inclusion_v2.py
│   ├── limpieza_pipeline_v2.py
│   ├── logs
│   │   ├── recolector_phishing.log
│   │   └── recolector_phishtank.log
│   ├── notebook_validacion.ipynb
│   ├── Readme_scripts.md
│   ├── scoring_v1.py
│   ├── scoring_v2.py
│   ├── scripts_select_phishing_v2.py
│   └── tweet_feed.py
└── src
