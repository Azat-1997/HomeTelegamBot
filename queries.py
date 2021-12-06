import sqlite3
with sqlite3.connect('test_database.db') as db:
        cur = db.cursor()
        
        cur.execute('''CREATE TABLE IF NOT EXISTS matches
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_chat INTEGER,
                game TEXT,
                wins INTEGER,
                loses INTEGER,
                total INTEGER)
            '''
           )

def update_stats(id_chat, game, winner):
    with sqlite3.connect('test_database.db') as db:
        cur = db.cursor()
        cur.execute("SELECT id_chat FROM matches WHERE id_chat = ? AND game = ?", (id_chat, game))
        # if user played first time in this game
        query_create = "INSERT INTO matches(id_chat, game, wins, loses, total) VALUES (?, ?, ?, ?, ?)"
        
        query_update_loses = """UPDATE matches SET loses = loses + 1,
                                total = total + 1 WHERE id_chat = ? AND game = ?"""
        
        query_update_wins = """UPDATE matches SET wins = wins + 1,
                                total = total + 1 WHERE id_chat = ? AND game = ?"""
        
        query_update_draw = """UPDATE matches SET total = total + 1 WHERE id_chat = ? AND game = ?"""
        
        if cur.fetchone() is None:
            if winner == "user":
                cur.execute(query_create, (id_chat, game, 1, 0, 1))
            elif winner == "bot":
                cur.execute(query_create, (id_chat, game, 0, 1, 1))
            else:
                cur.execute(query_create, (id_chat, game, 0, 0, 1))
                
        # if user played many times
        else:
            if winner == "user":
                cur.execute(query_update_wins, (id_chat, game))
            elif winner == "bot":
                cur.execute(query_update_loses, (id_chat, game)) 
            else:
                cur.execute( query_update_draw, (id_chat, game))



def get_stats(id_chat):
    message = "Вы еще не сыграли ни в одну игру. Наберите /info, чтобы узнать как сыграть."
    with sqlite3.connect('test_database.db') as db:
        cur = db.cursor()
        cur.execute("SELECT id_chat FROM matches WHERE id_chat = ? ", (id_chat, ))
        if cur.fetchone() is not None:
            template = "{}:\nпобед - {}\nпоражений - {}\nвсего сыграно в данную игру - {}\nпроцент побед ~ {} % \n"
            result = []
            cur.execute("SELECT game, wins, loses, total FROM matches WHERE id_chat = ?", (id_chat, ))
            for game, wins, loses, total in cur:
                result.append(template.format(game, wins, loses, total, round(wins * 100 / total, 2)))
                
            message = "\n".join(result)    
            
    return message


                
