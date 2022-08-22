import os


mp3s = []
for file in os.listdir("../sounds"):
    if file.endswith(".mp3"):
        mp3s.append(file)


print (mp3s)