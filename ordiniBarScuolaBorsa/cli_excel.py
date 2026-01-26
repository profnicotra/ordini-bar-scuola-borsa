#!/usr/bin/env python
"""
Script CLI per generare il file Excel del Codice Fiscale
Uso: python -m ordiniBarScuolaBorsa.cli_excel
     oppure: python cli_excel.py
"""

import sys
import os
import argparse
from .excel_generator import create_excel_cf_generator


def main():
    parser = argparse.ArgumentParser(
        description="Genera un file Excel per il Codice Fiscale (compatibile Excel 2016+)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Percorso di output (default: ~/Downloads/GeneratoreCF_TIMESTAMP.xlsx)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Non stampa messaggi a schermo"
    )
    
    args = parser.parse_args()
    
    try:
        file_path = create_excel_cf_generator(args.output)
        
        if not args.quiet:
            print(f"✓ File Excel creato con successo!")
            print(f"📁 Percorso: {file_path}")
            print(f"📊 Formato: Excel 2016+")
            print(f"📝 Contiene: Foglio Codice Fiscale + Istruzioni")
            
        return 0
        
    except Exception as e:
        print(f"❌ Errore: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
