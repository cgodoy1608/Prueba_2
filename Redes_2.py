from fastapi import FastAPI, HTTPException
from typing import List, Optional
import os

app = FastAPI()

campus = ["zona core", "campus uno", "campus matriz", "sector outsourcing"]

@app.get("/")
def read_root():
    return {"message": "API para gestión de dispositivos en campus"}

@app.get("/campus/")
def list_campuses():
    return {"campuses": campus}

@app.get("/devices/{campus_id}")
def view_devices(campus_id: int):
    if 1 <= campus_id <= len(campus):
        file_name = campus[campus_id - 1] + ".txt"
        try:
            with open(file_name, "r") as file:
                devices = [line.strip() for line in file.readlines()]
            return {"devices": devices}
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"No se encontró el archivo {file_name}")
    else:
        raise HTTPException(status_code=400, detail="ID de campus no válido")

@app.post("/devices/{campus_id}")
def add_device(
    campus_id: int, 
    device_type: str, 
    device_name: str, 
    hierarchy: str, 
    ip_address: str, 
    services: Optional[List[str]] = None
):
    if 1 <= campus_id <= len(campus):
        file_name = campus[campus_id - 1] + ".txt"
        services = services or []
        with open(file_name, "a") as file:
            file.write("\n---------------------------------\n")
            file.write(f"Dispositivo: {device_type}\n")
            file.write(f"Nombre: {device_name}\n")
            file.write(f"Jerarquía: {hierarchy}\n")
            file.write(f"IP: {ip_address}\n")
            file.write(f"Servicios: {', '.join(services)}\n")
            file.write("---------------------------------\n")
        return {"message": "Dispositivo añadido con éxito"}
    else:
        raise HTTPException(status_code=400, detail="ID de campus no válido")

@app.delete("/devices/{campus_id}")
def delete_devices(campus_id: int):
    if 1 <= campus_id <= len(campus):
        file_name = campus[campus_id - 1] + ".txt"
        if os.path.exists(file_name):
            os.remove(file_name)
            return {"message": f"Todos los dispositivos en {campus[campus_id - 1]} han sido borrados."}
        else:
            raise HTTPException(status_code=404, detail=f"No se encontró el archivo {file_name}")
    else:
        raise HTTPException(status_code=400, detail="ID de campus no válido")

@app.delete("/campus/{campus_id}")
def delete_campus(campus_id: int):
    if 1 <= campus_id <= len(campus):
        removed_campus = campus.pop(campus_id - 1)
        return {"message": f"Campus '{removed_campus}' ha sido eliminado de la lista."}
    else:
        raise HTTPException(status_code=400, detail="ID de campus no válido")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
