STATIC_POSTER = 'static_poster.png'

import hashlib, inspect, os

def Start():
  pass

class StaticMediaAgent(Agent.Movies):

  name = 'Static Media'
  languages = [Locale.Language.NoLanguage]
  primary_provider = True
  accepts_from = ['com.plexapp.agents.localmedia']

  def search(self, results, media, lang):

    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 99, lang = lang))

  def update(self, metadata, media, lang):

    if Prefs['static_poster_path']:
      data = Core.storage.load(Prefs['static_poster_path'])
    else:
      data = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_POSTER))
    
    media_hash = hashlib.md5(data).hexdigest()

    if media_hash not in metadata.posters:
      metadata.posters[media_hash] = Proxy.Media(data, sort_order=1)
      Log('Static poster added for %s' % metadata.title)
