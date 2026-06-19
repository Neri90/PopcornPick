CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    user_id    SERIAL       PRIMARY KEY,
    username   VARCHAR(50)  NOT NULL UNIQUE,
    email      VARCHAR(100) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP    DEFAULT NOW()
);

CREATE TABLE movies (
    movie_id      SERIAL        PRIMARY KEY,
    ml_movie_id   INT           NOT NULL UNIQUE,
    title         VARCHAR(500)  NOT NULL,
    title_ko      VARCHAR(500),
    overview      TEXT,
    poster_path   VARCHAR(500),
    vote_average  FLOAT         DEFAULT 0.0,
    release_year  INT,
    tmdb_id       INT,
    genres        VARCHAR(300)  NOT NULL DEFAULT '',
    click_count   INT           DEFAULT 0,
    avg_rating    FLOAT         DEFAULT 0.0,
    search_text   TEXT,
    embedding     vector(384),
    created_at    TIMESTAMP     DEFAULT NOW()
);

CREATE INDEX idx_movies_fulltext
    ON movies USING GIN (to_tsvector('simple', coalesce(search_text, '')));
CREATE INDEX idx_movies_click
    ON movies (click_count DESC);
CREATE INDEX idx_movies_rating
    ON movies (avg_rating DESC);
-- CREATE INDEX idx_movies_embedding
--     ON movies USING ivfflat (embedding vector_cosine_ops)
--     WITH (lists = 100);

CREATE TABLE ratings (
    rating_id BIGSERIAL PRIMARY KEY,
    user_id   INT       NOT NULL REFERENCES users(user_id),
    movie_id  INT       NOT NULL REFERENCES movies(movie_id),
    rating    FLOAT     NOT NULL CHECK (rating >= 0.5 AND rating <= 5.0),
    rated_at  TIMESTAMP DEFAULT NOW(),
    UNIQUE (user_id, movie_id)
);

CREATE INDEX idx_ratings_user  ON ratings (user_id);
CREATE INDEX idx_ratings_movie ON ratings (movie_id);

CREATE TABLE user_click_logs (
    log_id       BIGSERIAL    PRIMARY KEY,
    user_id      INT          NOT NULL REFERENCES users(user_id),
    movie_id     INT          NOT NULL REFERENCES movies(movie_id),
    action_type  VARCHAR(10)  NOT NULL CHECK (action_type IN ('CLICK', 'LIKE', 'RATING')),
    rating_value FLOAT        CHECK (rating_value >= 0.5 AND rating_value <= 5.0),
    genres       VARCHAR(300) NOT NULL DEFAULT '',
    logged_at    TIMESTAMP(3) DEFAULT NOW()
);

CREATE INDEX idx_click_logs_user_time ON user_click_logs (user_id, logged_at);

CREATE TABLE streaming_offsets (
    id          INT          PRIMARY KEY DEFAULT 1,
    last_log_id BIGINT       NOT NULL DEFAULT 0,
    updated_at  TIMESTAMP(3) DEFAULT NOW(),
    CONSTRAINT single_row CHECK (id = 1)
);

INSERT INTO streaming_offsets (id, last_log_id) VALUES (1, 0);

CREATE TABLE user_genre_weights (
    id         BIGSERIAL    PRIMARY KEY,
    user_id    INT          NOT NULL REFERENCES users(user_id),
    genre_name VARCHAR(50)  NOT NULL,
    weight     FLOAT        DEFAULT 0.0,
    updated_at TIMESTAMP(3) DEFAULT NOW(),
    UNIQUE (user_id, genre_name)
);

CREATE TABLE recommendations (
    rec_id       BIGSERIAL PRIMARY KEY,
    user_id      INT       NOT NULL REFERENCES users(user_id),
    movie_id     INT       NOT NULL REFERENCES movies(movie_id),
    score        FLOAT     NOT NULL,
    rank         INT       NOT NULL,
    batch_run_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_rec_user_rank  ON recommendations (user_id, rank);
CREATE INDEX idx_rec_user_batch ON recommendations (user_id, batch_run_at DESC);