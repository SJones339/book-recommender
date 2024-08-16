import os
import requests
import pandas as pd
from dotenv import load_dotenv
import pickle
import time


# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("BOOKS_API_KEY")

# Base URL for the Books API
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# List of diverse queries to cover different genres and topics
queries = [
    "Action", "Adventure", "Anthology", "Art", "Autobiography", "Biography", "Business", "Chick Lit",
    "Children's", "Classic", "Comic Book", "Coming of Age", "Contemporary", "Cookbook", "Crime",
    "Dark Fantasy", "Diary", "Dystopian", "Educational", "Epic", "Erotica", "Essay", "Fairy Tale",
    "Fantasy", "Fiction", "Folklore", "Food", "Gothic", "Graphic Novel", "Historical Fiction", 
    "History", "Horror", "Humor", "Inspirational", "Journal", "Literary Fiction", "Magic Realism",
    "Manga", "Memoir", "Metafiction", "Military", "Modern Classic", "Motivational", "Mystery",
    "Mythology", "Narrative", "Non-Fiction", "Occult", "Paranormal", "Philosophy", "Photography",
    "Plays", "Poetry", "Political Thriller", "Psychological Thriller", "Religion", "Romance", 
    "Satire", "Science", "Science Fiction", "Self-Help", "Short Story", "Sociology", "Southern Gothic",
    "Space Opera", "Spirituality", "Sports", "Steampunk", "Superhero", "Supernatural", "Suspense",
    "Sword and Sorcery", "Techno Thriller", "Thriller", "Time Travel", "Travel", "True Crime", 
    "Urban Fantasy", "War", "Western", "Women's Fiction", "Young Adult", "Absurdist Fiction",
    "Alternate History", "Animal Fiction", "Apocalyptic", "Archaeology", "Art History", "Art Instruction",
    "Art Photography", "Astrology", "Autofiction", "Avant-Garde", "Beat Generation", "Bildungsroman",
    "Black Comedy", "Body Horror", "Campus Novel", "Cannibalism", "Celtic Mythology", "Chaos Magic",
    "Chivalric Romance", "Climate Fiction", "Cyberpunk", "Dark Academia", "Detective Fiction",
    "Dieselpunk", "Dystopia", "Ecofiction", "Existential Fiction", "Fable", "Fairy Lore", "Family Saga",
    "Fantasy of Manners", "Film Studies", "First Contact", "Folk Horror", "Folktale", "Futurism",
    "Gastro Fiction", "Gentry Romance", "Gonzo Journalism", "Gothic Horror", "Grimdark", "Hard Science Fiction",
    "High Fantasy", "Historical Mystery", "Historical Romance", "Historical Thriller", "Holiday Fiction",
    "Hopepunk", "Horror Comedy", "Impressionism", "Islamic Fiction", "Japanese Literature", 
    "Judaica", "Juvenile Fiction", "Kitchen Sink Realism", "Legal Thriller", "Lesbian Fiction", 
    "Literary Horror", "Low Fantasy", "Lyrical Fiction", "Magical Realism", "Maritime Fiction", 
    "Mathematics", "Medical Fiction", "Medical Thriller", "Medieval Literature", "Metaphysical Fiction",
    "Modernism", "Musical", "Native American Literature", "Neo-Noir", "New Adult", "New Weird",
    "Noir", "Nordic Noir", "Oceanic Mythology", "Oulipo", "Outlaw Romance", "Picaresque",
    "Planetary Romance", "Political Satire", "Post-Apocalyptic", "Post-Modern", "Proletarian Literature",
    "Proto-Surrealism", "Psychic Fiction", "Queer Fiction", "Regional Fiction", "Revenge Tragedy",
    "Road Fiction", "Roman à Clef", "Romantic Comedy", "Romantic Fantasy", "Romantic Suspense",
    "Satirical Dystopia", "Science Fantasy", "Science Journalism", "Sea Stories", "Second Contact",
    "Secret History", "Serial Killer Fiction", "Sexual Politics", "Silkpunk", "Slapstick",
    "Social Satire", "Social Science", "Southern Noir", "Space Western", "Speculative Fiction",
    "Splatterpunk", "Spy Fiction", "Suburban Fiction", "Sword and Planet", "Tartan Noir",
    "Techno-Fantasy", "Theater Studies", "Transgressive Fiction", "Tribal Fiction", "True War Stories",
    "Afrofuturism", "Alien Invasion", "Alternate Reality", "Amish Romance", "Ancient History",
    "Animal Rights", "Anime", "Anthropology", "Art Criticism", "Astrobiology",
    "Astronomy", "Atomic Age", "Baroque", "Baseball", "Bizarro Fiction", "Bohemian", "Boxing",
    "Bridge Novel", "Burlesque", "Caribbean Fiction", "Celtic Fantasy", "Chekhovian", "Chick Noir",
    "Christian Fiction", "Circus Novel", "Civil War", "Classic Horror", "Climbing", "Cold War",
    "Comedy of Errors", "Comic Fantasy", "Comic Romance", "Conspiracy Thriller", "Contemporary Romance",
    "Counterculture", "Courtroom Drama", "Crime Noir", "Crossover Fiction", "Culinary Mystery",
    "Cult Fiction", "Cyber Thriller", "Cyborg Fiction", "Dark Romance", "Debut Novel", "Decadent Fiction",
    "Desert Noir", "Diesel Thriller", "Disaster Fiction", "Documentary Fiction", "Dystopian Romance",
    "Eastern Philosophy", "Egyptology", "Electric Literature", "Elizabethan", "Epic Fantasy",
    "Epic Poetry", "Erotic Thriller", "Esoteric Fiction", "Espionage", "Ethnic Fiction", "Evil Children",
    "Experimental Fiction", "Exploration Fiction", "Fantasy Comedy", "Fantasy Horror", "Fantasy Romance",
    "Feminist Fiction", "Fictional Biography", "First Nations Fiction", "Flat Earth Fiction",
    "French New Wave", "Frontier Fiction", "Funk", "Galactic Empire", "Gallows Humor", "Gaslamp Fantasy",
    "Genealogy", "Geopolitical Thriller", "Giallo", "Ghost Stories", "Gonzo Fantasy", "Gothic Romance",
    "Grief Memoir", "Haiku", "Hardboiled Fiction", "Haunted House", "Heist Thriller", "High Stakes",
    "Historiographic Metafiction", "Homage", "Household Drama", "Human Rights Fiction", "Hyper-Realism",
    "Ice Age", "Iconoclastic Fiction", "Illustrated Fiction", "Immigration Fiction", "Insect Fiction",
    "Inspirational Thriller", "Interactive Fiction", "Intergalactic", "Investigative Journalism",
    "Italian Neorealism", "Jazz Age", "Jungle Adventure", "Junkyard Noir", "King Arthur Mythos",
    "Knights and Ladies", "Lacanian Fiction", "Late Antiquity", "Law Enforcement", "Libertarian Fiction",
    "Linguistics", "Literary Criticism", "Literary Journalism", "Literary Memoir", "LitRPG", "Lonely Hearts",
    "Lost World", "Lovecraftian", "Lunar", "Macedonian Fiction", "Magic School", "Magical Detective",
    "Manor House Mystery", "Martian", "Masculinist Fiction", "Media Studies", "Medical Memoir",
    "Mega-Corporation", "Meta-Fantasy", "Middle Grade", "Midwestern Gothic", "Military History",
    "Minimalist Fiction", "Modern Noir", "Mosaic Novel", "Mountaineering", "Music Criticism", 
    "Mythic Fiction", "Near Future", "Neo-Pulp", "Neon Noir", "Norse Mythology", "Occupational Memoir",
    "Ocean Adventure", "Old West", "Outback Noir", "Outsider Fiction", "Parallel Universe", "Parody",
    "Party Fiction", "Patriotic Fiction", "Pirate Fiction", "Planetary Exploration", "Political Biography",
    "Post-Structuralism", "Postcolonial Fiction", "Postmodern Gothic", "Prison Fiction", "Propaganda",
    "Provincial Fiction", "Pulp Adventure", "Quantum Fiction", "Quirky Fiction", "Renaissance",
    "Resistance Literature", "Revenge Thriller", "Robinsonade", "Rock Opera", "Roman Noir", "Russian Noir",
    "Scandinavian Fiction", "School Story", "Sea Adventure", "Semi-Autobiographical", "Serial Fiction",
    "Slasher", "Slipstream", "Solarpunk", "Space Exploration", "Space Fantasy", "Space Horror",
    "Spy Thriller", "Stand-Alone", "Star-Crossed Lovers", "Stoner Fiction", "Suburban Horror", 
    "Subversive Fiction", "Sword and Sandal", "Sword Fantasy", "Tales of Terror", "Telepathic Fiction",
    "Terrorism Thriller", "Third Wave", "Time Slip", "Time-Loop Fiction", "Titanic Fiction", "Toxicology",
    "Toy Fiction", "Train Adventure", "Transhumanist Fiction", "Transporter Fiction", "Underworld Fiction",
    "Unreliable Narrator", "Urban Drama", "Vampire Fiction", "Vegetarian Fiction", "Victorian Fantasy",
    "Victorian Gothic", "Virtual Reality",
]


