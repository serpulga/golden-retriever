import json
import urllib2
import urlparse

from BeautifulSoup import BeautifulSoup as bs
from django.http import Http404
from django.shortcuts import render_to_response, HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

urlval = URLValidator()

def retrieve(request):
    if request.method == 'GET':
        siteurl = request.GET.get('url', None)
        response = dict(error='false')
        try:
            urlval(siteurl)
        except ValidationError:
            response.update({'msg': 'Invalid URL', 'error': 'true'})
        else:
            # Use BeautifulSoup to parse the site's HTML looking for images
            # and stores the result in 'allimages'.
            soup = bs(urllib2.urlopen(siteurl))
            response['title'] = soup.find("title").string
            allimages = soup.findAll("img")
            if len(allimages) == 0:
                # No images found
                response.update({'msg': 'No images found', 'error': 'true'})
            elif len(allimages) == 1:
                # Returns the only image
                response['imgsrc'] = urlparse.urljoin(siteurl, allimages[0]['src'])
            else:
                for image in allimages:
                    if not image['src'].endswith('.gif'):
                        # Returns the first image in the document that is not a gif.
                        response['imgsrc'] = urlparse.urljoin(siteurl, allimages[0]['src'])
                    
                # Fallbacks to the first image
                response.setdefault('imgsrc', urlparse.urljoin(siteurl, allimages[0]['src']))
            
        return HttpResponse(json.dumps(response), content_type='application/json')
            
    else:
        # Handling only GET requests
        raise Http404
                    

def home(request):
    return render_to_response('home.html')

                
            