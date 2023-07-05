
from pcconfig import config
import os
from typing import List
import pynecone as pc
import asyncio

color = "rgb(107,99,246)"

def colored_box(color: str): 
        ''' for some reason, must be defined outside of the state. 
        recieves 'EventSpec' object has no attribute 'key' if not. '''
        return pc.hstack(
            pc.box(pc.text(color), bg=color, padding = "0.1em"),
            pc.spacer())
class State(pc.State):
    """The app state."""

    # Whether we are currently uploading files.
    is_uploading: bool
    color: List[str] = [
        "red",
        "green",
        "blue",
        "yellow",
        "orange",
        "purple",
        "pink",
        "orange",
        "blue",
    ]
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
    def colored_box(color: str):
        return pc.box(pc.text(color), bg=color)


def index():
    return pc.responsive_grid(
        pc.foreach(State.color, colored_box),
        columns=[2, 4, 6],
    )

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()



#ssf = solid state fermentation = spore powder
# goal for today: be able to upload a bunch of images and render them in the grid (through a for each)
# """Welcome to Pynecone! This file outlines the steps to create a basic app."""
# from pcconfig import config
# import os
# from typing import List
# import pynecone as pc
# import asyncio

# filename = f"{config.app_name}/{config.app_name}.py"
# color = "rgb(107,99,246)"

# def image_box(filename: str):
#     return pc.center(
#         pc.vstack(
#             pc.image(src="ex_gfp_fungi.JPG", width="100px", height="auto"),
#             pc.box(pc.text(filename), bg="white"),
#             pc.text("LAB color space analysis")
#         ),
#     )

# class State(pc.State):
#     """The app state."""

#     # Whether we are currently uploading files.
#     is_uploading: bool
#     files : List[pc.UploadFile] = []
#     color: List[str] = [
#         "red",
#         "green",
#         "blue",
#         "yellow",
#         "orange",
#         "purple",
#         "pink",
#         "orange",
#         "blue",
#     ]

#     @pc.var
#     def file_str(self) -> str:
#         """Get the string representation of the uploaded files."""
#         return "\n".join(os.listdir(pc.get_asset_path()))
    
#     async def handle_upload(self, files: List[pc.UploadFile]):
#         """Handle the file upload."""
#         self.is_uploading = True
#         print("files", files)
#         print("state filestring", State.file_str())

#         # Iterate through the uploaded files.
#         for file in files:
#             # print("file", file) #<starlette.datastructures.UploadFile object at 0x10cf82dd0>
#             upload_data = await file.read()  #if you print this its a huge object of nonsense
#             outfile = pc.get_asset_path(file.filename) 
#             with open(outfile, "wb") as file_object:
#                 # print(file_object)
#                 file_object.write(upload_data)

#         # Stop the upload.
#         return State.stop_upload

#     async def stop_upload(self):
#         """Stop the file upload."""
#         await asyncio.sleep(1)
#         self.is_uploading = False

#     def process_files(self): #self is being passed in as State
#         self.files = pc.upload_files()
#         print("files stored in :", self.files)
#         # asyncio.run(self.handle_upload(self.files))
#         # self.handle_upload(self.files)

# def index():
#     return pc.center(
#         pc.vstack(
#         pc.vstack(
#             pc.heading("GFP Analysis", font_size="2em", margin_top="0.75em"),
#             pc.vstack(
#             pc.upload(
#                     pc.button(
#                             "Select File(s)",
#                             height="70px",
#                             width="200px",
#                             color=color,
#                             bg="white",
#                             text_align="center",
#                             border="1px dotted black",
#                             margin_top = "0.5em",
#                             margin_bottom = "0.5em"
#                         ),
#                 pc.text(
#                     "Drag and drop files here or click to select files",
#                     font_size="1em", 
#                     margin_top = "1em",
#                     margin_bottom = "0.25em"
#                 ),
#             padding="2em",
#             text_align="center",
#             ),
#             pc.button(
#                 "Upload",
#                 on_click = State.process_files(),
#                 # on_click=State.handle_upload(pc.upload_files()),
#                 padding="1.5em",
#                 margin_bottom="2em",
#             ),
#             border=f"1px solid {color}",
#             ),
#         ),
#         pc.vstack(  
#             pc.divider(border_color="black", margin_top = "1em", margin_bottom="1em"),
            
#         pc.heading("Files:"),
#         pc.cond(
#             State.is_uploading,
#             pc.progress(is_indeterminate=True, color="blue", width="100%"),
#             pc.progress(value=0, width="100%"),
#         ),
#         pc.hstack(
#             pc.text_area(
#                 is_disabled=True,
#                 value=State.file_str,
#                 width="50%",
#                 height="100%",
#                 bg="white",
#                 color="black",
#                 placeholder="No File",
#                 min_height="20em",
#             ),
#                 pc.responsive_grid(
#                     pc.foreach(State.files, image_box),
#                     columns=[2, 4, 6],
#                 )
#             ),
#             ),
#         ),
#         )

# def about():
#     return pc.text("About page!", font_size="2em")

# # Add state and page to the app.
# app = pc.App(state=State)
# app.add_page(index)
# app.add_page(about)
# app.compile()

# # #ssf = solid state fermentation = spore powder
# # # goal for today: be able to upload a bunch of images and render them in the grid (through a for each)