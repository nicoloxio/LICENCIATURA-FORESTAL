# Licenciatura Forestal — V3

## Cambios principales
- Mantiene la estructura visual de la V2.
- Las alternativas son tarjetas completas y ya no muestran A/B/C/D.
- 175 preguntas investigadas: 5 por cada uno de los 35 temas del Anexo 2b.
- Se conservan 17 preguntas tipo/oficiales: 192 preguntas totales.
- Las preguntas investigadas eliminan referencias de contexto como “según el material”.
- Distractores reescritos para ser plausibles, del mismo dominio y con longitud comparable.
- Cada pregunta investigada guarda referencias técnicas; se pueden consultar en el expander “Base técnica” después de responder.
- `quality_report.json` audita longitud de alternativas y lenguaje contextual.

## Ejecutar en Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Nota sobre legislación
Las preguntas investigadas de Ley 20.283 se basan en la versión vigente consultada en 2026. Algunas recopilaciones antiguas pueden contener umbrales previos o apuntes no oficiales; las preguntas tipo originales se mantienen separadas como “Tipo/oficial”.


## Despliegue
Esta versión guarda el progreso en el localStorage del navegador. La misma URL puede ser usada por varias personas sin compartir estadísticas entre dispositivos/navegadores.
