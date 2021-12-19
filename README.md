# Sistema-QA
Este programa ofrece respuestas de manera automática a una serie de consultas acerca de medicamentos. La única reestricción es que la consulta contenga un nombre del medicamento incluido en el sistema (dado por el nombre de los json) en la carpeta [Medicamentos](https://github.com/c-yanguas/Sistema-QA/tree/main/Codigo/Medicamentos) y alguna de las palabras incluidas en la base de conocimiento.

El sistema ofrece un menú al ejecutarse que es muy intuitivo, sin embargo, para comprender a fondo el sistema, es recomendable leer [Documentacion](https://github.com/c-yanguas/Sistema-QA/blob/main/Documentacion.pdf).

Además, este sistema dado que ofrece respuestas basadas en la inclusión de palabras dadas por la consulta en la base de conocimiento, es generalizable para cualquier documento, si se quiere añadir algún otro simplemente se debe añadir un fichero json con el nombre de dicho documento con la información asociada para cada atributo del mismo en [Medicamentos](https://github.com/c-yanguas/Sistema-QA/tree/main/Codigo/Medicamentos).

Se deja a continuación un ejemplo de consulta y la respuesta dada por el sistema:

consulta: ¿Tiene dezacor efectos adversos en el crecimiento de niños?

respuestas:

dezacor : efectos
---------------
efectos_adversos

- Trastornos gastrointestinales: úlcera gastrointestinal.
- Trastornos del sistema nervioso: dolor de cabeza, vértigo, agitación, trastornos del sueño.
- Trastornos de la piel y del tejido subcutáneo: problemas de cicatrización, lesiones en la piel.
- Trastornos cardiacos y vasculares: incremento de la presión arterial (hipertensión), retención de agua en los tejidos (edema).
- Trastornos endocrinos: aumento de peso, agravamiento de la diabetes mellitus, desaparición de la menstruación.
- Trastornos musculo esqueléticos y del tejido conjuntivo: debilidad muscular, osteoporosis.
- Trastornos oculares: alteraciones oculares.  

