import os
import sys
from analytics import Research
from config import *
if __name__ == '__main__':
    research = Research(sys.argv[1])
    file_content = research.file_reader()
    analysis = Research.Analytics(file_content)
    heads, tails = analysis.counts()
    flips = heads + tails
    heads_fraction, tails_fraction = analysis.fractions(heads, tails)
    predicted_list = analysis.predict_random(predict_flips)
    predict_heads, predict_tails = Research.Calculations(predicted_list).counts()
    
    final_res = REP_TEMPLATE.format(flips=flips, tails=tails, heads=heads, tails_percent=tails_fraction*100, heads_percent=heads_fraction*100, predict_flips=predict_flips, predict_tails=predict_tails, predict_heads=predict_heads)
    print(final_res)
    Research.Analytics.save_file(final_res, "test", "txt")
  