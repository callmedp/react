from .settings import *

DEBUG = False
IS_LIVE = True
STATIC_URL = 'https://origin-static3.shine.com/static/'
MEDIA_URL = 'https://origin-static3.shine.com/'
DOWNLOAD_URL = 'https://origin-static3.shine.com/download/'
DOWNLOAD_ROOT = os.path.join(MEDIA_ROOT, 'download')
RESUME_DIR = '/shineresume/ResumeServices/'
CELERY_ALWAYS_EAGER = False

########## DOMAIN SETTINGS ######################
SITE_DOMAIN = 'learning.shine.com'
MOBILE_SITE_DOMAIN = 'mlearning.shine.com'
SITEMAP_CACHING_TIME = 86400
SITE_PROTOCOL = 'https'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN) #'http://learning.shine.com'
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'tarun@123'
SHINE_API_TIMEOUT = 60
SHINE_SITE = 'https://www.shine.com'
SHINE_API_URL = 'https://mapi.shine.com/api/v2'
CLIENT_ACCESS_KEY = 'ZiHCJeTKh4EppsrOEHXIQPd2OKvV4JWrlKql0Y1JONE'
CLIENT_ACCESS_SECRET = 'QdEhIXFmhlHQdveZB1h9u9xxnfvFleET6bNUPlKYwU4'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.36:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
    'index': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.35:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    }
}

####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC48XECC'
CCAVENUE_WORKING_KEY = 'BB84397177B2D640744BA272627C2A61'

##### CCAVENUE MOBILE SETTINGS ###########
CCAVENUE_MOBILE_ACCESS_CODE = 'AVYX74EK04AB49XYBA'
CCAVENUE_MOBILE_WORKING_KEY = 'A5BD19BE780D68E36598D8FB051CF66C'

CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'careerplus',
        'USER': 'carrerplus',
        'PASSWORD': 'permitted@321',
        'HOST': '172.22.65.153',
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://172.22.65.131:6379/1",
            ],
        "TIMEOUT": 86400,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    },
    'session': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://172.22.65.131:6379/2",
            "redis://172.22.65.141:6379/2",
            ],
        "TIMEOUT": 86400,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    },
    'search_lookup': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.22.65.131:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    },
}

ADMINS = [
    '123snig@gmail.com',
    'snig_b@yahoo.com'
    'snigdha.batra@hindustantimes.com'
]

ROUNDONE_PRODUCT_ID = 2129


#### LEAD CRONS
SHINECPCRM_DICT = {
    'base_url': 'http://shinecpcrm.shine.com',
    'token': '73f53cf358b94156feb49d034081ed507334e02a',
    'create_lead_url': '/api/v1/create-lead/',
    'timeout': 8,
    'update_products_url': '/product/update_sale_product/',
    'update_cartleads_url': '/api/update-cartleads/',
    'ad_server_url': '/api/mobile-version-leads/'
}

### LINKEDIN SETTINGS
REDIRECT_URI = '{}/linkedin/login'.format(MAIN_DOMAIN_PREFIX)

