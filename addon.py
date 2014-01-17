#!/usr/bin/python
# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin, actions, xbmcgui, xbmc
from urllib import quote_plus, unquote_plus
import json
import urllib
import urllib2
import os
from PIL import Image
import PIL
import xbmcgui
import xbmc

img_file=''

plugin = Plugin()

addon_path = plugin.addon.getAddonInfo('path')
resources_path = xbmc.translatePath( os.path.join( addon_path, 'resources' ) ).decode('utf-8')
media_path = xbmc.translatePath( os.path.join( resources_path, 'media' ) ).decode('utf-8')
data_path = xbmc.translatePath( os.path.join( resources_path, 'data' ) ).decode('utf-8')

@plugin.route('/')
def show_menu():
    items = [
        {'label': 'Popular','thumbnail': os.path.join(media_path,'icon_popular.png'), 'path': plugin.url_for('show_movies',source='popular',page='1',query='none')},
        {'label': 'Top Rated','thumbnail': os.path.join(media_path,'icon_top_rated.png'), 'path': plugin.url_for('show_movies',source='top_rated',page='1',query='none')},
        {'label': 'Upcoming','thumbnail': os.path.join(media_path,'icon_upcoming.png'), 'path': plugin.url_for('show_movies',source='upcoming',page='1',query='none')},
        {'label': 'Now Playing','thumbnail': os.path.join(media_path,'icon_now_playing.png'), 'path': plugin.url_for('show_movies',source='now_playing',page='1',query='none')},
        {'label': 'Search','thumbnail': os.path.join(media_path,'icon_search.png'), 'path': plugin.url_for('show_movies',source='query',page='1',query='none')},
        {'label': 'Genres','thumbnail': os.path.join(media_path,'icon_genres.png'), 'path': plugin.url_for('show_genre')},
        {'label': 'Discover','thumbnail': os.path.join(media_path,'icon_discover.png'), 'path': plugin.url_for('show_movies',source='discover',page='1',query='none')},
        {'label': 'View Web Page','path':plugin.url_for('show_webpage',url='http://www.usatoday.com/story/life/movies/2014/01/15/jack-ryan-shadow-recruit-review/4272211/')}
    ]
    return items

@plugin.route('/show_webpage<url>')
def show_webpage(url):
    get_webpage(url)
    ww=webWindow('script-webWindow.xml',addon_path,'default')
    ww.doModal()
    plugin.finish()

