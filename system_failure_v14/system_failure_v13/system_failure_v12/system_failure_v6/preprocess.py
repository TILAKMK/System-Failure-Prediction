import pandas as pd

with open("data/raw_logs.txt", "r") as f:
    logs = [line.strip() for line in f.readlines() if line.strip()]

data = []
for log in logs:
    log_lower = log.lower()
    row = {
        "ERR_DISK":    1 if "disk" in log_lower else 0,
        "ERR_CPU":     1 if "cpu" in log_lower else 0,
        "ERR_MEM":     1 if "memory" in log_lower else 0,
        "ERR_NET":     1 if "network" in log_lower else 0,
        "FAILURE":     1 if any(k in log_lower for k in ["error", "critical", "fail", "leak", "lost", "timeout", "overheating"]) else 0,
    }
    data.append(row)

df = pd.DataFrame(data)
df.to_csv("data/processed_logs.csv", index=False)
print(f"Done. {len(df)} rows. Failures: {df['FAILURE'].sum()}, Normal: {(df['FAILURE']==0).sum()}")
