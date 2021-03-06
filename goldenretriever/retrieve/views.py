import json
import urllib.request
from urllib.parse import urlparse

import bs4
from django.http import Http404
from django.shortcuts import render_to_response, HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

urlval = URLValidator()

def retrieve(request):
    if request.method == 'GET':
        response = dict(error='false')
        siteurl = request.GET.get('url', None)
        try:
            urlval(siteurl)
        except ValidationError:
            response.update({'msg': 'Invalid URL', 'error': 'true'})
        else:
            # Use BeautifulSoup to parse the site's HTML looking for images
            # and stores the result in 'allimages'.
            soup = bs4.BeautifulSoup(urllib.request.urlopen(siteurl))
            response['title'] = soup.find("title").string
            allimages = soup.findAll("img")
            if len(allimages) == 0:
                # No images found
                response.update({'msg': 'No images found', 'error': 'true'})
            elif len(allimages) == 1:
                # Returns the only image
                response['imgsrc'] = urllib.parse.urljoin(siteurl, allimages[0]['src'])
            else:
                for image in allimages:
                    try:
                        imgsrc = image['src']
                        if not imgsrc:
                            # Source attribute might be empty
                            continue
                        else:
                            if not imgsrc.endswith('.gif'):
                                # Returns the first image in the document that is not a gif.
                                response['imgsrc'] = urllib.parse.urljoin(siteurl, imgsrc)
                                break
                    except KeyError:
                        continue

                # Fallbacks to the first image
                response.setdefault('imgsrc', urllib.parse.urljoin(siteurl, allimages[0]['src']))

        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        # Handling only GET requests
        raise Http404


def home(request):
    return render_to_response('home.html')
