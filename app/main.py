@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # validating file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "Only image files are allowed")
    
    # generating unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_id = uuid.uuid4().hex  
    new_filename = f"{unique_id}{file_ext}"
    save_path = os.path.join(settings.upload_folder, new_filename)

    # save file
    with open(save_path, "wb") as f:
        f.write(await file.read())

    # send to RabbitMQ
    try:
        channel = await get_rabbitmq_channel()
        await channel.default_exchange.publish(
            Message(
                body=new_filename.encode(),
                delivery_mode=2
            ),
            routing_key=settings.queue_name
        )
    except Exception as e:
        # Log the detailed error message
        print(f"Error while sending to RabbitMQ: {e}")
        raise HTTPException(500, f"Message queue error: str({e})")
    
    return {"filename": new_filename}
