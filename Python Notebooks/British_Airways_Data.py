from bs4 import BeautifulSoup as bs
import pandas as pd
import plotly.offline as poff
import plotly.graph_objects as go
import requests

URL = "https://www.airlinequality.com/airline-reviews/british-airways/page/1/?pagesize=100&filterby=cabin%3Afirst"
page = requests.get(URL)
soup = bs(page.content, "html.parser")

results = soup.find(id="main")


text_reviews = results.find_all("div", class_= "text_content")
stat_reviews = results.find_all("table", class_= "review-ratings")

for statr in stat_reviews:
  travtype = statr.find("td", class_= "review-rating-header type_of_traveller")
  print(travtype)
  
travel_type = results.find_all("td", class_= "review-value")

date_pub = results.find_all("time", itemprop = "datePublished")
review_summary = results.find_all("h2", class_ = "text_header")
reviewer_name = results.find_all("span", itemprop = "name")
reviewer_rating = results.find_all("span", itemprop = "ratingValue")
headers = results.find_all("td", itemprop = "review-rating-header")

reviewer_rating = reviewer_rating[1:]

for i in range(100):
    date_pub[i] = date_pub[i].text.strip()
    review_summary[i] = review_summary[i].text.strip()
    reviewer_name[i] = reviewer_name[i].text.strip()
    reviewer_rating[i] = reviewer_rating[i].text.strip()
    text_reviews[i] = text_reviews[i].text.strip()


dataset = {'Reviewer_Name': list(reviewer_name), 'Date_Published':list(date_pub),'Summary':list(review_summary),'Overall_Rating':list(reviewer_rating),'Review':list(text_reviews)}
    
Data = pd.DataFrame(dataset)

Data[['Review_Verification' , 'Review']] = Data['Review'].str.split('|', expand=True)

Data.to_csv("C:\\Users\\ADMIN\\Desktop\\acads\\British_Air1.csv", index = False)


plotpi = go.Figure(data = [go.Pie(labels = Data['Overall_Rating'], values = Data['Overall_Rating'].value_counts())])

plotpi.update_layout(title = "Ratings_Distribution")

poff.plot(plotpi)
