import psycopg2
from config import DB_CONFIG
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL database!")
        except Exception as e:
            print(f"Database connection error: {e}")
            print("Running without database...")
            self.conn = None
    
    def create_tables(self):
        if not self.conn:
            return
        
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            self.conn.commit()
            print("Tables created/verified!")
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()
    
    def get_or_create_player(self, username):
        if not self.conn:
            return None
        
        try:
            # Try to insert new player
            self.cursor.execute(
                "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING RETURNING id",
                (username,)
            )
            
            result = self.cursor.fetchone()
            
            if result:
                player_id = result[0]
            else:
                # Player exists, get their id
                self.cursor.execute(
                    "SELECT id FROM players WHERE username = %s",
                    (username,)
                )
                player_id = self.cursor.fetchone()[0]
            
            self.conn.commit()
            return player_id
        except Exception as e:
            print(f"Error with player: {e}")
            self.conn.rollback()
            return None
    
    def save_score(self, username, score, level_reached):
        if not self.conn:
            return False
        
        player_id = self.get_or_create_player(username)
        if not player_id:
            return False
        
        try:
            self.cursor.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (player_id, score, level_reached)
            )
            self.conn.commit()
            print(f"Score saved: {username} - {score} points")
            return True
        except Exception as e:
            print(f"Error saving score: {e}")
            self.conn.rollback()
            return False
    
    def get_top_scores(self, limit=10):
        if not self.conn:
            return []
        
        try:
            self.cursor.execute("""
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                ORDER BY gs.score DESC
                LIMIT %s
            """, (limit,))
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'username': row[0],
                    'score': row[1],
                    'level': row[2],
                    'date': row[3].strftime("%Y-%m-%d %H:%M")
                })
            
            return results
        except Exception as e:
            print(f"Error fetching scores: {e}")
            return []
    
    def get_personal_best(self, username):
        if not self.conn:
            return 0
        
        try:
            self.cursor.execute("""
                SELECT MAX(gs.score)
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                WHERE p.username = %s
            """, (username,))
            
            result = self.cursor.fetchone()
            return result[0] if result[0] else 0
        except Exception as e:
            print(f"Error fetching personal best: {e}")
            return 0
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")