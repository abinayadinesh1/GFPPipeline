pc.heading("GFP Analysis", font_size="2em"),
            pc.upload(
            pc.button(
                "Select File(s)",
                height="70px",
                width="200px",
                color=color,
                bg="white",
                border=f"1px solid {color}",
            ),
            pc.text(
                "Drag and drop files here or click to select files",
                font_size="5em"
            ),
            border="1px dotted black",
            padding="2em",
        ),
        pc.hstack(
            pc.button(
                "Upload",
                on_click=State.handle_upload(pc.upload_files()),
            ),
        ),
        pc.heading("Files:"),
        pc.cond(
            State.is_uploading,
            pc.progress(is_indeterminate=True, color="blue", width="100%"),
            pc.progress(value=0, width="100%"),
        ),
        pc.text_area(
            is_disabled=True,
            value=State.file_str,
            width="100%",
            height="100%",
            bg="white",
            color="black",
            placeholder="No File",
            min_height="20em",
        ),
            spacing="1.5em",
            font_size="2em",
        ),
        padding_top="10%",