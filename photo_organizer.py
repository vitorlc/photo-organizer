#!/usr/bin/env python
from os import rename
from os import mkdir
from os import listdir
from os import path
from os import chmod
from os import rmdir
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
import json
import stat
from tqdm import tqdm

arquivos = listdir('.')

print(" ___ _        _          ___                     _           \n"
     "| _ \ |_  ___| |_ ___   / _ \ _ _ __ _ __ _ _ _ (_)______ _ _ \n"
     "|  _/ ' \/ _ \  _/ _ \ | (_) | '_/ _` / _` | ' \| |_ / -_) '_|\n"
     "|_| |_||_\___/\__\___/  \___/|_| \__, \__,_|_||_|_/__\___|_|  \n"
     "                                 |___/                        \n")

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    image = Image.open(filename)
    image.load()
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

def rename(arquivo, date):
  print(aquivo)
  print(date) 

def move_files(): 
  dest = '.'
  arquivos = listdir('.')
  for fname in arquivos:
    pathName = path.join('.', fname)
    if path.isdir(pathName):
        files = listdir(pathName)
        for fname2 in files:
            shutil.move(pathName +"/"+ fname2, dest)
        rmdir(fname)

if path.isdir("SemInformacao") != True:
  mkdir("SemInformacao")

print("\n=====|=====| CONFIG |=====|=====")

print("Deseja retirar todas os aquivos de dentro das pastas? \n"
      " S: Sim / N: Não ")
retirar = input(">")

print("Deseja renomear as fotos e vídeos para : DD_MM_YYYY_QTD ? \n"
      " S: Sim / N: Não ")
renomear = input(">")

print("\n\n")

if retirar == 'S':
  move_files()

for arquivo in tqdm(arquivos):
    if arquivo.endswith(".jpg") or arquivo.endswith(".jpeg") or arquivo.endswith(".JPG") or arquivo.endswith(".JPEG")  :
      exif = get_exif("%s"%arquivo)
      if exif and exif != 'None':
        labeled = get_labeled_exif(exif)
        if ('DateTimeOriginal' not in labeled):
          shutil.move("%s"%arquivo, path.basename("SemInformacao"))
          continue
        month_year = get_month_year(labeled['DateTimeOriginal'] if labeled['DateTimeOriginal'] else labeled['DateTime'] )
        if path.isdir(month_year) != True:
          mkdir(month_year)
        # arquivo = rename(arquivo, labeled['DateTimeOriginal'])
        shutil.move("%s"%arquivo, path.basename("%s"%month_year))
      else:
        shutil.move("%s"%arquivo, path.basename("SemInformacao"))