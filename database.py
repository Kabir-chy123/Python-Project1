import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="kuser",        # change if needed
        password="1234",     # change if needed
        database="flight_game"
    )
    return conn

# -------------------------------
# 2. FETCH AIRPORTS (with filter)
# -------------------------------
def fetch_airports(limit=5, airport_type="all"):
    """
    Fetch random airports from DB.
    airport_type can be 'large_airport', 'medium_airport', 'small_airport', or 'all'.
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    if airport_type == "all":
        query = """
            SELECT ident, name, iso_country, type
            FROM airport
            ORDER BY RAND() LIMIT %s;
        """
        cursor.execute(query, (limit,))
    else:
        query = """
            SELECT ident, name, iso_country, type
            FROM airport
            WHERE type = %s
            ORDER BY RAND() LIMIT %s;
        """
        cursor.execute(query, (airport_type, limit))

    airports = cursor.fetchall()
    cursor.close()
    conn.close()
    return airports

# -------------------------------
# 3. PHANTOM AIRPORTS
# -------------------------------
phantom_airports = [
    {"id": "X-LOOP", "name": "Cyclone Airfield", "effect": "loop", "zone": "Twilight"},
    {"id": "X-DEC", "name": "Drowned Terminal", "effect": "stranded", "zone": "Twilight"},
    {"id": "X-HAUNT", "name": "Collapsed Runway", "effect": "crash", "zone": "Twilight"}
]

# -------------------------------
# 4. AURORA BEACON
# -------------------------------
aurora_airport = {
    "id": "X-AURORA",
    "name": "Aurora Beacon",
    "effect": "win",
    "zone": "Aurora Frontier"
}
# -------------------------------
# HALL OF FAME FUNCTIONS
# -------------------------------
def save_run(player_name, ending, survivors, fuel):
    """Save a completed game run to the Hall of Fame table."""
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        INSERT INTO hall_of_fame (player_name, ending, survivors, fuel)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (player_name, ending, survivors, fuel))
    conn.commit()
    cursor.close()
    conn.close()


def fetch_runs(limit=5):
    """Fetch past runs from the Hall of Fame table."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT player_name, ending, survivors, fuel, played_at
        FROM hall_of_fame
        ORDER BY played_at DESC
        LIMIT %s;
    """
    cursor.execute(query, (limit,))
    runs = cursor.fetchall()
    cursor.close()
    conn.close()
    return runs
# -------------------------------
# HALL OF FAME FUNCTIONS
# -------------------------------
def save_run(player_name, ending, survivors, fuel):
    """Save a completed game run to the Hall of Fame table."""
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        INSERT INTO hall_of_fame (player_name, ending, survivors, fuel)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (player_name, ending, survivors, fuel))
    conn.commit()
    cursor.close()
    conn.close()


def fetch_runs(limit=5):
    """Fetch past runs from the Hall of Fame table."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT player_name, ending, survivors, fuel, played_at
        FROM hall_of_fame
        ORDER BY played_at DESC
        LIMIT %s;
    """
    cursor.execute(query, (limit,))
    runs = cursor.fetchall()
    cursor.close()
    conn.close()
    return runs