@plugin.route('/show_genre')
def show_genre():
    items =[
        {'label': 'Action','path': plugin.url_for('show_movies',source='genre',page='1',query='28')},
        {'label': 'Adventure','path': plugin.url_for('show_movies',source='genre',page='1',query='12')},
        {'label': 'Animation','path': plugin.url_for('show_movies',source='genre',page='1',query='16')},
        {'label': 'Comedy','path': plugin.url_for('show_movies',source='genre',page='1',query='35')},
        {'label': 'Crime','path': plugin.url_for('show_movies',source='genre',page='1',query='80')},
        {'label': 'Disaster','path': plugin.url_for('show_movies',source='genre',page='1',query='105')},
        {'label': 'Documentary','path': plugin.url_for('show_movies',source='genre',page='1',query='99')},
        {'label': 'Drama','path': plugin.url_for('show_movies',source='genre',page='1',query='18')},
        {'label': 'Eastern','path': plugin.url_for('show_movies',source='genre',page='1',query='82')},
        {'label': 'Erotic','path': plugin.url_for('show_movies',source='genre',page='1',query='2916')},
        {'label': 'Family','path': plugin.url_for('show_movies',source='genre',page='1',query='10751')},
        {'label': 'Fan film','path': plugin.url_for('show_movies',source='genre',page='1',query='10750')},
        {'label': 'Fantasy','path': plugin.url_for('show_movies',source='genre',page='1',query='14')},
        {'label': 'Film Noir','path': plugin.url_for('show_movies',source='genre',page='1',query='10753')},
        {'label': 'Foreign','path': plugin.url_for('show_movies',source='genre',page='1',query='10769')},
        {'label': 'History','path': plugin.url_for('show_movies',source='genre',page='1',query='36')},
        {'label': 'Holiday','path': plugin.url_for('show_movies',source='genre',page='1',query='10595')},
        {'label': 'Horror','path': plugin.url_for('show_movies',source='genre',page='1',query='27')},
        {'label': 'Indie','path': plugin.url_for('show_movies',source='genre',page='1',query='10756')},
        {'label': 'Music','path': plugin.url_for('show_movies',source='genre',page='1',query='10402')},
        {'label': 'Musical','path': plugin.url_for('show_movies',source='genre',page='1',query='22')},
        {'label': 'Mystery','path': plugin.url_for('show_movies',source='genre',page='1',query='9648')},
        {'label': 'Neo-noir','path': plugin.url_for('show_movies',source='genre',page='1',query='10754')},
        {'label': 'Road Movie','path': plugin.url_for('show_movies',source='genre',page='1',query='1115')},
        {'label': 'Romance','path': plugin.url_for('show_movies',source='genre',page='1',query='10749')},
        {'label': 'Science Fiction','path': plugin.url_for('show_movies',source='genre',page='1',query='878')},
        {'label': 'Short','path': plugin.url_for('show_movies',source='genre',page='1',query='10755')},
        {'label': 'Sport','path': plugin.url_for('show_movies',source='genre',page='1',query='9805')},
        {'label': 'Sporting Event','path': plugin.url_for('show_movies',source='genre',page='1',query='10758')},
        {'label': 'Sports Film','path': plugin.url_for('show_movies',source='genre',page='1',query='10757')},
        {'label': 'Suspense','path': plugin.url_for('show_movies',source='genre',page='1',query='10748')},
        {'label': 'TV Movie','path': plugin.url_for('show_movies',source='genre',page='1',query='10770')},
        {'label': 'Thriller','path': plugin.url_for('show_movies',source='genre',page='1',query='53')},
        {'label': 'War','path': plugin.url_for('show_movies',source='genre',page='1',query='10752')},
        {'label': 'Western','path': plugin.url_for('show_movies',source='genre',page='1',query='37')}
    ]
    return items

@plugin.route('/show_movies/<source>/<page>/<query>')
def show_movies(source,page,query):
    page=int(page)
    plugin.set_content('movies')
    if source =='query':
        if query=='none':query=plugin.keyboard('','Enter Movie Title to Search For')
    if source =='discover':
        if query=='none':plugin.open_settings()
        settings=getSettings()
        query=settings
    items = get_movies(source,page,query)
    addNext = True
    addPrevious = True
    toRemove=[]
    
    for i in items:
        if i['label']=='Next Page >>' or i['label'] == '<< Previous Page':
            toRemove.append(i)
    for i in toRemove:
        items.remove(i)
 
    items.insert(len(items)+1, {
        'label': 'Next Page >>',
        'path': plugin.url_for('show_movies', source=source, page = str(page+1),query=query)
    })
    
    if page > 1:
        items.insert(0, {
            'label': '<< Previous Page',
            'path': plugin.url_for('show_movies', source=source , page= str(page - 1),query=query)
        })
    return items

@plugin.route('/show_actors/<movie_id>')
def show_actors(movie_id):
    actors=getActors(movie_id)
    items = []
    def __context(name,id):
        return [
        (
            'Get Movies for ' + name,
            actions.update_view(plugin.url_for('show_movies', source='actor', page='1', query=str(id)))
        )
            ]
    for actor in actors:
        tagline = format_tagline(actor)
        if actor['profile_path'] !=None and actor['biography'] != None:
            item = {
                'label': actor['name'] + ' - ' + actor['role'],
                'thumbnail': 'http://image.tmdb.org/t/p/w185/' + str(actor['profile_path']),
                'path': plugin.url_for('show_movies',source='actor',page='1',query=actor['id']),
                'context_menu': __context(actor['name'],actor['id']),
                'replace_context_menu': True,
                'info': {
                    'title': actor['name'],
                    'plot': actor['biography'],
                    'tagline': tagline,
                    'title': actor['name'] + ' - ' + actor['role'],
                    'plot': actor['biography'],
                    'tagline': tagline
                        }
                }
            items.append(item)
    return items

