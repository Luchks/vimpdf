# S00.1.02 — Corpus generado C01–C10

Corpus controlado para evaluar motores PDF durante el spike S00.1.

## Archivos principales

| Caso | Archivo | Propósito | SHA-256 |
|---|---|---|---|
| C01 | `C01.pdf` | Una columna con texto fuente conocido | `1ac5a0e658c47c64c771e3ee4a76de203876ae780202a86534a136ca3c9d7e4a` |
| C02 | `C02.pdf` | Documento de dos columnas | `00350da88197e9eda9be10c5669db64c0478644f1be38e6bf00f4ba88b9973cc` |
| C03 | `C03.pdf` | Contenido mixto: imagen raster y gráficos vectoriales | `87f52da73b12561553d0e89326809c4c164e3b4ebb8b31acf64e60b726bb67b2` |
| C04 | `C04.pdf` | Documento con páginas de tamaños distintos | `9afcbd7af0cb7fef5c853bc1fe609c9e4cc97f6cdca577b80ef5dbcf393ea8cf` |
| C05 | `C05.pdf` | Página con `/Rotate 90` para observación del motor | `1a39824fdfff86de0817a322afa818587f313d8d0bda02ba6637dc008439a2d5` |
| C06 | `C06.pdf` | Unicode: caracteres acentuados y secuencia combinante `e + U+0301` | `3f464e0ae5ce1140087504456fa9b24e84747e4dcbf3d22b9b7d0b54fb68397c` |
| C07 | `C07.pdf` | Documento escaneado, solo imagen, sin capa de texto | `27169d62ab2cb79e034a8972870e120cadcb1e9c8af9b766a1767d7fc87f08e9` |
| C08 | `C08.pdf` | PDF cifrado con contraseña de usuario | `05e966a6c8e5bb579bcd33d3c36585ed2871d0c257d6f4a8d16378ac9eb8e859` |
| C09 | `C09.pdf` | PDF deliberadamente truncado/corrupto | `555dffc40b2dcbfa31fbc4f75fca132c3e7dd1656275ce86bb1b78664658e828` |
| C10 | `C10.pdf` | PDF con árbol de páginas que declara `/Count 0` | `5b2baf4dd26ee51161f727d6d51331663ca63b2713ad7fff65ee0c1a66d19b9c` |

## Verdad de terreno y construcción

### C01 — Una columna

Texto controlado almacenado en `C01-source.txt`.

La extracción mediante `pdftotext -layout` coincide con la fuente después de eliminar líneas vacías y espacios finales.

### C02 — Dos columnas

Contiene columnas izquierda y derecha separadas espacialmente.

La extracción con `pdftotext -layout` conserva la disposición de ambas columnas.

### C03 — Imagen y vectores

Contiene una imagen raster incrustada y elementos vectoriales nativos.

`pdfimages -list` detecta la imagen raster de 200 x 120 píxeles.

Archivo auxiliar: `C03-image.png`.

### C04 — Tamaños distintos

Documento de tres páginas:

1. A4: 595 x 842 pt
2. Letter: 612 x 792 pt
3. Cuadrada: 400 x 400 pt

### C05 — Rotate

Página A4 cuyo diccionario PDF contiene `/Rotate 90`.

La rotación pertenece a la página y no fue simulada rotando manualmente el contenido.

### C06 — Unicode

Fuente controlada almacenada en `C06-source.txt`.

Casos principales:

- Precompuesto `café`: `U+0063 U+0061 U+0066 U+00E9`
- Combinante `café`: `U+0063 U+0061 U+0066 U+0065 U+0301`

La extracción mediante `pdftotext` preserva ambas secuencias de puntos de código.

### C07 — Escaneado sin texto

Documento construido exclusivamente a partir de una imagen raster.

`pdfimages -list` detecta una imagen de 1240 x 1754 píxeles.

`pdftotext` devuelve cero caracteres no blancos; no existe capa de texto extraíble.

Archivo auxiliar: `C07-scan.png`.

### C08 — Cifrado

PDF cifrado mediante AES-256.

Credenciales públicas exclusivas para este corpus de prueba:

- User password: `vimpdf`
- Owner password: `vimpdf-owner`

Sin contraseña, `pdfinfo` responde `Incorrect password`.

Con la contraseña de usuario, el documento se abre correctamente.

### C09 — Truncado/corrupto

Se generó primero un PDF válido de 3805 bytes y posteriormente se eliminaron deliberadamente los últimos 256 bytes.

Tamaño final: 3549 bytes.

Conserva la cabecera `%PDF-1.4`, pero carece de una estructura final válida.

Comportamiento observado con `pdfinfo`:

- no encuentra el trailer dictionary;
- no puede leer la tabla xref;
- termina con código de salida 1.

### C10 — Cero páginas

PDF mínimo con catálogo y árbol `/Pages` estructurados, pero con:

`/Kids [] /Count 0`

Comportamiento observado con `pdfinfo`:

- `Invalid page count 0`;
- código de salida 99.

Este caso representa explícitamente la condición de cero páginas contemplada por el corpus.

## Archivos auxiliares

- `C01-source.txt`: fuente textual controlada de C01.
- `C03-image.png`: imagen raster utilizada en C03.
- `C06-source.txt`: fuente Unicode controlada de C06.
- `C07-scan.png`: imagen raster utilizada para construir C07.

## Herramientas utilizadas

- Ghostscript / `ps2pdf`
- Pango/Cairo (`pango-view`)
- qpdf
- Poppler (`pdfinfo`, `pdftotext`, `pdfimages`)
- ImageMagick
- Python

