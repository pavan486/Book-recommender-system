from flask import Flask, render_template, request
import pickle
import pandas as pd
import re

# Loading data

good = pickle.load(open('Data/processed_data.pkl', 'rb'))
pop_good_reads = pickle.load(open('Data/popular.pkl', 'rb'))
sig = pickle.load(open('Data/sigmoid_scores.pkl', 'rb'))

business = pickle.load(open('Data/business.pkl', 'rb'))
business_short = business.head(3)

novels = pickle.load(open('Data/novel.pkl', 'rb'))
novels_short = novels.head(3)

fiction = pickle.load(open('Data/fiction.pkl', 'rb'))
fiction_short = fiction.head(3)

philosophy = pickle.load(open('Data/philosophy.pkl', 'rb'))
philosophy_short = philosophy[3:6]

print(good.columns)

app = Flask(__name__)


# index page

@app.route('/')
def index():
    return render_template('index.html',
                           book_bus=list(business_short['Book'].values),
                           author_bus=list(business_short['Author'].values),
                           image_bus=list(business_short['images'].values),
                           votes_bus=list(business_short['Num_Ratings'].values),
                           rating_bus=list(business_short['Avg_Rating'].values),
                           url_bus=list(business_short['URL'].values),

                           book_fic=list(fiction_short['Book'].values),
                           author_fic=list(fiction_short['Author'].values),
                           image_fic=list(fiction_short['images'].values),
                           votes_fic=list(fiction_short['Num_Ratings'].values),
                           rating_fic=list(fiction_short['Avg_Rating'].values),
                           url_fic=list(fiction_short['URL'].values),

                           book_nov=list(novels_short['Book'].values),
                           author_nov=list(novels_short['Author'].values),
                           image_nov=list(novels_short['images'].values),
                           votes_nov=list(novels_short['Num_Ratings'].values),
                           rating_nov=list(novels_short['Avg_Rating'].values),
                           url_nov=list(novels_short['URL'].values),

                           book_phi=list(philosophy_short['Book'].values),
                           author_phi=list(philosophy_short['Author'].values),
                           image_phi=list(philosophy_short['images'].values),
                           votes_phi=list(philosophy_short['Num_Ratings'].values),
                           rating_phi=list(philosophy_short['Avg_Rating'].values),
                           url_phi=list(philosophy_short['URL'].values)
                           )


# Business page

@app.route('/business')
def business_books():
    return render_template('business.html',
                           book_busi=list(business['Book'].values),
                           author_busi=list(business['Author'].values),
                           image_busi=list(business['images'].values),
                           votes_busi=list(business['Num_Ratings'].values),
                           rating_busi=list(business['Avg_Rating'].values),
                           url_busi=list(business['URL'].values)
                           )



# Fiction page

@app.route('/fiction')
def fiction_books():
    return render_template('fiction.html',
                           book_fict=list(fiction['Book'].values),
                           author_fict=list(fiction['Author'].values),
                           image_fict=list(fiction['images'].values),
                           votes_fict=list(fiction['Num_Ratings'].values),
                           rating_fict=list(fiction['Avg_Rating'].values),
                           url_fict=list(fiction['URL'].values)
                           )


# Philosophy page

@app.route('/philosophy')
def philosophy_books():
    return render_template('philosophy.html',
                           book_phis=list(philosophy['Book'].values),
                           author_phis=list(philosophy['Author'].values),
                           image_phis=list(philosophy['images'].values),
                           votes_phis=list(philosophy['Num_Ratings'].values),
                           rating_phis=list(philosophy['Avg_Rating'].values),
                           url_phis=list(philosophy['URL'].values)
                           )


# Novels page

@app.route('/novels')
def novels_books():
    return render_template('novels.html',
                           book_nove=list(novels['Book'].values),
                           author_nove=list(novels['Author'].values),
                           image_nove=list(novels['images'].values),
                           votes_nove=list(novels['Num_Ratings'].values),
                           rating_nove=list(novels['Avg_Rating'].values),
                           url_nove=list(novels['URL'].values)
                           )


# ALL Books page

@app.route('/all_books')
def get_all_books():
    return render_template('books.html',
                           books=list(good['Book'].values),
                           authors=list(good['Author'].values),
                           images=list(good['images'].values),
                           num_rates=list(good['Num_Ratings'].values),
                           ratings=list(good['Avg_Rating'].values),
                           genres=list(good['Genres_up'].values),
                           url=list(good['URL'].values)
                           )


# Top 50 books page

@app.route('/top_50_books')
def top_books():
    return render_template('top_50_books.html',
                           books_50=list(pop_good_reads['Book'].values),
                           authors_50=list(pop_good_reads['Author'].values),
                           image_50=list(pop_good_reads['images'].values),
                           votess_50=list(pop_good_reads['Num_Ratings'].values),
                           ratings_50=list(pop_good_reads['Avg_Rating'].values),
                           url_50=list(pop_good_reads['URL'].values)
                           )


# Recommend page

def process(book_name):
    if book_name.find('(') != -1:
        book_name = book_name[:book_name.find('(')].strip()
        book_name = book_name.lower()
        book_name = re.sub(r'[^\w\s]', '', book_name)
        return book_name
    else:
        book_name = book_name.lower().strip()
        book_name = re.sub(r'[^\w\s]', '', book_name)
        return book_name


@app.route('/get_info_and_rec', methods=['POST'])
def get_info_and_rec():
    user_input = request.form.get('user_input')
    user_input = process(user_input)
    books_data = [good[good['book_processed'] == user_input]['Book'].values[0],
                  good[good['book_processed'] == user_input]['Author'].values[0],
                  good[good['book_processed'] == user_input]['Description'].values[0],
                  good[good['book_processed'] == user_input]['Avg_Rating'].values[0],
                  good[good['book_processed'] == user_input]['Num_Ratings'].values[0],
                  good[good['book_processed'] == user_input]['images'].values[0],
                  good[good['book_processed'] == user_input]['URL'].values[0]
                  ]

    indices = pd.Series(good.index, index=good['book_processed']).drop_duplicates()
    idx = indices[user_input]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:9]
    book_indices = [i[0] for i in sig_scores]

    recommendations = []
    for i in book_indices:
        item = []
        temp_df = good[good['book_processed'] == good['book_processed'].iloc[i]]
        item.extend(list(temp_df.drop_duplicates('book_processed')['Book'].values))
        item.extend(list(temp_df.drop_duplicates('book_processed')['Author'].values))
        item.extend(list(temp_df.drop_duplicates('book_processed')['images'].values))
        item.extend(list(temp_df.drop_duplicates('book_processed')['URL'].values))
        recommendations.append(item)

    return render_template('recommend.html', book_info=books_data, recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)