@plugin.route('/show_directors/<movie_id>')
def show_directors(movie_id):
    directors=getDirectors(movie_id)
    items = []
    def __context(name,id):
        return [
        (
            'Get Movies for ' + name,
            actions.update_view(plugin.url_for('show_movies', source='director', page='1', query=str(id)))
        )
            ]
    for director in directors:
        tagline = format_tagline(director)
        if director['profile_path'] !=None and director['biography'] != None:
            item = {
                'label': director['name'],
                'thumbnail': 'http://image.tmdb.org/t/p/w185/' + str(director['profile_path']),
                'path': plugin.url_for('show_movies',source='director',page='1',query=director['id']),
                'context_menu': __context(director['name'],director['id']),
                'replace_context_menu': True,
                'info': {
                    'title': director['name'],
                    'plot': director['biography'],
                    'tagline': tagline
                        }
                }
            items.append(item)
    return items

@plugin.route('/show_reviews/<imdb_id>')
def show_reviews(imdb_id):
    reviews=get_reviews(imdb_id)
    items = []
    for review in reviews:
        thumbnail=''
        path=''
        if 'review' in review['links']:path=review['links']['review']

        if review['freshness'] == 'fresh': thumbnail=os.path.join(media_path,'fresh.png')
        if review['freshness'] == 'rotten': thumbnail=os.path.join(media_path,'rotten.png')
        item = {
           'label': review['critic'] + ' - '+ review['publication'],
           'thumbnail': thumbnail,
                'path': plugin.url_for('show_webpage',url=path),
                'info': {
                    'title': review['critic'] + ' - '+ review['publication'],
                    'plot': review['quote']
                        }
                }
        items.append(item)
    return items

def get_reviews(imdb_id):
    reviews = []
    data = {}
    data['type'] = 'imdb'
    data['apikey'] = '99dgtphe3c29y85m2g8dmdmt'
    data['id'] = imdb_id[2:]
    url_values = urllib.urlencode(data)
    url = 'http://api.rottentomatoes.com/api/public/v1.0/movie_alias.json'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    response = urllib2.urlopen(req).read()
    try:
        response = json.loads(response)
        if 'id' in response:
            id=response['id']
            data ={}
            data['review_type']='top_critic'
            data['page_limit'] = 20
            data['country']='us'
            data['apikey'] =  '99dgtphe3c29y85m2g8dmdmt'
            url_values = urllib.urlencode(data)
            url = 'http://api.rottentomatoes.com/api/public/v1.0/movies/' + str(id) + '/reviews.json'
            full_url = url + '?' + url_values
            req = urllib2.Request(full_url)
            response = urllib2.urlopen(req).read() 
            response = json.loads(response)  
            reviews=response['reviews']
    except:
        pass
    return reviews
          
def get_webpage(url):
    global img_file
    data = {}
    data['url'] = url
    url_values = urllib.urlencode(data)
    url = 'http://www.sciweavers.org/iWeb2Shot'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    response = urllib2.urlopen(req)
    name_of_file = 'webpage.jpg'
    img_file = os.path.join(data_path, name_of_file)
    f= open(img_file,'wb')
    f.write(response.read())
    f.close
    
