STATIC_POSTER = 'static_poster.png'
STATIC_BACKGROUND = 'static_background.png'

import hashlib, inspect, os

def Start():
  pass
  
def ValidatePrefs():
  pass
  
def loadStaticMediaMovies(metadata, media):
  part = media.items[0].parts[0]
  (root_file, ext) = os.path.splitext(os.path.basename(part.file))
  metadata.title = root_file

  if Prefs['static_poster']:  
    if Prefs['static_poster_path']:
      data = Core.storage.load(Prefs['static_poster_path'])
    else:
      data = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_POSTER))
    media_hash = hashlib.md5(data).hexdigest()

    if media_hash not in metadata.posters:
      metadata.posters[media_hash] = Proxy.Media(data, sort_order=1)
      Log('[STATIC] Static poster added for %s' % metadata.title)
  
  if Prefs['static_background']:  
    if Prefs['static_background_path']:
      data = Core.storage.load(Prefs['static_background_path'])
    else:
      data = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_BACKGROUND))
    media_hash = hashlib.md5(data).hexdigest()

    if media_hash not in metadata.art:
      metadata.art[media_hash] = Proxy.Media(data, sort_order=1)
      Log('[STATIC] Static background added for %s' % metadata.title)

def loadStaticMediaTVShows(metadata, media):
  metadata.title = media.title
  
  if Prefs['static_poster']:  
    if Prefs['static_poster_path']:
      poster = Core.storage.load(Prefs['static_poster_path'])
    else:
      poster = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_POSTER))
    media_hash_poster = hashlib.md5(poster).hexdigest()
    
    if Prefs['static_background_path']:
      background = Core.storage.load(Prefs['static_background_path'])
    else:
      background = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_BACKGROUND))
    media_hash_background = hashlib.md5(background).hexdigest()
    
    if media_hash_poster not in metadata.posters:
      metadata.posters[media_hash_poster] = Proxy.Media(poster, sort_order=1)
      Log('[STATIC] Static poster added for %s' % metadata.title)
    
    for snum, season in media.seasons.iteritems():       
      if media_hash_poster not in metadata.seasons[season.index].posters:
        metadata.seasons[season.index].posters[media_hash_poster] = Proxy.Media(poster, sort_order=1)
        Log('[STATIC] Static poster added for season %s' % season.index)
      
      for enum, episode in season.episodes.iteritems():         
        part = episode.items[0].parts[0]
        (root_file, ext) = os.path.splitext(os.path.basename(part.file))
        metadata.seasons[season.index].episodes[episode.index].title = root_file
        
        if media_hash_background not in metadata.seasons[season.index].episodes[episode.index].thumbs:
          metadata.seasons[season.index].episodes[episode.index].thumbs[media_hash_background] = Proxy.Media(background, sort_order=1)
          Log('[STATIC] Static thumb added for %s' % root_file)
      
  if Prefs['static_background']:
    if Prefs['static_background_path']:
      data = Core.storage.load(Prefs['static_background_path'])
    else:
      data = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_BACKGROUND))
    media_hash = hashlib.md5(data).hexdigest()
    
    if media_hash not in metadata.art:
      metadata.art[media_hash] = Proxy.Media(data, sort_order=1)
      Log('[STATIC] Static background added for %s' % metadata.title)

    for snum, season in media.seasons.iteritems():       
      if media_hash not in metadata.seasons[season.index].art:
        metadata.seasons[season.index].art[media_hash] = Proxy.Media(data, sort_order=1)
        Log('[STATIC] Static background added for season %s' % season.index)
      
      for enum, episode in season.episodes.iteritems():         
        part = episode.items[0].parts[0]
        (root_file, ext) = os.path.splitext(os.path.basename(part.file))
        metadata.seasons[season.index].episodes[episode.index].title = root_file
 
class StaticMediaAgent(Agent.Movies):

  name = 'Static Media'
  languages = [Locale.Language.NoLanguage]
  primary_provider = True
  accepts_from = ['com.plexapp.agents.localmedia']

  def search(self, results, media, lang):

    Log('[STATIC] Searching for %s' % media.name)
    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):
  
    loadStaticMediaMovies(metadata, media)
  
class StaticMediaAgent(Agent.TV_Shows):

  name = 'Static Media'
  languages = [Locale.Language.NoLanguage]
  primary_provider = True
  accepts_from = ['com.plexapp.agents.localmedia']

  def search(self, results, media, lang):

    Log('[STATIC] Searching for %s' % media.show)
    results.Append(MetadataSearchResult(id = media.id, name = media.show, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):
  
    loadStaticMediaTVShows(metadata, media)