# Booster Recruiters
BOOSTER_RECRUITERS = [
'voyaze@gmail.com',
'hr@adducos.com',
'yashaswi@vsnl.net',
'wish4jobs@vsnl.net',
'wingsbs@gmail.com',
'widexpune@widexindia.com',
'west@2coms.com',
'vvp_2003@indiatimes.com',
'vthehunters@gmail.com',
'vsubu@meru.co.in',
'vsriram@elorasoft.com',
'vrconsultancyservices@gmail.com',
'vr1india@rediffmail.com',
'vprosyshr@gmail.com',
'voyaze1234@gmail.com',
'vm@careeroneindia.com',
'vivek@placefirst.com',
'vishwas@vbinfotech.com',
'vishnu@lider.in',
'virgo.valar@gmail.com',
'vipulbaranwal@gmail.com',
'vinod@innovativeevents.co.in',
'vinod@globali.in',
'vinod.kumar@impigertech.com',
'vineet@search-international.net',
'vinay.chittora@gmail.com',
'vimala@elakshya.in',
'vilash@staffingstudio.com',
'vikram@infeonglobal.com',
'vikash@zeesoft.com',
'vikas.margdarshan@gmail.com',
'vijay_business@yahoo.com',
'vijay@hrworksindia.com',
'vijay.sow@gmail.com',
'vibgyorvisuals@yahoo.co.in',
'VGPInternationalService@Yahoo.com',
'venkosa@yahoo.co.in',
'venkatprimezone@rediffmail.com',
'venkatesh@kripya.com',
'venkat@pavanconsultancy.com',
'venkat@brainsnskills.com',
'vazeplace@youtele.com',
'varma@infogenex.net',
'vaithy@persuaders.in',
'vaishali@manavconsultants.com',
'uthaay@yahoo.co.in',
'urmila@fusionconsultants.net',
'universalmanagement@airtelmail.in',
'unitech@unitechconsultants.com',
'uconsult@satyam.net.in',
'turningpoint.mail@gmail.com',
'triumph_consultant@rediffmail.com',
'training@plexus.co.in',
'total.tba@gmail.com',
'top_career@rediffmail.com',
'todayvision@rediffmail.com',
'thomas@indranetworks.com',
'thomas@exzeal.com',
'thirumal.ramakrishnan@relianceada.com',
'thiru@ascenderstech.com',
'thalha.ms@gmail.com',
'techskillshr@gmail.com',
'teamhr@consultoneindia.com',
'tara@mindselectconsultants.com',
'sylves@6csos.com',
'swami@hunterdouglas.in',
'surya.narayanan@enterpriseits.com',
'surindam.redwood@gmail.com',
'suresh@nonifamily.net',
'support@straighthire.co.in',
'support@iqs-ndt.org',
'support@horizonhrsolution.com',
'support@brainmagic.info',
'sunilmsathe@rediffmail.com',
'sunilKumar.bv@vibrantinfosystems.com',
'sunil.k.in@gmail.com',
'Sundarrao@convergentinc.com',
'sumir@careersindia.com',
'sumana@indiegenie.com',
'sukumaran@comfyisolution.com',
'sudhakar@stepstoneindia.net',
'subramaniyan@primeabccs.com',
'stride_india@vsnl.net',
'standon@tannet.com',
'ssservices@asia.com',
'sscsjobs@gmail.com',
'ssathya@sancotrans.com',
'srivatsan@inventg.com',
'srivathsan@t2orbit.com',
'sriram@grcconsultants.net',
'sriganesh@catchconsulting.com',
'sreevatsava@avyayh.com',
'sreenidhi@sify.com',
'spectral.rec@gmail.com',
'south@emtindia.com',
'soumyadeep@binarytree.co.in',
'smasunil@vsnl.com',
'smartmoveplacements@gmail.com',
'smartconsultancys@yahoo.com',
'smartcall_pune@rediff.com',
'sm@laporte.co.in',
'skyyreach@gmail.com',
'sivaprasad2350@gmail.com',
'simha@pegasusstaffing.com',
'silverliningjobs@rediffmail.com',
'silskies@hotmail.com',
'signaturehr@gmail.com',
'siebel.prem@gmail.com',
'sidharth.gupta@shine.com',
'shweta.j@peoplesource.in',
'shreedhar@natupathak.com',
'shivangi.bhatla@manpower.co.in',
'shiva@poorvika.com',
'sheriff@rps-india.com',
'shekar@3ssolutions-tech.com',
'shayne@deeva.com',
'sharath@dewdrop.co.in',
'shan@qualitree.net',
'shalomhrsolution@yahoo.co.in',
'shalini@naukriguru.in',
'shafee@jobspoint.com',
'senthil@accesstech.in',
'sensetechnology@gmail.com',
'senscohrd@yahoo.com',
'SELVA@EL-LINK.COM',
'seaspmsadvertising@gmail.co',
'seasonsadvertising@gmail.com',
'searchcon@rediffmail.com',
'sbconsultants2007@gmail.com',
'SaYICons@Rediffmail.com',
'saxena_a07@yahoo.com',
'sathish@summitworks.com',
'satheesh@amsoftsolutions.com',
'sarth@vsnl.net',
'saravanan@vtmanpower.net',
'saravanan.ramasamy@hasutechnologies.com',
'sarang@webteklabs.com',
'sanjeevkl@rediffmail.com',
'sanjay@impetusplacements.com',
'sandeep@vision.in',
'sandeep.dasharatha@gmail.com',
'samrat_technoindustries@yahoo.com',
'sales@utilityforms.com',
'sales.India@wabrasives.com',
'sakshigurha@gmail.com',
'saiplacement@gmail.com',
'saikat.c@accentus-india.com',
'sageer.k@gmail.com',
'safetechindustries@gmail.com',
's.madhusudhanan@twsol.com',
's.lata@acubessolutions.com',
'r_n_diwakar@yahoo.com',
'rushivj@rediffmail.com',
'rupag@optionsconsultancy.com',
'ruchi@synergysurge.com',
'rtpune@rteservices.com',
'rrao@agora.in',
'royce@eljayhr.com',
'rosni2@rediffmail.com',
'rohini@nncpl.org',
'rohin@goldenopportunities.biz',
'rkindian@hotmail.com',
'rke@vsnl.net',
'ritu@pdvpl.com',
'RGRaj511@DataOne.in',
'resume_brightfuture@yahoo.co.in',
'resumes@manhuntconsultants.com',
'resumeforcareer@gmail.com',
'resume@techstosuit.com',
'resume@ple.co.in',
'resume@jobdrome.com',
'resume@hindco.com',
'resourcespune@rediffmail.com',
'reliable_links@rediffmail.com',
'reji@maagnus.com',
'reachus@vsnl.net',
'reachhyd@vsnl.net',
'reachglobalplacementservices@gmail.com',
'reach@reach.co.in',
'ravi_k25@rediffmail.com',
'raviraj_india11@yahoo.co.in',
'ravi@packngo.in',
'ravi@gatesandwindows.in',
'rasitravels@hotmail.com',
'rashmeet_kaur@yahoo.co.in',
'rao@empowerconsultancy.com',
'rameshrahul@yahoo.com',
'ramesh@orbitglobalsolutions.com',
'ramdas@jobkompass.net',
'ram@rkmc.net',
'ram@launchpad.in',
'rakeshmoni@yorscorp.com',
'rakeshb54@yahoo.com',
'rakesh88@hotmail.com',
'rajesh@peoplefy.com',
'rajesh@infoworldpune.com',
'rajesh@aparajitha.com',
'rajesh.upadhyay66@gmail.com',
'rajeevkjha@ymail.com',
'rajeev@jobachievers.com',
'rajat.lahiri@aiplindia.com',
'raj@powersourcejobs.com',
'raj@enoah.in',
'rahulpune@gmail.com',
'radhika@krysalisco.com',
'ra.placements@gmail.com',
'r@achconsultants.com',
'questconsultants@moomia.com',
'pyramid.jobs@gmail.com',
'pvijayaraghavan@amnet-systems.com',
'PVijay@Everestconsulting.net',
'pushpanathan@stlfasteners.com',
'punecc@wwicsgroup.com',
'pune@omamconsultants.com',
'pune@factjobs.com',
'pune@ccrjobs.com',
'puja@signjobs.com',
'pssblr@pssindia.com',
'promptpoint@yahoo.co.in',
'profile@sriramanujaajobs.com',
'prithu@optionsindia.net',
'prismpeople@yahoo.com',
'prem@krishtechnologies.com',
'prathap@bpozitions.com',
'prakash@shriram.com',
'prahalathan@progressions.in',
'pragmacs@vsnl.com',
'pragatijobs@vsnl.net',
'pradeep@mpgroup.in',
'pradeep@greenpepper.in',
'plan100@vsnl.com',
'placement@mbgpaam.com',
'pkj_68@yahoo.com',
'piyushsharmaback@gmail.com',
'pismanpower@rediffmail.com',
'pioneertrvl@eth.net',
'phoenixgh2002@yahoo.co.in',
'peter.k@agnieconsulting.com',
'perfectplacerc@vnl.net',
'perfectplacepune@yahoo.co.in',
'pepc@vsnl.com',
'People4U@Gmail.com',
'payal@ndts.co.in',
'patsheetal@rediffmail.com',
'patnaik@cherrytec.com',
'Parimal@HRKonnect.com',
'paragshinde@gmail.com',
'panju@crozzroadz.com',
'p.vidya@stantonchase.com',
'p.balasubramaniam@marsh.com',
'nsps@eth.net',
'npalande@gmail.com',
'nithyanandam@coremindtechnologies.com',
'nithya@lucidindia.com',
'nirali.herbalife@gmail.com',
'nilesh.doke@yahoo.co.in',
'nikhil@hexagonsearch.com',
'nidhi@headrecruitment.com',
'newdelhi@kellyservices.co.in',
'neha@mindspacehr.com',
'neha.pcil@gmail.com',
'neethu.ivan@marketbuilders.co.in',
'neelesh@altavisionindia.com',
'navneet@launchers.org.',
'navin@ntechmanagement.com',
'nationalplacement@gmail.com',
'nasser101@hotmail.com',
'nareshsaini@smilejobs.net',
'nandu@advancedfea.net',
'nairm@pn3.vsnl.net.in',
'muthukumar@datamaticsindia.com',
'muthu@speedfam.co.in',
'muralisvasan@yahoo.com',
'murali@amra.in',
'mumbai@geniusjobs.com',
'multiservices.ms@gmail.com',
'msplacement@yahoo.co.in',
'msajobsonline.com',
'msa.jobs@gmail.com',
'mrps.jobs@vsnl.net',
'mrdelhi@geniusjobs.com',
'moni@tti.co.in',
'mohan@annshr.com',
'mnstaffingsolution@gmail.com',
'ml@enkonindia.com',
'mistasa@gmail.com',
'mikk1@rediffmail.com ',
'mhrsolutions@gmail.com',
'mgs@t2orbit.com',
'mfmgmt@vsnl.net',
'megarecruitment@yahoo.co.in',
'med@jobsup.com',
'mdstouch@gmail.com',
'mc@mechci.com',
'maxguardpestcon@yahoo.co.in',
'mavin.in@gmail.com',
'mattootrading@hotmail.com',
'matrixplacements@gmail.com',
'matrixconsultant@gmail.com',
'MasDishnetDSLnet',
'marketing@chemseals.com',
'manum@sambhavindia.com',
'manojrc@satyam.net.in',
'manohar@aquadesigns.in',
'manjulaj@executiveplacements.com',
'manishguptanv@gmail.com',
'manisha@consultmagnum.com',
'mani@phrcs.com',
'manasi@oikos.in',
'manas.rekha1@gmail.com',
'manager@handsonsuccessindia.com',
'mamtamisthi@yahoo.com',
'malti_placement@yahoo.com',
'mail@manpower.co.in',
'mail@lexicontechnologies.com',
'mail@frontiercorporateservices.com',
'mail@acme-manpower.com',
'magesh@armaven.com',
'magesh@24x7.com',
'mafoihyd@mafoi.com',
'mafoical@mafoi.com',
'mafoiban@mafoi.com',
'madheshwari@gmail.com',
'maan1938@yahoo.com',
'lokesh.anand@aslhr.com',
'lmcmc@vsnl.net',
'lekshmi.c@telesisglobal.com',
'lekhamanagement@yahoo.co.in',
'leedshr@yahoo.com',
'leadcon@satyam.net.in',
'lakshmi@goldentrianglehr.co.in',
'lakshman.pillai@lpcube.com',
'lak.krk5@yahoo.co.in',
'laabahr@yahoo.co.in',
'kumar@tetratech.in',
'kumar@ramsol.in',
'kt@avtarcc.com',
'ksb.cik@gmail.com',
'krs@krest.in',
'kriya.raman@gmail.com',
'krahul.shree@gmail.com',
'kpr@neccyber.com',
'kotagiripramod@gmail.com',
'kolkata@geniusjobs.com',
'kolherajiv@yahoo.com',
'kjsbakshi@call10.com',
'kishore@alpconsultants.com',
'KGOV@Rediffmail.com',
'kevalmehta@rediffmail.com',
'kennedynesamoney@yahoo.com',
'ken@2coms.com',
'kedarb@vsnl.com',
'kavitha@3iinovation.com',
'kavita.kavanal@bsigroup.com',
'karun_kathuria@yahoo.com',
'karan@fingerprintcreative.com',
'kailash@morpheusconsulting.co.in',
'Jyoti.malhotra@naukri.com',
'jvi@bom3.vsnl.net.in',
'jsampath@jbsoftsystem.com',
'jrv@vsnl.com',
'jp@jiffysolutions.com',
'joseph@vertexenterprises.co.in',
'john@lionelindia.com',
'jobsolution62@yahoo.in',
'jobsindia01@gmail.com',
'jobsdesire67@yahoo.com',
'jobs@tusthi.com',
'jobs@trans.co.in',
'jobs@smartsolworld.com',
'jobs@smarthrsolutions.com',
'jobs@shreeit.com',
'jobs@sampoorna.com',
'jobs@propeopleconsulting.com',
'jobs@profileconsultantsindia.com',
'jobs@pravritti.com',
'jobs@lucentconsultants.com',
'jobs@genesismanpower.com',
'jobs@factjobs.com',
'jobs@careerpointplacement.com',
'jobs@careermatrixindia.com',
'jobkol@tpconsultants.com',
'jemi-hr@touchtelindia.net',
'jayavel@varehouse.com',
'jayashreeb@vibrantinfosystems.com',
'jayaam@gmail.com',
'jaspreet.oberoi@hindustantimes.com',
'jana@mileztone.com',
'jameelkhan85@gmail.com',
'iupune@yahoo.com',
'it@affirmservices.com',
'iseonline@vsnl.net',
'ipp@indiapharmapeople.com',
'ipgroup123@indiatimes.com',
'intrmgmt@vsnl.com',
'inquiry@firesolutionsindia.com',
'informex2004@yahoo.com',
'info@visacare.in',
'info@unitedprotech.com',
'info@technisearch.co.in',
'info@surajconsultants.com',
'info@rkresourcing.com',
'info@r2rconsults.com',
'info@quickjobplacement.in',
'info@placefirst.com',
'info@pantechsolutions.net',
'info@onlysuccess.net',
'info@mindsourceconsulting.com',
'info@microbasetech.com',
'info@manage-o-soft.com',
'info@kcsindia.net',
'info@isoconsultants.in',
'info@instantnaukri.com',
'info@infosoftech.com',
'info@iconium-consulting.com',
'info@hipro.co.in',
'info@goripe.com',
'info@everestconsulting.net',
'info@dhonadhi.in',
'info@dbvazhikaatti.org',
'info@cybertechnologies.in',
'info@coremindtechnologies.com',
'info@corecompt.com',
'info@careerfinance.com',
'info@career1000.com',
'info@bascosys.com',
'info@akankshaindia.com',
'info@adonisstaff.in',
'info@3edge.in',
'indiabusinessleague@gmail.com',
'india@contactrec-india.com',
'imports_chennai@lineaitalia.in',
'ideasinc3@gmail.com',
'iap.chennai@gmail.com',
'hyderabad@hr-one.in',
'hyderabad@geniusjobs.com',
'hr_chn@innovservices.com',
'hr_arwa@yahoo.co.in',
'hrtrcs@gmail.com',
'hrpune@360degreesindia.com',
'hrms@hrmsindia.com',
'hrmg@placementmall.com',
'hrmarutiplacement@gmail.com',
'hrjpitara@gmail.com',
'hrd@mantecconsultants.com',
'hrd@jasperinternational.com',
'hrd@horizone.in',
'hrd@agriya.in',
'hrcons2002@yahoo.co.in',
'hrcg@hotmail.com',
'hrakansha@hotmail.com',
'hraccess@sify.com',
'hr@winningedgeconsultants.net',
'hr@ssdkolkata.info',
'hr@snjoshiconsultants.com',
'hr@servicesquare.com',
'hr@selec.com',
'hr@seagullconsultancy.com',
'hr@sbem.co.in',
'hr@ringforjobs.com',
'hr@provizor.net',
'hr@neptuneconsultants.com',
'hr@magtrice.com',
'hr@itfission.com',
'hr@igenesisconsultant.com',
'hr@i5tech.net',
'hr@hotelcentrepoint.co.in',
'hr@globalintegra.com',
'hr@futurecalls.com',
'hr@fusiongs.com',
'hr@dooncompany.com',
'hr@atharvajobs.com',
'hr@arunexcello.com',
'hr4nation@gmail.com',
'hr.smartstep@gmail.com',
'hr.jemi@gmail.com',
'hnsinghal@owmnahar.com',
'hkv@acessjobs.com',
'himanshupruthi@hotmail.com',
'hellovetri@yahoo.com',
'headmnc_ngp@sancharnet.in',
'headhunter@vsnl.com',
'harsha@greatcareers.in',
'harsh.pillai@ktaglobal.com',
'harjaat@gmail.com',
'hariharan@headhunterindia.com',
'hariee@geedeesinfo.com',
'gunjan.jobrecruit@gmail.com',
'greenhouse1972@yahoo.co.in',
'govindarajan.s@pay4pay.co.in',
'gouthamjain@88db.co.in',
'Gopal@AscentPS.com',
'godwill_2001@rediffmail.com',
'globalxs@bol.net.in',
'gj@ritejobs.com',
'girirajconsultancy@gmail.com',
'geetha@mnwjobs.com',
'geeta@mindsourceconsulting.com',
'gecparakh10@yahoo.co.in',
'ganesh@emergesolution.net',
'ganesan@jobspoint.com',
'futures@hrnext.in',
'futureprogresspalace@gmail.com',
'fjdirect@vsnl.net',
'finoz.u@alliedconsultancy.com',
'ethosindia@vsnl.net',
'esp@vsnl.com',
'ermrec@ermrecruits.com',
'enquiry@geniusconsultant.com',
'enquiry@fitjobs.com',
'enquiry@aldeainfotech.com',
'enablesys@gmail.com',
'elementsconsl@yahoo.com',
'elan@inodesys.com',
'eclat@airtelmail.in',
'durwink@gmail.com',
'dr_anjankdas@rediffmail.com',
'dreamvisas@yahoo.com',
'dranandindia@gmail.com',
'dowell@dowelltech.com',
'doverseas@vsnl.com',
'dkmanagement@sify.com',
'dishaplace@yahoo.com',
'dimakh@dimakhconsultants.com',
'dilipsshukla@yahoo.co.in',
'dest_ina_tions@yahoo.co.in',
'denzil@tentsoftware.com',
'delhi@omamconsultants.com',
'delhi@heidrick.com',
'delhi@geniusjobs.com',
'delhi@focusonit.com',
'delhi@abcconsultants.net',
'deepti@andconsultancy.in',
'deepak@aceconsultancy.net',
'deepa@mindselectconsultants.com',
'deepa.saiya@achconsultants.com',
'deepa.mahori@manpower.co.in',
'dawradm@vsnl.com',
'datta@zmgindia.com',
'darryljj@nextindia.net',
'dakshin2@vsnl.com',
'cvs@asia.com',
'cv@happyplacements.com',
'customerisking@gmail.com',
'crm@alpha2omega.in',
'Creative404@Yahoo.co.in',
'cosmicbcm1@yahoo.com',
'corporate@bonsaitechnologies.com',
'contactjohn40@yahoo.com',
'contact@vconnect-cs.com',
'contact@topplanetconsulting.com',
'contact@cruxcs.com',
'contact@clickitjobs.com',
'consultancygaloreinc@yahoo.co.in',
'consult@indosoftnet.com',
'chn@parc.in',
'chn@coherentglobal.com',
'cheruba@covenantindia.net',
'chennai@sinclus.com',
'chennai@isbm.org.in',
'chennai@hr-one.in',
'chennai@holostik.com',
'chennai@headwayconsultant.com',
'chennai@handimanservicesltd.com',
'chennai@geniusjobs.com',
'chennai@asmacs.net',
'chennai@armsindia.net',
'chennai@aimsintl.in',
'chennai@aarviencon.com',
'chennai.stardotstar@gmail.com',
'chella@systoleonline.com',
'checoord1@ambe.com',
'chandplacement@vsnl.net',
'chanchal@apvision.in',
'cguide@rediffmail.com',
'cffa91@hotmail.com',
'cbkk@pscl.net',
'catalysts@vsnl.com',
'CareIndia@Gmail.com',
'careervision@vsnl.com',
'careers_royassociates@yahoo.com',
'careerspune@bv.com',
'careers@texsasindia.com',
'careers@linkageindia.net',
'careers@koplindia.com',
'careers@careerdimensions.net',
'careerlink1@yahoo.com',
'careerline_pn@rediffmail.com',
'careerav@rediffmail.com',
'candor_services@rediffmail.com',
'campusuk.001@gmail.com',
'brsjobs@airtelmail.in',
'bril@vsnl.com',
'brightopportunities@gmail.com',
'brightcv8@gmail.com',
'bramhabps@rediffmail.com',
'bplaced@gmail.com',
'bombay@oxfordcpl.com',
'bnsharma@brainwarehrsolutions.com',
'bluebird_advertising@vsnl.com',
'blqs@ttml.co.in',
'blazonconsultants@gmail.com',
'bharat@perfectprofiles.net',
'benjamin@springboards.in',
'bellsprime@gmail.com',
'beeki@genius-digital.com',
'bareddy@astroved.com',
'balu.chidambaram@geinfoserve.com',
'balasubiramaniyan.vasudevan@manpower.co.in',
'balaji@lightningsolutions.co.in',
'bala.kannan@hasutechnologies.com',
'bader_sir@yahoo.co.in',
'avinash@iavindia.com',
'auric@vsnl.com',
'asst.hr@gmail.com',
'ashwin@firstfinishingschool.com',
'ascentmgt@eth.net',
'arun@swathisolutions.com',
'apply.eijobs@gmail.com',
'apex_naukri@rediffmail.com',
'apex@apexplacement.com',
'anuvajobs@gmail.com',
'ann.edem@yahoo.com',
'ankulbatra@yahoo.com',
'anju@promptpersonnel.com',
'anjali@rightstep.co.in',
'anitadorle@rediffmail.com',
'anil@jayemployment.com',
'andrews@zenhr.com',
'andheri@epsiloncons.com',
'anandaraj@vipulfacility.com',
'anand@careerkarthaa.com',
'anand.sinha@hindustantimes.com',
'anand.sinha444@gmail.com',
'amit@angeleyecentre.com',
'amishicallnet@gmail.com',
'amconmds@vsnl.com',
'amayarecruit@airtelbroadband.in',
'amardeep.avsarr@gmail.com',
'amar@dossier.co.in',
'amar@ablindian.com',
'alwarpet@maacmail.com',
'alpinemumbai@gmail.com',
'alphaplacements@vsnl.net',
'alphamncjobs@yahoo.in',
'allzone@allzonems.com',
'alisha.globaledge@gmail.com',
'alex@grasshoppersindia.com',
'akila@theforte.com',
'ajit_hps@yahoo.com',
'aim_placementservices@yahoo.co.in',
'ag@tespaindia.com',
'affhyd@eth.net',
'afferguson.com',
'advisor@indoreinstitute.com',
'advantagehr@vsnl.net',
'adroitinc@rediffmail.com',
'adphatarphod@yahoo.co.in',
'admin@emberatech.com',
'admin.fortunehr@gmail.com',
'adhyaconsultants@yahoo.com',
'Adeenesh123@Rediffmail.com',
'acs.santosh@gmail.com',
'acmeplacements@rediffmail.com',
'acehrsolutions@rediffmail.com',
'accounts@pmcindia.com',
'abhishek.singh@evolvexl.com',
'abhay_rr@hotmail.com',
'aakkam_06@dataone.in',
'3rdeyeitjobs@3rdeyeconsultants.com'
]

