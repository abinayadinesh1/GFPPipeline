import pynecone as pc

class State(pc.State):
    """The app state."""

    # The image to show.
    img: str

    async def handle_upload(self, file: pc.UploadFile):
        """Handle the upload of a file.
        
        Args:
            file: The uploaded file.
        """
        upload_data = await file.read()
        outfile = f".web/public/{file.filename}"

        # Save the file.
        with open(outfile, "wb") as file_object:
            file_object.write(upload_data)

        # Update the img var.
        self.img = file.filename


def upload_image():
    """The main view."""
    return pc.vstack(
        pc.upload(
            pc.button("Select File"),
            pc.text("Drag and drop files here or click to select files"),
            border="1px dotted black",
            padding="20em",
        ),
        pc.button(
            "Upload", 
            on_click=lambda: State.handle_upload(pc.upload_files())
        ),
        pc.image(src=State.img),
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(upload_image, title="Upload")
app.compile()