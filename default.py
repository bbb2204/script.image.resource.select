import sys
import xbmc, xbmcgui, xbmcaddon
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__        = xbmcaddon.Addon()
__addonid__      = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')
__cwd__          = __addon__.getAddonInfo('path').decode('utf-8')

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode('utf-8')
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode('utf-8'), level=xbmc.LOGDEBUG)

class Main:
    def __init__(self):
        TYPE = self._parse_argv()
        if TYPE:
            ITEMS = self._get_addons(TYPE)
            self._select(ITEMS, TYPE)

    def _parse_argv(self):
        TYPE = None
        try:
            params = dict(arg.split('=') for arg in sys.argv[ 1 ].split('&'))
        except:
            params = {}
        log('params: %s' % params)
        TYPE = params.get('type', '')
        return TYPE

    def _get_addons(self, TYPE):
        listitems = []
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddons", "params": {"type": "kodi.resource.images", "properties": ["name", "thumbnail"]}, "id": 1}')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and (json_response['result'] != None) and json_response['result'].has_key('addons'):
            for item in json_response['result']['addons']:
                if item['addonid'].startswith(TYPE):
                    name = item['name']
                    icon = item['thumbnail']
                    path = item['addonid']
                    listitem = xbmcgui.ListItem(label=name, label2=path, iconImage='DefaultAddonImages.png', thumbnailImage=icon)
                    listitems.append(listitem)
        return listitems

    def _select(self, addonlist, category):
        w = Gui('DialogSelect.xml', __cwd__, listing=addonlist, category=category)
        w.doModal()
        del w

class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listing = kwargs.get('listing')
        self.type = kwargs.get('category')

    def onInit(self):
        self.container = self.getControl(6)
        self.button = self.getControl(5)
        self.getControl(3).setVisible(False)
        self.getControl(1).setLabel(xbmc.getLocalizedString(20464) % xbmc.getLocalizedString(24000))
        self.button.setLabel(xbmc.getLocalizedString(21452))
        listitem = xbmcgui.ListItem(label=xbmc.getLocalizedString(231), iconImage='DefaultAddonNone.png')
        self.container.addItem(listitem)
        for item in self.listing :
            self.container.addItem(item)
        self.setFocus(self.container)

    def onAction(self, action):
        if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448,):
            self.close()

    def onClick(self, controlID):
        if controlID == 6:
            num = self.container.getSelectedPosition()
            if num == 0:
                xbmc.executebuiltin('Skin.Reset(%s)' % self.type)
            else:
                path = self.container.getSelectedItem().getLabel2()
                xbmc.executebuiltin('Skin.SetString(%s,%s)' % (self.type, 'resource://%s/' % path))
            xbmc.sleep(100)
            self.close()
        elif controlID == 5:
            xbmc.executebuiltin('ActivateWindow(AddonBrowser, addons://repository.xbmc.org/kodi.resource.images/)')
            xbmc.sleep(100)
            self.close()

    def onFocus(self, controlID):
        pass


if (__name__ == '__main__'):
    log('script version %s started' % __addonversion__)
    Main()
log('script stopped')