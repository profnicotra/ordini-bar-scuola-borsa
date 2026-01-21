
from flask import Blueprint, render_template, send_file
from .excel_generator import create_excel_cf_generator
import os
import tempfile

bp = Blueprint("index", __name__)

@bp.get("/")
def index():
    data = {"title" : "Bar Scuola Borsa",
        "open": True,   
        "items" : []}
    
    return render_template('index.html', data=data)

@bp.get("/download-excel")
def download_excel():
    """Genera e scarica il file Excel per il Codice Fiscale"""
    try:
        # Crea il file in una cartella temporanea
        temp_dir = tempfile.gettempdir()
        file_path = create_excel_cf_generator(
            os.path.join(temp_dir, "GeneratoreCF.xlsx")
        )
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name="GeneratoreCF_Excel2016.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return {"error": str(e)}, 500