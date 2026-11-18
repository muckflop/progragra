import csv


from flask import Flask, render_template, request
app = Flask(__name__)


def load_data():
        with open("data.csv", mode="r", encoding="utf-8") as f:
             reader = csv.DictReader(f)
             headers = reader.fieldnames
             data = list(reader)
        return headers, data

def filter_data(data, header):
     diets = request.args.get("diet","")
     seasons = request.args.get("season","")
     gluten = request.args.get("glu","")
     lactose = request.args.get("lac","")
     taste = request.args.get("tas","")
     prices = request.args.get("price","")
     time = request.args.get("time","")
     filtered = []
     for row in data:
          if diets and row.get("Diet") != diets:
               continue
          if seasons and row.get("Season") != seasons:
               continue
          if gluten and row.get("Gluten free") != gluten:
               continue
          if lactose and row.get("Lactose free") != lactose:
               continue
          if taste and row.get("Taste") != taste:
               continue
          if prices and row.get("Price") != prices:
               continue
          if time and row.get("Time") != time:
               continue
          filtered.append(row)
     return filtered


@app.get("/")
def index():
    headers, data = load_data()
    filtered_data = filter_data(data, headers)
    
    diets = sorted({row["Diet"] for row in data if row.get("Diet")})
    seasons = sorted({row["Season"] for row in data if row.get("Season")})
    gluten = sorted({row["Gluten free"] for row in data if row.get("Gluten free")})
    lactose = sorted({row["Lactose free"] for row in data if row.get("Lactose free")})
    taste = sorted({row["Taste"] for row in data if row.get("Taste")})
    prices = sorted({row["Price"] for row in data if row.get("Price")})
    time = sorted({row["Time"] for row in data if row.get("Time")})
    

    return render_template("index.html",
                           data = filtered_data,
                           headers=headers,
                           diets=diets,
                           seasons=seasons,
                           gluten=gluten,
                           lactose=lactose,
                           taste=taste,
                           prices=prices,
                           time=time,
                           selected_diet=request.args.get("diet",""),
                           selected_season=request.args.get("season", ""),
                           selected_gluten=request.args.get("glu", ""),
                           selected_lactose=request.args.get("lac", ""),
                           selected_taste=request.args.get("tas",""),
                           selected_prices=request.args.get("price", ""),
                           selected_time=request.args.get("time", ""),
                           total=len(filtered_data),
                           original_total=len(data))

if __name__ == "__main__":
    app.run(debug=True)