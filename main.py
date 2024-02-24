# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import send_file, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 * 1024
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
basePath = os.path.abspath(os.path.dirname(__file__))  # 当前文件所在路径
app.config['UPLOADED_DIR'] = basePath + '/static/uploads'


@app.route('/manage')
def manage_file():
    files_list = os.listdir(app.config['UPLOADED_DIR'])
    return render_template('manage.html', files_list=files_list)


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = app.config['UPLOADED_DIR']  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/delete/<filename>')
def delete_file(filename):
    os.remove(os.path.join(app.config['UPLOADED_DIR'] , filename))
    return redirect(url_for('manage_file'))

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if "url" in request.form and request.form["url"].strip():
            print("url is ", request.form["url"])
            filename = request.form["url"].split("/")[-1]
            os.system("wget -P ./static/uploads %s -o %s --no-check-certificate" % (request.form["url"], filename))
            return render_template('upload.html', content="")
        else:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            f = request.files['file']

            if not f.filename.strip():
                flash('No selected file')
                upload_path = "Please upload file"
#           else:
#                upload_path = os.path.join(app.config['UPLOADED_DIR'], secure_filename(f.filename))  #  注意：没有的文件夹一定要先创建，不然会提示没有该路径
#                dir_list = os.listdir(app.config['UPLOADED_DIR'])
#                dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOADED_DIR'], x)))
#                f.save(upload_path)
#                for item in dir_list[1:]:
#                    os.remove(os.path.join(app.config['UPLOADED_DIR'], item))
#                    upload_path += "\nFiles' num is more than 10, `rm %s`" % item
#                upload_path = upload_path.replace('\n', '<br/>')
                # os.system('sleep 2d && rm -rf %s && echo "rm %s done" &' % (upload_path, upload_path))
            else:
                    upload_path = os.path.join(app.config['UPLOADED_DIR'], secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
                    dir_list = os.listdir(app.config['UPLOADED_DIR'])
                    dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOADED_DIR'], x)))
                    f.save(upload_path)
                    upload_path = "wget http://szwg-sys-rpm0446.szwg01.baidu.com:8009/download/" + secure_filename(f.filename)
                    for item in dir_list[100:]:
                        os.remove(os.path.join(app.config['UPLOADED_DIR'], item))
                        upload_path += "\nFiles' num is more than 10, `rm %s`" % item
                    upload_path = upload_path.replace('\n', '<br/>')
                    return render_template('upload.html', content=upload_path)
        #return redirect(url_for('upload'), content=upload_path)
    return render_template('upload.html')


@app.route('/decode')
def decode():
    files_list = os.listdir(app.config['UPLOADED_DIR'])
    return render_template('manage.html', files_list=files_list)




@app.route('/', methods=['POST', 'GET'])
def init():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8009, host="0.0.0.0", debug=True)
