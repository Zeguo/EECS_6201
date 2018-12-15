

##from rake_nltk import Metric,Rake
##from nltk.corpus import stopwords
##text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."

def rake_text(text,phrase_min_length_set, phrase_max_length_set):
    from rake_nltk import Metric,Rake

    ##    from rake_nltk import Metric, Rake

    # To use it with a specific language supported by nltk.
    r = Rake(language='english')

    ##stop_words = set(stopwords.words('english'))
    # If you want to provide your own set of stop words and punctuations to
    ##r = Rake(
    ##    stopwords,
    ##    punctuations='`~!@#$%^&*()_+|}{":?><,./;[\\]=-'
    ##)

    # If you want to control the metric for ranking. Paper uses d(w)/f(w) as the
    # metric. You can use this API with the following metrics:
    # 1. d(w)/f(w) (Default metric) Ratio of degree of word to its frequency.
    # 2. d(w) Degree of word only.
    # 3. f(w) Frequency of word only.

    r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)
    r = Rake(ranking_metric=Metric.WORD_DEGREE)
    r = Rake(ranking_metric=Metric.WORD_FREQUENCY)

    # If you want to control the max or min words in a phrase, for it to be
    # considered for ranking you can initialize a Rake instance as below:

    r = Rake(min_length=phrase_min_length_set, max_length=phrase_max_length_set)
    key_words = r.extract_keywords_from_text(text)
    ranked_phrases = r.get_ranked_phrases()
    ranked_phrases_scores = r.get_ranked_phrases_with_scores()
    
##    print(key_words)
##    print(r.get_ranked_phrases())
    return ranked_phrases
##    print(ranked_phrases_scores)
##t= rake_text(text,2,2)
##print(t)
