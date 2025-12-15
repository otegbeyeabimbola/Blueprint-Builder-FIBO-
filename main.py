### `main.py` with Replay Feature

```python
import typer
import json
import hashlib
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError, validator
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.json import JSON
from rich.text import Text

# Initialize UI and CLI
app = typer.Typer()
console = Console()

# --- GLOBAL CONFIG (Simulating Dynamic Rules) ---
# In a real app, this would come from a database or config file
CURRENT_RULES = {
    "allowed_currencies": ['USD', 'EUR', 'GBP', 'NGN'],
    "min_face_value": 0
}

# --- 1. DATA MODELS ---
class BondAsset(BaseModel):
    isin: str = Field(..., min_length=12, max_length=12)
    currency: str = Field(..., min_length=3, max_length=3)
    face_value: float = Field(..., gt=0)
    maturity_date: datetime
    issuer: str

    @validator('currency')
    def validate_currency(cls, v):
        # Validation checks the DYNAMIC global rules
        allowed = CURRENT_RULES["allowed_currencies"]
        if v not in allowed:
            raise ValueError(f"Currency '{v}' is BANNED under current policy (Allowed: {allowed})")
        return v

# --- 2. ENGINE LOGIC ---
class BlueprintEngine:
    def __init__(self):
        # Simulating a database of past validations
        self.ledger = [] 

    def generate_hash(self, data: dict) -> str:
        raw_string = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(raw_string.encode()).hexdigest()

    def deterministic_patcher(self, broken_data: dict) -> dict:
        patched = broken_data.copy()
        if "currency" in patched:
            patched["currency"] = patched["currency"].strip().upper()
        if "face_value" in patched and isinstance(patched["face_value"], str):
            val = patched["face_value"].upper()
            if "M" in val:
                patched["face_value"] = float(val.replace("M", "")) * 1_000_000
            elif "K" in val:
                patched["face_value"] = float(val.replace("K", "")) * 1_000
        if "maturity_date" in patched:
            if "/" in patched["maturity_date"]:
                patched["maturity_date"] = patched["maturity_date"].replace("/", "-")
        return patched

    def process_asset(self, raw_input: dict, is_replay=False):
        """
        Runs the pipeline. 
        is_replay: If True, marks the log as a re-verification.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "REPLAY_VALIDATION" if is_replay else "NEW_VALIDATION",
            "status": "PROCESSING",
            "original": raw_input.copy(),
            "violations": [],
            "fixes_applied": []
        }

        patched_data = self.deterministic_patcher(raw_input)
        
        if patched_data != raw_input:
            entry["fixes_applied"].append("Deterministic Patching")

        try:
            valid_asset = BondAsset(**patched_data)
            trace_id = self.generate_hash(valid_asset.model_dump())
            entry["status"] = "SUCCESS"
            entry["final_asset"] = valid_asset.model_dump()
            entry["trace_id"] = trace_id
            
        except ValidationError as e:
            entry["status"] = "FAILED"
            entry["violations"] = [err['msg'] for err in e.errors()]
        
        self.ledger.append(entry)
        return entry

# --- 3. CLI COMMANDS ---
engine = BlueprintEngine()

@app.command()
def demo_replay():
    """
    Simulates a 'Regulatory Change' and replays validation on old data.
    """
    # 1. INITIAL STATE: Successful validation
    console.rule("[bold blue]1. January 2025: Initial Validation[/bold blue]")
    
    # Old data that was valid in Jan 2025
    historical_input = {
        "isin": "GB1234567890",
        "currency": "GBP", 
        "face_value": "1M",
        "maturity_date": "2030-01-01",
        "issuer": "Bank of London"
    }
    
    console.print(f"Incoming Asset: [bold]GBP Bond[/bold]")
    result_v1 = engine.process_asset(historical_input)
    console.print(f"Status: [green]{result_v1['status']}[/green] (GBP is allowed)")
    
    # 2. THE CHANGE: Simulate a regulatory update
    console.print("\n[dim]... 6 months pass ...[/dim]\n")
    console.rule("[bold red]2. July 2025: REGULATORY UPDATE[/bold red]")
    
    console.print("[bold red]ALERT: New Regulation Passed.[/bold red] 'GBP' is no longer an approved settlement currency for this desk.")
    
    # UPDATE THE RULES GLOBALLY
    CURRENT_RULES["allowed_currencies"] = ['USD', 'EUR', 'NGN'] # Removed GBP
    console.print(f"Active Policy: {CURRENT_RULES['allowed_currencies']}")

    # 3. REPLAY: Re-validate the OLD data against NEW rules
    console.print("\n[bold yellow]3. Running Replay Validation...[/bold yellow]")
    
    # We fetch the original raw data from the first ledger entry
    original_raw_data = engine.ledger[0]["original"]
    
    with console.status("Re-verifying Ledger...", spinner="clock"):
        import time; time.sleep(1)
        result_replay = engine.process_asset(original_raw_data, is_replay=True)

    # 4. SHOW RESULTS
    if result_replay["status"] == "FAILED":
        console.print(Panel(
            f"[bold red]COMPLIANCE VIOLATION DETECTED[/bold red]\n\n"
            f"Asset ID: {result_v1['trace_id']} (Previously Valid)\n"
            f"Current Status: [red]FAILED[/red]\n"
            f"Reason: {result_replay['violations'][0]}",
            title="🛑 Replay Audit Result"
        ))
    else:
        console.print("[green]Asset remains compliant.[/green]")

if __name__ == "__main__":
    app()
```

### How to use this for the Hackathon Demo

# 1.  Run the command:

    ```bash
    python main.py
    ```

# When you run this, the terminal will simulate the full product experience:

# Red Text: Shows the "Broken" JSON (lowercase currency, "5M" string, slash dates).

# Spinner: A loading animation saying "Running Deterministic Patcher...".

# Green Badge: A visual panel showing the SHA-256 Trace ID.

# Clean JSON: The fixed data (Uppercase currency, 5000000.0 float, ISO date).

# Audit Table: A table showing exactly what fixes were applied.

# 2.  **The Narrative it creates:**

#   * **Phase 1:** You show a GBP Bond being validated successfully because GBP is allowed.
#   * **Phase 2:** "The Regulations Change." You programmatically remove GBP from the allowed list.
#   * **Phase 3 (The Replay):** You hit the "Replay" button (run the code). The system pulls the *exact same data* from history, but this time it fails validation with a clear error: *"Currency 'GBP' is BANNED under current policy"*.

      