###### ROUNDONE SETTING ###############################

ROUNDONE_API_BASEURL = "http://api.roundone.in"  # This is the live api
ROUNDONE_API_BASEURL_ORDER = "http://www.roundone.in"
ROUNDONE_ORDER_SECRET_KEY = 'xHVEbrvpiH8BMol5rZt7YuDO'
ROUNDONE_JOBDETAIL_SECRET_KEY = 'cQMYGVYxrMqHGPSAZeRDm4G'
ROUNDONE_CP_CLIENT_ID = 'lnVPB3Oe9YPA3g)!F9zrFbg'
ROUNDONE_CP_CLIENT_SECRET = 'c&OMxZ^0T*6qvyi0e3lU9OjWc!(%Wp+'
ROUNDONE_ENCODING_KEY = '#r0und0n3k3y'
ROUNDONE_ENCODING_SALT = '#r0und0n354l7'
ROUNDONE_DEFAULT_PASSWORD = 'cp@roundone'
ROUNDONE_API_TIMEOUT = 60

ROUNDONE_API_DICT = {
    'amount': 1999,
    'organisationId': 11,
    'affiliateName': 'CP',
    'client_id': ROUNDONE_CP_CLIENT_ID,
    'client_secret': ROUNDONE_CP_CLIENT_SECRET,
    'order_secret_key': ROUNDONE_ORDER_SECRET_KEY,
    'jobdetail_secret_key': ROUNDONE_JOBDETAIL_SECRET_KEY,
    'location_url': ROUNDONE_API_BASEURL + "/applicant/location-list",
    'order_save_url': ROUNDONE_API_BASEURL_ORDER + "/api/careerplus/save",
    'job_search_url': ROUNDONE_API_BASEURL + "/applicant/search",
    'oauth_url': ROUNDONE_API_BASEURL + "/oauth-token",
    'job_detail_url': ROUNDONE_API_BASEURL + "/applicant/job-details",
    'is_premium_url': ROUNDONE_API_BASEURL + "/applicant/is-premium",
    'save_job_url': ROUNDONE_API_BASEURL + "/applicant/save-jobs",
    'get_profile_url': ROUNDONE_API_BASEURL + "/applicant/get-profile",
    'post_profile_url': ROUNDONE_API_BASEURL + "/applicant/post-profile",
    'submit_resume': ROUNDONE_API_BASEURL + "/applicant/submit-resume",
    'referral_request_url': ROUNDONE_API_BASEURL + "/applicant/referral-request",
    'referral_status_url': ROUNDONE_API_BASEURL + "/applicant/referral-status",
    'referral_confirm_url': ROUNDONE_API_BASEURL + "/applicant/confirm-interaction",
    'upcoming_interaction_url': ROUNDONE_API_BASEURL + "/applicant/upcoming-interactions",
    'past_interaction_url': ROUNDONE_API_BASEURL + "/applicant/past-interactions",
    'saved_history_url': ROUNDONE_API_BASEURL + "/applicant/get-saved-jobs",
    'delete_job_url': ROUNDONE_API_BASEURL + "/applicant/delete-saved-job",
    'feedback_submit_url': ROUNDONE_API_BASEURL + "/applicant/submit-feedback",
    'interaction_result_url': ROUNDONE_API_BASEURL + "/applicant/view-interaction-result",
    'update_credential_url': ROUNDONE_API_BASEURL + "/applicant/update-credentials"
}