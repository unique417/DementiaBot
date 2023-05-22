import random

from evaluators import scattershot_ranker
from evaluators import length_ranker
from evaluators import offensive_text_ranker
from evaluators import keyword_match_ranker
from evaluators import repetition_filter_ranker
from evaluators import qq_ranker

scatter_ranker = scattershot_ranker.ScattershotRanker() 
length_ranker = length_ranker.LengthRanker()
offensive_text_ranker = offensive_text_ranker.OffensiveTextRanker()
k_m_ranker = keyword_match_ranker.KeywordMatchRanker()
rep_ranker = repetition_filter_ranker.RepetitionFilterRanker()
a_qq_ranker = qq_ranker.QQRanker()

response_evaluators = [length_ranker, k_m_ranker, a_qq_ranker, scatter_ranker]
response_filters = [offensive_text_ranker, rep_ranker]
