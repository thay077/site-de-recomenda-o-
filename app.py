import random
import numpy as np
from flask import Flask, render_template_string, request, redirect, url_for, session

# --- DADOS DO SISTEMA ---
# Para simplificar, usamos uma base de dados de filmes fictícia.
# Cada filme possui um ID, título, poster, sinopse, gêneros e uma popularidade inicial (0-1).
# Gêneros disponíveis: Ação, Aventura, Animação, Comédia, Documentário, Drama, Fantasia, Ficção Científica, Romance, Suspense, Terror.

all_genres = ["Ação", "Aventura", "Animação", "Comédia", "Documentário", "Drama", "Fantasia", "Ficção Científica", "Romance", "Suspense", "Terror"]

movies = [
    {'id': 1, 'title': 'A Grande Aventura', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+1', 'synopsis': 'Uma jornada épica para encontrar um artefato perdido.', 'genres': ['Aventura', 'Fantasia'], 'popularity': 0.8},
    {'id': 2, 'title': 'O Robô Amigo', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+2', 'synopsis': 'Um robô solitário descobre a amizade em um mundo pós-apocalíptico.', 'genres': ['Animação', 'Ficção Científica'], 'popularity': 0.7},
    {'id': 3, 'title': 'Riso Contagiante', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+3', 'synopsis': 'As trapalhadas de um grupo de amigos em uma viagem de verão.', 'genres': ['Comédia', 'Romance'], 'popularity': 0.9},
    {'id': 4, 'title': 'A Queda do Império', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+4', 'synopsis': 'Um drama histórico sobre a ascensão e queda de uma civilização antiga.', 'genres': ['Drama', 'Ação'], 'popularity': 0.6},
    {'id': 5, 'title': 'O Terror da Floresta', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+5', 'synopsis': 'Um grupo de jovens acampa e descobre uma lenda aterrorizante.', 'genres': ['Terror', 'Suspense'], 'popularity': 0.5},
    {'id': 6, 'title': 'Expedição Extrema', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+6', 'synopsis': 'Um documentário sobre escaladas perigosas e a busca por novos limites.', 'genres': ['Documentário', 'Aventura'], 'popularity': 0.4},
    {'id': 7, 'title': 'Estrelas no Céu', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+7', 'synopsis': 'Uma comédia romântica sobre um astrônomo e uma artista que se apaixonam.', 'genres': ['Romance', 'Comédia'], 'popularity': 0.85},
    {'id': 8, 'title': 'O Ladrão de Almas', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+8', 'synopsis': 'Um suspense psicológico sobre um detetive tentando capturar um criminoso peculiar.', 'genres': ['Suspense', 'Drama'], 'popularity': 0.75},
    {'id': 9, 'title': 'Heróis do Futuro', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+9', 'synopsis': 'No futuro, um grupo de jovens com superpoderes enfrenta uma ameaça global.', 'genres': ['Ação', 'Ficção Científica'], 'popularity': 0.95},
    {'id': 10, 'title': 'A Viagem de Tim', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+10', 'synopsis': 'Uma jornada mágica por mundos fantásticos.', 'genres': ['Animação', 'Fantasia'], 'popularity': 0.65},
    {'id': 11, 'title': 'Encontro de Duas Vidas', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+11', 'synopsis': 'Um encontro inesperado muda o destino de duas pessoas completamente diferentes.', 'genres': ['Romance', 'Drama'], 'popularity': 0.7},
    {'id': 12, 'title': 'Lobisomem na Cidade', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+12', 'synopsis': 'Um mistério assustador se desenrola quando um monstro é avistado na cidade.', 'genres': ['Terror', 'Ação'], 'popularity': 0.6},
    {'id': 13, 'title': 'A Teia da Conspiração', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+13', 'synopsis': 'Um thriller de espionagem que explora segredos governamentais.', 'genres': ['Suspense', 'Ação'], 'popularity': 0.8},
    {'id': 14, 'title': 'O Segredo da Floresta Encantada', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+14', 'synopsis': 'Uma aventura mágica em uma floresta cheia de criaturas.', 'genres': ['Fantasia', 'Aventura'], 'popularity': 0.7},
    {'id': 15, 'title': 'A Última Gargalhada', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+15', 'synopsis': 'Uma comédia sobre um comediante que tenta recuperar sua carreira.', 'genres': ['Comédia', 'Drama'], 'popularity': 0.65},
    {'id': 16, 'title': 'O Planeta Esquecido', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+16', 'synopsis': 'Uma missão de exploração espacial a um planeta remoto e misterioso.', 'genres': ['Ficção Científica', 'Aventura'], 'popularity': 0.85},
    {'id': 17, 'title': 'O Fantasma da Rua', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+17', 'synopsis': 'Um suspense sobre um fantasma que assombra uma rua inteira.', 'genres': ['Terror', 'Suspense'], 'popularity': 0.75},
    {'id': 18, 'title': 'A Vida de um Artista', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+18', 'synopsis': 'Um documentário sobre a vida e a obra de um pintor famoso.', 'genres': ['Documentário', 'Drama'], 'popularity': 0.5},
    {'id': 19, 'title': 'Amor em Paris', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+19', 'synopsis': 'Um casal americano se encontra em Paris e se apaixona.', 'genres': ['Romance', 'Comédia'], 'popularity': 0.9},
    {'id': 20, 'title': 'O Ataque dos Goblins', 'poster': 'https://placehold.co/200x300/F1713A/ffffff?text=Poster+20', 'synopsis': 'Uma comédia de fantasia sobre uma vila atacada por criaturas.', 'genres': ['Fantasia', 'Comédia'], 'popularity': 0.6},
]

# --- LÓGICA DO SISTEMA DE RECOMENDAÇÃO ---
def get_genre_vector(genres):
    """Converte uma lista de gêneros em um vetor numérico."""
    vector = np.zeros(len(all_genres))
    for genre in genres:
        if genre in all_genres:
            vector[all_genres.index(genre)] = 1
    return vector

def sigmoid(x):
    """Função sigmoide para converter similaridade em probabilidade."""
    return 1 / (1 + np.exp(-x))

def calculate_similarity(user_vector, movie_vector):
    """Calcula a similaridade de cosseno entre dois vetores."""
    if np.linalg.norm(user_vector) == 0 or np.linalg.norm(movie_vector) == 0:
        return 0
    return np.dot(user_vector, movie_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(movie_vector))

def get_recommendations(user_data):
    """Gera uma lista de filmes recomendados para o usuário."""
    rated_movie_ids = {m['id'] for m in user_data['rated_movies']}
    
    # Se o usuário não avaliou nada, as recomendações são baseadas em popularidade e nos gêneros de interesse iniciais.
    if not user_data['rated_movies']:
        initial_genre_vector = get_genre_vector(user_data.get('initial_genres', []))
        if np.linalg.norm(initial_genre_vector) == 0:
            # Se não houver gêneros iniciais, recomenda-se os mais populares.
            return sorted(movies, key=lambda x: x['popularity'], reverse=True)[:10]
        
        # Combina popularidade com a similaridade inicial de gênero
        recommendations = []
        for movie in movies:
            movie_vector = get_genre_vector(movie['genres'])
            score = calculate_similarity(initial_genre_vector, movie_vector) * 0.7 + movie['popularity'] * 0.3
            recommendations.append({'movie': movie, 'score': score})
        
        return [item['movie'] for item in sorted(recommendations, key=lambda x: x['score'], reverse=True)[:10]]

    # A partir daqui, o sistema é baseado no perfil do usuário (gêneros avaliados)
    user_genre_profile = {genre: 0 for genre in all_genres}
    for rated_movie in user_data['rated_movies']:
        for genre in rated_movie['genres']:
            user_genre_profile[genre] += rated_movie['rating'] - 3  # Pondera por notas > 3
    
    user_vector = get_genre_vector([g for g, score in user_genre_profile.items() if score > 0])
    
    if np.linalg.norm(user_vector) == 0:
        return sorted(movies, key=lambda x: x['popularity'], reverse=True)[:10]

    recommendations = []
    for movie in movies:
        if movie['id'] in rated_movie_ids:
            continue # Evita repetir itens já avaliados

        movie_vector = get_genre_vector(movie['genres'])
        similarity = calculate_similarity(user_vector, movie_vector)
        score = similarity * 0.9 + movie['popularity'] * 0.1 # Combina similaridade com popularidade
        
        recommendations.append({
            'movie': movie,
            'score': score,
            'similarity': similarity
        })
    
    # Penaliza a similaridade excessiva para promover diversidade
    recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    final_recommendations = []
    added_genres = set()
    for rec in recommendations:
        movie_genres = set(rec['movie']['genres'])
        if not movie_genres.intersection(added_genres) or len(final_recommendations) < 3:
            final_recommendations.append(rec)
            added_genres.update(movie_genres)
        if len(final_recommendations) >= 10:
            break
            
    return [rec['movie'] for rec in final_recommendations]

def get_recommendation_reason(user_data, movie):
    """Gera uma breve explicação para a recomendação."""
    user_genre_profile = {genre: 0 for genre in all_genres}
    for rated_movie in user_data['rated_movies']:
        for genre in rated_movie['genres']:
            user_genre_profile[genre] += rated_movie['rating'] - 3
    
    liked_genres = [g for g, score in user_genre_profile.items() if score > 0]
    
    common_genres = set(movie['genres']).intersection(set(liked_genres))
    if common_genres:
        return f"Você gostou de filmes de {', '.join(common_genres)}."
    
    # Se não houver gêneros em comum, a recomendação é por popularidade ou novidade
    if movie['popularity'] > 0.8:
        return "Filme muito popular, pode ser do seu gosto."
    
    return "Talvez seja uma boa novidade para a sua lista!"


# --- APLICAÇÃO FLASK ---
app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('recommendations'))
    
    return render_template_string(HTML_TEMPLATE,
        title="Bem-vindo(a)!",
        content=f"""
        <div class="flex items-center justify-center min-h-screen bg-gray-100">
            <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
                <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">CineGuide</h1>
                <p class="text-center text-gray-600 mb-8">Cadastre-se para começar a receber recomendações!</p>
                <form action="{url_for('register')}" method="post">
                    <div class="mb-4">
                        <label for="username" class="block text-gray-700 font-bold mb-2">Nome:</label>
                        <input type="text" id="username" name="username" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500" required>
                    </div>
                    <div class="mb-6">
                        <label for="age" class="block text-gray-700 font-bold mb-2">Idade:</label>
                        <input type="number" id="age" name="age" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500" required>
                    </div>
                    <div class="mb-6">
                        <label class="block text-gray-700 font-bold mb-2">Gêneros de Interesse (opcional):</label>
                        <div class="flex flex-wrap gap-2">
                            {render_genre_checkboxes()}
                        </div>
                    </div>
                    <button type="submit" class="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 transition-colors">
                        Começar
                    </button>
                </form>
            </div>
        </div>
        """, show_nav=False
    )

@app.route('/register', methods=['POST'])
def register():
    session['username'] = request.form['username']
    session['age'] = request.form['age']
    session['initial_genres'] = request.form.getlist('genres')
    session['rated_movies'] = []
    session['watchlist'] = []
    return redirect(url_for('recommendations'))

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect(url_for('home'))
        
    user_data = session
    recommended_movies = get_recommendations(user_data)
    
    # Adiciona a probabilidade de gostar e o motivo
    for movie in recommended_movies:
        movie_vector = get_genre_vector(movie['genres'])
        user_vector = get_genre_vector([g['name'] for g in get_user_genre_profile().get('genres', []) if g['score'] > 0])
        
        # Se o usuário não avaliou nada, a similaridade é baseada nos gêneros iniciais
        if not user_data['rated_movies']:
            user_vector = get_genre_vector(user_data.get('initial_genres', []))
        
        similarity = calculate_similarity(user_vector, movie_vector)
        # Multiplica por um fator para tornar a probabilidade mais expressiva
        movie['probability'] = int(sigmoid(similarity * 5) * 100)
        movie['reason'] = get_recommendation_reason(user_data, movie)
        
    rated_movie_ids = {m['id'] for m in session['rated_movies']}
    
    return render_template_string(HTML_TEMPLATE,
        title="Recomendados para Você",
        content=render_movie_list(recommended_movies, show_rating=True, rated_ids=rated_movie_ids)
    )

@app.route('/rate/<int:movie_id>/<int:rating>')
def rate_movie(movie_id, rating):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie:
        rated_movies = session.get('rated_movies', [])
        # Atualiza a nota se o filme já foi avaliado
        existing_rating = next((m for m in rated_movies if m['id'] == movie_id), None)
        if existing_rating:
            existing_rating['rating'] = rating
        else:
            new_rated_movie = movie.copy()
            new_rated_movie['rating'] = rating
            rated_movies.append(new_rated_movie)
        session['rated_movies'] = rated_movies
        
    return redirect(request.referrer or url_for('recommendations'))

@app.route('/explore')
def explore():
    sort_by = request.args.get('sort_by', 'popularidade')
    genre_filter = request.args.get('genre_filter', 'Todos')
    
    filtered_movies = movies
    if genre_filter != 'Todos':
        filtered_movies = [m for m in filtered_movies if genre_filter in m['genres']]
        
    if sort_by == 'popularidade':
        filtered_movies = sorted(filtered_movies, key=lambda x: x['popularity'], reverse=True)
    elif sort_by == 'titulo':
        filtered_movies = sorted(filtered_movies, key=lambda x: x['title'])
    
    return render_template_string(HTML_TEMPLATE,
        title="Explorar Filmes",
        content=f"""
        <div class="flex flex-wrap gap-4 mb-8">
            <h2 class="text-xl font-bold text-gray-800 self-center">Filtrar por:</h2>
            <div class="flex-grow">
                <label for="genre_filter" class="sr-only">Gênero</label>
                <select id="genre_filter" onchange="window.location.href='/explore?sort_by={sort_by}&genre_filter=' + this.value" class="w-full md:w-auto p-2 border border-gray-300 rounded-md">
                    <option value="Todos" {'selected' if genre_filter == 'Todos' else ''}>Todos os Gêneros</option>
                    {"".join([f'<option value="{g}" {"selected" if genre_filter == g else ""}>{g}</option>' for g in all_genres])}
                </select>
            </div>
            <div class="flex-grow">
                <label for="sort_by" class="sr-only">Ordenar por</label>
                <select id="sort_by" onchange="window.location.href='/explore?sort_by=' + this.value + '&genre_filter={genre_filter}'" class="w-full md:w-auto p-2 border border-gray-300 rounded-md">
                    <option value="popularidade" {'selected' if sort_by == 'popularidade' else ''}>Popularidade</option>
                    <option value="titulo" {'selected' if sort_by == 'titulo' else ''}>Título</option>
                </select>
            </div>
        </div>
        {render_movie_list(filtered_movies)}
        """
    )

@app.route('/details/<int:movie_id>')
def movie_details(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return redirect(url_for('recommendations'))
        
    related_movies = get_related_movies(movie)
    
    return render_template_string(HTML_TEMPLATE,
        title=movie['title'],
        content=f"""
        <div class="flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-8 mb-8">
            <img src="{movie['poster']}" alt="{movie['title']}" class="rounded-xl shadow-lg w-48 md:w-64 flex-shrink-0">
            <div class="flex-grow">
                <h1 class="text-4xl font-extrabold text-gray-900 mb-2">{movie['title']}</h1>
                <p class="text-gray-500 text-lg mb-4">{' • '.join(movie['genres'])}</p>
                <p class="text-gray-700 text-lg mb-4">{movie['synopsis']}</p>
                <div class="flex items-center space-x-4">
                    <button onclick="window.location.href='{url_for('add_to_watchlist', movie_id=movie['id'])}'" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full transition-colors">
                        <i class="fas fa-plus-circle"></i> Adicionar à Minha Lista
                    </button>
                    <div class="flex space-x-1">
                        {render_rating_stars(movie['id'], get_user_rating(movie['id']))}
                    </div>
                </div>
            </div>
        </div>
        <hr class="my-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Filmes Similares</h2>
        {render_movie_list(related_movies, show_rating=True)}
        """
    )
    
@app.route('/watchlist')
def watchlist():
    watchlist_movies = [m for m in movies if m['id'] in session.get('watchlist', [])]
    return render_template_string(HTML_TEMPLATE,
        title="Minha Lista",
        content=render_movie_list(watchlist_movies, show_rating=True)
    )

@app.route('/add_to_watchlist/<int:movie_id>')
def add_to_watchlist(movie_id):
    watchlist = session.get('watchlist', [])
    if movie_id not in watchlist:
        watchlist.append(movie_id)
        session['watchlist'] = watchlist
    return redirect(request.referrer or url_for('recommendations'))

@app.route('/my-ratings')
def my_ratings():
    rated_movies = session.get('rated_movies', [])
    user_profile = get_user_genre_profile()
    
    return render_template_string(HTML_TEMPLATE,
        title="Minhas Notas & Perfil",
        content=f"""
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Seu Perfil por Gênero</h2>
        <div class="bg-gray-100 p-6 rounded-xl shadow-md mb-8">
            <ul class="list-disc list-inside space-y-2">
                {"".join([f'<li><strong class="text-gray-900">{g["name"]}:</strong> Nota Média de {g["avg_rating"]:.1f} (Avaliados: {g["count"]})</li>' for g in user_profile['genres']])}
            </ul>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Filmes que Você Avaliou</h2>
        {render_movie_list(rated_movies, show_rating=True, rated_ids={m['id'] for m in rated_movies})}
        """
    )
    
@app.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        results = [m for m in movies if query.lower() in m['title'].lower()]
    else:
        results = []
    
    return render_template_string(HTML_TEMPLATE,
        title="Busca",
        content=f"""
        <div class="flex items-center mb-8">
            <input type="text" id="search_input" placeholder="Buscar por título..." value="{query}" class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500">
            <button onclick="window.location.href='/search?query=' + document.getElementById('search_input').value" class="ml-2 bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-4 rounded-md transition-colors">
                Buscar
            </button>
        </div>
        {render_movie_list(results, show_rating=True)}
        """
    )

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('home'))


# --- FUNÇÕES AUXILIARES DE RENDERIZAÇÃO ---
def render_genre_checkboxes():
    checkboxes = ""
    for genre in all_genres:
        checkboxes += f"""
        <label class="inline-flex items-center p-2 bg-gray-200 hover:bg-gray-300 rounded-full transition-colors cursor-pointer">
            <input type="checkbox" name="genres" value="{genre}" class="form-checkbox h-4 w-4 text-orange-500 rounded-md">
            <span class="ml-2 text-sm text-gray-700 font-medium">{genre}</span>
        </label>
        """
    return checkboxes
    
def render_movie_card(movie, show_rating=False, rated_ids=None):
    rated_ids = rated_ids or set()
    current_rating = get_user_rating(movie['id'])
    
    rating_section = ""
    if show_rating:
        rating_section = f"""
        <div class="mt-4 flex flex-col items-center">
            <p class="text-sm text-gray-500 mb-1">Nota:</p>
            <div class="flex space-x-1">
                {render_rating_stars(movie['id'], current_rating)}
            </div>
            {'<p class="mt-2 text-sm font-semibold text-orange-600">%s de você gostar</p>' % (movie.get('probability', '')) if 'probability' in movie else ''}
            {'<p class="text-xs text-gray-500 text-center mt-1">Motivo: %s</p>' % movie.get('reason', '') if 'reason' in movie else ''}
        </div>
        """
    
    return f"""
    <div class="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-300 overflow-hidden flex flex-col justify-between">
        <a href="{url_for('movie_details', movie_id=movie['id'])}">
            <img src="{movie['poster']}" alt="{movie['title']}" class="w-full h-auto object-cover rounded-t-xl">
        </a>
        <div class="p-4 flex-grow flex flex-col justify-between">
            <div>
                <h3 class="font-bold text-lg text-gray-800 mb-1 leading-tight">{movie['title']}</h3>
                <p class="text-sm text-gray-500 mb-2">{' • '.join(movie['genres'])}</p>
            </div>
            {rating_section}
        </div>
    </div>
    """

def render_movie_list(movies_to_render, show_rating=False, rated_ids=None):
    if not movies_to_render:
        return "<p class='text-center text-gray-500 text-lg'>Nenhum filme encontrado.</p>"
        
    rated_ids = rated_ids or set()
    cards = "".join([render_movie_card(m, show_rating, rated_ids) for m in movies_to_render])
    return f"""
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
        {cards}
    </div>
    """

def render_rating_stars(movie_id, current_rating):
    stars = ""
    for i in range(1, 6):
        fill = "text-yellow-400" if i <= current_rating else "text-gray-300"
        stars += f"""
        <a href="{url_for('rate_movie', movie_id=movie_id, rating=i)}" class="cursor-pointer transition-colors duration-200">
            <i class="fas fa-star {fill} text-xl hover:text-yellow-500"></i>
        </a>
        """
    return stars

def get_user_rating(movie_id):
    rated_movies = session.get('rated_movies', [])
    movie = next((m for m in rated_movies if m['id'] == movie_id), None)
    return movie['rating'] if movie else 0

def get_user_genre_profile():
    rated_movies = session.get('rated_movies', [])
    genre_data = {g: {'total_rating': 0, 'count': 0} for g in all_genres}
    
    for movie in rated_movies:
        rating = movie.get('rating', 0)
        for genre in movie['genres']:
            genre_data[genre]['total_rating'] += rating
            genre_data[genre]['count'] += 1
            
    profile = {
        'genres': []
    }
    for genre, data in genre_data.items():
        if data['count'] > 0:
            profile['genres'].append({
                'name': genre,
                'avg_rating': data['total_rating'] / data['count'],
                'count': data['count'],
                'score': data['total_rating']
            })
    
    return profile
    
def get_related_movies(base_movie):
    """Encontra filmes similares ao filme base."""
    movie_vector = get_genre_vector(base_movie['genres'])
    related = []
    for movie in movies:
        if movie['id'] == base_movie['id']:
            continue
        
        related_vector = get_genre_vector(movie['genres'])
        similarity = calculate_similarity(movie_vector, related_vector)
        if similarity > 0.4:  # Limiar de similaridade
            related.append({'movie': movie, 'similarity': similarity})
    
    related = sorted(related, key=lambda x: x['similarity'], reverse=True)
    return [item['movie'] for item in related[:5]]

# --- TEMPLATE HTML COMPLETO ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - CineGuide</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f7fafc;
        }}
    </style>
</head>
<body class="bg-gray-100 text-gray-800 antialiased">
    {% if show_nav %}
    <nav class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex flex-col md:flex-row justify-between items-center">
            <div class="flex items-center space-x-4 mb-4 md:mb-0">
                <a href="{{ url_for('recommendations') }}" class="text-2xl font-extrabold text-orange-500 rounded-md px-2 py-1 transition-colors">CineGuide</a>
                <span class="text-sm font-medium text-gray-500 hidden md:block">Olá, {{ session.username }}!</span>
            </div>
            <div class="flex flex-wrap justify-center md:justify-end gap-2 md:gap-4">
                <a href="{{ url_for('recommendations') }}" class="py-2 px-3 rounded-full text-sm font-semibold transition-colors bg-orange-100 text-orange-800 hover:bg-orange-200">Recomendados</a>
                <a href="{{ url_for('explore') }}" class="py-2 px-3 rounded-full text-sm font-semibold transition-colors bg-gray-100 text-gray-800 hover:bg-gray-200">Explorar</a>
                <a href="{{ url_for('watchlist') }}" class="py-2 px-3 rounded-full text-sm font-semibold transition-colors bg-gray-100 text-gray-800 hover:bg-gray-200">Minha Lista</a>
                <a href="{{ url_for('my_ratings') }}" class="py-2 px-3 rounded-full text-sm font-semibold transition-colors bg-gray-100 text-gray-800 hover:bg-gray-200">Minhas Notas</a>
                <a href="{{ url_for('search') }}" class="py-2 px-3 rounded-full text-sm font-semibold transition-colors bg-gray-100 text-gray-800 hover:bg-gray-200">Busca</a>
            </div>
            <a href="{{ url_for('reset') }}" class="mt-4 md:mt-0 py-2 px-4 rounded-full text-sm font-semibold transition-colors bg-red-100 text-red-800 hover:bg-red-200">Resetar</a>
        </div>
    </nav>
    {% endif %}
    <main class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-extrabold text-gray-900 mb-6">{{ title }}</h1>
        {{ content | safe }}
    </main>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
