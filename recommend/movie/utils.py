import pandas as pd
from surprise import Reader, Dataset, SVD, evaluate
import pickle

with open("C:/Users/hp/Desktop/movie/gen_md.dat", "rb") as input_file:
    gen_md = pickle.load(input_file)
with open("C:/Users/hp/Desktop/movie/dumped/indices.dat", "rb") as input_file:
    indices = pickle.load(input_file)
with open("C:/Users/hp/Desktop/movie/dumped/id_map.dat", "rb") as input_file:
    id_map = pickle.load(input_file)
with open("C:/Users/hp/Desktop/movie/dumped/cosine_sim.dat", "rb") as input_file:
    cosine_sim = pickle.load(input_file)
with open("C:/Users/hp/Desktop/movie/dumped/smd.dat", "rb") as input_file:
    smd = pickle.load(input_file)
with open("C:/Users/hp/Desktop/movie/dumped/indices_map.dat", "rb") as input_file:
    indices_map = pickle.load(input_file)

reader = Reader()
ratings = pd.read_csv('C:/Users/hp/Desktop/movie/ratings_small.csv')
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
data.split(n_folds=5)
svd = SVD()
evaluate(svd, data, measures=['RMSE', 'MAE'])
trainset = data.build_full_trainset()
svd.train(trainset)


def build_chart(genre, percentile=0.85):
    global gen_md
    df = gen_md[gen_md['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][
        ['id','title', 'year', 'vote_count', 'vote_average', 'popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')

    qualified['wr'] = qualified.apply(
        lambda x: (x['vote_count'] / (x['vote_count'] + m) * x['vote_average']) + (m / (m + x['vote_count']) * C),
        axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    print(qualified.head())
    return [list(qualified.id),list(qualified.title)]

def update_dataset(user_id,movie_id,rating):
    old= open('C:/Users/hp/Desktop/movie/ratings_small.csv','a')
    old.write(str(user_id)+","+str(movie_id)+","+str(rating)+",0\n")
    old.close()

def hybrid(userId,title):
    global indices,id_map,indices_map,cosine_sim,smd
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending=False).head(10)
    return [list(movies.title),list(movies.id)]
