#IMPORTING REQUIRED MODULES
import concurrent.futures
from bs4 import BeautifulSoup
import requests


def Get_Movie_Data(movie):
    movie_name = movie.a.text
    year = movie.span.text[1:-1]

    #REDIRECTING TO THE SPECIFIC MOVIE PAGE USING THE HYPERLINK ON THE TITLE
    url = "https://www.imdb.com/"+movie.a["href"]      

    #GETTING RESPONSE FROM THE MOVIE PAGE AND PARSING IT
    page2 = requests.get(url).text         
    soup2 = BeautifulSoup(page2)            

    #EXTRACTIING REQUIRED DATA
    rating = soup2.find("span", class_ = "AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV").text
    genre = soup2.find("span", class_ = "ipc-chip__text").text
    desc = soup2.find("span", class_ = "GenresAndPlot__TextContainerBreakpointXS_TO_M-sc-cum89p-0 kHlJyu").text
    director = soup2.find("a", class_ = "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
    nominations = soup2.find("span", class_ = "ipc-metadata-list-item__list-content-item").text
    language = soup2.find("li", {"class": "ipc-metadata-list__item", "data-testid": "title-details-languages"}).a.text
    temp_runtime = soup2.find("li", {"class": "ipc-metadata-list__item", "data-testid": "title-techspec_runtime"})
    runtime = temp_runtime.find("div", class_ = "ipc-metadata-list-item__content-container").text
    temp_budget = soup2.find("li", {"class": "ipc-metadata-list__item BoxOffice__MetaDataListItemBoxOffice-sc-40s2pl-2 gwNUHl", "data-testid": "title-boxoffice-budget"})
    budget = "Not Available"
    #SINCE BUDGET IS NOT AVAILABLE FOR SOME MOVIES, APPLYING CONDITION.
    if temp_budget:
        budget = temp_budget.find("span", class_ = "ipc-metadata-list-item__list-content-item").text.split()[0]

    temp_gross = soup2.find("li", {"class": "ipc-metadata-list__item BoxOffice__MetaDataListItemBoxOffice-sc-40s2pl-2 gwNUHl", "data-testid": "title-boxoffice-cumulativeworldwidegross"})
    gross = "Not Available"
    #SINCE GROSS IS NOT AVAILABLE FOR SOME MOVIES, APPLYING CONDITION.
    if temp_gross:
        gross = temp_gross.find("span", class_ = "ipc-metadata-list-item__list-content-item").text.split()[0]

    #WRITING THE GATHERED DATA INTO THE FILE CREATED IN THE BEGINNING.
    f.write(f"Name: {movie_name} \n")
    f.write(f"Year: {year} \n")
    f.write(f"Rating: {rating} \n")
    f.write(f"Genre: {genre} \n")
    f.write(f"Director: {director} \n")
    f.write(f"Language: {language} \n")
    f.write(f"Runtime: {runtime} \n")
    f.write(f"Description: {desc} \n")
    f.write(f"Estimated Budget: {budget} \n")
    f.write(f"Worldwide Gross: {gross} \n")
    f.write(f"Awards: {nominations} \n")
    f.write("\n")

    print(f"{movie_name} added to list")
    

#CREATING A NEW FILE 
with open("./Movies.txt", "w", encoding="utf-8") as f:

    #GETTING RESPONSE FROM THE MAIN PAGE
    main_page = requests.get("https://www.imdb.com/chart/top/").text  

    #PARSING THE MAIN PAGE           
    soup = BeautifulSoup(main_page, "lxml")     

    #GETTING ALL THE MOVIES
    movies = soup.find_all("td", class_ = "titleColumn")    

    #CONCURRENTLY ITERATING THROUGH EACH MOVIE    
    with concurrent.futures.ThreadPoolExecutor() as executor:
      executor.map(Get_Movie_Data, movies)

    
    #CLOSING FILE
    f.close()
    print("Done")





