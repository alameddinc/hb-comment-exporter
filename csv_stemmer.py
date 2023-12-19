
import pandas as pd

def read_csv():
    df = pd.read_csv("comments2.csv")
    return df

def write_csv(df):
    df.to_csv("processed_comments.csv")

def sentence_to_word(df):
    df['comment'] = df['comment'].apply(lambda x: x.split())
    ## lower case
    df['comment'] = df['comment'].apply(lambda x: [y.lower() for y in x])
    return df

def stemmer(df):
    from TurkishStemmer import TurkishStemmer
    stemmer = TurkishStemmer()
    df['comment'] = df['comment'].apply(lambda x: [stemmer.stem(y) for y in x])
    return df


def word_avarage_rate(df):
    ### comment has list of words and rating is a number
    ### we need to find avarage rate of each word
    word_rate_df = pd.DataFrame(columns=['word','count', 'rating'])
    word_rate_df['word'] = df['comment'].explode().unique()
    word_rate_df['count'] = word_rate_df['word'].apply(lambda x: df['comment'].apply(lambda y: x in y).sum())
    word_rate_df['rating'] = word_rate_df['word'].apply(lambda x: df[df['comment'].apply(lambda y: x in y)]['rating'].mean())
    return word_rate_df


def normalize(rate_df):
    ### delete words that has less than 10 occurence
    rate_df = rate_df[rate_df['count'] > 10]
    ### normalize rating



def main():
    df = read_csv()
    df = sentence_to_word(df)
    df = stemmer(df)
    rate_df = word_avarage_rate(df)
    rate_df = normalize(rate_df)
    write_csv(rate_df)

if __name__ == "__main__":
    main()


