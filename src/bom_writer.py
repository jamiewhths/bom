import models as m

def write(bom: m.BillOfMaterials, filepath: str):
    with open(filepath, 'w') as file:
        file.write('test')
