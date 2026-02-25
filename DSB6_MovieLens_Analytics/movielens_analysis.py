import os
from collections import defaultdict
import sys
from datetime import datetime
import re
import pytest
from collections import Counter
import requests
from bs4 import BeautifulSoup

@staticmethod
def parse_csv(line):
    movie_list = []
    current_val = ''
    in_quotes = False
    for char in line.strip():
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            movie_list.append(current_val)
            current_val = ''
        else:
            current_val += char
    movie_list.append(current_val)
    return movie_list   

class Tags:
    def __init__(self, path_to_the_file):
        self.tags_list = self._load_csv(path_to_the_file)
 
    def _load_csv(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError()
        tags = []
        try:
            with open(path, 'r') as file:
                header = file.readline().strip()
                expected_header = "userId,movieId,tag,timestamp"
                if header != expected_header:
                    raise ValueError('Wrong file structure')
                lines = file.readlines()
                for line in lines[1:]: 
                    row = line.strip().split(',')
                    if len(row) != 4:
                        raise ValueError('Wrong file structure')
                    tags.append(row[2].strip())
        except Exception as e:
            print(e)
            sys.exit()
        return tags

    
    def most_words(self, n):
        """Returns top-n tags with most words inside."""
        tag_word_count = {tag: len(tag.split()) for tag in set(self.tags_list)}
        sorted_tags = sorted(tag_word_count.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_tags[:n])
    
    def longest(self, n):
        """Returns top-n longest tags in terms of number of characters."""
        unique_tags = set(self.tags_list)
        sorted_tags = sorted(unique_tags, key=len, reverse=True)
        return sorted_tags[:n]
    
    def most_words_and_longest(self, n):
        """Returns the intersection between most words and longest tags."""
        most_words_tags = set(self.most_words(n).keys())
        longest_tags = set(self.longest(n))
        intersection = most_words_tags & longest_tags
        return sorted(intersection)
    
    def most_popular(self, n):
        """Returns the most popular tags based on their frequency."""
        tag_counts = Counter(self.tags_list)
        most_common = tag_counts.most_common(n)
        return dict(most_common)
    
    def tags_with(self, word):
        """Returns all unique tags that include the specified word."""
        tags_with_word = {tag for tag in set(self.tags_list) if word.lower() in tag.lower()}
        return sorted(tags_with_word)



class Movies:
    def __init__(self, path_to_the_file):
        self.movies = self.create_list(path_to_the_file)
        
    def create_list(self, path_to_the_file):
        res = []
        if not os.path.exists(path_to_the_file):
            raise FileNotFoundError()
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                expected_header = "movieId,title,genres"
                actual_header = lines[0].strip()
                if actual_header != expected_header:
                    raise ValueError('Wrong file structure')
                for line in lines[1:]: 
                    movie_list = parse_csv(line)
                    if len(movie_list) != 3:
                        raise ValueError('Wrong file structure')
                    res.append(movie_list)
        except Exception as e:
            print(e)
            sys.exit()
            

        return res

    def dist_by_genres(self):
        genres = {}
        for movie in self.movies:
            genre_list = movie[2].split('|')
            for genre in genre_list:
                genre = genre.strip()
                genres[genre] = genres.get(genre, 0) + 1
        sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_genres)

    def most_genres(self, n):
        all_movies_genre = {}
        for movie in self.movies:
            one_movie_count = len(movie[2].split('|'))
            all_movies_genre[movie[1]] = one_movie_count
        sorted_movies = sorted(all_movies_genre.items(), key=lambda x: x[1], reverse=True)[:n]
        return dict(sorted_movies)

    def dist_by_release(self):
        years_n_num = {}
        for movie in self.movies:
            pattern = re.search(r'\((\d{4})\)', movie[1])
            if pattern:
                year = pattern.group(1)
                years_n_num[year] = years_n_num.get(year, 0) + 1
        return dict(sorted(years_n_num.items(), key=lambda x: x[1], reverse=True))


