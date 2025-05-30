from flask import *
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename
from PIL import Image
from pytesseract import image_to_string
from PIL import Image
import pytesseract
from pytesseract import pytesseract
import random
from gtts import gTTS
import os
from langdetect import detect
UPLOAD_FOLDER = 'C:\ALL FILES\SATHWIKA\sathwika documents\Folder\Mini_project\static'
   
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('tts.html',data=[{'name':'text'}, {'name':'pdftext'},{'name':'imgtext'},{'name':'textdocument text'}])

@app.route("/text" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    if(str(select)=='text'):
        return render_template('text_option.html')
    elif(str(select)=='pdftext'):
        return render_template('pdffile.html')
    elif(str(select)=='imgtext'):
        return render_template('imagetext.html')
    elif(str(select)=='textdocument text'):
        return render_template('textdocument.html')

@app.route('/text_option',methods=['POST','GET'])
def login():
    if request.method =="POST":
        text_val=request.form['speech']
        language=detect(text_val)
        obj=gTTS(text=text_val,lang=language,slow=False,lang_check=True,tld='co.in')
        file=str('{:06}'.format(random.randrange(1, 10**3)))+'.mp3' 
        obj.save(file)
        obj.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
    return render_template('text_option.html',file_name=file)#return Response(playsound("welcome.mp3"), mimetype="mp3")

@app.route('/pdftext', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        pages=convert_from_path(f.filename,500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
        text=" "
        
        for i in range(len(pages)):
            pages[i].save('page'+ str(i) +'.jpg', 'JPEG')
            text+=(image_to_string(pages[i]) )
        text_val=text
        language=detect(text_val)
        obj=gTTS(text=text_val,lang=language,slow=False,tld='co.in')
        file=str('{:06}'.format(random.randrange(1, 10**3)))+'.mp3' 
        obj.save(file)
        obj.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
    return render_template('pdffile.html',file_name=file)
@app.route('/imgtext', methods = ['GET', 'POST'])
def upload_img():
   if request.method == 'POST':
         f = request.files['file']
         im=Image.open(f.filename)
         text=pytesseract.image_to_string(im)
         f.save(secure_filename(f.filename))
         text=(image_to_string(Image.open(f.filename)))
         language=detect(text)
         obj=gTTS(text=text,lang=language,slow=False,tld='co.in')
         file=str('{:06}'.format(random.randrange(1, 10**3)))+'.mp3' 
         obj.save(file)
         obj.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
   return render_template('imagetext.html',file_name=file)
@app.route('/textdoc', methods = ['GET', 'POST'])
def text_document():
   if request.method == 'POST':
         f = request.files['file']
         f.save(secure_filename(f.filename))
         myfile=open(f.filename,encoding="utf8") # open lorem.txt for reading text
         text = myfile.read()         # read the entire file to string
         myfile.close()                   # close the file
         language=detect(text)
         obj=gTTS(text=text,lang=language,slow=False,tld='co.in')
         file=str('{:06}'.format(random.randrange(1, 10**3)))+'.mp3' 
         obj.save(file)
         obj.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
   return render_template('textdocument.html',file_name=file)


@app.route('/reset',methods=['POST','GET'])
def reset():
     return render_template('tts.html',data=[{'name':'text'}, {'name':'pdftext'},{'name':'imgtext'},{'name':'textdocument text'}])


if __name__=='__main__':
    app.run(debug=True)