SELECT PATH FROM [dam:Asset] AS a WHERE 
a.[jcr:content/dam:assetState] = 'processed' AND a.[jcr:content/contentFragment] IS NULL 
AND 
(a.[jcr:content/metadata/lcl:ims] ='GS1 Ecommerce' 
AND a.[jcr:content/metadata/lcl:facing] ='front' 
AND (a.[jcr:content/metadata/lcl:imageCategory] ='ecomm' OR a.[jcr:content/metadata/lcl:imageCategory] ='marketing'))
AND ISDESCENDANTNODE(a,[/content/dam/loblaw-companies-limited/product-assets/pharmacy])
AND a.[jcr:content/jcr:lastModified] > CAST('2021-02-22T15:02:00.000Z' AS DATE)


SELECT PATH FROM [dam:Asset] AS a WHERE 
a.[jcr:content/dam:assetState] = 'processed' 
AND a.[jcr:content/contentFragment] IS NULL 
AND 
(a.[jcr:content/metadata/lcl:ims] = 'Marketing' AND (a.[jcr:content/metadata/lcl:imageCategory] = 'ecomm' OR a.[jcr:content/metadata/lcl:imageCategory] = 'marketing') 
AND ISDESCENDANTNODE(a,[/content/dam/loblaw-companies-limited/product-assets/]))


SELECT PATH FROM [dam:Asset] AS a WHERE 
a.[jcr:content/dam:assetState] = 'processed' 
AND a.[jcr:content/contentFragment] IS NULL 
AND a.[jcr:content/metadata/lcl:ims] = 'GS1 Marketing' 
AND a.[jcr:content/metadata/lcl:facing] = 'front'
AND ISDESCENDANTNODE(a,[/content/dam/loblaw-companies-limited/product-assets/])

SELECT PATH FROM [dam:Asset] AS a WHERE 
a.[jcr:content/dam:assetState] = 'processed' 
AND a.[jcr:content/contentFragment] IS NULL 
AND a.[jcr:content/metadata/lcl:ims] = 'GS1 Marketing' 
AND a.[jcr:content/metadata/lcl:imageAngle] = 'centre'
AND ISDESCENDANTNODE(a,[/content/dam/loblaw-companies-limited/product-assets/])