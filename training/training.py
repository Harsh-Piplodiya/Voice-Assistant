import json
import random
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation
from keras.optimizers import SGD

lemmit = WordNetLemmatizer()
intents=json.loads(open('path of the JSON file /intents.json').read())

words=[]
classes=[]
documents = []
ignore_letters = ['?','!',',','.']

for intent in intents['intents']:
    for patterns in intent['patterns']:
        word_list = nltk.word_tokenize(patterns)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


words= [lemmit.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))

# #----------------------------------------------------------------------------------------------------------------
training =[]
output_empty=[0]*len(classes)
for document in documents:
    bag=[]
    word_patterns = document[0]
    word_patterns= [lemmit.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    # output_empty= [0]*len(bag)
    output_row= list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append(bag + output_row)
# print((bag, output_row))
# print(bag)
# print(output_row)
  
# training =[]

# for document in documents:
#     bag=[]
#     word_patterns = document[0]
#     word_patterns= [lemmit.lemmatize(word.lower()) for word in word_patterns]
#     for word in words:
#         bag.append(1) if word in word_patterns else bag.append(0)
#     output_empty= [0]*len(bag)
#     output_row= list(output_empty)
#     output_row[classes.index(document[1])] = 1
#     training.append([bag, output_row])
    
# #-------------------------------Training Our Nural Network----------------------------
    
print('training\n',(training))
random.shuffle(training)
training = np.array(training)

train_x = training[:,:len(words)]
train_y = training[:,len(words):]

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd= SGD(lr=0.01, weight_decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist=model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5,verbose=1)
model.save('chatbotmodel.h5',hist)
print('Done')