# Licenciatura Forestal — V6

Versión enfocada en separar claramente el origen de las preguntas y priorizar material real de examen.

## Banco
- 270 preguntas totales.
- 18 preguntas tipo/oficiales de los anexos.
- 38 preguntas recuperadas de `Cuestionario Ex. Licenciatura.pdf`.
- 214 preguntas investigadas/construidas para práctica.
- 57 preguntas con apoyo visual.

## Qué cambió en V6
- Nuevo origen **Examen anterior**.
- Se recorrió completo el `Cuestionario Ex. Licenciatura.pdf`.
- Se importaron únicamente preguntas de alternativa completas y suficientemente verificables.
- Se ignoraron subrayados, marcas `VERDADERO`, desarrollos, respuestas recordadas y comentarios estudiantiles.
- Las claves fueron resueltas de nuevo con el material académico, cálculo independiente y referencias técnicas.
- Se reemplazaron 9 preguntas generadas que duplicaban casi exactamente preguntas reales recuperadas.
- Se recuperaron gráficos y fotografías originales cuando eran necesarios para responder.
- El filtro **Origen** permite practicar solo Tipo/oficial, Examen anterior o Investigada.

## Archivos
`recovered_exam_audit.json` documenta qué criterio se usó y ejemplos de preguntas no importadas por ambigüedad, datos faltantes o duplicación.

## Ejecutar
```powershell
python -m streamlit run app.py
```

## Despliegue
Subir a la raíz del repositorio:
- app.py
- questions.json
- curriculum.json
- sources.json
- requirements.txt
- assets/
- coverage_report.json
- quality_report.json
- recovered_exam_audit.json

El progreso continúa guardándose localmente en el navegador.
