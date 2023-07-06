"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import os
from typing import List
import pynecone as pc
import asyncio

filename = f"{config.app_name}/{config.app_name}.py"
color = "rgb(107,99,246)"

def image_box(filename: str):
    return pc.center(
        pc.vstack(
            pc.image(src=filename, width="120px", height="auto"), #so far hardcoded, in the for each need to add path for image
            pc.box(pc.text(filename), bg="white"),
            pc.text("LAB color space analysis")
            
        ),
        padding="2em",
    )

class State(pc.State):
    """The app state."""

    # Whether we are currently uploading files.
    is_uploading: bool
    color: List[str] = [
        "red",
        "green",
        "blue",
        "yellow",
    ]

    @pc.var
    def file_str(self) -> str:
        """Get the string representation of the uploaded files."""
        return "\n".join(os.listdir(pc.get_asset_path()))

    @pc.var
    def file_list(self) -> str:
        """Get the names of each file as a list of strings."""
        return os.listdir(pc.get_asset_path())


    async def handle_upload(self, files: List[pc.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = pc.get_asset_path(file.filename)

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)
    
    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False

def index():
    return pc.center(
        pc.vstack(
        pc.vstack(
            pc.heading("GFP Analysis", font_size="2em", margin_top="0.75em"),
            pc.vstack(
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
                    margin_top = "1em",
                    margin_bottom = "0.25em"
                ),
            padding="2em",
            text_align="center",
            ),
            pc.button(
                "Upload",
                on_click=lambda: State.handle_upload(pc.upload_files()),
                padding="1.5em",
                margin_bottom="2em",
            ),
            border=f"1px solid {color}",
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
        pc.hstack(
            pc.text_area(
                is_disabled=True,
                value=State.file_str,
                width="50%",
                height="100%",
                bg="white",
                color="black",
                placeholder="No File",
                min_height="20em",
            ),
                pc.responsive_grid(
                    pc.foreach(State.file_list, image_box),
                    columns=[2, 4, 6],
                )
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

#be able to upload image without it crashing