@plugin.cached()
def get_movies(source,page,query):
    if source =='query':
        movieIds=searchTmdb(query,page)
    elif source =='similar':
        movieIds = getTmdbSimilar(query,page)
    elif source == 'discover':
        movieIds = discoverMovies(page,query)
    elif source =='genre':
        movieIds = getMoviesByGenre(query,page)
    elif source =='actor':
        movieIds = getMoviesByActor(query,page)
    elif source =='director' or source =='actor':
        movieIds = getMoviesByPerson(query,page,source)
    else:
        movieIds=getTmdbMovies(source,page)
    movies=[]
    for id in movieIds:
        movies.append(getTmdbMovie(id))
    #Populate Movie Items
    items =[]
    movies=sorted(movies, key=lambda k: k['popularity'],reverse=True)
    for movie in movies:
        context_items=[]
        context_items.append((plugin.addon.getLocalizedString(30001),'XBMC.RunPlugin("plugin://plugin.video.couchpotato_manager/movies/add?title=' + movie['title']+ ')'))
        context_items.append((plugin.addon.getLocalizedString(30002),'XBMC.RunPlugin("plugin://plugin.video.trakt_list_manager/movies/add?title=' + movie['title'] + ')'))
        context_items.append((plugin.addon.getLocalizedString(30000),actions.update_view(plugin.url_for('show_movies', source='similar', page='1', query=movie['id']))))
        context_items.append(('Actors', actions.update_view(plugin.url_for('show_actors',movie_id=movie['id']))))
        context_items.append(('Similar',actions.update_view(plugin.url_for('show_movies', source='similar', page='1', query=movie['id']))))
        context_items.append(('Actors', actions.update_view(plugin.url_for('show_actors',movie_id=movie['id']))))
        context_items.append(('Directors', actions.update_view(plugin.url_for('show_directors',movie_id=movie['id']))))
        context_items.append(('Reviews', actions.update_view(plugin.url_for('show_reviews',imdb_id=movie['imdb']))))
        cast=[]
        for c in movie['cast']:
            cast.append(c['name'])
        item = {
            'label': movie['title'],
            'thumbnail': movie['thumbnail'],
            'info': {
                'title': movie['title'],
                'originaltitle': movie['title'],
                'year': movie['year'],
                'studio': movie['studio'],
                'mpaa': movie['mpaa'],
                'cast': cast,
                'director': movie['director'],
                'genre': movie['genre'],
                'tagline': movie['tagline'],
                'credits': movie.get('writer'),
                'plot':movie['plot'],
                'trailer':movie['trailer'],
                'duration':movie['runtime'],
                'country':movie['country']
            },
            'properties': {
                'fanart_image': movie['fanart'],
            },
            'context_menu': context_items,
            'replace_context_menu': True,
            'is_playable': True,
            'path': movie['trailer']
        } 
        items.append(item)
    return items
    
def getTmdbMovies(source,page):
    movieIds=[]
    data = {}
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    data['page'] = page
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/movie/' + source
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    for result in infostring['results']:
        id=result['id']
        movieIds.append(id)
    return movieIds
    
def getMoviesByGenre(genre,page):
    sort_by=plugin.get_setting('sort_by')
    if sort_by=='0':sort_by='release_date.desc'
    if sort_by=='1':sort_by='release_date.asc'
    if sort_by=='2':sort_by='popularity.desc'
    if sort_by=='3':sort_by='vote_average.desc'
    movieIds=[]
    data = {}
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    data['page'] = page
    data['language']='en'
    data['with_genres']=genre
    data['sort_by']=sort_by
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/discover/movie'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    for result in infostring['results']:
        id=result['id']
        movieIds.append(id)
    return movieIds

def getMoviesByPerson(person_id,page,source):
    movieIds=[]
    data = {}
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    data['page'] = page
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/person/' + actor + '/movie_credits'
    url = 'https://api.themoviedb.org/3/person/' + person_id + '/movie_credits'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    xbmc.log(infostring)
    infostring = json.loads(infostring)
    for cast in infostring['cast']:
        id=cast['id']
        movieIds.append(id)
    if source=='actor':
        for cast in infostring['cast']:
            id=cast['id']
            movieIds.append(id)
    if source=='director':
        for crew in infostring['crew']:
            if crew['job']=='Director':
                id=crew['id']
                movieIds.append(id)

    return movieIds
    
