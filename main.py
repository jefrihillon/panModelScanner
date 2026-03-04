import sys
from web_app import app

def main():
    print("Hello from airs-api!")
    print("Starting web interface...")
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

def run_cli():
    # Import and run the original CLI version
    from scan_hf_models import run_scan
    run_scan()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        main()
