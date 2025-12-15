### 📄 main.py

```python
import json
import hashlib
import re
import sys
from datetime import datetime
from typing import List, Optional, Union, Any
from pathlib import Path
from uuid import uuid4

import typer
from pydantic import BaseModel, Field, ValidationError, field_validator
from rich.console import Console
from rich.table import Table

# Initialize App and Console
app = typer.Typer()
console = Console()

# --- 1. FIBO SCHEMA DEFINITIONS (Pydantic) ---

class FinancialAsset(BaseModel):
    asset_id: str = Field(..., min_length=5, description="Unique identifier, uppercase required")
    asset_type: str = Field(..., pattern="^(Stock|Bond|Derivative|FX)$")
    issuer_name: str = Field(..., min_length=5)
    price: float = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    maturity_date: Optional[datetime] = None
    required_docs: List[str] = Field(default_factory=list)

    @field_validator('asset_id')
    def enforce_uppercase(cls, v):
        if not v.isupper():
            raise ValueError('Asset ID must be uppercase')
        return v

# --- 2. DETERMINISTIC PATCHER ENGINE ---

class PatchEngine:
    """
    Analyzes raw dictionary data and attempts to fix common AI hallucinations
    or formatting errors deterministically.
    """
    
    @staticmethod
    def fix_dates(data: dict) -> dict:
        """Fixes slash-formatted dates to ISO format."""
        for key, val in data.items():
            if "date" in key or key == "maturity":
                if isinstance(val, str) and "/" in val:
                    try:
                        # Convert YYYY/MM/DD to ISO
                        dt = datetime.strptime(val, "%Y/%m/%d")
                        data[key] = dt.isoformat()
                        console.print(f"[yellow]🔧 Patched date format for field '{key}'[/yellow]")
                    except ValueError:
                        pass
        return data

    @staticmethod
    def fix_numbers(data: dict) -> dict:
        """Converts human-readable number strings (e.g., '1M') to floats."""
        for key, val in data.items():
            if isinstance(val, str):
                # Handle 'k' (thousands) and 'M' (millions)
                if re.match(r"^\d+(\.\d+)?[kKmM]$", val):
                    multiplier = 1000 if val.lower().endswith('k') else 1000000
                    num_part = float(val[:-1])
                    data[key] = num_part * multiplier
                    console.print(f"[yellow]🔧 Patched number string '{val}' to {data[key]} for field '{key}'[/yellow]")
        return data

    @staticmethod
    def fix_uppercase(data: dict) -> dict:
        """Enforces uppercase for known ID fields."""
        if 'asset_id' in data and isinstance(data['asset_id'], str):
            if not data['asset_id'].isupper():
                data['asset_id'] = data['asset_id'].upper()
                console.print(f"[yellow]🔧 Patched casing for asset_id[/yellow]")
        return data

    @classmethod
    def run(cls, data: dict) -> dict:
        data = cls.fix_dates(data)
        data = cls.fix_numbers(data)
        data = cls.fix_uppercase(data)
        return data

# --- 3. CRYPTOGRAPHIC UTILS ---

def generate_trace_id(data: dict) -> str:
    """Generates a SHA-256 hash of the canonicalized JSON string."""
    canonical_json = json.dumps(data, sort_keys=True)
    return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

def append_to_ledger(record: dict, filename: str = "ledger.json"):
    """Appends the validated record to an immutable ledger file."""
    ledger_path = Path(filename)
    if not ledger_path.exists():
        with open(ledger_path, 'w') as f:
            json.dump([], f)
    
    with open(ledger_path, 'r+') as f:
        try:
            current_data = json.load(f)
        except json.JSONDecodeError:
            current_data = []
        
        current_data.append(record)
        f.seek(0)
        json.dump(current_data, f, indent=2)

# --- 4. CLI COMMANDS ---

@app.command()
def build(
    input_file: Path = typer.Option(..., "--input", "-i", help="Path to input JSON file"),
    fix: bool = typer.Option(False, "--fix", "-f", help="Attempt to auto-patch errors"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Path to save validated output")
):
    """
    Validates, Patches, and Certifies financial assets from raw JSON.
    """
    console.print(f"[bold blue]🏗️  Blueprint Builder v1.0[/bold blue]")
    
    # 1. Load Data
    try:
        with open(input_file, 'r') as f:
            raw_data = json.load(f)
    except Exception as e:
        console.print(f"[bold red]❌ Error loading file:[/bold red] {e}")
        raise typer.Exit(code=1)

    # 2. Validation Loop
    valid_asset = None
    try:
        # First attempt
        valid_asset = FinancialAsset(**raw_data)
        console.print("[green]✅ Data is valid on first pass.[/green]")

    except ValidationError as e:
        console.print("[bold red]🚫 Validation Failed:[/bold red]")
        for err in e.errors():
            console.print(f" - {err['loc'][0]}: {err['msg']}")
        
        if not fix:
            console.print("\n[dim]Run with --fix to attempt auto-correction.[/dim]")
            raise typer.Exit(code=1)
        
        # 3. Patching
        console.print("\n[bold cyan]🔧 Attempting Deterministic Patching...[/bold cyan]")
        patched_data = PatchEngine.run(raw_data.copy())
        
        try:
            valid_asset = FinancialAsset(**patched_data)
            console.print("[bold green]✅ Patch Successful! Asset is now compliant.[/bold green]")
        except ValidationError as final_e:
            console.print("[bold red]❌ Auto-fix failed. Manual intervention required.[/bold red]")
            raise typer.Exit(code=1)

    # 4. Certification & Hashing
    final_dict = valid_asset.model_dump(mode='json')
    trace_id = generate_trace_id(final_dict)
    
    certified_record = {
        "trace_id": trace_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "VALIDATED",
        "method": "AUTO_PATCHED" if fix else "DIRECT",
        "data": final_dict
    }

    # 5. Output
    console.print("\n[bold]📜 Certified Asset Record:[/bold]")
    console.print_json(data=certified_record)

    # 6. Save to Ledger
    append_to_ledger(certified_record)
    console.print(f"[dim]💾 Recorded to ledger.json[/dim]")

    if output:
        with open(output, 'w') as f:
            json.dump(certified_record, f, indent=2)
        console.print(f"[blue]📁 Saved certified output to {output}[/blue]")

@app.command()
def history():
    """View the validation ledger."""
    if not Path("ledger.json").exists():
        console.print("[yellow]No history found.[/yellow]")
        return

    with open("ledger.json", 'r') as f:
        data = json.load(f)

    table = Table(title="Validation Ledger")
    table.add_column("Trace ID", style="cyan", no_wrap=True)
    table.add_column("Timestamp", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Price", style="white")

    for item in data[-5:]: # Show last 5
        asset = item['data']
        table.add_row(
            item['trace_id'][:8] + "...", 
            item['timestamp'][:19], 
            asset['asset_type'], 
            f"${asset['price']:,.2f}"
        )

    console.print(table)

if __name__ == "__main__":
    app()
