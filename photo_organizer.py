#!/usr/bin/env python
from os import rename
from os import mkdir
from os import listdir
from os import path
from os import chmod
from os import rmdir
from os import rename
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

def get_name(arquivo, date):
  name = date[8:-9]+"-"+date[5:-12]+"-"+date[:-15]+" "+date[11:-6]+"-"+date[14:-3]
  return name

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

def main():

  print("\n=====|=====| CONFIG |=====|=====")

  print("Deseja retirar todas os aquivos de dentro das pastas? \n"
        " S: Sim / N: Não ")
  retirar = input("> ")

  print("Deseja renomear as fotos para : DD-MM-YYYY HH-MM ? \n"
        " S: Sim / N: Não ")
  renomear = input("> ")

  print("Deseja organizar as fotos por pastas ? \n"
        " S: Sim / N: Não ")
  organizar = input("> ")

  print("\n\n")
  
  while True:
    if retirar == 'S':
      move_files()

    if renomear == 'N' and organizar == 'N':
      break

    if path.isdir("SemInformacao"):
      print('Ja existe a pasta SemInformacao')
    else:
      mkdir("SemInformacao")

    for arquivo in tqdm(arquivos):
        if arquivo.endswith(".jpg") or arquivo.endswith(".jpeg") or arquivo.endswith(".JPG") or arquivo.endswith(".JPEG")  :
          exif = get_exif("%s"%arquivo)
          if exif and exif != 'None':
            labeled = get_labeled_exif(exif)
            if ('DateTimeOriginal' not in labeled):
              shutil.move("%s"%arquivo, path.basename("SemInformacao")) 
              continue
            month_year = get_month_year(labeled['DateTimeOriginal'] if labeled['DateTimeOriginal'] else labeled['DateTime'] )
            if path.isdir(month_year) != True and organizar == 'S':
              mkdir(month_year)
            if renomear == 'S':
              file_extension = path.splitext(arquivo)[1]
              newName = get_name(arquivo, labeled['DateTimeOriginal'])
              if path.exists(path.basename("%s"%month_year)+'/'+ newName + file_extension) and organizar == 'S':
                i = 1
                while path.exists(path.basename("%s"%month_year)+'/'+ newName + file_extension):
                  newName += str(i)
                  i += 1
            if organizar == 'S' and renomear == 'S':
              shutil.move("%s"%arquivo, path.basename("%s"%month_year))
              rename(path.join(path.basename("%s"%month_year), arquivo), path.join(path.basename("%s"%month_year), newName+file_extension))
            elif organizar == 'N' and renomear == 'S':
              rename(path.join('.', arquivo), newName+file_extension)
            elif organizar == 'S' and renomear == 'N':
              shutil.move("%s"%arquivo, path.basename("%s"%month_year))
          else:
            shutil.move("%s"%arquivo , path.basename("SemInformacao")) 
    break

if __name__ == "__main__":
    main()