# Required Libraries
from tkinter import *
from tkinter import ttk
import requests  
from PIL import Image, ImageTk 
import customtkinter
from urllib.request import urlopen
from io import BytesIO                               
from tkinter import messagebox
import pygame

# App Class
class MovieFinderApp:
    def __init__(self, window):
        self.window = window
        window.title("🎥Movie DB App")  
        window.geometry("810x730")
        window.resizable(0, 0)
    
     # Initialize the pygame mixer
        pygame.mixer.init()
    
    # Initialize sounds
        self.click_sound = pygame.mixer.Sound("click_sound.mp3")
        error_sound = pygame.mixer.Sound("click_sound.mp3")
    # Notebook for TABS
        self.notebook = ttk.Notebook(window)
        self.notebook.pack(expand=True, fill="both")  
        
    # HOME TAB Frame
        self.home_frame = customtkinter.CTkFrame(self.notebook)
        self.notebook.add(self.home_frame, text="🏠 Home")

    # Add content to the "Home" tab
        self.home_tab()

    # Movie Tab Frame
        self.movies_frame = customtkinter.CTkFrame(self.notebook)
        self.notebook.add(self.movies_frame, text="🎬 Movies")

        # Initialize movie_results and current_movie_index
        self.current_movie_index = 0
        self.movie_results = []

        # Create the movies tab
        self.movies_tab()

    # About Tab Frame
        self.about_frame = customtkinter.CTkFrame(self.notebook)
        self.notebook.add(self.about_frame, text="ℹ️ About")

        self.about_tab()

        self.current_movie_index = 0
        self.movie_results = []


    # FUNCTION CREATED.. FOR MOVIE SECTION// TO STORE CONTENTS IN THAT SPECFIC TAB
    def movies_tab(self):

        # BG IMAGE SETTING FOR EACH TAB 
        bg_image = ImageTk.PhotoImage(Image.open("moviee.jpg").resize((1100, 900)))
        bg_label = customtkinter.CTkLabel(self.movies_frame, text="", image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL WIDGET FOR HEADING FOR WINDOW TWO
        self.l1 = customtkinter.CTkLabel(self.movies_frame, text="✨ MOVIE EXPLORER ✨", font=(('Cascadia code light', 26, 'bold')), bg_color="white", fg_color="#131313")
        self.l1.place(x=320, y=20)

        # FRAME 1 FOR CONTENTS: SEARCH BAR WIDGET AND SEARCH BTN WIDGET
        self.f1 = customtkinter.CTkFrame(self.movies_frame, width=570, height=130)
        self.f1.place(x=130, y=70)

        self.label = customtkinter.CTkLabel(self.f1, text="Enter Movie Name:", font=(('Cascadia code light', 15)))
        self.label.place(x=80, y=20)

        self.entry = customtkinter.CTkEntry(self.f1, width=270, height=40, font=(('Cascadia code light', 15)) )
        self.entry.place(x=80, y=60)
        
        self.search_button = customtkinter.CTkButton(self.f1, text="🔍Search", command=self.search_movie, width=90, height=40, bg_color="#333333", fg_color="black", hover_color="#282A2A")
        self.search_button.place(x=370, y=60)

        # MOVIE DETAIL FRAME2 WIDGET INCLUDED LABEL WIDGET FOR HEADER
        self.detail_frame = customtkinter.CTkFrame(self.movies_frame, width=250, height=300)
        self.detail_frame.place(x=130, y=220)

        self.l2 = customtkinter.CTkLabel(self.detail_frame, text="MOVIE DETAILS", font=(('Cascadia code light', 15, 'bold')))
        self.l2.place(x=50, y=20)

        # FRAME3 WIDGET FOR DISPLAYING POSTER/IMAGE OF THE MOVIE
        self.poster_frame = customtkinter.CTkFrame(self.movies_frame, width=250, height=300)
        self.poster_frame.place(x=450, y=220)

        self.l3 = customtkinter.CTkLabel(self.poster_frame, text="POSTER", font=(('Cascadia code light', 15, 'bold')))
        self.l3.place(x=90, y=20)

        ## BTN WIDGET FOR NEXT AND PREVIOUS MOVIE GENERATOR
        self.prev_btn = customtkinter.CTkButton(self.movies_frame, text="<", width=40, height=40, command=self.prev_movie, bg_color="#333333", fg_color="black", hover_color="#9D9D9D", font=(('Cascadia code light',15,"bold")))
        self.prev_btn.place(x=400, y=350)

        self.next_btn = customtkinter.CTkButton(self.movies_frame, text=">", width=40, height=40, command=self.next_movie, bg_color="#333333", fg_color="black", hover_color="#9D9D9D", font=(('Cascadia code light',15,"bold")))
        self.next_btn.place(x=710, y=350)

        # FRAME4 WIDGET FOR DISPLAYING overview OF THE MOVIE
        self.overview_frame = customtkinter.CTkFrame(self.movies_frame, width=570, height=160)
        self.overview_frame.place(x=130, y=530)

        self.l4 = customtkinter.CTkLabel(self.overview_frame, text="OVERVIEW", font=(('Cascadia code light', 15, 'bold')))
        self.l4.place(x=220, y=10)

        # Create summary_text as an instance variable
        self.summary_text = Text(self.overview_frame, wrap=WORD, font=(('Cascadia code light', 14)), height=6, width=70, bg="#333333", fg="white")
        self.summary_text.place(x=40, y=50)

        # FRAME 5 FOR LEFT NAVIGATION BAR WIDGET
        self.nav_frame = customtkinter.CTkFrame(self.movies_frame, width=75, height=750, fg_color="#131313", bg_color="#131313")
        self.nav_frame.place(x=0, y=0)

        # Logo Buttons
        logo_1 = ImageTk.PhotoImage(Image.open("Home.png").resize((30, 30)))
        logo_2 = ImageTk.PhotoImage(Image.open("Movie.png").resize((40, 40)))
        logo_3 = ImageTk.PhotoImage(Image.open("About.png").resize((40, 40)))

        # BTN WIDGETS FOR LEFT NAVIGATION
        self.nav_button1 = customtkinter.CTkButton(self.nav_frame, image=logo_1, text="", width=40, height=40, bg_color="#131313", fg_color="#131313", command=self.nav_option1)
        self.nav_button1.place(x=20, y=250)

        self.nav_button2 = customtkinter.CTkButton(self.nav_frame, image=logo_2, text="", width=40, height=40, bg_color="#131313", fg_color="#131313", command=self.nav_option2)
        self.nav_button2.place(x=15, y=300)

        self.nav_button3 = customtkinter.CTkButton(self.nav_frame, image=logo_3, text="", width=40, height=40, bg_color="#131313", fg_color="#131313", command=self.nav_option3)
        self.nav_button3.place(x=15, y=350)


## FUNCTION CREATED.. FOR HOME/MAIN SECTION// TO STORE CONTENTS IN IT'S SPECFIC TAB
    def home_tab(self):

        # BG IMAGE SETTING FOR EACH TAB 
        bg_image = ImageTk.PhotoImage(Image.open("moviee.jpg").resize((1000, 900)))
        bg_label = customtkinter.CTkLabel(self.home_frame, text="", image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL WIDGET FOR HEADING FOR HOME TAB
        self.l_home = customtkinter.CTkLabel(self.home_frame, text="✨ MOVIE EXPLORER ✨", font=(('Helvetica', 35, 'bold')), bg_color="white", fg_color="#262626")
        self.l_home.place(x=200, y=200)

        self.btn3 = customtkinter.CTkButton(self.home_frame, text="DISCOVER", font=(('Helvetica', 15, 'bold')), width=150, height=50, bg_color="#2D2D2D", fg_color="#D8D8D8", text_color="black", hover_color="#282A2A", corner_radius=7, command=self.nav_option2)
        self.btn3.place(x=350, y=300)

    
        # FRAME 5 FOR LEFT NAVIGATION BAR WIDGET
        self.nav_frame = customtkinter.CTkFrame(self.home_frame, width=75, height=750, fg_color="#131313", bg_color="#131313")
        self.nav_frame.place(x=0, y=0)

        # BTNS AS LOGOS
        logo_1 = ImageTk.PhotoImage(Image.open("Home.png").resize((40, 40)))
        logo_2 = ImageTk.PhotoImage(Image.open("Movie.png").resize((40, 40)))
        logo_3 = ImageTk.PhotoImage(Image.open("About.png").resize((40, 40)))

        # Buttons FOR LEFT NAVIGATION
        self.nav_button1 = customtkinter.CTkButton(self.nav_frame, image=logo_1, text="", width=30, height=30, bg_color="#131313", fg_color="#131313", command=self.nav_option1)
        self.nav_button1.place(x=20, y=250)

        self.nav_button2 = customtkinter.CTkButton(self.nav_frame, image=logo_2, text="", width=30, height=30, bg_color="#131313", fg_color="#131313", command=self.nav_option2)
        self.nav_button2.place(x=15, y=300)

        self.nav_button3 = customtkinter.CTkButton(self.nav_frame, image=logo_3, text="", width=30, height=30, bg_color="#131313", fg_color="#131313", command=self.nav_option3)
        self.nav_button3.place(x=15, y=350)


## FUCNTION CREATED.. FOR ABOUT THE APP SECTION// TO STORE CONTENTS IN IT'S SPECFIC TAB
    def about_tab(self):

        # BG IMAGE SETTING FOR EACH TAB 
        bg_image = ImageTk.PhotoImage(Image.open("moviee.jpg").resize((1100, 900)))
        bg_label = customtkinter.CTkLabel(self.about_frame, text="", image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        

        # LABEL WIDGET FOR HEADING FOR ABOUT TAB
        self.l_about = customtkinter.CTkLabel(self.about_frame, text="✨ MOVIE MIXER ✨", font=(('Cascadia code light', 35, 'bold')), bg_color="white", fg_color="#131313")
        self.l_about.place(x=250, y=50)

        # FRAME FOR CONTENTS IN ABOUT TAB
        self.f_about = customtkinter.CTkFrame(self.about_frame, width=610, height=320)
        self.f_about.place(x=130, y=190)

        
        self.label_home = customtkinter.CTkLabel(self.f_about, text="Explore and discover movies!", font=(('Cascadia code light', 20, 'bold')))
        self.label_home.place(x=150, y=25)


        self.details_about = customtkinter.CTkLabel(self.f_about, text="Movie Mixer is a fun and intuitive app designed for movie lovers who enjoy spontaneous film discovery. With just a movie name, users can instantly access key information like release date, director, genre, title, and a concise summary. This unique tool takes the guesswork out of movie hunting, offering a refreshing way to explore films you might not have considered. Whether you're looking for something new or want to stumble upon hidden gems, Movie Mixer adds an element of surprise to every search. Let it fuel your movie adventures and inspire your next cinematic pick!"
                                                   , font=(('Cascadia code light', 15)), wraplength=550, justify="left")
        self.details_about.place(x=17, y=80)

        # FRAME 5 FOR LEFT NAVIGATION BAR WIDGET
        self.nav_frame = customtkinter.CTkFrame(self.about_frame, width=75, height=750, fg_color="#131313", bg_color="#131313")
        self.nav_frame.place(x=0, y=0)

        # BTNS AS LOGOS
        logo_1 = ImageTk.PhotoImage(Image.open("Home.png").resize((30, 30)))
        logo_2 = ImageTk.PhotoImage(Image.open("Movie.png").resize((40, 40)))
        logo_3 = ImageTk.PhotoImage(Image.open("About.png").resize((40, 40)))

        # BTN WIDGETS FOR LEFT NAVIGATION
        self.nav_button1 = customtkinter.CTkButton(self.nav_frame, image=logo_1, text="", width=50, height=50, bg_color="#131313", fg_color="#131313", command=self.nav_option1)
        self.nav_button1.place(x=20, y=250)

        self.nav_button2 = customtkinter.CTkButton(self.nav_frame, image=logo_2, text="", width=50, height=50, bg_color="#131313", fg_color="#131313", command=self.nav_option2)
        self.nav_button2.place(x=15, y=300)

        self.nav_button3 = customtkinter.CTkButton(self.nav_frame, image=logo_3, text="", width=50, height=50, bg_color="#131313", fg_color="#131313", command=self.nav_option3)
        self.nav_button3.place(x=15, y=350)


# FUNCTIONS TO NAVIGATE TO TABS WHEN BUTTONS ARE CLICKED
    def nav_option1(self):
        self.notebook.select(0)
        self.click_sound.play()

    def nav_option2(self):
        self.notebook.select(1)
        self.click_sound.play()
    def nav_option3(self):
        self.notebook.select(2)
        self.click_sound.play()
    
# FUNCTION CREATED... TO SEARCH FOR ANY MOVIE 
    def search_movie(self):
        movie_name = self.entry.get()   ## ENTRY WIDGET GETS THE DATA TYPED IN

        if not movie_name:  ## MOVIE NAME IS EMPTY
            messagebox.showinfo("Error", "Please enter a movie name.")
            self.error_sound.play()  # Play error sound
            return

        api_key = "108163e927c263e075fa3487ca0babfd"  ## API KEY
        api_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"  ## API URL FOR SEARCHING MOVIES

        try:  
            response = requests.get(api_url)  ## REQUEST TO THE API WEBSITE
            data = response.json()

    
            if response.status_code == 200:
                self.click_sound.play()  # Play success sound when a movie is found
                if "results" in data and data["results"]:
                    self.movie_results = data["results"] # MOVIES RESULTS STORED AND INFO IS DISPLAYED FOR THE FIRST MOVIE
                    self.current_movie_index = 0
                    self.movie_info(self.movie_results[self.current_movie_index])
                else:
                    messagebox.showinfo("Error", "Movie not found.")  ## ERROR MESSAGE IF NO MOVIES FOUND
            else:
                messagebox.showinfo("Error", f"Failed to retrieve movie data. Status Code: {response.status_code}\n{data}")
        except requests.exceptions.RequestException as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
        
        if movie_found:
            self.click_sound.play()  # Play success sound when a movie is found
        else:
            self.error_sound.play()  # Play error sound if no movie is found

# FUNCTION FOR NEXT BTN TO DISPLAY NEXT MOVIE
    def next_movie(self):
        if self.movie_results and self.current_movie_index < len(self.movie_results) - 1:
            self.current_movie_index += 1  ## increment to move foward
            self.movie_info(self.movie_results[self.current_movie_index])
        else:
            messagebox.showinfo("Sorry!", "No more movies in the list.")


# FUNCTION FOR PREVIOUS BTN TO DISPLAY NEXT MOVIE
    def prev_movie(self):
        if self.movie_results and self.current_movie_index > 0:
            self.current_movie_index -= 1 ## decrement to move backwrads
            self.movie_info(self.movie_results[self.current_movie_index])
        else:
            messagebox.showinfo("ERROR!", "Cannot go more further.")


 # FUNCTION TO DISPLAY MOVIE DETAILS, OVERVIEW AND POSTER
    def movie_info(self, data):
        if self.movie_results:              ## MOVIES RESULTS AVAILABILTY
            data = self.movie_results[self.current_movie_index]   ## GET FUNCTION TO FETCH DATA FOR THE INDEX
            title = data.get("title", "N/A")
            director = self.director_detail(data.get("id"))
            genre = self.movie_genres(data.get("id"))
            release_date = data.get("release_date", "N/A")
            summary = data.get("overview", "N/A")
            poster_url = data.get("poster_path", "")

             # MOVIES DETAILS DISPLAYED ON THE FRAME
            customtkinter.CTkLabel(self.detail_frame, text=f"Title: {title}", font=(('Impact', 12))).place(x=15, y=60)
            customtkinter.CTkLabel(self.detail_frame, text=f"Director: {director}", font=(('Impact', 12))).place(x=15, y=100)
            customtkinter.CTkLabel(self.detail_frame, text=f"Genre: {genre}", font=(('Impact', 12))).place(x=15, y=140)
            customtkinter.CTkLabel(self.detail_frame, text=f"Release Date: {release_date}", font=(('Impact', 12))).place(x=15, y=180)

            ## FOR A NEW POSTER TO BE DISPLAYED
            for widget in self.poster_frame.winfo_children():
                widget.destroy()

            ## MOVIE OVERVIEW DISPLAYED ON THE OVERVIEW FRAME
            self.summary_text.delete(1.0, END)
            self.summary_text.insert(INSERT, summary)
            self.summary_text.place(x=40, y=3)

            # MOVIE POSTER DISPLAYED ON THE POSTER FRAME
            poster_image = self.movie_poster(poster_url)
            if poster_image:
                poster_label = Label(self.poster_frame, image=poster_image) 
                poster_label.image = poster_image
                poster_label.place(x=30, y=10)  
            else:
                messagebox.showinfo("Error", "Error loading poster.")


## FUNCTION CREATED..TO FETCH DETAILS FOR DIRECTOR
    def director_detail(self, movie_id):
        api_key = "108163e927c263e075fa3487ca0babfd"  # TMDb API key
        api_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"

        try:
            response = requests.get(api_url)   # REQUEST TO THE API WEBSITE TO FETCH MOVIE CREW
            data = response.json()
            crew = data.get("crew", [])
            directors = [member["name"] for member in crew if member["job"] == "Director"]
            return ", ".join(directors) if directors else "N/A"
        except requests.exceptions.RequestException:
            return "N/A"


## FUNCTION CREATED..TO RETRIEVE DATA/DETAILS FOR MOVIE GENRE
    def movie_genres(self, movie_id):
        api_key = "108163e927c263e075fa3487ca0babfd"  
        api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

        try:
            response = requests.get(api_url)   # REQUEST TO THE API WEBSITE TO FETCH MOVIE GENRE
            data = response.json()
            genres = data.get("genres", [])
            genre_names = [genre["name"] for genre in genres]
            return ", ".join(genre_names) if genre_names else "N/A"
        except requests.exceptions.RequestException:
            return "N/A"  # ERROR DURING THE API REQUEST


## FUNCTION CREATED..TO RETRIEVE MOVIE POSTERS
    def movie_poster(self, path):
        if not path:
            return None

        base_url = "https://image.tmdb.org/t/p/w500"
        url = f"{base_url}{path}"

        try:
            response = urlopen(url)   ## REQUEST TO THE API WEBSITE TO FETCH MOVIE POSTER
            image_data = response.read()
            image = Image.open(BytesIO(image_data))
            image = image.resize((250, 350), Image.LANCZOS)  
            photo_image = ImageTk.PhotoImage(image)
            return photo_image
        except Exception as e:
            messagebox.showinfo("Error", f"Error loading poster: {e}")
            return None
        
        

window = customtkinter.CTk()
app = MovieFinderApp(window)
window.mainloop()