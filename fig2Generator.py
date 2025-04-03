import json
import requests
import os
import csv
import numpy
import matplotlib.pyplot as plt
from collections import defaultdict
from fuzzywuzzy import process

def fig2Generator(MainTable):
    TitleOfChart = "#UserInput?"
    StartYear = ""
    EndYear = ""
    SelectedCountry ="" #Given as an ISO code preferably
    FieldOfStudy = " " #Can be all
    NumOfCollabs = ""
    NumOfAuthors = ""
    #Output
    ListOfConnectedCountrys = {"Iso Code":"Country"}
    NumOfPapers = ["Num"]

    #Matplotlib pie graph as output 