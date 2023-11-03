from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
import json
from django.contrib import messages
import datetime
from haversine import haversine, Unit

from PIL import Image, ImageDraw, ImageFont
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(_file_))
STATIC_ROOT = os.path.join(PROJECT_ROOT,'static')
from .models import Members
from .useful_scripts import generate_random_id, encrypt, decrypt, generate_random_no
from .deploy import register_blood_bank, bblogin, register_hospital, hosplogin, \
    register_donor, blood_bank_get_info, collect_sample, retreive_collected_samples, \
    change_sample_state, list_samples_of_blood_type, hospital_get_info, \
    hospital_request_blood, get_hospital_agreements, getBloodType
# Create your views here.
def home(request):
    return render(request, 'blood_bank/index.html', {})
def about(request):
    return render(request, 'blood_bank/about.html', {})
def bregister(request):
    return render(request, 'blood_bank/bregister.html', {})
def hregister(request):
    return render(request, 'blood_bank/hregister.html', {})
def donor(request):
    return render(request, 'blood_bank/donor.html', {})
def login_blood(request):
    return render(request,'blood_bank/blogin.html', {})
def login_hosp(request):
    return render(request,'blood_bank/hlogin.html', {})
def donorreg(request):
    return render(request,'blood_bank/donorreg.html', {})
def hindex(request):
    return render(request,'blood_bank/hindex.html', {})
def requestsample(request):
    return render(request,'blood_bank/requestsample.html', {})
def orderedsample(request):
    return render(request,'blood_bank/orderedsample.html', {})
def viewportal(request):
    samples={}
    if request.POST:
        data = request.POST
        blood_type = data['blood']
        eblood_type = encrypt(blood_type)
        samples = list_samples_of_blood_type(eblood_type)
        samples,count = hosp_get_data(samples)
        request.session['samples']=samples
    else:
        try:
            del request.session['samples']
        except:
            pass
    return render(request,'blood_bank/viewportal.html', {})
def collectsample(request):
    return render(request,'blood_bank/collectsample.html', {})
def collectionlist(request):
    bb_id = request.session['blood_bank_id']
    bb_name, bb_email, bb_licence_no, bb_address,bb_lat,bb_lng = blood_bank_get_info(bb_id)
    bb_name, bb_email, bb_licence_no, bb_address,bb_lat,bb_lng = decrypt(bb_name), decrypt(bb_email), decrypt(bb_licence_no), decrypt(bb_address),decrypt(bb_lat),decrypt(bb_lng)
    context={}
    context['name'] = bb_name
    context['id'] = bb_id
    context['email'] = bb_email
    context['licence'] = bb_licence_no
    samples = retreive_collected_samples(bb_id)
    samples,donate_num = get_data(samples)
    context['samples'] = samples
    context['not_allowed_states'] = ["Requested", "Sent"]
    context['sample_num'] = len(samples)
    context['donate_num'] = donate_num
    context['rem_samples'] = len(samples) - donate_num
    return render(request,'blood_bank/collectionlist.html', context)
def bloodstate(request):
    bb_id = request.session['blood_bank_id']
    bb_name, bb_email, bb_licence_no, bb_address,bb_lat,bb_lng = blood_bank_get_info(bb_id)
    bb_name, bb_email, bb_licence_no, bb_address,bb_lat,bb_lng = decrypt(bb_name), decrypt(bb_email), decrypt(bb_licence_no), decrypt(bb_address),decrypt(bb_lat),decrypt(bb_lng)
    context={}
    context['name'] = bb_name
    context['id'] = bb_id
    context['email'] = bb_email
    context['licence'] = bb_licence_no
    samples = retreive_collected_samples(bb_id)
    samples,donate_num = get_data(samples)
    context['samples'] = samples
    context['not_allowed_states'] = ["Requested", "Sent"]
    context['sample_num'] = len(samples)
    context['donate_num'] = donate_num
    context['rem_samples'] = len(samples) - donate_num
    return render(request,'blood_bank/bloodstate.html', context)
