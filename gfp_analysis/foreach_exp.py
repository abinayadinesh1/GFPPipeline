"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import os
from typing import List
import pynecone as pc
import asyncio

color = "rgb(107,99,246)"

class ForeachState(pc.State):
    color: List[str] = [
        "red",
        "green",
        "blue",
        "yellow",
        "orange",
        "purple",
    ]

def colored_box(color: str):
    return pc.box(pc.text(color), bg=color)

class State(pc.State):
    """The app state."""

    # Whether we are currently uploading files.
    is_uploading: bool
    # files : List[pc.UploadFile] = []

    @pc.var
    def file_str(self) -> str:
        """Get the string representation of the uploaded files."""
        return "\n".join(os.listdir(pc.get_asset_path()))
    
    async def handle_upload(self, files: List[pc.UploadFile]):
        """Handle the file upload."""
        self.is_uploading = True

        # Iterate through the uploaded files.
        for file in files:
            # print("file", file) #<starlette.datastructures.UploadFile object at 0x10cf82dd0>
            upload_data = await file.read()  #if you print this its a huge object of nonsense
            outfile = pc.get_asset_path(file.filename) 
            with open(outfile, "wb") as file_object:
                # print(file_object)
                file_object.write(upload_data)

        # Stop the upload.
        return State.stop_upload

    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False


def index():
    return pc.responsive_grid(
        pc.foreach(ForeachState.color, colored_box),
        columns=[2, 4, 6],
    )

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
