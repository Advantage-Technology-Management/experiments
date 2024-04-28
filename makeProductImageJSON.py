
import json
import datetime
import requests

products = ["https://dis-prod.assetful.loblaw.ca/content/product/styleCode/T4WR043080009/*.json"]
#,"https://dis-prod.assetful.loblaw.ca/content/product/styleCode/T4WR043080009/*.json"]

for product in products:
    getRequest = "https://dis-prod.assetful.loblaw.ca/content/product/styleCode/T4WR043080011/*.json"
    response = requests.get(getRequest)
#print(response.text)
    assets = json.loads(response.text)

#image_filename = "/apparel/apparel/women-s-tops/sweaters-women-s/pullover/t4wr043080_ea/t4wr043080_jf-black_ea/"

HOSTURL = "https://dis-prod.assetful.loblaw.ca/content/dam/"
RENDITIONTEXT = "/_jcr_content/renditions/cq5dam.web.4096.4096.jpeg"

count = 0
imagesizes = ["32","120","400","800","2000"]
print('{"product-assets" : [')
for asset in assets['assets']:
    #print(asset['productPath'])
    #print("Product", asset)
    url = HOSTURL+asset['productPath']+RENDITIONTEXT
    imageAngle = asset['imageAngle']
    presentationType = asset['presentationType']
    en = asset['colourCode']
    fr = asset['colourCode']
    standardEn = asset['colourCode']
    standardFr = asset['colourCode']
    colorUrl = asset['colourCode']
    colorStandardUrl =asset['colourCode']


    for article in asset['articleId']:
        liam = article+"_EA"
        styleCode = article[:-3]
        image_angles = []
        
        
        imageJSON = {
            "product_type" : "JF",
            "liam" : liam,
            "article_number" : article,
            "style_code" : styleCode,
            "last_update_ts" : datetime.datetime.now().isoformat(),
            "thumbnail_image" : url+"?imWidth=32", "image_angles" : image_angles,
            "options": {
                "color": {
                    "en": en,
                    "fr": fr,
                    "standard_en": standardEn,
                    "standard_fr": standardFr,
                    "url": colorStandardUrl,
                    "standard_url": colorUrl
                }
            }
        }
        
        for imagesize in imagesizes:
            image_angle = {"url" : url+"?imWidth="+imagesize, "angle" : imageAngle, "presentation_type" : presentationType, "height" : imagesize, "width" : imagesize, "rank" : "999"}
            image_angles.append(image_angle)
    y =json.dumps(imageJSON)
    print(y,",")
print(']}')
        


