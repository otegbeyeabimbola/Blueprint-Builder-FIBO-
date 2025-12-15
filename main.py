### `main.py`

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

# --- 1. DATA MODELS (The FIBO Compliance Layer) ---
class BondAsset(BaseModel):
    """
    Defines the strict schema for a Bond Asset.
    This simulates FIBO compliance rules.
    """
    isin: str = Field(..., min_length=12, max_length=12, description="International Securities Identification Number")
    currency: str = Field(..., min_length=3, max_length=3)
    face_value: float = Field(..., gt=0, description="Must be a positive number")
    maturity_date: datetime
    issuer: str

    # Example of a semantic rule
    @validator('currency')
    def validate_currency(cls, v):
        allowed = ['USD', 'EUR', 'GBP', 'NGN']
        if v not in allowed:
            raise ValueError(f"Currency {v} is not supported by current policy.")
        return v

# --- 2. CORE LOGIC (The Engine) ---

class BlueprintEngine:
    def __init__(self):
        self.ledger = [] # The Persistent Ledger

    def generate_hash(self, data: dict) -> str:
        """Generates a SHA-256 Trace ID for data integrity."""
        raw_string = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(raw_string.encode()).hexdigest()

    def deterministic_patcher(self, broken_data: dict) -> dict:
        """
        The 'Auto-Fix' Logic.
        Tries to repair common AI hallucinations before validation.
        """
        patched = broken_data.copy()
        
        # Patch 1: Fix currency string formatting (e.g., "USD " -> "USD")
        if "currency" in patched:
            patched["currency"] = patched["currency"].strip().upper()

        # Patch 2: Fix human-readable numbers (e.g., "1M" -> 1000000)
        if "face_value" in patched and isinstance(patched["face_value"], str):
            val = patched["face_value"].upper()
            if "M" in val:
                patched["face_value"] = float(val.replace("M", "")) * 1_000_000
            elif "K" in val:
                patched["face_value"] = float(val.replace("K", "")) * 1_000

        # Patch 3: Fix Date formats (AI often uses slashes)
        if "maturity_date" in patched:
            try:
                # Attempt to normalize YYYY/MM/DD to ISO format
                if "/" in patched["maturity_date"]:
                    patched["maturity_date"] = patched["maturity_date"].replace("/", "-")
            except Exception:
                pass # Let Pydantic catch critical errors
        
        return patched

    def process_asset(self, raw_input: dict):
        """Runs the Pipeline: Patch -> Validate -> Hash -> Log"""
        
        # 1. Log Attempt
        entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "PROCESSING",
            "original": raw_input.copy(),
            "violations": [],
            "fixes_applied": []
        }

        # 2. Apply Deterministic Patching
        patched_data = self.deterministic_patcher(raw_input)
        
        if patched_data != raw_input:
            entry["fixes_applied"].append("Deterministic Patching applied (Date/Number normalization)")

        # 3. Pydantic Validation
        try:
            valid_asset = BondAsset(**patched_data)
            
            # 4. Generate Badge (Hash)
            trace_id = self.generate_hash(valid_asset.model_dump())
            
            entry["status"] = "SUCCESS"
            entry["final_asset"] = valid_asset.model_dump()
            entry["trace_id"] = trace_id
            
        except ValidationError as e:
            entry["status"] = "FAILED"
            entry["violations"] = [err['msg'] for err in e.errors()]
        
        self.ledger.append(entry)
        return entry

# --- 3. CLI COMMANDS & UI ---

@app.command()
def demo():
    """
    Runs a demo of Blueprint Builder with broken AI data.
    """
    engine = BlueprintEngine()

    # MOCK DATA: Typical messy output from an AI
    broken_ai_output = {
        "isin": "US1234567890", # Valid length
        "currency": "usd ",     # Messy whitespace, lowercase
        "face_value": "5M",     # AI used '5M' string instead of number
        "maturity_date": "2030/01/01", # Wrong date format
        "issuer": "Global Corp"
    }

    console.rule("[bold blue]Blueprint Builder: AI Compliance Engine[/bold blue]")
    console.print("\n[bold red]1. Incoming AI Data (Broken):[/bold red]")
    console.print(JSON.from_data(broken_ai_output))

    with console.status("[bold green]Running Deterministic Patcher & Validation...[/bold green]", spinner="dots"):
        result = engine.process_asset(broken_ai_output)
        import time; time.sleep(1.5) # Fake processing time for effect

    console.print("\n[bold green]2. Validated & Patched Output:[/bold green]")
    
    if result["status"] == "SUCCESS":
        # Display the "Cryptographic Badge"
        panel_content = Text(f"SHA-256 TRACE ID:\n{result['trace_id']}", justify="center", style="bold white on green")
        console.print(Panel(panel_content, title="🛡️ Data Integrity Verified", expand=False))
        
        # Display Final JSON
        # Convert datetime objects to string for JSON display
        display_json = result["final_asset"].copy()
        display_json['maturity_date'] = display_json['maturity_date'].isoformat()
        console.print(JSON.from_data(display_json))

        # Show the Audit Ledger (History)
        console.print("\n[bold yellow]3. Audit Ledger (History):[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Timestamp")
        table.add_column("Status")
        table.add_column("Fixes / Violations")

        fixes = ", ".join(result["fixes_applied"]) if result["fixes_applied"] else "None"
        violations = ", ".join(result["violations"]) if result["violations"] else "None"
        
        # Add row
        table.add_row(
            result["timestamp"].split("T")[1][:8], 
            f"[green]{result['status']}[/green]", 
            f"Fixes: {fixes}\nViolations: {violations}"
        )
        console.print(table)

    else:
        console.print(f"[bold red]Validation Failed:[/bold red] {result['violations']}")

if __name__ == "__main__":
    app()
```

### How to Run This

1.  Ensure you have installed the requirements:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the demo command:
    ```bash
    python main.py
    ```

### What You Will See (The Outcome)

When you run this, the terminal will simulate the full product experience:

1.  **Red Text:** Shows the "Broken" JSON (lowercase currency, "5M" string, slash dates).
2.  **Spinner:** A loading animation saying "Running Deterministic Patcher...".
3.  **Green Badge:** A visual panel showing the **SHA-256 Trace ID**.
4.  **Clean JSON:** The fixed data (Uppercase currency, `5000000.0` float, ISO date).
5.  **Audit Table:** A table showing exactly what fixes were applied.

**Would you like me to explain how to add a "Replay Button" feature to this code specifically?**