def bbreg(request):
    if request.POST:
        data = request.POST
        name = data.get('name')
        address = data.get('Location')
        email = data.get('email')
        licence = data.get('License')
        password = data.get('password')
        t = Members.objects.filter(email = email)
        if(len(t)>0):
            messages.error(request,"User Already Registered!")
            return redirect('bregister')
        m = Members(email = email, password = password, flag = 'B')
        m.save()
        id = str(Members.objects.filter(email = email).first().id)
        lat, longi = get_coordinates(address)
        eid, ename, eaddress = encrypt(id), encrypt(name), encrypt(address),
        eemail, elicence, epassword = encrypt(email), encrypt(licence), encrypt(password)
        elat,elong = encrypt(str(lat)),encrypt(str(longi))
        register_blood_bank(eid, ename, eemail, eaddress, epassword, elicence, elat, elong)
        messages.success(request,"Registered Successfully")
        return redirect('login_blood')

def get_data(samples):
    s = []
    states = ["Collected","Tested OK","Tested NOT OK","Expired","Requested","Sent","Recieved"]
    if not len(samples) == 0:
        count = 0
        for sample in samples:
            ed_id, ebb_id, eblood_id, eblood_type ,state, edate = sample
            if not '' in [ed_id, ed_id, ebb_id, eblood_id, eblood_type,edate]:
                if sample == 5:
                    count+=1
                d_id, bb_id, blood_id, blood_type,state,date = decrypt(ed_id), decrypt(ebb_id), decrypt(eblood_id), decrypt(eblood_type),states[state],decrypt(edate)
                s.append({'d_id': d_id, 'bb_id': bb_id, 'blood_id': blood_id, 'blood_type': blood_type, 'state': state,'date':date})
    else:
        count = 0
    return (s,count)
def blogin(request):
    context = {}
    if request.POST:
        data = request.POST
        email = data.get('username')
        pwd = data.get('password')
        try:
            id = str(Members.objects.filter(email = email, password = pwd, flag = 'B').first().id)
        except:
            messages.error(request,"Invalid Credentials!")
            return redirect('login_blood')
        eid = encrypt(id)
        request.session['blood_bank_id'] = eid
        bb_name, bb_email, bb_licence_no, bb_address, bb_lat, bb_long= bblogin(eid)
        name, email, licence, address= decrypt(bb_name), decrypt(bb_email), decrypt(bb_licence_no), decrypt(bb_address)
        context['name'] = name
        context['id'] = id
        context['email'] = email
        context['licence'] = licence
        samples = retreive_collected_samples(eid)
        
        samples,donate_num = get_data(samples)
        context['samples'] = samples
        context['not_allowed_states'] = ["Requested","Sent"]
        context['sample_num'] = len(samples)
        context['donate_num'] = donate_num
        context['rem_samples'] = len(samples) - donate_num
        messages.success(request,"Logged In Successfully!")
    elif request.session.get('blood_bank_id',"none") != "none":
        bb_id = request.session['blood_bank_id']
        bb_name, bb_email, bb_licence_no, bb_address,bb_lat,bb_lng = blood_bank_get_info(bb_id)
        bb_name, bb_email, bb_licence_no, bb_address,bb_lat,bb_lng = decrypt(bb_name), decrypt(bb_email), decrypt(bb_licence_no), decrypt(bb_address),decrypt(bb_lat),decrypt(bb_lng)
        context={}
        context['name'] = bb_name
        context['id'] = bb_id
        context['email'] = bb_email
        context['licence'] = bb_licence_no
        samples = retreive_collected_samples(bb_id)
        samples,donate_num = get_data(samples)
        context['samples'] = samples
        context['not_allowed_states'] = ["Requested", "Sent"]
        context['sample_num'] = len(samples)
        context['donate_num'] = donate_num
        context['rem_samples'] = len(samples) - donate_num
    else:
        return redirect('login_blood')
    return render(request,'blood_bank/bb_index.html',context)



def dreg(request):
    if request.POST:
        data = request.POST
        name = data.get('name')
        blood_type = data.get('blood')
        email = data.get('email')
        aadhar = data.get('aadhar')
        dob = data.get('DOB')
        t = Members.objects.filter(email = email)
        if(len(t)>0):
            messages.error(request,"User Already Registered!")
            return redirect('blogin')
        m = Members(email = email, password = aadhar, flag = 'D')
        m.save()
        id = str(Members.objects.filter(email = email).first().id)
        eid, ename, eblood_type, edob = encrypt(id), encrypt(name), encrypt(blood_type), encrypt(dob)
        eemail, eaadhar = encrypt(email), encrypt(aadhar)
        register_donor(ename, eid, eemail, eaadhar, eblood_type, edob)
        return redirect('blogin')
