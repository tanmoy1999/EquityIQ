# justfile

# Default task
default:
    check-api-key

# Check that API_KEY is set
check-api-key:
    if [ -z "{{ env_var("API_KEY") }}" ]; then \
        echo "❌ API_KEY is not set"; \
        exit 1; \
    else \
        echo "✅ API_KEY is present"; \
    fi

# Run the app (after checking)
run:
    just check-api-key
    python main.py
