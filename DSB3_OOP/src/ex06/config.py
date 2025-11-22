import os
predict_flips = 3
REP_TEMPLATE = "We made {flips} observations by tossing a coin: {tails} were tails and {heads} were heads. The probabilities are {tails_percent}% and {heads_percent}%, respectively. Our forecast is that the next {predict_flips} observations will be: {predict_tails} tail and {predict_heads} heads."
API_TOKEN = os.environ.get("TG_API")