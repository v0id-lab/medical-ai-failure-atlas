#!/usr/bin/env bash
# MedFailBench Weekly Model Evaluation Runner
# Hedef: haftada 1 model seti çalıştır, skorla, rapora ekle
# Durum: TASLAK — gerçek API key ve model listesi G onayıyla doldurulacak
# Issue #185
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
DATE_TAG=$(date +%Y%m%d)
OUTPUT_DIR="$REPO_DIR/model_runs/weekly_${DATE_TAG}"
mkdir -p "$OUTPUT_DIR"

echo "=== MedFailBench Weekly Eval: $DATE_TAG ==="

# TODO: OpenRouter API key — .env'den oku veya G'den al
# OPENROUTER_KEY="${OPENROUTER_KEY:-}"

# TODO: model listesini doldur
MODELS=(
  "deepseek/deepseek-v4-flash"
  "qwen/qwen-2.5-7b-instruct"
  "meta-llama/llama-3.3-70b-instruct"
)

# TODO: prompt setini oku
PROMPTS_DIR="$REPO_DIR/data/prompts"
# ls "$PROMPTS_DIR"/*.json

echo "Models: ${MODELS[*]}"
echo "Output: $OUTPUT_DIR"
echo "Script skeleton — fill API key and prompt paths before running"

# python3 "$SCRIPT_DIR/score_outputs.py" "$OUTPUT_DIR"
# python3 "$SCRIPT_DIR/generate_weekly_report.py" "$OUTPUT_DIR" >> "$REPO_DIR/docs/MEDFAILBENCH_WEEKLY_MODEL_RESPONSE_EVAL_${DATE_TAG}.md"

exit 0