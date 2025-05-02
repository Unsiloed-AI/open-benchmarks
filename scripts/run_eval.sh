#!/bin/bash
set -e

# Set working directory to the project root regardless of where the script is called from
cd "$(dirname "$0")/.."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Display usage information
function show_usage {
    echo -e "${YELLOW}Usage:${NC} $0 [options]"
    echo ""
    echo "Options:"
    echo "  --inference-only     Only run inference with Qwen2VL, skip evaluation"
    echo "  --skip-inference     Skip running inference, only evaluate existing predictions"
    echo "  --model MODEL_NAME   Evaluate only a specific model (e.g., qwen2vl)"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                   # Run both inference and evaluation"
    echo "  $0 --inference-only  # Only run inference"
    echo "  $0 --model qwen2vl   # Run inference and evaluation only for qwen2vl"
    echo ""
}

# Process command line arguments
ARGS=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --inference-only)
            ARGS="$ARGS --inference-only"
            shift
            ;;
        --skip-inference)
            ARGS="$ARGS --skip-inference"
            shift
            ;;
        --model)
            if [[ -z "$2" || "$2" == --* ]]; then
                echo -e "${YELLOW}Error:${NC} --model requires a model name"
                show_usage
                exit 1
            fi
            ARGS="$ARGS --model $2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Unknown option:${NC} $1"
            show_usage
            exit 1
            ;;
    esac
done

# Print execution information
echo -e "${GREEN}Running evaluation with arguments:${NC} $ARGS"

# Execute the evaluation script
python -m evaluation.eval_helper $ARGS

echo -e "${GREEN}Evaluation completed.${NC}"
