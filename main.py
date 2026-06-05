import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import get_scorer_names

#from wordcloud import WordCloud
def load_dataset(path: str):
    df = pd.read_csv(path)
    # print(df.shape)
    return df
    
def visulize_dataset(df):
    #
    # s = set(df.loc[df["is_ip"] == 0, 'tld'])
    # n = set()
    # for i in s:
    #    n.add(type(i))
    #    if type(i) == float:
    #        print(i)
    # print(n)
    text = ' '.join(df.loc[(df["tld_len"] > 0), 'tld'].astype(str).tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(3,1,figsize=(7,7))
    ax[1].imshow(wordcloud, interpolation='bilinear')
    df['label'].value_counts().plot(kind='bar', color=['#E24B4A','#639922'], ax=ax[2])
    plt.title('Phishing vs Legitimate URLs')
    plt.xlabel('Status'); plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def compare_classifiers(df):
    x = df.drop(columns=["url", "dom", "label", "tld"])
    y = df["label"]

    models = [GaussianNB(), DecisionTreeClassifier(), RandomForestClassifier()]
    rskf = RepeatedStratifiedKFold(n_repeats=2, n_splits=5)
    results = []

    for model in models:
        scores = cross_validate(model, x, y, cv=rskf, scoring=["balanced_accuracy"])
        results.append([model.__class__.__name__ , scores["test_balanced_accuracy"].mean()])

    return results

if __name__ == "__main__":
    df = load_dataset("C:\\Users\\oem\\Desktop\\ai\\FindMaliciousURL\\Dataset.csv")
    #visulize_dataset(df)
    print(df)
    print(compare_classifiers(df))