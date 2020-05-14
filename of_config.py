db = {'host':'rds593f78790z8p64dz1.mysql.rds.aliyuncs.com',
      'port': 3306,
      'user':'lin',
      'passwd':'Qwert123',
      'database':'channel_chic_mini',
      'charset':'utf8'}

rqueue = {'host':'localhost',
           'port':'6379',
           'key':'ofashion'}

spiders = 'spiders' # spider路径

status_new = 'new'
status_failed = 'failed'
status_finished = 'finished'

unit_euro = 'EURO'
unit_jpy = 'JPY'
unit_hkd = 'HKD'
unit_rmb = 'RMB'
unit_usd = 'USD'

mapping = { 'store.tods.cn': 'tods',
            'cn.vancleefarpels.com': 'vancleef',
            'www.vancleefarpels.cn':'vancleef',
            'www.omegawatches.cn': 'omega',
            'www.longines.cn': 'longines',
            'www.patek.com': 'patek',
            'www.vacheron-constantin.cn': 'constantin',
            'cn.jaeger-lecoultre.com': 'lecoultre',
            'www.panerai.cn': 'panerai',
            'www.iwc.com': 'iwc',
            'www.iwc.cn': 'iwc',
            'www.blancpain.com': 'blancpain',
            'www.audemarspiguet.com': 'audemarspiguet',
            'www.breguet.com': 'breguet',
            'www.chaumet.cn': 'chaumet',
            'www.chaumet.com':'chaumet',
            'www.tudorwatch.cn': 'tudor',
            'www.mikimoto.com.hk': 'mikimoto',
            'store.stellamccartney.cn': 'stellamccartney',
            'cn.boucheron.com': 'boucheron',
            'www.girard-perregaux.com': 'perregaux',
            'www.kenzoparfums.cn': 'kenzo',
            'www.kenzo.com': 'kenzo',
            'www.loreal-paris.com.hk': 'loreal',
            'www.lancome.com.cn': 'lancome',
            'cn.chowsangsang.com': 'chowsangsang',
            'www.skii.com.cn': 'skii',
            'www.jeanrichard.com': 'jeanrichard',
            'www.ulysse-nardin.com': 'nardin',
            'cn.qeelin.com': 'qeelin',
            'www.pomellato.com': 'pomellato',
            'cn.puma.com': 'puma',
            'www.esteelauder.com.cn': 'esteelauder',
            'www.swarovski.com.cn': 'swarovski',
            'www.olay.com.cn': 'olay',
            'cn.ecco.com': 'ecco',
            'www.dhc.net.cn': 'dhc',
            'www.danielwellington.cn': 'danielwellington',
            'www.ysl.com': 'ysl',
            'www.yslbeautycn.com': 'ysl',
            'www.gucci.cn': 'gucci',
            'www.bottegaveneta.com': 'bv',
            'china.elizabetharden.com': 'elizabetharden',
            'www.etro.com': 'etro',
            'cn.fresh.com': 'fresh',
            'www.fancl.com.cn': 'fancl',
            'www.guerlain.com.cn': 'guerlain',
            'www.giuseppezanotti.cn': 'giuseppezanotti',
            'www.hublot.cn': 'hublot',
            'www.helenarubinstein.cn': 'helenarubinstein',
            'www.hamiltonwatch.com': 'hamiltonwatch',
            'www.kanebo-global.com': 'kanebo',
            'www.isaknox.com.hk': 'isaknox',
            'www.innisfree.cn': 'innisfree',
            'www.freeplus.cn': 'freeplus',
            'www.lunasol-net.com': 'lunasol',
            'www.izzue.com': 'izzue',
            'www.jurlique.com.cn': 'jurlique',
            'www.kiehls.com.cn': 'kiehls',
            'sekkisei.kose.com.cn': 'kose',
            'store.moncler.cn': 'moncler',
            'www.hugoboss.cn': 'hugoboss',
            'cn.mcmworldwide.com': 'mcm',
            'www.harrywinston.cn': 'harrywinston',
            'www.arcteryx.com': 'arcteryx',
            'cn.sportmax.com': 'sportmax',
            'www.maje.cn': 'maje',
            'www.sandro-paris.cn': 'sandroparis',
            'www.pinko.com': 'pinko',
            'www.chopard.cn': 'chopard',
            'www.debeers.com.cn': 'debeers',
            'www.dsquared2.cn': 'dsquared2',
            'www.jimmychoo.cn': 'jimmychoo',
            'www.banilaco.com.cn': 'banilaco',
            'www.chanel.com': 'chanel',
            'www.chanel.cn': 'chanel',
            'www.dior.cn': 'dior',
            'www.louisvuitton.cn': 'louisvuitton',
            'www.prada.com': 'prada',
            'cn.burberry.com': 'burberry',
            'store.balenciaga.cn': 'balenciaga',
            'www.cartier.cn': 'cartier',
            'www.tiffany.cn': 'tiffany',
            'store.dolcegabbana.com': 'dolcegabbana',
            'china.coach.com': 'coach',
            'www.valentinodaydream.cn': 'valentino',
            'www.valentino.com.cn': 'valentino',
            'www.chloe.cn': 'chloe',
            'www.acnestudios.com': 'acnestudios',
            'www.alexandermcqueen.cn': 'alexandermcqueen',
            'www.alexandermcqueen.com.cn': 'alexandermcqueen',
            'www.alexanderwang.cn': 'alexanderwang',
            'www.apm-monaco.cn': 'apmmonaco',
            # 'www.apm-monaco.cn': 'apm',
            'www.hermes.cn': 'hermes',
            'www.bally.cn': 'bally',
            'www.bobbibrown.com.cn': 'bobbibrown',
            'www.loewe.com': 'loewe',
            'www.michaelkors.cn': 'michaelkors',
            'www.ferragamo.cn': 'ferragamo',
            'www.stuartweitzman.cn': 'stuartweitzman',
            'www.furla.cn': 'furla',
            'www.givenchy.com': 'givenchy',
            'www.givenchybeauty.cn': 'givenchybeauty',
            'www.bulgari.cn':'bulgari',
            'www.celine.com':'celine',
            'www.versace.cn':'versace',
            'store.miumiu.cn':'miumiu',
            'www.fendi.cn':'fendi',
            'cn.iteshop.com':'it',
            'cn.pandora.net':'pandora',
            'www.montblanc.cn':'montblanc',
            'www.zegna.cn':'zegna',
            'www.dunhill.cn':'dunhill',
            'www.hogan.cn':'hogan',
            'www.armani.com':'armani',
            'www.giorgioarmanibeauty.cn':'armani_beauty',
            'www.rolex.cn':'rolex',
            'www.piaget.cn':'piaget',
            'www.tods.cn':'tods',
            'www.laprairie.com.cn':'laprairie',
            'qeelinchina.com':'qeelinchina',
            'www.lorealparis.com.cn':'lorealparis',
            'www.maccosmetics.com.cn':'mac',
            'www.ipsa.com.cn':'ipsa',
            'www.marcjacobs.com':'marcjacobs',
            'cn.maxmara.com':'maxmara',
            'www.jomalone.com.cn':'jomalone',
            'eshop.narshk.com':'narshk',
            'www.cledepeau-beaute.com.cn':'cpb',
            'store.nike.com':'nike',
            'www.y-3.com':'y3',
            'www.champion.com':'champion',
            'www.rejinapyo.com':'rejinapyo',
            'www.off---white.com':'offwhite',
            'www.31philliplim.com':'philliplim',
            'shop.swatch.cn':'swatch',
            'us.christianlouboutin.com':'christianlouboutin',
            'vans.com.cn':'vans',
            'www.adidas.com.cn':'adidas',
            'rejinapyo.com':'rejinapyo',
            'www.nike.com':'nike',
            'www.msgm.it':'msgm',
            'www.converse.com.cn':'converse',
            'www.clubclio-cn.com':'clubclio',
            'www.mtmskincare.com':'mtm',
            'www.pola.com.cn':'pola',
            'www.alexandre-zouari-accessories.com':'alexandrezouari',
            'www.arte-madrid.com':'arte',
            'www.follifollie.com.cn':'follifollie',
            'store.bottegaveneta.cn':'bv',
            'store.alexandermcqueen.cn':'alexandermcqueen',
            'www.christopherkane.com':'christopherkane',
            'www.marni.com':'marni',
            'www.volcom.com':'volcom',
            'www.paulsmith.com':'paulsmith',
            'www.breitling.cn':'breitling',
            'annasui.com':'annasui',
            'www.garnier.co.uk':'garnier',
            'www.donnakaran.com':'donnakaran',
            'chcarolinaherrera.com':'chcarolinaherrera',
            'store.lanvin.cn':'lanvin',
            'www.clinique.com.cn':'clinique',
            'www.christofle.com':'christofle',
            'www.buccellati.com.cn':'buccellati',
            'www.balmain.com':'balmain',
            'www.victoriabeckhambeauty.com':'victoriabeckhambeauty',
            'www.longchamp.cn':'longchamp',
            'www.lamer.com.cn':'lamer',
            'www.tissotwatches.cn':'tissot',
            'www.katespade.cn':'katespade',
            'www.fentybeauty.com':'fentybeauty',
            'www.berluti.com':'berluti',
            'www.emiliopucci.com':'emiliopucci',
            'cn.loropiana.com':'loropiana',
            'www.nicholaskirkwood.com':'nicholaskirkwood',
            'international.victoriabeckham.com':'victoriabeckham',
            'www.ugg.cn':'ugg',
            'www.rado.cn':'rado',
            'www.canadagoose.com':'canadagoose',
            'www.thombrowne.cn':'thombrowne',
            'www.asprey.com':'asprey',
            'www.oscardelarenta.com':'oscardelarenta',
            'www.supremenewyork.com':'supreme',
            'www.briston-watches.com':'bristonwatches',
            'www.agentprovocateur.com':'agentprovocateur',
            'www.saint-james.com':'saintjames',
            'www.missoni.com':'missoni',
            'shop.brunellocucinelli.cn':'brunellocucinelli',
            'www.tomford.com':'tomford',
            'www.oyang.co.uk':'oyang',
            'www.claudiepierlot.cn':'claudiepierlot',
            'www.ports-intl.com':'ports',
            'www.dickies.com.cn':'dickies',
            'www.newbalance.com.cn':'newbalance',
            'www.rimowa.com':'rimowa',
            'www.etude.cn':'etude',
            'www.shuuemura.com.cn':'shuuemura',
            'www.loccitane.cn':'loccitane',
            'www.shiseido.com.cn':'shiseido',
            'www.lesjeunesetoiles.com':'lesjeunesetoiles',
            'www.fred.cn':'fred',
            'www.thomaspink.com':'thomaspink',
            'www.baccarat.cn':'baccarat',
            'www.garrard.com':'garrard',
            'www.acquadiparma.cn':'acquadiparma',
            'www.victoriassecret.cn':'victoriassecret',
            'www.sergiorossi.com':'sergiorossi',
            'www.benefitcosmetics.com':'benefitcosmetics',
            'www.katvondbeauty.com':'katvondbeauty',
            'www.franciskurkdjian.com':'franciskurkdjian',
            'www.amiparis.com':'ami',
            'www.makeupforever.cn':'makeupforever',
            'www.tagheuer.com':'tagheuer',
            'www.baume-et-mercier.cn':'baumeetmercier',
            'www.zenith-watches.com':'zenith',
           }
