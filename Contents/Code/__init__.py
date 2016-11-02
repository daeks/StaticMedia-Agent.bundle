STATIC_POSTER = 'static_poster.png'
STATIC_BACKGROUND = 'static_background.png'

import hashlib, inspect, os

def Start():
  pass
  
def ValidatePrefs():
  pass

class StaticMediaAgent(Agent.Movies):

  name = 'Static Media'
  languages = [Locale.Language.NoLanguage]
  primary_provider = True
  accepts_from = ['com.plexapp.agents.localmedia']

  def search(self, results, media, lang):

    Log('Searching for %s' % media.name)
    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):
  
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
        Log('Static poster added for %s' % metadata.title)
    
    if Prefs['static_background']:  
      if Prefs['static_background_path']:
        data = Core.storage.load(Prefs['static_background_path'])
      else:
        data = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_BACKGROUND))
      
      media_hash = hashlib.md5(data).hexdigest()

      if media_hash not in metadata.art:
        metadata.art[media_hash] = Proxy.Media(data, sort_order=1)
        Log('Static background added for %s' % metadata.title)  
