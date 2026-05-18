from fastapi import FastAPI  , Path ,HTTPException ,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field
from typing import Annotated, Optional, Literal
import json
app = FastAPI()

class criketer(BaseModel):
    id : Annotated[str ,  Field(..., description = 'ID of Player' ,  example = 'C001')]
    name : Annotated[str , Field(..., description = 'Name of Player' , example = 'Arjun')]
    city : Annotated[str , Field(..., description = 'City of Player' , example = 'Delhi')]
    gender : Annotated[Literal['male' , 'female' , 'others'] , Field(description  = 'Gender of player')]
    age :  Annotated[int  , Field(..., gt = 0 , lt = 120 , description = 'age of Player ')]
    weight :  Annotated[int , Field(..., description = 'Weight of Player')]                
    runs :  Annotated[int , Field(..., description = 'Runs of Player')]
    Average :Annotated[float , Field(..., description = 'Average of Player')]
    strike_rate : Annotated[float , Field(..., description = 'Strike rate of Player')]

class criketerupdate(BaseModel):
    name  : Annotated[Optional[str] , Field( default = None)]
    city : Annotated[Optional[str] , Field( default = None)]
    age :  Annotated[Optional[int] ,  Field( default = None , gt = 0)]
    gender : Annotated[Optional[Literal['male' , 'female' , 'other']] , Field(default = None)]
    runs : Annotated[Optional[float] , Field(default = None ,gt = 0)]
    strike_rate : Annotated[Optional[float] , Field(default = None ,gt = 0)]
    Average : Annotated[Optional[float] , Field(default = None ,gt = 0)]


def load_data():
    with open('criketer.json' , 'r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('criketer.json' , 'w') as f:
        json.dump(data ,f)

@app.get("/")
def Hello():
    return {'message' : 'hi cricket lovers'}

@app.get('/about')
def about():
    return {'message' : 'Fully functional API to manage Criketers Data'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/criketer/{criketer_id}')
def view_criketer(criketer_id : str = Path(..., description = "ID of the Criketer in DB" , example = "C001")):
    data = load_data()
    if criketer_id in data:
        return data[criketer_id]

    raise HTTPException(status_code = 404 , detail  = 'Player not Found')
@app.get('/sort')
def sort_criketer(
    sort_by : str = Query(...,description = 'sort on  Runs ,strike rate , Average or age'),
    order : str = Query(..., description = 'sort in asc or desc order')):

    field = ['runs' ,'strike_rate' , 'Average' , 'age' ]
    if sort_by not in field:
        raise HTTPException(status_code = 400 , detail = f'Invalid field select from{field}')
    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code = 404 ,detail = f'Invalid field select b/w asc or desc')
    
    data = load_data()
    reverse_order = True if order == 'desc' else False

    # convert dict -> list for sorting

    criketer_list = list(data.values())

    sorted_data = sorted(
        criketer_list,
        key = lambda x : x.get(sort_by  , 0),
        reverse = reverse_order)
    return sorted_data

@app.post('/create')
def create_data(criketer: criketer):
    data = load_data()
    if criketer.id in data:
        raise HTTPException(status_code = 404, detail = 'Criketer already exist')
    data[criketer.id] = criketer.model_dump(exclude = {'id'})
    save_data(data)

    return {'message' : 'criketer  created successfully'}

@app.put('/edit/{criketer_id}')
def update_criketer(criketer_id : str , criketer_update : criketerupdate):
    data = load_data()

    if criketer_id not in data:
        raise HTTPException(status_code = 404 , detail = 'Criketer not found')
    
    updated_data = criketer_update.model_dump(exclude_unset = True)

    data[criketer_id].update(updated_data)

    save_data(data)
    return {'message' : 'Criketer Updated Successfully'}

@app.delete('/Delete/{criketer_id}')
def delete_criketer(criketer_id  : str):
    data = load_data()

    if criketer_id not in data:
        raise HTTPException(status_code = 404 , detail = 'Criketer not found')
    del data[criketer_id]
    save_data(data)
    return{'message'   : 'Criketer record is deleted'}






    

    








    
    





    
