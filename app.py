from flask import Flask, render_template, send_file, jsonify, redirect, render_template, request, session, url_for,flash
import os
import json
import base64
import re
import string
import fitz  # PyMuPDF
import random  
import io
from mistralai import Mistral
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from collections import defaultdict
from datetime import datetime 
import mysql.connector  
from PIL import Image
import zipfile



app = Flask(__name__)
app.secret_key = "Qazwsx@123"  



link = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='questionpaper_2025'
)



# Mistral API
api_key = "WTuMOibXWmpTqjvscYHSaaCOjjXCakkJ"
model = "pixtral-large-2411"
client = Mistral(api_key=api_key)
















@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


def encode_image(image_filepath):
    with open(image_filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def pdf_to_images(pdf_filepath, output_folder):
    doc = fitz.open(pdf_filepath)
    output_images = []
    pdf_basename = os.path.splitext(os.path.basename(pdf_filepath))[0]

    zoom = 2
    mat = fitz.Matrix(zoom, zoom)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=mat)
        image_filename = f"{pdf_basename}_page_{page_num+1}.png"
        image_filepath = os.path.join(output_folder, image_filename)
        pix.save(image_filepath)
        output_images.append(image_filepath)

    return output_images


def parse_question_number(qnum):
    match = re.match(r"(\d+)([a-zA-Z])?", qnum)
    if match:
        main_num = int(match.group(1))
        sub_letter = match.group(2) if match.group(2) else ""
        return main_num, sub_letter.lower()
    return (9999, "")


def extract_questions_from_image(image_filepath, prompt):
    image_base64 = encode_image(image_filepath)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"}
            ],
            "response_format": {"type": "json_array"}
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )

    extracted_text = chat_response.choices[0].message.content
    try:
        data_start = extracted_text.find("[")
        data_end = extracted_text.rfind("]") + 1
        json_data_str = extracted_text[data_start:data_end]
        questions = json.loads(json_data_str)
        return questions
    except Exception as e:
        print("Error parsing JSON: ", e)
        return []


def renumber_questions(questions):
    grouped = defaultdict(list)
    for q in questions:
        num, _ = parse_question_number(q.get("question_number", ""))
        grouped[num].append(q)

    new_questions = []
    main_num = 1
    for group_key in sorted(grouped.keys()):
        sub_letter_index = 0
        for q in grouped[group_key]:
            new_qnum = f"{main_num}.{string.ascii_lowercase[sub_letter_index]}"
            q["question_number"] = new_qnum
            new_questions.append(q)
            sub_letter_index += 1
        main_num += 1

    return new_questions


