import requests

from config import Config

GITHUB_HEADERS={

    "Accept":"application/vnd.github+json", #kabul edilecek verş formatını ayarlama
    "Authorization": f"Bearer {Config.GITHUB_TOKEN}" #veri alırken doğrulama için access tokenı kullanma
}

def search_users(query): # kullanıcıyı arayacak fonksiyon
    #Bakcenddeki app.py den aldığı query sorgu yapısını GitHUB RESTAPI ye sorgu atar sonucu geri app.py ye döner
    #gelen kelimeye göre arama sonucunda kişilerin bilgilerini filtreleyrek soncuu app.py ye döner
    #oradan templet da listelenme üzere gönderilir

    api_url=f"{Config.GITHUB_API_BASE_URL}/search/users" #kullanıcı arama için kullanılacak apı endpointi

    query_params={
        "q":query, # kullanıcı adı
        "per_page":10 #max sonuç sayısı

    }

    #GitHub API ye HTTP GET isteği gönderme

    try:

        response=requests.get(
            api_url, #endpoint
            headers=GITHUB_HEADERS,#gerekli bağımlılıklar
            params=query_params, #parametreler
            timeout=5 #zaman aşımı

        )

    except requests.RequestException:
        #ağ hataları vs

        return []
    
    if response.status_code != 200: # sonuç başarılı değilse

        return []
    
    response_data= response.json() # json veriyi gönderme


    items=response_data.get("items",[]) #gelen ham veriyi alma

    users=[]

    for item in items: #verinin ayırştırılması listede gösterileceği için fotoğraf kullanıcı adı hesap türü
        user={
            "username": item.get("login"),
            "avatar":item.get("avatar_url"),
            "type":item.get("type")
        }
        users.append(user)


    return users



def get_user(username):

    #gelen kullancıı adını apı dena rar kullanıcnın bilgilerini filtreleyerke geri backende döner

    api_url=f"{Config.GITHUB_API_BASE_URL}/users/{username}" 

    try:

        response= requests.get(
            api_url,
            headers=GITHUB_HEADERS,
            timeout=5
        )

    except requests.RequestException:


        return None
    
    if response.status_code != 200:
        # kullanıcı yok, rate limit, yetki hatası vb.
        return None
    
    data=response.json()

    user = {
        "username": data.get("login"),
        "name": data.get("name"),
        "avatar": data.get("avatar_url"),
        "bio": data.get("bio"),
        "location": data.get("location"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "public_repos": data.get("public_repos"),
        "profile_url": data.get("html_url"),
        "repos_api_url": data.get("repos_url"),
        "blog": data.get("blog"),
        "created_at": data.get("created_at")
    } #filtrelenerek verinin gönderimi

    return user


def get_user_repos(username):

    #kullanıcı detayında repo tarafına tıklandığında repo bilfilerini liste şeklinde göstermek
    #için yazılan api fonksiyonu

    api_url = f"{Config.GITHUB_API_BASE_URL}/users/{username}/repos"

    params={

        "per_page": 100,
        "sort":"updated"
    }# ilk 100 repo güncele göre sıralanıp alınır github restapi daha fazlasını vermez paginaiton uygular


    try:

        response=requests.get(
            api_url,
            headers=GITHUB_HEADERS,
            params=params,
            timeout=5
        )
    
    except requests.RequestException:

        return []

    if response.status_code != 200: # başarılı sonuç dönmeidyse

        return []
    
    repos = []

    for repo in response.json():
            repos.append({
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "is_fork": repo.get("fork"),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "html_url": repo.get("html_url"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count")
            })
    
    return repos