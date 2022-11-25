from flask import Flask,render_template,request
import pandas as pd
import pickle



product_dict= pickle.load(open("product_dict.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
sample_data = pd.DataFrame(product_dict)

def match(product):
    p1_name=product
    p1_index=sample_data[sample_data["product_name"]==product].index[0]
    p1_retail_price=sample_data.iloc[p1_index].retail_price
    p1_discounted_price=sample_data.iloc[p1_index].discounted_price
    
    distances=similarity[p1_index]
    product_lists=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    products=[]
    for i in product_lists:
        if sample_data.iloc[i[0]].product_name[-1]!=product[-1]:
            products.append(sample_data.iloc[i[0]].product_name)
    p2_name=products[0]
    p2_index=sample_data[sample_data["product_name"]==products[0]].index[0]
    p2_retail_price=sample_data.iloc[p2_index].retail_price
    p2_discounted_price=sample_data.iloc[p2_index].discounted_price
    
    final_products=[[p1_name,p1_retail_price,p1_discounted_price],[p2_name,p2_retail_price,p2_discounted_price]]
    
    return final_products


app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("product.html",res=sample_data["product_name"].values)

@app.route("/action",methods=["POST"])
def action():
    product_1=request.form["product"]
    final_products=match(product_1)
    return render_template("show.html",final_products=final_products)

# @app.route("/movie1/<movie>",methods=["GET"])
# def movie1(movie):
#     title, tagline, runtime, popularity, overview, full_path=featch_movie_details(movie)
#     return render_template("show_details.html",title=title,tagline=tagline,runtime=runtime,popularity=popularity,overview=overview,poster=full_path)

# @app.route("/movie2/<movie>",methods=["GET"])
# def movie2(movie):
#     title, tagline, runtime, popularity, overview, full_path=featch_movie_details(movie)
#     return render_template("show_details.html",title=title,tagline=tagline,runtime=runtime,popularity=popularity,overview=overview,poster=full_path)

# @app.route("/movie3/<movie>",methods=["GET"])
# def movie3(movie):
#     title, tagline, runtime, popularity, overview, full_path=featch_movie_details(movie)
#     return render_template("show_details.html",title=title,tagline=tagline,runtime=runtime,popularity=popularity,overview=overview,poster=full_path)

# @app.route("/movie4/<movie>",methods=["GET"])
# def movie4(movie):
#     title, tagline, runtime, popularity, overview, full_path=featch_movie_details(movie)
#     return render_template("show_details.html",title=title,tagline=tagline,runtime=runtime,popularity=popularity,overview=overview,poster=full_path)

# @app.route("/movie5/<movie>",methods=["GET"])
# def movie5(movie):
#     title, tagline, runtime, popularity, overview, full_path=featch_movie_details(movie)
#     return render_template("show_details.html",title=title,tagline=tagline,runtime=runtime,popularity=popularity,overview=overview,poster=full_path)

if __name__ =="__main__":
    app.run(debug=True)