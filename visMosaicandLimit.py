import ee 
from ee_plugin import Map 

paleta = [ 
        'ffffff','129912','1f4423','006400','00ff00','687537','76a5af','29eee4','77a605','935132','bbfcac',
        '45c2a5','b8af4f','f1c232','ffffb2','ffd966','f6b26b','f99f40','e974ed','d5a6bd','c27ba0','fff3bf',
        'ea9999','dd7e6b','aa0000','ff99ff','0000ff','d5d5e5','dd497f','b2ae7c','af2a2a','8a2be2','968c46',
        '0000ff','4fd3ff','645617','f3b4f1','02106f','02106f','c59ff4','ba87f8','e787f8','cca0d4','d082de',
        'cd49e4','e04cfa']
visualizar = {
    'visclass2': {
            "min": 0, 
            "max": 34,
            "palette":  [ 
                'ffffff','129912','1f4423','006400','00ff00','687537','76a5af','29eee4','77a605','935132','bbfcac',
                '45c2a5','b8af4f','f1c232','ffffb2','ffd966','f6b26b','f99f40','e974ed','d5a6bd','c27ba0','fff3bf',
                'ea9999','dd7e6b','aa0000','ff99ff','0000ff','d5d5e5','dd497f','b2ae7c','af2a2a','8a2be2','968c46',
                '0000ff','4fd3ff'],
            "format": "png"
    },
    'visclassC5': {
            "min": 0, 
            "max": 45,
            "palette":  [ 
                'ffffff','129912','1f4423','006400','00ff00','687537','76a5af','29eee4','77a605','935132','bbfcac',
                '45c2a5','b8af4f','f1c232','ffffb2','ffd966','f6b26b','f99f40','e974ed','d5a6bd','c27ba0','fff3bf',
                'ea9999','dd7e6b','aa0000','ff99ff','0000ff','d5d5e5','dd497f','b2ae7c','af2a2a','8a2be2','968c46',
                '0000ff','4fd3ff','645617','f3b4f1','02106f','02106f','c59ff4','ba87f8','e787f8','cca0d4','d082de',
                'cd49e4','e04cfa'],
            "format": "png"
    },
    'visMosaic': {
        'min': 0,
        'max': 200,
        'bands': ['median_red', 'median_green', 'median_blue']
    },
    'visMosaicS2': {
        'min': 0,
        'max': 0.25,
        'bands': ['B4', 'B3', 'B2']
    },
    'props': { 
        'textColor': 'ff0000', 
        'outlineColor': 'ffffff', 
        'outlineWidth': 1.5, 
        'outlineOpacity': 0.2
    }    
} 
param = { 
    'assetMapB4': 'projects/mapbiomas-workspace/public/collection4_1/mapbiomas_collection41_integration_v1',
    'assetCol5' : "projects/mapbiomas-workspace/public/collection5/mapbiomas_collection50_integration_v1",
    'assetBaciaC4': 'users/CartasSol/shapes/baciasRecticadaCaatinga',
    'assetBaciaC5': "users/nerivaldogeo/bacias_caatinga_f",
    'assetlimitNew': 'users/CartasSol/shapes/nCaatingaBff3000',
    'assetlimit': 'users/CartasSol/shapes/Caatinga',
    'assetMosaic': 'projects/mapbiomas-workspace/MOSAICOS/workspace-c3',  

    'classMapB': [3, 4, 5, 9,12,13,15,18,19,20,21,22,23,24,25,26,29,30,31,32,33],
    'classNew': [3, 4, 3, 3,12,12,21,21,21,21,21,22,22,22,22,33,29,22,33,12,33],
    'anos': [],
    'bandas': ['median_red', 'median_green', 'median_blue'],
    #'743','732','747',
    'listaNameBacias': [
        '741','742','744', '745','746','749','751','752','753', '754',
        '755','756','757','758','759','76111','76116','7612','7613',
        '7614','7615','7616', '7617','7618','7619','762','763','764','765',
        '766','767','771','772','773', '774', '775','776','777','778'
    ]

}
ano = '2018'

limitCaatC5 = ee.FeatureCollection(param['assetlimit']) 
FeatColbacia = ee.FeatureCollection(param['assetBaciaC4'])

Mosaicos = ee.ImageCollection(param['assetMosaic']).filter(
                    ee.Filter.Or(
                        ee.Filter.eq("biome", 'CAATINGA'),
                        ee.Filter.eq("biome", 'CERRADO'),
                        ee.Filter.eq("biome", 'MATAATLANTICA')
                    ))\
                    .filterBounds(FeatColbacia).select(param['bandas'])\
                    .filter(ee.Filter.eq('year', int(ano))).mosaic()\
                    .clip(FeatColbacia).divide(10)

imgMap5_0 = ee.Image(param['assetCol5']).clip(limitCaatC5).select('classification_' + ano)
FeatBacias = ee.Image().byte().paint(FeatColbacia, 1, 1)
Featlimit = ee.Image().byte().paint(limitCaatC5, 1, 2)




# Map.addLayer(imgMap5_0, {min:1, max: 45, 'palette': paleta }, 'Col5')
Map.addLayer(imgMap5_0.visualize(**visualizar['visclassC5']))
# Map.addLayer(Featlimit, {'palette': '0000FF','opacity': 0.75}, 'lCaatinga')
# Map.addLayer(FeatBacias, {'palette': 'FF0000', 'opacity': 0.8}, 'Bacias')
# Map.addLayer(Mosaicos.visualize(**visualizar['visMosaic']))
#Center to point
Map.centerObject(limitCaatC5, 6)