def collect_blood_sample(request):
    data = request.POST
    d_aadhar = data['Donorid']
    try:
        d_id = str(Members.objects.filter(password=d_aadhar, flag='D').first().id)
    except:
        messages.error(request,"Invalid Credentials")
        return redirect('collectsample')
    bb_id = request.session['blood_bank_id']
    blood_id = str(generate_random_no())
    _,blood_type = getBloodType(encrypt(d_id))
    tod_date = str(datetime.datetime.now().date())
    eblood_type , ed_id, ebb_id, eblood_id, etod_date = blood_type,encrypt(d_id),bb_id,encrypt(blood_id),encrypt(tod_date)
    collect_sample(eblood_type,ed_id, ebb_id, eblood_id,etod_date)
    messages.success(request,f"Sample Collected: {blood_id}")
    return redirect('collectionlist')


def request_sample(request):
    data = request.POST
    blood_type = data['blood']
    context={}
    return render(request, 'blood_bank/hblood.html', context)
def changeState(request):
    if request.POST:
        data = request.POST
        blood_id = data['blood_id']
        state = data['state']
        change_sample_state(encrypt(blood_id),state)
        request.session['message'] = "Blood Sample State Changed"
        return HttpResponseRedirect(reverse('blogin'))

def h_reg(request):
    if request.POST:
        data = request.POST
        name = data.get('name')
        address = data.get('Location')
        email = data.get('email')
        licence = data.get('License')
        password = data.get('password')
        t = Members.objects.filter(email = email)
        if(len(t)>0):
            messages.error(request,"User Already Registered!")
            return redirect('hregister')
        m = Members(email = email, password = password, flag = 'H')
        m.save()
        id = str(Members.objects.filter(email = email).first().id)
        lat, longi = get_coordinates(address)
        eid, ename, eaddress = encrypt(id), encrypt(name), encrypt(address),
        eemail, elicence, epassword = encrypt(email), encrypt(licence), encrypt(password)
        elat, elong = encrypt(str(lat)), encrypt(str(longi))
        register_hospital(eid, ename, eemail, eaddress, epassword, elicence, elat, elong)
        messages.success(request,"Registered Successfully")
        return redirect('login_hosp')

def hlogin(request):
    context = {}
    if request.POST:
        data = request.POST
        email = data.get('username')
        pwd = data.get('password')
        try:
            id = str(Members.objects.filter(email = email, password = pwd, flag = 'H').first().id)
        except:
            messages.error(request,"Invalid Credentials!")
            return redirect('login_hosp')
        eid = encrypt(id)
        h_name, h_email, h_licence_no, h_address, h_lat, h_long = hosplogin(eid)
        name, email, licence, address, lat, longi = decrypt(h_name), decrypt(h_email), decrypt(h_licence_no), decrypt(h_address), decrypt(h_lat), decrypt(h_long)
        context['name'] = name
        context['id'] = id
        request.session['hosp_id'] = eid
        context['email'] = email
        context['licence'] = licence
        context['address'] = address
        
    elif request.session.get('hosp_id', "none") != "none":
        e_id = request.session['hosp_id']
        h_name, h_email, h_licence_no, h_address, h_lat, h_long  = hospital_get_info(e_id)
        name, email, licence, address ,lat, longi = decrypt(h_name), decrypt(h_email), decrypt(h_licence_no), decrypt(h_address), decrypt(h_lat), decrypt(h_long)
        context['name'] = name
        context['id'] = decrypt(e_id)
        context['email'] = email
        context['licence'] = licence
        context['address'] = address
        context['lat'] = lat
        context['longi'] = longi
    else:
        return redirect('login_hosp')
    pos={}
    pos['lat'] = lat
    pos['longi'] = longi 
    dataJson = json.dumps(pos)
    context['pos'] = dataJson
    return render(request, 'blood_bank/hindex.html', context)

def sampleList(request):
    if request.POST:
        data = request.POST
        blood_type = data['blood']
        eblood_type = encrypt(blood_type)
        samples = list_samples_of_blood_type(eblood_type)
        samples,count = hosp_get_data(samples)
        request.session['samples'] = samples
        e_id = request.session['hosp_id']
        h_name, h_email, h_licence_no, h_address, h_lat, h_long  = hospital_get_info(e_id)
        name, email, licence, address ,lat, longi = decrypt(h_name), decrypt(h_email), decrypt(h_licence_no), decrypt(h_address), decrypt(h_lat), decrypt(h_long)
        # samples = orderingSamples(samples,(lat,longi))
        print(samples)
    return HttpResponseRedirect(reverse('requestsample'))