class Links:

    def __init__(self, path_to_the_file):
        self.imdb_dict = {}
        self.imdb_list = self.get_imdb(self.list_ids(path_to_the_file), list_of_fields=['name', 'director','runtime','gross worldwide','budget'])

    def list_ids(self, path):
            if not os.path.isfile(path):
                raise FileNotFoundError()
            try:
                with open(path, 'r', encoding='utf-8') as file:
                        lines = file.read().splitlines()

                header = lines[0]
                if header.strip() != "movieId,imdbId,tmdbId":
                    raise ValueError("Wrong file structure")

                res = []
                for line in lines[1:]:
                    if line:
                        parts = line.split(',')
                        if len(parts) != 3:
                            raise ValueError("Wrong file structure")
                        res.append(parts[1])
            except Exception as e:
                print(e)
                sys.exit()
            return res

    def get_imdb(self, list_of_movies, list_of_fields):
        results = []
        sorted_films = sorted(list_of_movies, key=int, reverse=True)    
        for imdb_id in sorted_films:
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                    "Accept-Language": "en-US,en;q=0.5"
                }
            try:
                response = requests.get(url, headers=headers, timeout=10)  
            except requests.exceptions.Timeout as e:
                print(e)
                continue  
            except requests.exceptions.RequestException as e:
                print(e)
                continue  
            soup = BeautifulSoup(response.text, 'html.parser')
            #Processing the receieved html
            i = []
            results.append(i)
            name = None
            director = None
            budget = None
            gross_worldwide = None
            runtime = None
            min_only = None
            i.append(imdb_id)
            self.imdb_dict[imdb_id] = None
            if 'name' in list_of_fields:
                name_part = soup.find('span', {'class':"hero__primary-text"})
                if name_part:
                    name = name_part.text
                i.append(name)
                self.imdb_dict[imdb_id] = {'name': name}
                
            if 'runtime' in list_of_fields:
                runtime_part = soup.find('li', attrs={'data-testid': 'title-techspec_runtime'})
                if runtime_part:
                    values = runtime_part.text.split()
                    min_only = int(values[1].split('(')[1])
                    hours = min_only//60
                    minutes = min_only%60
                    runtime = f'{hours}h {minutes}m'
                i.append(runtime)
                self.imdb_dict[imdb_id]['runtime'] = min_only

            if 'director' in list_of_fields:
                director_part = soup.find('a', href=lambda x: x and '/name/' in x)
                if director_part:
                    director = director_part.text.strip()
                i.append(director)
                self.imdb_dict[imdb_id]['director'] = director

            if 'budget' in list_of_fields:
                budget_li = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
                if budget_li:
                    budget = budget_li.find('span', class_='ipc-metadata-list-item__list-content-item').text.strip().replace('\xa0', ' ')

                i.append(budget)
                self.imdb_dict[imdb_id]['budget'] = budget

            if 'gross worldwide' in list_of_fields:
                gross_world_li = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
                if gross_world_li:
                    gross_worldwide = gross_world_li.find('span', class_='ipc-metadata-list-item__list-content-item').text.strip()
                i.append(gross_worldwide)
                self.imdb_dict[imdb_id]['gross worldwide'] = gross_worldwide

        return results
    
    @staticmethod
    def parse_money(val):
        # if val != None:
        only_numbers = int(''.join([char for char in val if char.isdigit()]))
        # else:
        #     only_numbers = None
        return only_numbers

    def top_directors(self, n):

        director_counts = Counter(movie['director'] for movie in self.imdb_dict.values())
        top_n = director_counts.most_common(n)
        top_directors = {director: count for director, count in top_n}
        return top_directors
    
    def longest(self, n):        
        runtime_items = [(movie['name'], movie['runtime']) for movie in self.imdb_dict.values()]
        return dict(sorted(runtime_items, key=lambda x: x[1], reverse=True)[:n])
    
    
    def most_expensive(self,n):
        budget_dict = {item['name']: self.parse_money(item['budget']) for item in self.imdb_dict.values()
                       if item['budget']!=None}
        res = dict(sorted(budget_dict.items(), key=lambda item: item[1], reverse=True)[:n])
        return res
    
    def most_profitable(self, n):
        budget_dict = {item['name']: self.parse_money(item['gross worldwide'])-self.parse_money(item['budget']) for item in self.imdb_dict.values()
                       if item['gross worldwide']!=None and item['budget']!=None}
        res = dict(sorted(budget_dict.items(), key=lambda item: item[1], reverse=True)[:n])
        return res

    def top_cost_per_minute(self, n):
        budget_dict = {item['name']: round((self.parse_money(item['budget'])/item['runtime']),2) for item in self.imdb_dict.values()
                       if item['budget']!=None}
        res = dict(sorted(budget_dict.items(), key=lambda x: x[1],reverse=True)[:n])
        return res

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        #list of dictionaries
        # {'userId': '610', 'movieId': '170875', 'rating': '3.0', 'timestamp': '1493846415'}
        self.rating_data = self.from_csv_to_dicts(path_to_the_file)
    
    def from_csv_to_dicts(self, path_to_the_file):
        if not os.path.exists(path_to_the_file):
            raise FileNotFoundError()
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as f:
                    lines = f.read().splitlines()

            expected_header = ['userId', 'movieId', 'rating', 'timestamp']
            headers = lines[0].split(',')
            if headers != expected_header:
                raise ValueError("Wrong file structure")

            data = []
            for line in (lines[1:]):
                values = line.split(',')
                if len(values) != 4:
                    raise ValueError('Wrong file structure')
                row_item = dict(zip(headers, values))
                data.append(row_item)
        except Exception as e:
            print(e)
            sys.exit()
        return data
    
    class Movies:
        def __init__(self, outer):
            self.outer = outer
            #dict, keys - ids, values - names
            self.movies_data = self.create_movies_dict('default_datasets/movies.csv')

        def create_movies_dict(self, path_to_the_file):
            movies_dict = {}
            try:
                with open(path_to_the_file, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if lines:
                        for line in lines[1:]:
                            movie_list = parse_csv(line)
                            # if movie_list and len(movie_list) >= 2:
                            movie_id = movie_list[0].strip()
                            movies_dict[movie_id] = movie_list[1]
                    else:
                        raise ValueError('Error - The file is empty')
            except Exception as e:
                print(e)
            return movies_dict      
        
        def dist_by_year(self):
            year_count = {}
            for item in self.outer.rating_data:
                year = str(datetime.fromtimestamp(int(item['timestamp'])).year)
                year_count[year] = year_count.get(year, 0) + 1  
            return dict(sorted(year_count.items()))
        
        def dist_by_rating(self):
            rating_count = {}
            for item in self.outer.rating_data:
                rating = (item['rating'])
                rating_count[rating] = rating_count.get(rating,0) + 1
            return dict(sorted(rating_count.items()))
        
        def top_by_num_of_ratings(self, n):
            #  keys are titles, values are numbers.
            rating_count = {}
            for item in self.outer.rating_data:
                title = self.movies_data[item['movieId']]     
                rating_count[title] = rating_count.get(title,0) + 1     
            return dict(sorted(rating_count.items(),key=lambda x: x[1],reverse=True)[:n])
        
        @staticmethod
        def count_average(self,n):    
            rating_sums = defaultdict(float)
            rating_counts = defaultdict(float)

            for review in self.outer.rating_data:
                movie_id = review['movieId']
                rating = float(review['rating'])
                rating_sums[movie_id] += rating
                rating_counts[movie_id] += 1

            average_ratings = {}
            for movie_id in rating_sums:
                average_ratings[movie_id] = round(rating_sums[movie_id] / rating_counts[movie_id],2)
            # return average_ratings
            titles_n_avg = {self.movies_data[k]:v for k, v in average_ratings.items()}
            return dict(sorted(titles_n_avg.items(), key=lambda x: x[1], reverse=True)[:n])   
            # return dict(sorted(average_ratings.items(), key=lambda x: x[1], reverse=True)[:n])

        @staticmethod
        def single_median(lst):
            n = len(lst)
            if n == 0:
                raise ValueError("The list is empty")
            sorted_lst = sorted(lst)
            mid = n // 2
            if n % 2 == 0:
                return (sorted_lst[mid - 1] + sorted_lst[mid]) / 2.0
            else:
                return sorted_lst[mid]

        @staticmethod
        def count_median(self,n):
            ids_n_ratings = defaultdict(list)
            for review in self.outer.rating_data:
                id = review['movieId']
                # title = self.movies_data[id]
                rating = float(review['rating'])
                ids_n_ratings[id].append(rating)
            # return ids_n_ratings
            titles_n_medians = {self.movies_data[k]:self.single_median(v) for k,v in ids_n_ratings.items()}
            return dict(sorted(titles_n_medians.items(),key=lambda x: x[1],reverse=True)[:n])
            # return dict(sorted(ids_n_ratings.items(),key=lambda x: x[1],reverse=True)[:n])


        def top_by_ratings(self, n, metric='average'):
            if metric == 'average':
                return self.count_average(self,n)
            if metric == 'median':
                return self.count_median(self,n)
            
        def top_controversial(self, n):
            ids_n_ratings = defaultdict(list)
            for review in self.outer.rating_data:
                id = review['movieId']
                # title = self.movies_data[id]
                rating = float(review['rating'])
                ids_n_ratings[id].append(rating)
            titles_n_variances = {self.movies_data[k]:self.get_variance(v) for k,v in ids_n_ratings.items()}
            return dict(sorted(titles_n_variances.items(),key=lambda x: x[1],reverse=True)[:n])

        @staticmethod
        def get_variance(data):
            n = len(data)
            if n < 2:
                res = 0
            else:
                mean = sum(data) / n
                squared_diffs = [(x - mean) ** 2 for x in data]
                res = round((sum(squared_diffs) / (n - 1)),2)        
            return res
    
    #list of dictionaries
    # {'userId': '610', 'movieId': '170875', 'rating': '3.0', 'timestamp': '1493846415'}

    class Users(Movies):
        def u_distr_by_rating(self):
            #keys - number of rating, values - number of users
            users_n_ratings = defaultdict(int)
            for item in self.outer.rating_data:
                users_n_ratings[item['userId']] +=1  
            res = defaultdict(int)
            res = dict(Counter(users_n_ratings.values()).most_common())
            return res
        def u_avg_mdn_distr(self, metric):
            if metric == 'average' or 'median':
                user_n_rates = defaultdict(list)
                for item in self.outer.rating_data:
                    user_n_rates[item['userId']].append(float(item['rating']))
                if metric == 'average':
                    pre_res = {k:self.basic_avg(v) for k,v in user_n_rates.items()}
                    # res = defaultdict(int)
                    # res = dict(Counter(pre_res.values()).most_common())
                if metric == 'median':
                    pre_res = {k:self.single_median(v) for k,v in user_n_rates.items()}
                res = defaultdict(int)
                res = dict(Counter(pre_res.values()).most_common())
                return res
        
        @staticmethod
        def basic_avg(lst):
            return round(sum(lst)/len(lst),2)
        
        def u_variance(self, n):
        # keys - ids, values - variance
            user_n_rates = defaultdict(list)
            for item in self.outer.rating_data:
                user_n_rates[item['userId']].append(float(item['rating']))
            pre_res = {k:self.get_variance(v) for k,v in user_n_rates.items()}
            return dict(sorted(pre_res.items(),key=lambda x: x[1],reverse=True)[:n])
        


class Tests:
    def setup_method(self):
        self.ratings_obj = Ratings('default_datasets/ratings.csv')
        self.ratings_movies_obj = Ratings.Users(self.ratings_obj)
        self.tags_obj = Tags('datasets/tags_short.csv')
        self.small_movies = Movies('datasets/movies.csv')
        self.optimal_links = Links('datasets/links_3.csv')

##### MOVIES #####
    @pytest.mark.parametrize("method_name, arg, has_arg", [
        ("dist_by_release", None, False),
        ("dist_by_genres", None, False),
        ("most_genres", 10, True),
    ])

    def test_movies_data_type(self, method_name, arg, has_arg):
        method = getattr(self.small_movies, method_name)
        result = method(arg) if has_arg else method()
        assert isinstance(result, dict)
        for k in result.keys():
            assert isinstance(k, str)
        for v in result.values():
            assert isinstance(v, int)

    def test_dist_by_genres_sorting(self):
        res = self.small_movies.dist_by_genres()
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Drama'
        assert formatted_res[0][1] == 378
        assert formatted_res[-1][0] == 'IMAX'
        assert formatted_res[-1][1] == 3    
    
    def test_most_genres_sorting(self):
        res = self.small_movies.most_genres(10)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Strange Days (1995)'
        assert formatted_res[0][1] == 6
        assert formatted_res[-1][0] == 'Copycat (1995)'
        assert formatted_res[-1][1] == 5
    
    def test_dist_by_release_sorting(self):
        res = self.small_movies.dist_by_release()
        formatted_res = list(res.items())
        assert formatted_res[0][0] == '1995'
        assert formatted_res[0][1] == 220
        assert formatted_res[-1][0] == '1932'
        assert formatted_res[-1][1] == 1

##### LINKS #####
#6 methods
    #check types of all but cost per minute and get imdb
    @pytest.mark.parametrize("method_name, arg, has_arg", [
        ("top_directors", 10, True),
        ("most_expensive", 10, True),
        ("most_profitable", 10, True),
        ("longest", 10, True)
    ])

    def test_links_data_type(self, method_name, arg, has_arg):
        method = getattr(self.optimal_links, method_name)
        result = method(arg) if has_arg else method()
        assert isinstance(result, dict)
        for k in result.keys():
            assert isinstance(k, str)
        for v in result.values():
            assert isinstance(v, int)
    
    #get imdb 
    #all tests
    def test_get_imdb_type(self):
        assert isinstance(self.optimal_links.imdb_list, list)
    def test_get_imdb_item_type(self):
        assert all(isinstance(item, list) for item in self.optimal_links.imdb_list)
    def test_get_imdb_sorting(self):
        assert self.optimal_links.imdb_list[0][0] == '0320661'
    
    #top directors
    def test_top_directors_sorting(self):
        res = self.optimal_links.top_directors(1)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Ridley Scott'
        assert formatted_res[0][1] == 2
    #most expensive
    def test_most_expensive_sorting(self):
        res = self.optimal_links.most_expensive(1)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Kingdom of Heaven'
        assert formatted_res[0][1] == 130000000
    #most profitable
    def test_most_profitable_sorting(self):
        res = self.optimal_links.most_profitable(1)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Forrest Gump'
        assert formatted_res[0][1] == 623226465
        
    #longest
    def test_longest_sorting(self):
        res = self.optimal_links.longest(1)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Kingdom of Heaven'
        assert formatted_res[0][1] == 144
    #top cost per minute
    #all tests
    def test_top_cost_per_minute_type(self):
        assert isinstance(self.optimal_links.top_cost_per_minute(1),dict)
    def test_top_cost_per_minute_item_type(self):
        res = self.optimal_links.top_cost_per_minute(1)
        k, v = next(iter(res.items()))
        assert isinstance(k, str)
        assert isinstance(v, float)
    def test_top_cost_per_minute_sorting(self):
        res = self.optimal_links.top_cost_per_minute(1)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Kingdom of Heaven'
        assert formatted_res[0][1] == 902777.78

##### RATINGS #####

    @pytest.mark.parametrize("method_name, arg, has_arg", [
        ("dist_by_year", None, False),
        ("top_by_num_of_ratings", 10, True),
        ('dist_by_rating',None,False)
    ])
    
    def test_ratings_data_type(self, method_name, arg, has_arg):
        method = getattr(self.ratings_movies_obj, method_name)
        result = method(arg) if has_arg else method()
        assert isinstance(result, dict)
        for k in result.keys():
            assert isinstance(k, str)
        for v in result.values():
            assert isinstance(v, int)

    def test_dist_by_year_sorting(self):
        res = list(self.ratings_movies_obj.dist_by_year().items())
        assert res[0][0] == '1996'
        assert res[0][1] == 6040
    
    def test_dist_by_rating_sorting(self):
        res = list(self.ratings_movies_obj.dist_by_rating().items())
        assert res[0][0] == '0.5'
        assert res[0][1] == 1370    

    def test_top_by_num_of_ratings_sorting(self):
        res = list(self.ratings_movies_obj.top_by_num_of_ratings(1).items())
        assert res[0][0] == 'Forrest Gump (1994)'
        assert res[0][1] == 329        



    @pytest.mark.parametrize("method_name, arg1, arg2, has_2args", [
        ("top_by_ratings", 10, 'median', True),
        ("top_by_ratings", 10, 'average', True),
        ("top_controversial", 10, None, False),
    ])

    def test_other_ratings_data_type(self, method_name, arg1, arg2, has_2args):
        method = getattr(self.ratings_movies_obj, method_name)
        result = method(arg1,arg2) if has_2args else method(arg1)
        assert isinstance(result, dict)
        for k in result.keys():
            assert isinstance(k, str)
        for v in result.values():
            assert isinstance(v, float)
    
    def test_top_by_ratings(self):
        res = list(self.ratings_movies_obj.top_by_ratings(3,'average').items())
        assert res[0][0] == 'The Jinx: The Life and Deaths of Robert Durst (2015)'
        assert res[0][1] == 5.0       
        res = list(self.ratings_movies_obj.top_by_ratings(3,'median').items())
        assert res[0][0] == 'The Jinx: The Life and Deaths of Robert Durst (2015)'
        assert res[0][1] == 5.0   

    def test_top_controversial(self):
        res = list(self.ratings_movies_obj.top_controversial(1).items())
        assert res[0][0] == "Ivan's Childhood (a.k.a. My Name is Ivan) (Ivanovo detstvo) (1962)"
        assert res[0][1] == 10.12   

    
    ###USERS
    #user distribution by rating
    def test_u_distr_by_rating_type(self):
        assert isinstance(self.ratings_movies_obj.u_distr_by_rating(), dict)
    def test_u_distr_by_rating_item_type(self):
        assert all(isinstance(item, int) for item in self.ratings_movies_obj.u_distr_by_rating().keys())
        assert all(isinstance(item, int) for item in self.ratings_movies_obj.u_distr_by_rating().values())
    def test_u_distr_by_rating_sorting(self):
        res = self.ratings_movies_obj.u_distr_by_rating()
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 21
        assert formatted_res[0][1] == 15
    
    #avg and mdn distribution 
    def test_u_avg_mdn_distr_type(self):
        assert isinstance(self.ratings_movies_obj.u_avg_mdn_distr('average'), dict)
        assert isinstance(self.ratings_movies_obj.u_avg_mdn_distr('median'), dict)

    def test_u_avg_mdn_distr_item_type(self):
        assert all(isinstance(item, float) for item in self.ratings_movies_obj.u_avg_mdn_distr('average').keys())
        assert all(isinstance(item, int) for item in self.ratings_movies_obj.u_avg_mdn_distr('average').values())
        assert all(isinstance(item, float) for item in self.ratings_movies_obj.u_avg_mdn_distr('median').keys())
        assert all(isinstance(item, int) for item in self.ratings_movies_obj.u_avg_mdn_distr('median').values())

    def test_u_avg_mdn_distr_sorting(self):
        res = self.ratings_movies_obj.u_avg_mdn_distr('average')
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 4.0
        assert formatted_res[0][1] == 10
        res = self.ratings_movies_obj.u_avg_mdn_distr('median')
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 4.0
        assert formatted_res[0][1] == 298  
    
    #user variance
    def test_user_variance_type(self):
        assert isinstance(self.ratings_movies_obj.u_variance(1), dict)
    def test_user_variance_item_type(self):
        assert all(isinstance(item, str) for item in self.ratings_movies_obj.u_variance(1).keys())
        assert all(isinstance(item, float) for item in self.ratings_movies_obj.u_variance(1).values())
    def test_user_variance_sorting(self):
        res = self.ratings_movies_obj.u_variance(1)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == '3'
        assert formatted_res[0][1] == 4.37


##### TAGS #####
    @pytest.mark.parametrize("method_name, arg, has_arg", [
    ("most_words", 10, True),
    ("most_popular", 10, True),
    ])

    def test_tags_data_type(self, method_name, arg, has_arg):
        method = getattr(self.tags_obj, method_name)
        result = method(arg) if has_arg else method()
        assert isinstance(result, dict)
        for k in result.keys():
            assert isinstance(k, str)
        for v in result.values():
            assert isinstance(v, int)
    
    def test_most_words_sorting(self):
        res = self.tags_obj.most_words(10)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'actual four big words'
        assert formatted_res[0][1] == 4
    
    def test_most_popular_sorting(self):
        res = self.tags_obj.most_popular(10)
        formatted_res = list(res.items())
        assert formatted_res[0][0] == 'Al Pacino'
        assert formatted_res[0][1] == 3
    
    @pytest.mark.parametrize("method_name, arg, has_arg", [
    ("longest", 10, True),
    ("most_words_and_longest", 10, True),
    ("tags_with",'Al',True)
    ])

    def test_other_tags_data_type(self, method_name, arg, has_arg):
        method = getattr(self.tags_obj, method_name)
        result = method(arg) if has_arg else method()
        assert isinstance(result, list)
        for i in result:
            assert isinstance(i,str)
    
    def test_longest_sorting(self):
        res = self.tags_obj.longest(10)
        assert res[0] == 'actual four big words'

    def test_most_words_and_longest_sorting(self):
        res = self.tags_obj.most_words_and_longest(10)
        res[0] = 'Anthony Hopkins'

    def test_tags_with_sorting(self):
        res = self.tags_obj.tags_with('Al')
        res[0] = 'Al Einstein'
  


