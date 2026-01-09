from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
def admin():
    

    data = {"title" : "Amministrazione Bar Scuola Borsa",
        "open": True,   
        "items" : []}

    return render_template("admin.html", data=data)
#     with open("C:\\Users\\24-info-22\\Desktop\\ANNO 25-26\\Linguaggi di programmazione\\ordini-bar-scuola-borsa\\ordiniBarScuolaBorsa\\products.json", "w") as products:
#         data.append(newProduct)
#         json.dump(data, products)
