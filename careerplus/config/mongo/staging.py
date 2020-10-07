#python imports

#django imports

#local imports

#inter app imports

#third party imports

LEARNING_MONGO_PORT = '27017'
LEARNING_MONGO_USERNAME = 'mongoadmin'
LEARNING_MONGO_PASSWORD = 'mongoadmin'
LEARNING_MONGO_IP = '172.22.67.40'
LEARNING_MONGO_INSTANCE_ADDRESS = LEARNING_MONGO_IP + ":" + LEARNING_MONGO_PORT

MONGO_SETTINGS = {
    'default' : {
        'DB_NAME'  : 'learning',
        'USERNAME': LEARNING_MONGO_USERNAME,
        'PASSWORD': LEARNING_MONGO_PASSWORD,
        'HOST': LEARNING_MONGO_INSTANCE_ADDRESS,
        'MAX_POOL_SIZE' : 50,
    }
}