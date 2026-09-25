"""
run_all.py
==========
Convenience runner: runs all four chemical models back to back and prints
a final side-by-side comparison table. Each model also runs fine on its
own (`python model_pfna.py`, etc) -- use this only if you want to leave
the whole thing running unattended.

Total runtime: roughly 15-20 minutes on a typical laptop CPU (PFOA alone
is 8-12 of those minutes; the other three are each a few minutes).
"""

import subprocess
import sys
import time

SCRIPTS = ["model_pfna.py", "model_pfhxs.py", "model_pfos.py", "model_pfoa.py"]  # fastest first

PUBLISHED = {
    "model_pfna.py": ("PFNA", 2.31, 1.62, 3.15),
    "model_pfhxs.py": ("PFHxS", 8.47, 5.69, 13.46),
    "model_pfos.py": ("PFOS", 3.41, 2.63, 4.40),
    "model_pfoa.py": ("PFOA", 3.15, 2.62, 3.74),
}

if __name__ == "__main__":
    t0 = time.time()
    for script in SCRIPTS:
        print(f"\n{'#'*70}\n# Running {script}\n{'#'*70}\n")
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"\n*** {script} exited with an error (code {result.returncode}). Stopping. ***")
            sys.exit(1)

    print(f"\n\nAll four models finished in {time.time()-t0:.0f}s total.")
    print("Each model printed its own half-life estimate above; each also saved a")
    print(".nc posterior file and a .png diagnostic plot in this folder.")
    print("\nSee README.md's 'Results you should expect' table for the published")
    print("comparison values and how close a match is expected for each chemical.")
