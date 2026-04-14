import os
import json

def build_static_stlite_dashboard():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to your Streamlit logic and datasets
    app_path = os.path.join(base_dir, "system_failure_v14", "system_failure_v13", "system_failure_v12", "system_failure_v6", "app.py")
    csv_path = os.path.join(base_dir, "system_failure_v14", "system_failure_v13", "system_failure_v12", "system_failure_v6", "CMOS_Battery_Failure_Dataset.csv")
    output_html = os.path.join(base_dir, "index.html")

    # Read exactly what the user wrote in app.py
    with open(app_path, "r", encoding="utf-8") as f:
        app_code = f.read()

    # CRITICAL: WebAssembly (Pyodide) strictly does not support multiprocessing! 
    # n_jobs=-1 causes a crash in browser, so we MUST replace it natively with n_jobs=None
    app_code = app_code.replace("n_jobs=-1", "n_jobs=None")

    # Read the dataset securely to inject into Virtual FS
    with open(csv_path, "r", encoding="utf-8") as f:
        csv_data = f.read()

    # The magic of Stlite (Streamlit in the Browser via WebAssembly)
    html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>CMOS Failure Analysis Report</title>
    <!-- Stlite CSS for exact Streamlit styling -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.50.0/build/stlite.css" />
    <style>
      body, html {{
        margin: 0; padding: 0; height: 100%; width: 100%;
        background-color: #0e1117; /* Default Streamlit Dark Background */
      }}
      #root {{ height: 100%; min-height: 100vh; }}
    </style>
  </head>
  <body>
    <div id="root"></div>
    <!-- Load Stlite Engine -->
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.50.0/build/stlite.js"></script>
    <script>
      stlite.mount(
        {{
          // Request exact pip dependencies; pinning plotly prevents the pyarrow narwhals bug in Pyodide
          requirements: ["pandas", "numpy", "scikit-learn", "plotly==5.23.0"],
          entrypoint: "app.py",
          // Inject exactly identical file contents securely
          files: {{
            "app.py": {json.dumps(app_code)},
            "CMOS_Battery_Failure_Dataset.csv": {json.dumps(csv_data)}
          }},
        }},
        document.getElementById("root")
      );
    </script>
  </body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Success! Generated `index.html` using Pyodide/Stlite.")
    print("This HTML runs your original Streamlit Python code 100% natively in the browser via WebAssembly!")

if __name__ == "__main__":
    build_static_stlite_dashboard()
