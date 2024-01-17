# Importing necessary libraries for GUI (Tkinter), making HTTP requests (requests),
# and working with images (PIL - Python Imaging Library).
from tkinter import Tk, Frame, Label, Button, Text, Scrollbar, Entry
import requests
from PIL import ImageTk, Image

# Defining the main class for the CinemaniaApp
class CinemaniaApp:
    def __init__(self, window):
        # Initializing the main window with specific attributes.
        self.window = window
        self.window.title("Application")
        self.window.geometry("900x600")
        self.window['bg'] = 'white'

        # Creating the header and navigation sections.
        self.create_header()
        self.create_navigation()

    def create_header(self):
        # Creating the header frame with the Cinemania.com label and an image.
        header_frame = Frame(self.window, bg="#a4db24", height=90)
        header_frame.pack(fill="x")

        web_header = Label(header_frame, text="Cinemania.com", fg="white", bg="#a4db24",
                           font=("Arimo", 32, "bold"))
        web_header.place(x=20, y=20)
        
        # Adding an image to the header.
        img = ImageTk.PhotoImage(Image.open("img1.png"))
        imgLabel = Label(self.window, text="Welcome to Cinemania", image=img)
        imgLabel.image = img
        imgLabel.place(x=200, y=200)
        
    def create_navigation(self):
        # Creating the navigation frame with buttons for Home, Search, and Movies.
        nav_frame = Frame(self.window, bg="#22263d", width=150)
        nav_frame.pack(side="left", fill="y")

        buttons = [
            ("Home", self.onclick_home),
            ("Search", self.onclick_search),
            ("Movies", self.onclick_movies)  
        ]

        # Looping through button data to create buttons.
        for i, (text, command) in enumerate(buttons):
            button = Button(nav_frame, text=text, fg="white", bg="#22263d",
                            font=("Arimo", 18, "bold"), borderwidth=0, highlightthickness=0, command=command)
            button.place(x=10, y=20 + 70 * i)

    def onclick_home(self):
        # Handling the Home button click event by clearing the main frame and displaying welcome text.
        self.clear_main_frame()

        heading_text = "Home"
        heading_label = Label(self.window, text=heading_text, fg="#a4db24", bg="white",
                              font=("Arimo", 20, "bold"))
        heading_label.pack()

        welcome_text = """
        Welcome to Cinemania, your go-to hub for all things cinema! At Cinemania, we're dedicated to making your movie-watching experience not just enjoyable, but extraordinary. Whether you're a seasoned cinephile or a casual viewer, our user-friendly platform is designed to cater to your every cinematic need.\n
        Looking for personalized recommendations? Cinemania goes beyond the basics, offering tailored suggestions based on your viewing history and preferences. Let Cinemania guide you through the vast landscape of cinematic delights.\n
        Join us at Cinemania and open the door to a world of cinematic wonders. Explore, rate, review, and share your passion for movies like never before. Welcome to a community that shares your love for the seventh art – welcome to Cinemania!
        """
        text_widget = Text(self.window, wrap="word", width=80, height=20, font=("Arimo", 12))
        text_widget.insert("1.0", welcome_text)
        text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.window, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

    def onclick_search(self):
        # Handling the Search button click event by clearing the main frame and displaying search elements.
        self.clear_main_frame()

        heading_text = "Search Movies"
        heading_label = Label(self.window, text=heading_text, fg="#a4db24", bg="white",
                            font=("Arimo", 20, "bold"))
        heading_label.pack()

        search_frame = Frame(self.window, bg="white")
        search_frame.pack(pady=10)

        self.search_bar = Entry(search_frame, width=40, font=("Arimo", 14), borderwidth=2, relief="groove")
        self.search_bar.pack(side="left")

        search_button = Button(search_frame, text="Search", fg="white", bg="#22263d",
                            font=("Arimo", 12, "bold"), borderwidth=0, highlightthickness=0,
                            command=self.perform_search)
        search_button.pack(side="left", padx=5)

        self.search_results_frame = Frame(self.window, bg="white")
        self.search_results_frame.pack(fill="both", expand=True)

    def perform_search(self):
        # Performing a movie search based on user input and displaying the results.
        user_input = self.search_bar.get()
                
        # api link
        if user_input:
            api_key = 'f0c6d98d026e07d9250be25cb0a3a1f8'
            api_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={user_input}'

            try:
                response = requests.get(api_url)
                response.raise_for_status()  
                movie_data = response.json()
                self.display_movie_information(movie_data)
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

    def display_movie_information(self, movie_data):
        # Displaying movie information based on the search results.
        results = movie_data.get('results', [])

        if results:
            for widget in self.search_results_frame.winfo_children():
                widget.destroy()

            info_frame = Frame(self.search_results_frame, bg="white")
            info_frame.pack(fill="both", expand=True)

            scrollbar = Scrollbar(info_frame, orient="vertical")

            movie_info_text = Text(info_frame, wrap="word", width=80, height=20, font=("Arimo", 12),
                                yscrollcommand=scrollbar.set)
            movie_info_text.pack(side="left", fill="both", expand=True)

            scrollbar.config(command=movie_info_text.yview)
            scrollbar.pack(side="right", fill="y")

            for movie in results:
                title = movie.get('title', 'N/A')
                release_date = movie.get('release_date', 'N/A')
                overview = movie.get('overview', 'N/A')

                movie_info_text.insert("end", f"Title: {title}\nRelease Date: {release_date}\nOverview: {overview}\n\n")
        else:
            error_label = Label(self.search_results_frame, text="Movie not found.", fg="red", bg="white",
                                font=("Arimo", 12))
            error_label.pack()


    def onclick_movies(self):
        # Handling the Movies button click event by clearing the main frame and displaying trending movies.
        self.clear_main_frame()

        heading_text = "Trending Movies"
        heading_label = Label(self.window, text=heading_text, fg="#a4db24", bg="white",
                              font=("Arimo", 20, "bold"))
        heading_label.pack()

        # api link
        api_key = 'f0c6d98d026e07d9250be25cb0a3a1f8'
        api_url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()  
            trending_movies_data = response.json().get('results', [])

            text_widget = Text(self.window, wrap="word", width=80, height=20, font=("Arimo", 12))
            text_widget.pack(side="left", fill="both", expand=True)

            scrollbar = Scrollbar(self.window, command=text_widget.yview)
            scrollbar.pack(side="right", fill="y")
            text_widget.config(yscrollcommand=scrollbar.set)

            for movie in trending_movies_data:
                title = movie.get('title', 'N/A')
                release_date = movie.get('release_date', 'N/A')
                overview = movie.get('overview', 'N/A')

                movie_info_text = f"Title: {title}\nRelease Date: {release_date}\nOverview: {overview}\n\n"

                text_widget.insert("end", movie_info_text,)

        except requests.exceptions.RequestException as e:
            error_label = Label(self.window, text=f"Error: {e}", fg="red", bg="white",
                                font=("Arimo", 12))
            error_label.pack()

    def clear_main_frame(self):
        # Clearing the main frame by destroying all widgets and recreating the header and navigation.
        for widget in self.window.winfo_children():
            widget.destroy()

        self.create_header()
        self.create_navigation()


# Starting the application when the script is run.
if __name__ == "__main__":
    window = Tk()
    app = CinemaniaApp(window)
    window.mainloop()
