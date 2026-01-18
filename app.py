from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from api import search_users ,get_user, get_user_repos

app= Flask(__name__)
app.config.from_object(Config)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/search" , methods=["POST"])
def search():

    #anasayfa arama doğrudan çıksın ekranda

        query = request.form.get("query", "").strip() #sorgulancak kulalnıcı adı aranması

        if not query : #form boş mu dolu mu kontorlü
             flash ("Lütfen aramak istediğiniz kişi bilgisini girin!","warning")
             return redirect(url_for("index"))
        
        #api.py den arama ve sonuçları alma

        try:

            users=search_users(query)
        
        except Exception:

            flash("GitHub Servisine Bağlanırken Bir Sorun Oluştu !!!","danger")
            return redirect(url_for("index"))

        if not users: #geri dönen sonuç yoksa

            flash("Arama ile Eşleşen Kullanıcı Bulunamadı !!!","danger")
            return redirect(url_for("index"))
        
        return render_template("results.html",users=users) #sonuç vasra gönderilir template a



@app.route("/user/<username>")
def user_detail(username):
    
    #kullanıcının profil detaularının olduğu yer 

    user=get_user(username)

    
    if not user: #apı hatalı veya boş dönerse
         
         flash("Kullanıcı Bilgileri Bulunamadı","danger")
         return redirect(url_for("index"))
    
    return render_template("user.html",user=user)


@app.route("/user/<username>/repos")
def repos(username):
     
    repos= get_user_repos(username)

    if not repos:

        flash("Repository Bilgileri Bulunamadı !!!","danger")

        return redirect(url_for("user_detail",username=username))
    
    repo_limit_warning= False #eğer 100 den fazla repo varsa uyarı için başlangıçta false değişken tanımı

    if len(repos) == 100:
          repo_limit_warning = True
        
    return render_template("repos.html",repos=repos, username=username , repo_limit_warning=repo_limit_warning)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":

    app.run(debug=True)