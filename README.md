#TRANSLATE SUBS

Simple tool to translate subtitles from the command prompt using google apis

#INSTALLATION

we recomend using virtualenv for this, once the virtualenv is activated just install the dependencies using pip

```console
foo@bar:~$ pip install requirements.txt
```

#USAGE

the tool has 3 work modes depending on the source type 

##MEDIA ID

In this mode it will translate a media.upv.es subtitle using google api

Example:
```console
foo@bar:~$ python translatesubs.py -t media -s a90ae7d0-5ccf-11e8-aab9-a1a4e108f2ab 
```

#SUBTITLE FILE

In this mode it will translate a ´.srt´ file 

```console
foo@bar:~$ python translatesubs.py -t file -s a90ae7d0-5ccf-11e8-aab9-a1a4e108f2ab_en.srt -langf en -langt es
```

#SUBTITLE FOLDER

In this mode it will translate every ´.srt´file in a folder and subfolders

```console
foo@bar:~$ python translatesubs.py -t folder -s test/ -langf en -langt es
```

#PARAMETERS
-h, --help            show this help message and exit
-v, --verbose         Verbose (activate this if you want to see what is being sent to google api to translate)
-t SOURCE_TYPE, --sourceType SOURCE_TYPE source type, pick between media|file|folder
-s SOURCE, --source SOURCE source of the subtitle/s 
-langf LANG_FROM, --langFrom LANG_FROM Language that we want to translate (optional default value =es)
-langt LANG_TO, --langTo LANG_TO Language of the output subtitle (optional default value =en)
-o OUTPUT, --output OUTPUT Output folder to store the result (optional default value = current folder)





