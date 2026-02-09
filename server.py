from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import io
import os
import uvicorn

from classifier import hybrid_classify_log_message

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Log Classification Server is running"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV.")

    try:
      
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if 'log_message' not in df.columns or 'source' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'log_message' and 'source' columns.")

        df['Predicted Label'] = df.apply(
            lambda row: hybrid_classify_log_message(row['log_message'], row['source']), 
            axis=1
        )

        output_file = "classified_logs_output.csv"
        df.to_csv(output_file, index=False)

        return FileResponse(path=output_file, filename="classified_logs.csv", media_type='text/csv')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)