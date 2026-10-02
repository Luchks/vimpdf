#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="PVT_kwHOCM6YPc4BlGjF"
START_FIELD_ID="PVTF_lAHOCM6YPc4BlGjFzhj7Ovc"
END_FIELD_ID="PVTF_lAHOCM6YPc4BlGjFzhj7O4U"

set_dates() {
  local item_id="$1"
  local start="$2"
  local end="$3"

  echo "→ $start → $end | $item_id"

  gh project item-edit \
    --id "$item_id" \
    --field-id "$START_FIELD_ID" \
    --project-id "$PROJECT_ID" \
    --date "$start"

  gh project item-edit \
    --id "$item_id" \
    --field-id "$END_FIELD_ID" \
    --project-id "$PROJECT_ID" \
    --date "$end"
}

# ============================================================
# S00.0 — Preparación
# ============================================================

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9fWx0" \
  "2026-09-30" "2026-09-30" \
  # S00.0.01 — Entornos y estructura de evidencia


# ============================================================
# S00.3 — Toolchain / baseline
# Se adelanta porque constituye prerrequisito para los builds.
# ============================================================

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iEdw" \
  "2026-10-01" "2026-10-02" \
  # S00.3.01 — Inventario de toolchain y baseline

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iEpI" \
  "2026-10-05" "2026-10-06" \
  # S00.3.02 — Build Linux x64 (C++17, estático y dinámico)


# ============================================================
# S00.1 — PDF / motores / corpus
# ============================================================

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9h2LY" \
  "2026-10-07" "2026-10-08" \
  # S00.1.01 — Fijar candidatos y versiones

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iA48" \
  "2026-10-09" "2026-10-12" \
  # S00.1.02 — Corpus generado C01–C10

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iBCI" \
  "2026-10-13" "2026-10-15" \
  # S00.1.03 — Corpus C11 (real) y C12 (largo)

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iBKs" \
  "2026-10-16" "2026-10-20" \
  # S00.1.04 — Oráculo y verdad de terreno

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iBQQ" \
  "2026-10-21" "2026-10-23" \
  # S00.1.05 — PDFium: build, abrir, render, dimensiones

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iBYU" \
  "2026-10-26" "2026-10-28" \
  # S00.1.06 — MuPDF: build, abrir, render, dimensiones

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iBhs" \
  "2026-10-29" "2026-11-03" \
  # S00.1.07 — PDFium: texto, palabras, líneas, coordenadas

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iBno" \
  "2026-11-04" "2026-11-06" \
  # S00.1.08 — MuPDF: texto, palabras, líneas, coordenadas

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iBw4" \
  "2026-11-09" "2026-11-11" \
  # S00.1.09 — Comparador y métricas de fiabilidad

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iB4Y" \
  "2026-11-12" "2026-11-13" \
  # S00.1.10 — Imágenes, identificación de páginas, determinismo

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iCCQ" \
  "2026-11-16" "2026-11-18" \
  # S00.1.11 — Modelo de errores

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iCJU" \
  "2026-11-19" "2026-11-20" \
  # S00.1.12 — Rendimiento

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iCTg" \
  "2026-11-23" "2026-11-24" \
  # S00.1.13 — Repetición en Windows x64

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iCbw" \
  "2026-11-25" "2026-11-26" \
  # S00.1.14 — Poppler (contingencia condicional)

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iCkc" \
  "2026-11-27" "2026-12-02" \
  # S00.1.15 — Informe y veredicto S00.1


# ============================================================
# S00.2 — Window / input / latencia
# ============================================================

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iCr4" \
  "2026-12-03" "2026-12-08" \
  # S00.2.01 — Fijar biblioteca de ventana/input

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iCx4" \
  "2026-12-09" "2026-12-14" \
  # S00.2.02 — Prototipo Linux

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iC6w" \
  "2026-12-15" "2026-12-16" \
  # S00.2.03 — Prototipo Windows

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iDL4" \
  "2026-12-17" "2026-12-18" \
  # S00.2.04 — Instrumentación de latencia

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iDR8" \
  "2026-12-21" "2026-12-21" \
  # S00.2.05 — Latencia por proxy en Linux

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iDac" \
  "2026-12-22" "2026-12-23" \
  # S00.2.06 — Latencia por proxy en Windows

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iDss" \
  "2026-12-24" "2026-12-24" \
  # S00.2.08 — Autorepeat

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iD0o" \
  "2026-12-28" "2026-12-29" \
  # S00.2.09 — Pérdida de foco

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iD8E" \
  "2026-12-30" "2026-12-31" \
  # S00.2.10 — KeyEvent

# 2027-01-01 no se usa: Año Nuevo.
set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iEF0" \
  "2027-01-04" "2027-01-05" \
  # S00.2.11 — TextInputEvent (canal separado)

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iDhI" \
  "2027-01-06" "2027-01-07" \
  # S00.2.07 — Medición física extremo a extremo

set_dates \
  "PVTI_lAHOCM6YPc4BlGjFzg9iEPE" \
  "2027-01-08" "2027-01-12" \
  # S00.2.12 — Informe y veredicto S00.2


echo
echo "✓ Fechas actualizadas."