def orderingSamples(samples,hosp):
    values = []
    Hospital_cord = hosp
    for loc in samples:
        co_ord = (loc['lat'],loc['long'])
        distance=haversine(Hospital_cord,co_ord)
        values.append(round(distance,2))
    Distances = dict(zip(samples, values))
    Distances = dict(sorted(Distances.items(), key = lambda kv: kv[1]))
    return Distances

def orderBloodSample(request):
    if request.POST:
        data = request.POST
        blood_id = data['blood_id']
        h_id = data['h_id']
        a_id = str(generate_random_no())
        eblood_id,eh_id,ea_id = encrypt(blood_id),encrypt(h_id),encrypt(a_id)
        hospital_request_blood(eblood_id,eh_id,ea_id)
        agreements = get_hospital_agreements(eh_id)
        agreements = agreement_decrypt(agreements)
        request.session['agreements'] = agreements
    return HttpResponseRedirect(reverse('hlogin'))

def formAgreement(request):
    if request.POST:
        pass
def viewagreement(request):
    if request.POST:
        data = request.POST
        agreement = data['agreement_data']
        print(agreement)
def agreement_decrypt(agreements):
    a = []
    if not len(agreements) == 0:
        for agreement in agreements:
            eh_id, ebb_id, eb_id, ea_id = agreement
            if '' not in [eh_id, ebb_id, eb_id, ea_id]:
                a.append({"h_id":decrypt(eh_id) , "bb_id": decrypt(ebb_id),"b_id":decrypt(eb_id),"a_id":decrypt(ea_id)})
    return a
def hosp_get_data(samples):
    s = []
    states = ["Collected","Tested OK","Tested NOT OK","Expired","Requested","Sent"]
    if not len(samples) == 0:
        count = 0
        for sample in samples:
            ed_id, ebb_id, eblood_id, eblood_type ,state,date = sample
            if not '' in [ed_id, ed_id, ebb_id, eblood_id, eblood_type,date]:
                if sample == 5:
                    count+=1
                _, _, _, ebb_address,elat,elong = blood_bank_get_info(ebb_id)
                bb_address, bb_id, blood_id, blood_type,state,lat,long = decrypt(ebb_address), decrypt(ebb_id), decrypt(eblood_id), decrypt(eblood_type),states[state],decrypt(elat),decrypt(elong)
                s.append({'bb_address':bb_address, 'bb_id': bb_id, 'blood_id': blood_id, 'blood_type': blood_type, 'state': state, 'lat':lat,'long':long})
    else:
        count = 0
    return (s,count)


    
def get_coordinates(loc):
    key = 'AIzaSyDZ5NuyRVyV1oBa76J1HDOp4BkxTos_MIs'

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    params = {'key':key, 'address':loc}
    resp = requests.get(base_url,params)
    loc = resp.json()['results'][0]['geometry']['location']
    coord = (loc['lat'],loc['lng'])
    return coord



def dResult(request):
    if request.POST:
        data = request.POST
        aadhar = data['aadhar']
        name,btype = getBloodType(encrypt(aadhar))
        name,btype = decrypt(name),decrypt(btype)
        a = generate_cert(name,btype)
        if a:
            return render(request,"blood_bank/certificate.html",{"name":a})
        else:
            return redirect('index')
def generate_cert(name,type):
    im = Image.open(f"{STATIC_ROOT}/images/certificate.png")
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(f"{STATIC_ROOT}/fonts/alex-brush/AlexBrush-Regular.ttf",100)
    w, h = font.getsize(name)
    print(w)
    loc = ((1000-(w/2)),565)
    d.text(loc,str(name),fill = '#33362f',font = font)
    oswald = ImageFont.truetype(f"{STATIC_ROOT}/fonts/oswald/Oswald-Light.ttf",50)
    d.text((950,1240),str(datetime.date.today()),fill = '#33362f',font = oswald)
    d.text((1730,1240),str(type),fill = '#33362f',font = oswald)
    # im.show()
    im.save(f"blood_bank/Static/images/certificates/certificate.png")
    return 1