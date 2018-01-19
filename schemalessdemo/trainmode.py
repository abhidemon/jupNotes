
from time import sleep as g
import requests
import json
import time


def prt(*args):
    from time import sleep as g
    import json
    g(0.5)
    msg = ""
    for p in args:
        if type(p) == type(""):
            msg += " " + p
        else:
            msg += " " + json.dumps(p)
    print msg


def ln():
    prt("==================================================================================")


def getStRepr(entry):
    if entry['multivalued']:
        multiValued = "multiValued"
    else:
        multiValued = "singleValued"
    return  "(" + str(entry['type']) + "," + multiValued + ")"

def analyseSchema(prevSchema, curSchema):
    added = []
    changed = []
    for entry in curSchema:
        isnew = True
        for pentry in prevSchema:
            if pentry['name'] == entry['name']:
                isnew = False
                if pentry['type'] != entry['type']:
                    changed.append(str(entry['name']) + " : " + getStRepr(pentry) + " -> " + getStRepr(entry))
        if isnew:
            added.append( str(entry['name']) + " : " +"\t" + getStRepr(entry) )

    addedStr = ""
    for addded1 in added:
        addedStr+="\n\t"+addded1
    if (addedStr==""):
        addedStr="None"

    changedStr = ""
    for ch in changed:
        changedStr+="\n\t"+ch
    if (changedStr==""):
        changedStr="None"
    return (addedStr, changedStr)


# In[ ]:




# In[13]:


collName = "myOnlineStore" + str(int(time.time()))
confName = "schemaless"
prt(">Creating collection..")
CREATE_CORE_API = 'http://localhost:8983/solr/admin/collections?_=1493961385150&action=CREATE&collection.configName={}&maxShardsPerNode=1&name={}&numShards=1&replicationFactor=1&router.name=compositeId&routerName=compositeId&wt=json'.format(
    confName, collName)
START_API = "http://localhost:8983/solr/{}/schema/train/start"

resp = requests.get(CREATE_CORE_API.format(collName))
prt(json.dumps(json.loads(resp.content)))
prt("\n>Collection Created : {}\n".format(collName))
prt(">Creating A Training Session...")
START_API = START_API.format(collName)
prt("\n\tcurl ", "'" + START_API + "'")
resp = requests.get(START_API)

respc = resp.content
schema_training_id = json.loads(respc)['schemaTrainingId']

print "\n>We have initiated a training Session : " + schema_training_id + "\n"

# In[3]:




# In[14]:


import requests, json, time

prt(">Now, training SOLR with our products....")
trainURL = "http://localhost:8983/solr/{}/schema/train".format(collName)
yieldUrl = "http://localhost:8983/solr/{}/schema/train/yield".format(collName)
dataFile = [
    {"title": "How to Train Your Schema", "price": 23, "cur": "USD", "qty": 1000, "sku": "2017-01-18", "isAvailable":"true"},
    {"title": "Be Sane, Like Always", "price": 456.4, "cur": "EUR", "qty": 1000, "sku": "b-1122323", "rank":"2011"},
    {"name" : "Alex Marbles", "favourites": ["bottles", 9999, "warts"], "rank":[201, 2999.334]},
    {"name" : "Arjan Kant", "favourites": ["ppp", "qwerty", "warts"], "rank": [201, 2999.334], "isAvailable":"false"}
]

cnt = 1
prt(">Fetching Trained Schema:\n\t curl -X POST -d \t", trainURL + "?schemaTrainingId=" + schema_training_id)
resp = requests.get(yieldUrl, params={"schemaTrainingId": schema_training_id, "indent": "false"})
respc = json.loads(resp.content)
prevSchema = respc['schema']['add-field-type']
prt(">Response: ", json.dumps(respc, indent=4))
raw_input()

def aassd(data, prevSchema):
    # prt(cnt, ". \tEntry : ", data)
    ln()
    prt(">Sending Entry:\n\t curl -X POST -d '", data, "'\t", trainURL + "?schemaTrainingId=" + schema_training_id)
    resp = requests.post(trainURL, params={"schemaTrainingId": schema_training_id, "indent": "false"},
                         data=json.dumps([data]))
    prt("\tResponse: ", json.loads(resp.content), "\n")
    # raw_input()
    prt(">Fetching Trained Schema:\n\t curl -X POST -d \t", trainURL + "?schemaTrainingId=" + schema_training_id)
    resp = requests.get(yieldUrl, params={"schemaTrainingId": schema_training_id, "indent": "false"})

    respc = json.loads(resp.content)
    prt("Response: ", json.dumps(respc, indent=4))
    curSchema = respc['schema']['add-field-type']

    (added, changed) = analyseSchema(prevSchema, curSchema)
    prt("Fields Added: ", added)
    prt("Fields Changed: ", changed)

    prevSchema = curSchema

    # cnt += 1
    ln()
    raw_input()
    return prevSchema


for data in dataFile:
    prevSchema = aassd(data, prevSchema)

prevSchema = aassd({"asdfg": "assdf", "assa": 222.333}, prevSchema)

# In[5]:





# In[11]:


prevSchema = aassd(
    {"singlevaluedfield2": "assdfr", "mvf": ["a", "as"], "mullong": [1234, 234, 345.45], "assa": [111122.333, 222.333]},
    prevSchema)