def discoverMovies(page,settings):
    settings=settings.split(',')
    sort_by=settings[0]
    genres=settings[1]
    rating_limit=settings[2]
    release_year=settings[3]
    movieIds=[]
    data = {}
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    data['page'] = page
    data['language']='en'
    data['sort_by']=sort_by
    if rating_limit != '0':data['certification_country'] ='US'
    if release_year != '0':data['primary_release_year'] = release_year
    if rating_limit !='0':data['certification.lte'] = rating_limit
    data['with_genres'] = genres
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/discover/movie'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    for result in infostring['results']:
        id=result['id']
        movieIds.append(id)
    return movieIds
    
def getTmdbSimilar(query,page):
    movieIds=[]
    data = {}
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    data['page']=page
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/movie/' + query + '/similar_movies'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    for result in infostring['results']:
        id=result['id']
        movieIds.append(id)
    return movieIds

def searchTmdb(query,page):
    movieIds=[]
    data = {}
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    data['page']=page
    data['query']=query
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/search/movie'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    for result in infostring['results']:
        id=result['id']
        movieIds.append(id)
    return movieIds    
    
def getTmdbMovie(movieId):
    image_base_url='http://image.tmdb.org/t/p/'
    you_tube_base_url='plugin://plugin.video.youtube/?action=play_video&videoid='
    trailer_url=''
    trailers=[]
    trycount=0
    title=''
    type=''
    thumbnail=''
    fanart=''
    director=''
    writer=''
    cast=[]
    plot=''
    runtime=''
    year=''
    genre=''
    studio=''
    mpaa=''
    tagline=''
    country=[]
    data = {}
    imdb = ''
    popularity=''
    data['append_to_response']='credits,trailers,releases'
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/' + str(movieId)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    movieString = urllib2.urlopen(req).read()
    movieString = unicode(movieString, 'utf-8', errors='ignore')
    movieString = json.loads(movieString)
    imdb = movieString['imdb_id']
    trailers=movieString['trailers']['youtube']
    for trailer in movieString['trailers']['youtube']:
        if 'source' in trailer:
            trailer_url=you_tube_base_url + trailer['source'].encode('ascii', 'ignore')
            type=trailer['type']
            break
    countries = movieString['releases']['countries']
    for c in countries:
        if c['iso_3166_1'] =='US':
            mpaa=c['certification']
    production_countries = movieString['production_countries']
    for c in production_countries:
        country.append(c['name'])
    if len(country)>0:country=country[:-3]
    year=movieString['release_date'][:-3]
    tagline=movieString['tagline']
    fanart=image_base_url + 'w780' +str(movieString['backdrop_path'])
    thumbnail=image_base_url + 'w342'+ str(movieString['poster_path'])
    title=movieString['title']
    plot=movieString['overview']
    runtime=movieString['runtime']
    studios=movieString['production_companies']
    popularity=movieString['popularity']
    for s in studios:
        studio = studio + (s['name']) + " / "
    if len(studio)>0:studio = studio[:-3]
    genres=movieString['genres']
    for g in genres:
        genre=genre+(g['name'])+" / "
    if len(genre)> 0:genre=genre[:-3]
    castMembers = movieString['credits']['cast']
    for castMember in castMembers:
        cast.append({ 'id':castMember['id'], 'name':castMember['name'] })
    crewMembers = movieString['credits']['crew']
    for crewMember in crewMembers:
        if crewMember['job'] =='Director':
            director=director+crewMember['name']+" / "
        if crewMember['department']=='Writing':
            writer=writer+crewMember['name']+" / "
    if len(writer)>0:writer=writer[:-3]
    if len(director)>0:director=director[:-3]
    dictInfo = {'id': movieId,'title':title,'tagline':tagline,'country':country,'trailer': trailer_url, 'trailers':trailers,'year':year,'studio':studio,'mpaa':mpaa,'thumbnail':thumbnail,'fanart':fanart,'director':director,'writer':writer,'plot':plot,'cast':cast,'runtime':runtime,'genre':genre,'source': 'tmdb','type':type} 
    dictInfo = {'id': movieId,'title':title,'imdb':imdb,'popularity':popularity,'tagline':tagline,'country':country,'trailer': trailer_url, 'trailers':trailers,'year':year,'studio':studio,'mpaa':mpaa,'thumbnail':thumbnail,'fanart':fanart,'director':director,'writer':writer,'plot':plot,'cast':cast,'runtime':runtime,'genre':genre,'source': 'tmdb','type':type} 
    return dictInfo

