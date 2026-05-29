# build_web.py
# Build Echo Shift for browser using pygbag.
#
# Usage:
#   python build_web.py          # build only
#   python build_web.py --serve  # build and open in browser for testing

import os
import subprocess
import sys
import webbrowser
import time
import threading


def open_browser(url, delay=2):
    """Open browser after a short delay to let the server start."""
    time.sleep(delay)
    webbrowser.open(url)


def main():
    serve = "--serve" in sys.argv

    print("=== Echo Shift Web Build ===")
    print()

    # Force UTF-8 mode (required on Chinese Windows systems)
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    # Install dependencies
    print("[1/3] Installing dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "pygame-ce>=2.5.0", "pygbag>=0.9.0"],
        check=True,
    )
    print()

    # Build
    print("[2/3] Building web version with pygbag...")
    if serve:
        # Local testing: serve and open browser
        print("Starting local server...")
        print("Press Ctrl+C to stop.")
        print()
        url = "http://localhost:8000"
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()
        subprocess.run(
            [sys.executable, "-m", "pygbag", "--ume_block", "0", "."],
            cwd=".",
            env=env,
        )
    else:
        # Production build
        subprocess.run(
            [sys.executable, "-m", "pygbag", "--build", "--ume_block", "0", "."],
            cwd=".",
            env=env,
            check=True,
        )
        print()
        print("[3/3] Build complete!")
        print()
        print("Output directory: build/web/")
        print("Files ready for deployment:")
        print("  - build/web/index.html")
        print("  - build/web/ (wasm + js + data files)")
        print()
        print("To deploy to GitHub Pages:")
        print("  1. Copy contents of build/web/ to your gh-pages branch")
        print("  2. Push to GitHub")
        print()
        print("To test locally:")
        print("  python build_web.py --serve")


if __name__ == "__main__":
    main()