def create_questions_pdf(questions_data, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    flowables = []

    # Randomly select 12 questions
    selected_questions = random.sample(questions_data, min(12, len(questions_data)))

    parts = ["A", "B", "C", "D"]
    question_index = 0

    for part_number in range(4):  # Part A to Part D
        part_title = f"<b>Part {parts[part_number]}</b>"
        flowables.append(Paragraph(part_title, styles["Heading2"]))
        flowables.append(Spacer(1, 12))

        for sub_index in range(3):  # 3 questions per part
            if question_index >= len(selected_questions):
                break
            q = selected_questions[question_index]
            q["question_number"] = f"{part_number + 1}.{string.ascii_lowercase[sub_index]}"
            marks = q.get("marks", "")
            try:
                marks = int(marks)
            except:
                marks = ""
            text = f"<b>{q['question_number']}</b>. {q.get('question_text', '')}"
            if marks:
                text += f" <i>({marks} marks)</i>"
            flowables.append(Paragraph(text, styles["Normal"]))
            flowables.append(Spacer(1, 12))
            question_index += 1

    doc.build(flowables)
    return output_pdf_path


@app.route("/download_pdf/<uid>")
def download_pdf(uid):
    final_pdf_path = os.path.join("workspace", uid, "final_question_bank.pdf")
    if os.path.exists(final_pdf_path):
        return send_file(final_pdf_path, as_attachment=True)
    return {"error": "PDF not found"}, 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ulogin', methods=['GET', 'POST'])
def ulogin():
    if 'user' in session:
        return redirect(url_for('userhome'))

    if request.method == "GET":
        return render_template('ulogin.html') 

    cursor = link.cursor()
    try: 
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM questionpaper_2025_user WHERE email = '"+email+"' AND password = '"+password+"'")
        user = cursor.fetchone()

        if user:
            session['user'] = user[3] 
            session['username'] = user[2]  
            return redirect(url_for('userhome'))
        else:
            return render_template('ulogin.html', error='Invalid email or password') 
    except Exception as e:
        return render_template('ulogin.html', error=str(e))
    finally:
        cursor.close()




 

 





@app.route('/uregister', methods=['GET', 'POST'])
def uregister():
      
  if 'user' in session:
    return redirect(url_for('userhome'))
  
  if request.method == "GET": 

    return render_template('uregister.html')  
  
  else: 
    cursor = link.cursor()  
    try: 
      name = request.form["name"]
      email = request.form["email"]
      password = request.form["password"] 
      phone = request.form["phone"]  

      # check = responseaccess()
      # if check:
      #     return check


      uid = 'uid_'+''.join(random.choices(string.ascii_letters + string.digits, k=10))
      cursor.execute("SELECT * FROM questionpaper_2025_user WHERE email = '"+email+"'")
      user = cursor.fetchone()
 
      if user:
        return render_template('uregister.html', exists='User already exists') 
      else:
        cursor.execute("INSERT INTO questionpaper_2025_user (uid,name,email,password,phone) VALUES ('"+uid+"','"+name+"','"+email+"','"+password+"','"+phone+"')") 
        link.commit()
        return render_template('uregister.html', success='Registration successful') 
       
    except Exception as e:
      error = e
      return render_template('uregister.html', error=error)
      
    finally:
        cursor.close() 


@app.route('/userhome', methods=['GET'])
def userhome(): 
    if 'user' not in session:
        return redirect(url_for('ulogin'))
    return render_template('userhome.html')  


@app.route('/upload', methods=["GET", "POST"])
def upload():  
  if 'user' not in session:
    return redirect(url_for('ulogin'))
  
  if request.method == "GET": 
    return render_template('upload.html') 

  else:
    uid = 'uid_' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    base_folder = os.path.join("workspace", uid)
    pdf_folder = os.path.join(base_folder, "pdfs")
    image_folder = os.path.join(base_folder, "images")
    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs(image_folder, exist_ok=True)

    uploaded_files = request.files.getlist("files")
    if not uploaded_files or len(uploaded_files) != 3:
        return {"error": "Please upload exactly 3 PDF files."}, 400

    pdf_filepaths = []
    for file in uploaded_files:
        filepath = os.path.join(pdf_folder, file.filename)
        file.save(filepath)
        pdf_filepaths.append(filepath)

    all_pdf_images = []
    for pdf_path in pdf_filepaths:
        page_images = pdf_to_images(pdf_path, image_folder)
        all_pdf_images.append(page_images)

    prompt = (
        "Extract all the questions from this question paper image. "
        "Ignore any headings with total marks like '15M'. "
        "For each question, return its number, the question text, and the marks assigned to it "
        "(like 5, 6, 8, etc. – not the total marks). "
        "Use the JSON array format with fields: 'question_number', 'question_text', and 'marks'."
    )

    all_extracted_questions = []
    for page_images in all_pdf_images:
        for img_path in page_images:
            questions = extract_questions_from_image(img_path, prompt)
            for q in questions:
                try:
                    q['marks'] = int(q.get('marks', 0))
                except:
                    q['marks'] = 0
            all_extracted_questions.extend(questions)

    all_extracted_questions.sort(key=lambda x: parse_question_number(x.get("question_number", "")))
    all_extracted_questions = renumber_questions(all_extracted_questions)

    final_pdf_path = os.path.join(base_folder, "final_question_bank.pdf")
    create_questions_pdf(all_extracted_questions, final_pdf_path)

    cursor = link.cursor()
    try:
        data_uid = 'uid_' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        insert_query = """
            INSERT INTO questionpaper_2025_data (id, uid, user, username, directory)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (None, data_uid, session['user'], session['username'], uid)
        cursor.execute(insert_query, values)
        link.commit()
    except Exception as e:
        print("DB Insertion Error:", e)
    finally:
        cursor.close()


    flash('upload')
    return redirect(url_for('udata')) 
  




 



@app.route('/udata', methods=['GET'])
def udata():
    if 'user' not in session:
        return redirect(url_for('ulogin'))

    cursor = link.cursor()
    try:
        query = "SELECT * FROM questionpaper_2025_data WHERE user = %s"
        cursor.execute(query, (session['user'],))
        results = cursor.fetchall()
        return render_template('udata.html', data=results)
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()









@app.route('/download_zip/<uid>')
def download_zip(uid):
    pdf_folder = os.path.join("workspace", uid, "pdfs")
    zip_path = os.path.join("workspace", uid, "original_pdfs.zip")

    if not os.path.exists(pdf_folder):
        return {"error": "PDFs not found"}, 404

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(pdf_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, pdf_folder)
                zipf.write(file_path, arcname=arcname)

    return send_file(zip_path, as_attachment=True)











@app.route('/ulogout')
def ulogout():
    session.pop('user', None) 
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