def getActors(movie_id):
    data = {}
    data['append_to_response']='credits'
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/' + str(movie_id)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    movieString = urllib2.urlopen(req).read()
    movieString = unicode(movieString, 'utf-8', errors='ignore')
    movieString = json.loads(movieString)
    cast=movieString['credits']['cast']
    cast=sorted(cast, key=lambda k: k['order'])
    actors=[]
    for castMember in cast:
        actor = getPerson(castMember['id'])
        actor['role']=castMember['character']
        actors.append(actor)
    sorted_actors=sorted(actors, key=lambda k: k['id'])
    return sorted_actors

@plugin.cached() 
def getDirectors(movie_id):
    data = {}
    data['append_to_response']='credits'
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/' + str(movie_id)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    movieString = urllib2.urlopen(req).read()
    movieString = unicode(movieString, 'utf-8', errors='ignore')
    movieString = json.loads(movieString)
    crew=movieString['credits']['crew']
    directors=[]
    for crewMember in crew:
        if crewMember['job']=='Director':
            director = getPerson(crewMember['id'])
            directors.append(director)
    return directors
   
def getPerson(person_id):
    data = {}
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/person/' + str(person_id)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    personString = urllib2.urlopen(req).read()
    personString = json.loads(personString)
    return personString

def getSettings():
    release_year=plugin.get_setting('release_year') 
    rating_limit=plugin.get_setting('rating_limit')
    if rating_limit=='1':rating_limit='G'
    if rating_limit=='2':rating_limit='PG'
    if rating_limit=='3':rating_limit='PG-13'
    if rating_limit=='4':rating_limit='R'
    if rating_limit=='5':rating_limit='NC17'
    genres=''
    if plugin.get_setting('g_action',bool): genres=genres + '28|'
    if plugin.get_setting('g_adventure',bool): genres=genres + '12|'
    if plugin.get_setting('g_animation',bool): genres=genres + '16|'
    if plugin.get_setting('g_comedy',bool): genres=genres + '35|'
    if plugin.get_setting('g_crime',bool): genres=genres + '80|'
    if plugin.get_setting('g_disaster',bool): genres=genres + '105|'
    if plugin.get_setting('g_documentary',bool): genres=genres + '99|'
    if plugin.get_setting('g_drama',bool): genres=genres + '18|'
    if plugin.get_setting('g_eastern',bool): genres=genres + '82|'
    if plugin.get_setting('g_erotic',bool): genres=genres + '2916|'
    if plugin.get_setting('g_family',bool): genres=genres + '10751|'
    if plugin.get_setting('g_fan_film',bool): genres=genres + '10750|'
    if plugin.get_setting('g_fantasy',bool): genres=genres + '14|'
    if plugin.get_setting('g_film_noir',bool): genres=genres + '10753|'
    if plugin.get_setting('g_foreign',bool): genres=genres + '10769|'
    if plugin.get_setting('g_history',bool): genres=genres + '36|'
    if plugin.get_setting('g_holiday',bool): genres=genres + '10595|'
    if plugin.get_setting('g_horror',bool): genres=genres + '27|'
    if plugin.get_setting('g_indie',bool): genres=genres + '10756|'
    if plugin.get_setting('g_music',bool): genres=genres + '10402|'
    if plugin.get_setting('g_musical',bool): genres=genres + '22|'
    if plugin.get_setting('g_mystery',bool): genres=genres + '9648|'
    if plugin.get_setting('g_neo_noir',bool): genres=genres + '10754|'
    if plugin.get_setting('g_road_movie',bool): genres=genres + '1115|'
    if plugin.get_setting('g_romance',bool): genres=genres + '10749|'
    if plugin.get_setting('g_science_fiction',bool): genres=genres + '878|'
    if plugin.get_setting('g_short',bool): genres=genres + '10755|'
    if plugin.get_setting('g_sport',bool): genres=genres + '9805|'
    if plugin.get_setting('g_sporitng_event',bool): genres=genres + '10758|'
    if plugin.get_setting('g_sports_film',bool): genres=genres + '10757|'
    if plugin.get_setting('g_suspense',bool): genres=genres + '10748|'
    if plugin.get_setting('g_tv_movie',bool): genres=genres + '10770|'
    if plugin.get_setting('g_thriller',bool): genres=genres + '53|'
    if plugin.get_setting('g_war',bool): genres=genres + '10752|'
    if plugin.get_setting('g_western',bool): genres=genres + '37|'
    sort_by=plugin.get_setting('sort_by')
    if sort_by=='0':sort_by='release_date.desc'
    if sort_by=='1':sort_by='release_date.asc'
    if sort_by=='2':sort_by='popularity.desc'
    if sort_by=='3':sort_by='vote_average.desc'
    settings=sort_by +','+genres+','+rating_limit+','+release_year
    return settings

