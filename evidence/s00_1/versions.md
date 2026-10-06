# S00.1.01 — Candidatos y versiones congeladas

Fecha de congelación: 2026-10-05

## Regla de congelación

Se fija la versión/revisión estable seleccionada al inicio del spike S00.1.
Los candidatos no se actualizarán durante el spike.

Motores principales:
- PDFium
- MuPDF

Motor de contingencia:
- Poppler

---

## PDFium

### Identificación

- Referencia estable: Chromium 154.0.8037.97 / Milestone 154
- Commit PDFium: `2358b16c1947eff67f0732754af6b3c4e1715ff9`
- Tag PDFium: no aplica; PDFium no publica releases mediante tags versionados equivalentes a MuPDF.
- Origen: código fuente oficial de PDFium.
- Fuente estable: revisión de PDFium referenciada por Chromium Stable 154.0.8037.97.
- URL del repositorio: `https://pdfium.googlesource.com/pdfium`
- URL del artefacto: `https://pdfium.googlesource.com/pdfium/+archive/2358b16c1947eff67f0732754af6b3c4e1715ff9.tar.gz`

### Artefacto verificado

- Archivo local de verificación: `pdfium-m154-2358b16c.tar.gz`
- Tipo: gzip compressed data
- Tamaño aproximado: 12 MB
- SHA-256: `7e63c7a4361fa4533cc6ae530687559d9b524caaec0af315cccd196fce36e3ef`

El artefacto descargado se utiliza para verificación de integridad y no se versiona en Git.

### Configuración de build congelada

Sistema de build:
- GN
- Ninja

Argumentos GN previstos:
- `use_remoteexec = false`
- `is_debug = false`
- `pdf_use_skia = false`
- `pdf_enable_fontations = false`
- `pdf_enable_xfa = true`
- `pdf_enable_v8 = true`
- `is_component_build = false`
- `pdf_is_standalone = true`
- `clang_use_chrome_plugins = false`

Target de verificación previsto: `pdfium_test`

Compilador previsto:
- Clang 22.1.8
- C++20
- Clang del sistema con `clang_use_chrome_plugins = false`

Estado actual de herramientas:
- Clang: 22.1.8
- Ninja: 1.13.2
- GN: no instalado actualmente
- depot_tools: no instalado actualmente

La preparación del toolchain se realizará en la etapa de build y no modifica la revisión congelada.

---

## MuPDF

### Identificación

- Tag: `1.28.5`
- Commit: `8ad45e92f0935d3d87f1db3f873086472a5e1b24`
- Origen: código fuente del tag oficial.
- URL del repositorio: `https://github.com/ArtifexSoftware/mupdf.git`
- URL del artefacto: `https://github.com/ArtifexSoftware/mupdf/archive/refs/tags/1.28.5.tar.gz`

El tag `1.28.5` apunta directamente al commit indicado.

### Artefacto verificado

- Archivo local de verificación: `mupdf-1.28.5.tar.gz`
- Tipo: gzip compressed data
- Tamaño aproximado: 44 MB
- SHA-256: `eb902f036011f6e57979a1c6b00f724de8a8a724bb423f5bb54b6fa38999fdc0`

El artefacto descargado se utiliza para verificación de integridad y no se versiona en Git.


### Configuración de build congelada

Sistema de build:
- GNU Make

Configuración:
- `build=release`
- `CC=gcc`
- `CXX=g++`

Comando previsto:
- `make build=release CC=gcc CXX=g++`

Compilador:
- GCC: 16.2.1 20260810
- G++: 16.2.1 20260810

Se fija explícitamente `build=release`, `CC=gcc` y `CXX=g++` para mantener reproducible la configuración utilizada durante el spike.

---

## Poppler — contingencia

Poppler no forma parte de los candidatos principales del spike.

Referencia disponible al inicio:
- Distribución: Arch Linux
- Repositorio: extra
- Paquete: poppler
- Versión: `26.08.0-1`
- Arquitectura: x86_64
- URL upstream: `https://poppler.freedesktop.org/`

No se congela todavía un artefacto fuente ni un SHA-256 de Poppler porque su uso es exclusivamente contingente.

Si la contingencia se activa, antes de utilizar Poppler se deberá registrar:
- versión/revisión exacta;
- commit/tag correspondiente;
- URL del artefacto;
- SHA-256;
- configuración de build;
- compilador.

---

## Resultado

Candidatos principales congelados:

| Motor | Versión / referencia | Commit | Origen |
|---|---|---|---|
| PDFium | Chromium 154.0.8037.97 / M154 | `2358b16c1947eff67f0732754af6b3c4e1715ff9` | fuente |
| MuPDF | 1.28.5 | `8ad45e92f0935d3d87f1db3f873086472a5e1b24` | fuente |

Contingencia:

| Motor | Referencia | Estado |
|---|---|---|
| Poppler | Arch `26.08.0-1` | No activada |

Los candidatos principales quedan congelados para S00.1 y no deberán actualizarse durante el spike.
