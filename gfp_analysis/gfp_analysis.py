"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import os
from typing import List
import pynecone as pc
import asyncio


filename = f"{config.app_name}/{config.app_name}.py"

class State(pc.State):
    """The app state."""

    # Whether we are currently uploading files.
    is_uploading: bool

    @pc.var
    def file_str(self) -> str:
        """Get the string representation of the uploaded files."""
        return "\n".join(os.listdir(pc.get_asset_path()))
    
    async def handle_upload(self, files: List[pc.UploadFile]):
        """Handle the file upload."""
        self.is_uploading = True

        # Iterate through the uploaded files.
        for file in files:
            upload_data = await file.read()
            outfile = pc.get_asset_path(file.filename)
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

        # Stop the upload.
        return State.stop_upload

    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False

color = "rgb(107,99,246)"


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
        pc.vstack(
            pc.heading("GFP Analysis", font_size="2em", margin_top="0.75em"),
                pc.upload(
                    pc.button(
                            "Select File(s)",
                            height="70px",
                            width="200px",
                            color=color,
                            bg="white",
                            text_align="center",
                            border="1px dotted black",
                            margin_top = "0.5em",
                            margin_bottom = "0.5em"
                        ),
                pc.text(
                    "Drag and drop files here or click to select files",
                    font_size="1em", 
                    margin_top = "0.25em"
                ),
            pc.button(
                "Upload",
                on_click=State.handle_upload(pc.upload_files()),
                padding="2em",
                margin_bottom = "0.5em",
                margin_top="0.5em"
            ),
            border=f"1px solid {color}",
            padding="2em",
            text_align="center",
            ),
        ),
        pc.vstack(  
            pc.divider(border_color="black", margin_top = "1em", margin_bottom="1em"),
            pc.heading("Files:"),
            pc.cond(
                State.is_uploading,
                pc.progress(is_indeterminate=True, color="blue", width="100%"),
                pc.progress(value=0, width="100%"),
                ),
            ),
        ),
        )

def about():
    return pc.text("About page!", font_size="2em")

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.add_page(about)
app.compile()