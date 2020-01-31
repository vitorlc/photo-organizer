#!/usr/bin/env python
from os import rename
from os import mkdir
from os import listdir
from os import path
from os import chmod
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
import json
import stat

arquivos = listdir('.')

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled

def get_month_year(date):
  month = int(date[5:-12])
  if month == 1:  monthString = "Janeiro"   
  elif month == 2:  monthString = "Fevereiro"   
  elif month == 3:  monthString = "Marco"
  elif month == 4:  monthString = "Abril"
  elif month == 5:  monthString = "Maio"
  elif month == 6:  monthString = "Junho"          
  elif month == 7:  monthString = "Julho"          
  elif month == 8:  monthString = "Agosto"          
  elif month == 9:  monthString = "Setembro"         
  elif month == 10: monthString = "Outubro"         
  elif month == 11: monthString = "Novembro"         
  elif month == 12: monthString = "Dezembro"
  year = int(date[:-15])
  monthYear = monthString + " - " + str(year)
  return monthYear

if path.isdir("SemInformacao"):
  print 'Ja existe a pasta SemInformacao'
else:
  mkdir("SemInformacao")


for arquivo in arquivos:
    if arquivo.endswith(".jpg") or arquivo.endswith(".jpeg"):
      print "\n"
      print "Arquivo: ", arquivo
      exif = get_exif("%s"%arquivo)
      if exif:
        labeled = get_labeled_exif(exif)
        if ('DateTimeOriginal' not in labeled):
          shutil.move("%s"%arquivo, path.basename("SemInformacao"))
          continue
        print labeled['DateTimeOriginal']
        month_year = get_month_year(labeled['DateTimeOriginal'] if labeled['DateTimeOriginal'] else labeled['DateTime'] )
        if path.isdir(month_year):
          print 'Ja existe uma pasta com esse nome!'
        else:
          mkdir(month_year)
          print 'Pasta criada com sucesso!'
        print path.basename("%s"%month_year)
        shutil.move("%s"%arquivo, path.basename("%s"%month_year))
      else:
        print("Desculpa, Imagem sem exif data.")
        shutil.move("%s"%arquivo, path.basename("SemInformacao"))