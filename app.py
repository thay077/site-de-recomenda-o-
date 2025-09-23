import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🎬 Base de filmes
filmes = [
    {"titulo": "Matrix", "generos": "Ação, Ficção", "descricao": "Um hacker descobre a verdade sobre sua realidade."},
    {"titulo": "Senhor dos Anéis", "generos": "Fantasia, Aventura", "descricao": "Um hobbit parte em uma jornada para destruir um anel poderoso."},
    {"titulo": "John Wick", "generos": "Ação", "descricao": "Um ex-assassino volta à ativa após a morte de seu cachorro."},
    {"titulo": "Harry Potter", "generos": "Fantasia, Magia", "descricao": "Um garoto descobre que é um bruxo e vai estudar em Hogwarts."},
    {"titulo": "Interestelar", "generos": "Ficção, Drama", "descricao": "Astronautas viajam por um buraco de minhoca buscando um novo lar."},
    {"titulo": "Duna", "generos": "Ficção, Aventura", "descricao": "Um jovem nobre lidera a luta por um planeta desértico valioso."},
    {"titulo": "A Origem", "generos": "Ficção, Suspense", "descricao": "Um ladrão invade sonhos para roubar segredos do subconsciente."},
    {"titulo": "Avatar", "generos": "Ficção, Aventura", "descricao": "Um soldado paraplégico se envolve com nativos em um planeta alienígena."},
    {"titulo": "Oppenheimer", "generos": "Drama, Biografia", "descricao": "A história do cientista que liderou o Projeto Manhattan."},
    {"titulo": "Clube da Luta", "generos": "Drama, Psicológico", "descricao": "Um homem funda um clube de luta secreto para extravasar sua frustração."}
]

# 🔍 Sistema de recomendação
df = pd.DataFrame(filmes)
df['conteudo'] = df['generos'] + " " + df['descricao']

vetor = TfidfVectorizer(stop_words='portuguese')
matriz = vetor.fit_transform(df['conteudo'])

def recomendar_filmes(titulo: str, n: int = 5) -> pd.DataFrame | None:
    if titulo not in df['titulo'].values:
        return None

    idx = df[df['titulo'] == titulo].index[0]
    similaridades = cosine_similarity(matriz[idx], matriz).flatten()
    indices = similaridades.argsort()[::-1][1:n+1]
    return df.iloc[indices][['titulo', 'generos', 'descricao']]

# 💻 Interface terminal
def main():
    print("===== NetMovies Terminal 🎬 =====")
    print("Filmes disponíveis:")
