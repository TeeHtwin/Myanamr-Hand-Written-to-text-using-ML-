import streamlit as st
import requests
import io
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import base64

def main():
    PAGES = {
        "About": about,
        "App": canvas_app,
        
    }
    page = st.sidebar.selectbox("Page:", options=list(PAGES.keys()),format_func=str)
    PAGES[page]()

    with st.sidebar:
        st.markdown("---")
       
        st.markdown(
            'Go to pages'
        )

def about():
      st.markdown(
        """
    Welcome to the demo of Pendora using  [Streamlit Drawable Canvas](https://github.com/andfanilo/streamlit-drawable-canvas).
    
    This site will allow you to write Burmese words and get text result.
    """
    )
      
def canvas_app():
    # set up canvas and buttons
    stroke_width = st.sidebar.slider("Stroke width: ", 5, 15, 5)
   
    canvas_result = st_canvas(
        fill_color= "#eee", #rgba(255, 165, 0,0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        update_streamlit=True,
        height=300,
        width=1000,
        background_color="#fff",
        drawing_mode="freedraw",
        key="canvas",
    )

    if st.button("Submit"):
        # get image from canvas
        img = canvas_result.image_data
        img = Image.fromarray(img.astype("uint8"), "RGBA")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()

        # send image to Flask API
        response = requests.post("http://127.0.0.1:5000/image", data=img_bytes)
        response_json = response.json()
        st.write("Response from server:", response_json['message']) # might delete later

    if st.button("Get Image"):
        # get saved image from Flask API
        response = requests.get("http://127.0.0.1:5000/get_image")
        if response.status_code == 200:
            response_json = response.json()
            st.write(response_json['success'])
            # display image in Streamlit UI
            img_bytes = response_json['image']
            img = io.BytesIO(base64.b64decode(response_json['image']))
            st.image(img, caption="Saved image", use_column_width=True)
        else:
            st.warning("Failed to get saved image from server.")

    


if __name__ == "__main__":
    st.set_page_config(
        page_title="Pendora Demo", page_icon=":pencil2:"
    )
    st.title("Pendora")
    st.sidebar.subheader("Pages")
    main()