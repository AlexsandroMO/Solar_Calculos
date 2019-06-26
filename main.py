from flask import Flask, render_template, url_for, request,send_from_directory
import Calcula
import db
#===================================================================

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route("/teladados")
def teladados():
  return render_template('teladados.html')

@app.route('/userarea', methods = ['POST', 'GET'])
def userarea():
  if request.method == 'POST':
    resultuserarea = request.form
    email = resultuserarea['email']
    password = resultuserarea['password']

    convert_ = db.query_email_confere(email, password)

    email_ = convert_[0]['EMAIL']
    password_ = convert_[0]['PASSWORD']
    name_user = convert_[0]['FIRST_NAME']

    status = True
    
    if email == '' or password == '':
      return f"""
        <p>Atenção, Todos os campos precisam ser preenchidos... :( </p>
        <br>
        <br>
        <br>
        <p><a href="/cotation"><img src="https://image.flaticon.com/icons/png/512/54/54906.png" alt="some text" width=40 height=40></p>

     """

    if email == email_.lower() and password == password_:
      return render_template("userarea.html", title='Python_Flask', status=status, name_user=name_user.lower().capitalize())
    else:
      return render_template("message.html", email=email)

@app.route('/result', methods = ['POST', 'GET'])
def result():

  if request.method == 'POST':
    resultcep = request.form
    print(resultcep)
    consultCEP = resultcep['cep']
    print(consultCEP)

    DF_Data = Calcula.calculogeral(consultCEP)
    tal_log = Calcula.consultlog_lat(consultCEP)

    dados = DF_Data[0]
    local_name = DF_Data[1]

    print(dados)
    print(local_name)
    print(tal_log)

    lat = tal_log[0]
    log = tal_log[1]

    return render_template("result.html", consultCEP=consultCEP,  lat=lat, log=log, local_name=local_name, dados=dados, tables=[dados.to_html(classes='data')], titles=dados.columns.values)

@app.route('/result2', methods = ['POST', 'GET'])
def result2():

  if request.method == 'POST':
    result_calc = request.form
    print(result_calc)

    cep = result_calc['cep']
    prop_name = result_calc['prop_name']

    kwp = float(result_calc['kwp'])
    w_ = float(result_calc['w_'])
    kwh = float(result_calc['kwh'])

    var_efic_ano = float(result_calc['var_efic_ano'])
    tx = float(result_calc['tx'])
    inf_eneg = float(result_calc['inf_eneg'])
    kit = float(result_calc['kit'])
    frete = float(result_calc['frete'])
    var_proj = float(result_calc['var_proj'])
    var_inst = float(result_calc['var_inst'])

    print(cep)
    print(prop_name)

    print(kwp)
    print(w_)
    print(kwh)
    print(var_efic_ano)
    print(tx)
    print(inf_eneg)
    print(kit)
    print(frete)
    print(var_proj)
    print(var_inst)

    chama_dfinal = Calcula.calcula_DataFrame(cep, prop_name, kwp, w_, kwh, var_efic_ano, tx, inf_eneg, kit, frete, var_proj, var_inst)

    Ano_Saldo = chama_dfinal[0]
    Gera_Econ = chama_dfinal[1]
    P_Base1 = chama_dfinal[2]
    P_Base2 = chama_dfinal[3]
    rs_p = chama_dfinal[4]
    #TMS = chama_dfinal[5]

    print(Ano_Saldo)
    print(Gera_Econ)
    print(P_Base1)
    print(P_Base2)
    print(rs_p)
    #print(TMS)

    return render_template("result2.html", tables=[Ano_Saldo.to_html(classes='data')], titles=Ano_Saldo.columns.values, tables1=[Gera_Econ.to_html(classes='data')], titles1=Gera_Econ.columns.values, tables2=[P_Base1.to_html(classes='data')], titles2=P_Base1.columns.values, tables3=[P_Base2.to_html(classes='data')], titles3=P_Base2.columns.values, tables4=[rs_p.to_html(classes='data')], titles4=rs_p.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
