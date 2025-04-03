from Flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import tkinter as tk 

app = Flask(__name__)

UserEnteredInfo = []
