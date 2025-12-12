from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
def admin():
    

   # with open("C:\\Users\\24-info-22\\Desktop\\ANNO 25-26\\Linguaggi di programmazione\\ordini-bar-scuola-borsa\\ordiniBarScuolaBorsa\\products.json", "r") as products:
   #     data = json.load(products)

    #data.update("id:3")
    
    #with open ("C:\\Users\\24-info-22\\Desktop\\ANNO 25-26\\Linguaggi di programmazione\\ordini-bar-scuola-borsa\\ordiniBarScuolaBorsa\\products.json", "w"):
    #    json.dump(data)
        

    #print(data)

    return render_template("admin.html")
#     with open("C:\\Users\\24-info-22\\Desktop\\ANNO 25-26\\Linguaggi di programmazione\\ordini-bar-scuola-borsa\\ordiniBarScuolaBorsa\\products.json", "w") as products:
#         data.append(newProduct)
#         json.dump(data, products)