def format_tagline(actor):
    tagline=''
    place_of_birth=''
    birthday=''
    if actor['place_of_birth']!='' and str(actor['place_of_birth'])!='None':
        place_of_birth = actor['place_of_birth']
    if actor['birthday']!='' and str(actor['birthday'])!='None':
        birthday = format_date(actor['birthday'])    
    if place_of_birth !='' and birthday !='':
        tagline= 'Born in ' + place_of_birth + ' on ' + birthday
    elif place_of_birth !='':
        tagline = 'Born in ' + place_of_birth
    elif birthday != '':
        tagline = 'Born on ' + birthday
    return tagline

def format_date(strDate):
    strDate=str(strDate)
    if strDate=='None':strDate=''
    if '-' in strDate:
        d=strDate.split('-')
        if d[1]=='01':d[1]='January'
        if d[1]=='02':d[1]='February'
        if d[1]=='03':d[1]='March'
        if d[1]=='04':d[1]='April'
        if d[1]=='05':d[1]='May'
        if d[1]=='06':d[1]='June'
        if d[1]=='07':d[1]='July'
        if d[1]=='08':d[1]='August'
        if d[1]=='09':d[1]='September'
        if d[1]=='10':d[1]='October'
        if d[1]=='11':d[1]='November'
        if d[1]=='12':d[1]='December'
        strDate=d[1] + ' ' + d[2] + ', ' + d[0]
    return strDate

def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id])
    else:
        plugin.log.warning('String is missing: %s' % string_id)
        return string_id

class webWindow(xbmcgui.WindowXMLDialog):
    def onInit(self):   
        global img_file
        maxWidth=1024
        im = Image.open(img_file)
        w=im.size[0]
        h=im.size[1]
        r = w / maxWidth
        h = h * r
        self.getControl(32900).setHeight(h)
        self.getControl(32900).setWidth(maxWidth)
        self.getControl(32900).setImage(img_file)  

    def onAction(self, action):
        ACTION_UP = 3
        ACTION_DOWN = 4
        ACTION_PREVIOUS_MENU = 10

        if action==ACTION_PREVIOUS_MENU:
            self.close()

        if action==ACTION_DOWN:
            im = Image.open(img_file)
            im_w=im.size[0]
            im_h=im.size[1]
            x = self.getControl(32900).getX()
            y = self.getControl(32900).getY()
            i=0
            i=i-im_h
            i=i+720
            y=y-100
            xbmc.log('i = ' + str(i))
            xbmc.log('y = ' +str(y))
            if y > i: 
                self.getControl(32900).setPosition(x,y)

        if action==ACTION_UP:
            im = Image.open(img_file)
            im_w=im.size[0]
            im_h=im.size[1]
            x = self.getControl(32900).getX()
            y = self.getControl(32900).getY()
            if y < 0:
                y=y+100 
                self.getControl(32900).setPosition(x,y)

if __name__ == '__main__':
    plugin.run()
