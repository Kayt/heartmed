from models import Doctor

float_formatter = lambda x: "%.1f" % x

def generate_res(pred):
    if float_formatter(pred) == '1.0':
        return 'Severe'
    elif float_formatter(pred) == '0.5':
        return 'Mild'
    elif float_formatter(pred) == '0.2':
        return 'Low'
    elif float_formatter(pred) == '0.0':
        return 'Safe'

def get_status(res):
    if res == 'Safe':
        return False 
    return True 


def get_doc(name):
    doc = Doctor.query.filter_by(username=name).first()
    return doc.id