# Set the number of results to fetch per query
max_results = 40  

# Initialize an empty DataFrame to hold all books data
books_df = pd.DataFrame(columns=[
    'title', 'authors', 'categories', 'average_rating', 'ratings_count', 
    'description', 'published_date', 'isbn_13'
])

# Iterate over each query
for query in queries:
    print(f"Fetching data for query: {query}")
    params = {
        'q': query,
        'key': API_KEY,
        'maxResults': max_results
    }

    response = requests.get(BASE_URL, params=params)
    #print(f"Status Code: {response.status_code}")  # Debug: Check the response status code
    data = response.json()
    #print(f"Response Content: {response.text}")  # Debug: Check the response content length

    if 'items' not in data:
        print(f"No items found for query: {query}")
        continue

    # Extract relevant fields from the response
    for item in data.get('items', []):
        book_info = item['volumeInfo']
        title = book_info.get('title')
        authors = ', '.join(book_info.get('authors', []))
        categories = ', '.join(book_info.get('categories', []))
        average_rating = book_info.get('averageRating')
        ratings_count = book_info.get('ratingsCount')
        description = book_info.get('description')
        published_date = book_info.get('publishedDate')
        isbn_13 = ', '.join([identifier['identifier'] for identifier in book_info.get('industryIdentifiers', []) if identifier['type'] == 'ISBN_13'])

        # Debug: Print the book details
        #print(f"Processing book: {title} by {authors}")

        # Check for duplicates based on title and authors
        if not books_df[(books_df['title'] == title) & (books_df['authors'] == authors)].empty:
            #print(f"Duplicate found: {title} by {authors}")
            continue
        
        # Append the new book data to the DataFrame
        new_book = pd.DataFrame([{
            'title': title,
            'authors': authors,
            'categories': categories,
            'average_rating': average_rating,
            'ratings_count': ratings_count,
            'description': description,
            'published_date': published_date,
            'isbn_13': isbn_13
        }])
        #print(f"DataFrame shape before appending: {books_df.shape}")
        books_df = pd.concat([books_df, new_book], ignore_index=True)
        #print(f"DataFrame shape after appending: {books_df.shape}")
    
    # To avoid hitting the API rate limit, introduce a small delay between requests
    time.sleep(1)  # Adjust delay as needed

    
#has_duplicates = books_df.duplicated(subset=['title', 'authors']).any()
len(books_df)
books_df.to_pickle("../../data/raw/01_data_processed.pkl")
